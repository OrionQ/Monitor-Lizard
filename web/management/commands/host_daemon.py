
import inspect
from django.core.management.base import BaseCommand
from web.host_report import HostReport
from web.host_reports import hourly_report
import json

# Send reports to the server from the host.


class HostState:
    def __init__(self, guid=None, reports_sent=[]):
        assert guid is not None
        # guid of the host we are running on
        self.guid = guid
        # reports is a dictionary mapping report class names to when they were last sent.
        # It will be persisted and loaded from a file on each host
        self.reports_sent = reports_sent


class Command(BaseCommand):
    help = 'To be run on the host via cron. Will send all reports due'

    # The file on each host where we keep our state including reports sent and when last, and our guid
    __state_file = "monitor_lizard_host_state.json"
    # The file that should contain the registration key
    __registration_key_file = "monitor_lizard_registration.txt"

    reports = [
        hourly_report.HourlyReport
    ]

    def is_registered(self):
        """If we have initialized and registered our commands yet"""
        # The implementation should check the existence of __state_file, then check the existence of a guid in that file
        return True

    def register(self):
        """Register with the host server"""
        # Should first check for the existence of __registration_key_file, and if it doesn't exist return false
        # IF it does exist then try to register via the registration route
        # Once it has the guid, save that to the __state_file
        # If all that completes successfully, return true
        return True

    def load_state(self):
        """Load the state of the host from __state_file"""
        return HostState("4530ad55-0c68-4b78-97d8-f5664defb316")

    def should_send(self, report, state):
        """Return if we should send the report, because we haven't sent it or enough time has elapsed that we should send it again."""
        return True

    def send(self, report):
        """Replace this with pika serializing and sending the report over json"""
        print(json.dumps(report))

    def handle(self, *args, **options):
        if not self.is_registered():
            if not self.register():
                return 1

        state = self.load_state()

        hostReports = []
        for report in self.reports:
            if self.should_send(report, state):
                newReport = report(state.guid)
                self.send(newReport)
