from time import sleep
from django.core.management.base import BaseCommand
from web.host_reports import HourlyReport
from web.models import Report
import json

# Receive reports from the host on the server, process, and save them.


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
        return "{}"

    def handle(self, *args, **options):
        while True:
            if self.queue_is_empty():
                sleep(options['sleep'])
            else:
                reports = []
                while not self.queue_is_empty():
                    report = json.loads(self.queue_pop())
                    reports.extend(report.generate_report_models())
                Report.objects.bulk_create(reports)
