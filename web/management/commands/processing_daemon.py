from time import sleep
from django.core.management.base import BaseCommand
from web.models import Report
from web.message_queue import MessageQueue
from .host_daemon import HostReport
from json import JSONDecoder, loads

# Receive reports from the host on the server, process, and save them.


class HostReportDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'guid' in obj:
            report = HostReport(obj['guid'])
            report.metrics = obj['metrics']
            obj = report
        return obj


class Command(BaseCommand):
    help = 'To be run on the server via cron to process reports'

    def __init__(self):
        BaseCommand.__init__(self)
        self.reports = []

    def on_message(self, ch, method, properties, body):
        """Upon receiving a message over the message queue, decode it into a report and, if we've received enough reports, save it"""
        report = loads(body.decode(), cls=HostReportDecoder)
        self.reports.extend(report.generate_report_models())
        if (self.reports.count() > 100):
            Report.objects.bulk_create(self.reports)
            self.reports = []

    def handle(self, *args, **options):
        queue = MessageQueue()
        try:
            queue.receive(self.on_message)
        except KeyboardInterrupt:
            queue.close()
