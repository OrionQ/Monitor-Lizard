from django.core.management.base import BaseCommand
from web.host_reports import HourlyReport

# Send reports to the server from the host.


class Command(BaseCommand):
    help = 'To be run on the host via cron. Will send all reports it is told to via flags'

    def add_arguments(self, parser):
        parser.add_argument('-h', '--hourly', action='store_true',
                            help='Collect and send an hourly report', default=False)

    def handle(self, *args, **options):
        if (options['hourly']):
            hourlyreport = HourlyReport(
                guid='GUID HERE', cpu_usage=80, cpu_temperature=80)
            #serialize and send
