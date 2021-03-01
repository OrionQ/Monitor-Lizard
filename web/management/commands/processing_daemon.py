from django.core.management.base import BaseCommand
from web.host_reports import HourlyReport

# Receive reports from the host on the server, process, and save them.


class Command(BaseCommand):
    help = 'To be run on the server via cron to process reports'

    def handle(self, *args, **options):
        while (True):  # The condition here would be while the message queue is full, or we process a maximum number of reports
            report = HourlyReport(  # Instead of constructing this report we would pop and unserialize a report on the message queue
                guid='GUID HERE', cpu_usage=80, cpu_temperature=80)
            report.persist()
