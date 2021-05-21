
import json
import re
from os import path
from glob import glob
from time import sleep
from importlib import import_module
from configparser import ConfigParser
from json import JSONEncoder, dumps
import logging
from web.models import Report, Metric, Host
from web.message_queue import MessageQueue
from django.core.management.base import BaseCommand
from http import client
from urllib.parse import urlencode

# Send reports to the server from the host.


class HostReport():
    """Report from host to be sent over message bus"""

    def __init__(self, guid=None):
        assert guid is not None
        self.guid = guid
        self.metrics = {}

    def should_send(self):
        return self.metrics is not {}

    def generate_report_models(self):
        """
        Generate multiple report models from this plugin.
        To be used once the report is on the processing daemon!
        """
        reports = []
        try:
            host = Host.objects.get(guid=self.guid)
            for metric, value in self.metrics.items():
                try:
                    reports.append(Report(metric=Metric.objects.get(
                        name=metric), host=host, value=value))
                except Report.DoesNotExist:
                    logging.error(
                        'Host with guid ' + self.guid + ' sent report with nonexistant metric ' + metric)
        except Host.DoesNotExist:
            logging.error(
                'Received report from host with nonexistant guid ' + self.guid)
        return reports


class HostReportEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Command(BaseCommand):
    help = 'To be run on the host. Will check every second to send all due metrics as report'

    # The file on each host where we keep our guid
    GUID_FILE = "monitor_lizard_guid.txt"
    # The file that should contain the registration key
    REGISTRATION_KEY_FILE = "monitor_lizard_registration.txt"

    HOST_PLUGIN_CONFIG_FILE = 'host_plugin_config.ini'

    def is_registered(self):
        """If we have initialized and registered our commands yet"""
        # The implementation should check the existence of GUID_FILE, then check the existence of a guid in that file
        if path.exists(self.GUID_FILE):
            with open(self.GUID_FILE) as fp:
                guid = fp.readline().strip()
                regex = "^[{]?[0-9a-fA-F]{8}" + \
                    "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$"
                p = re.compile(regex)
                if(re.search(p, guid)):
                    return True

        return False

    def register(self):
        """Register with the host server"""
        conn = client.HTTPConnection("localhost:8000")
        if path.exists(self.REGISTRATION_KEY_FILE):
            with open(self.REGISTRATION_KEY_FILE) as fp:
                registration_key = fp.readline().strip()
            conn.request(
                "POST", "/api/host/", urlencode({'registration_key': registration_key}))
        else:
            conn.request(
                "POST", "/api/host/")
        guid = json.loads(
            conn.getresponse().read().decode('utf-8'))['guid']
        conn.close()
        with open(self.GUID_FILE, 'x') as fp:
            fp.write(guid)
        return True

    def load_guid(self):
        """Load the guid of the host from GUID_FILE"""
        with open(self.GUID_FILE) as fp:
            guid = fp.readline().strip()
        return guid

    def send(self, report):
        """Replace this with pika serializing and sending the report over json"""
        print()

    def get_metric_polling_config(self):
        config = ConfigParser()
        config.read(self.HOST_PLUGIN_CONFIG_FILE)
        if not config.has_section('polling_intervals'):
            config.add_section('polling_intervals')
        return config

    def probePlugins(self):
        """Find and return the probe plugin reports the host should send"""
        # Construct directory to host reports
        dir_path = path.realpath(path.join(__file__, "../../../host_plugins/"))
        # Full file names
        probeModules = glob(path.join(dir_path, "*.py"))
        probePlugins = []
        for probeModule in probeModules:
            probeModule = import_module(
                'web.host_plugins.'+path.basename(probeModule)[:-3])
            probePlugins.append(getattr(probeModule, 'ProbePlugin'))
        return probePlugins

    def handle(self, *args, **options):
        if not self.is_registered():
            if not self.register():
                return 1

        guid = self.load_guid()
        #guid = "8eb5fe61-877f-4321-83d5-c735dc715a67"
        polling_config = self.get_metric_polling_config()
        # Dictionary of probe name to last poll time
        last_polls = {}
        queue = MessageQueue()
        plugins = self.probePlugins()

        while True:
            report = HostReport(guid)
            # Look through probes for metrics that might be due
            for plugin in plugins:
                # Append all metrics the probe plugin measures to our report
                report.metrics.update(
                    plugin.measure(last_polls, polling_config))
            # Only send nonempty reports
            if report.should_send():
                queue.send(dumps(report, cls=HostReportEncoder))
            sleep(1)
