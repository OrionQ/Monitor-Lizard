from django.core.management.base import BaseCommand
from django.core.management import call_command
from web.models import AlertRule, HostTag, Host, Alert, Report
import logging
from time import sleep


class Command(BaseCommand):
    help = 'Set up application for first run.'

    def handle(self, *args, **options):
        call_command('flush')
        call_command('migrate')
        call_command('createsuperuser', username='admin')
        call_command('populate_probes')
        HostTag.objects.create(name='Unsorted')
        return 0
