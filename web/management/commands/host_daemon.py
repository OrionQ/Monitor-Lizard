
import json
from os import path
from glob import glob
from django.core.management.base import BaseCommand
from importlib import import_module
# Send reports to the server from the host.


class Command(BaseCommand):
    help = 'To be run on the host via cron. Will send all reports due'

    # The file on each host where we keep our guid
    GUID_FILE = "monitor_lizard_guid.json"
    # The file that should contain the registration key
    REGISTRATION_KEY_FILE = "monitor_lizard_registration.txt"

    def is_registered(self):
        """If we have initialized and registered our commands yet"""
        # The implementation should check the existence of GUID_FILE, then check the existence of a guid in that file
        return True

    def register(self):
        """Register with the host server"""
        # Should first check for the existence of REGISTRATION_KEY_FILE, and if it doesn't exist return false
        # If it does exist then try to register via the registration route
        # Once it has the guid, save that to the GUID_FILE
        # If all that completes successfully, return true
        return True

    def load_guid(self):
        """Load the guid of the host from GUID_FILE"""
        return "4530ad55-0c68-4b78-97d8-f5664defb316"

    def send(self, report):
        """Replace this with pika serializing and sending the report over json"""
        print(report)

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

        hostReports = []
        for probePlugin in self.probePlugins():
            newProbeReport = probePlugin(guid)
            self.send(newProbeReport)
