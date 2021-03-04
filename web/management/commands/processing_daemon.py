from time import sleep
from django.core.management.base import BaseCommand
from web.models import Report
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

    def add_arguments(self, parser):
        parser.add_argument('-s', '--sleep', type=int, dest='sleep',
                            help='seconds to sleep between processing batches', default=5)

    def queue_is_empty(self):
        """Temp function to represent if the message queue is empty. Eventually replace calls to this with pika"""
        return False

    def queue_pop(self):
        """Temp function to represent popping a message from the queue, should be a json string serialized report. Eventually replace calls to this with pika"""
        return '{"guid": "4530ad55-0c68-4b78-97d8-f5664defb316", "metrics": {"cpu_usage": 60, "cpu_temperature": 60}}'

    def handle(self, *args, **options):
        while True:
            if self.queue_is_empty():
                sleep(options['sleep'])
            else:
                reports = []
                while not self.queue_is_empty():
                    report = loads(self.queue_pop(), cls=HostReportDecoder)
                    reports.extend(report.generate_report_models())
                Report.objects.bulk_create(reports)
