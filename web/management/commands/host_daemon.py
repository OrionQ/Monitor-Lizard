
import json
from os import path
from glob import glob
from django.core.management.base import BaseCommand
from web.host_report import HostReport
from importlib import import_module
# Send reports to the server from the host.


class Command(BaseCommand):
    help = 'To be run on the host via cron. Will send all reports due'

    # The file on each host where we keep our guid
    _guid_file = "monitor_lizard_guid.json"
    # The file that should contain the registration key
    _registration_key_file = "monitor_lizard_registration.txt"

    def is_registered(self):
        """If we have initialized and registered our commands yet"""
        # The implementation should check the existence of _guid_file, then check the existence of a guid in that file
        return True

    def register(self):
        """Register with the host server"""
        # Should first check for the existence of __registration_key_file, and if it doesn't exist return false
        # If it does exist then try to register via the registration route
        # Once it has the guid, save that to the _guid_file
        # If all that completes successfully, return true
        return True

    def load_guid(self):
        """Load the guid of the host from _guid_file"""
        return "4530ad55-0c68-4b78-97d8-f5664defb316"

    def send(self, report):
        """Replace this with pika serializing and sending the report over json"""
        print(report)

    def reports(self):
        """Find and return the reports the host should send"""
        # Construct directory to host reports
        dir_path = path.realpath(path.join(__file__, "../../../host_reports/"))
        # Full file names
        reportPlugins = glob(path.join(dir_path, "*.py"))
        reports = []
        for reportPlugin in reportPlugins:
            report_module = import_module(
                'web.host_reports.'+path.basename(reportPlugin)[:-3])
            reports.append(getattr(report_module, 'Report'))
        return reports

    def handle(self, *args, **options):
        if not self.is_registered():
            if not self.register():
                return 1

        guid = self.load_guid()

        hostReports = []
        for report in self.reports():
            newReport = report(guid)
            self.send(newReport)
