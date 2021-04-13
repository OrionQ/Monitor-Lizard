from django.core.management.base import BaseCommand
from django.core.management import call_command
from web.models import HostTag
from multiprocessing import Process
from time import sleep


class Command(BaseCommand):
    help = 'Demo the application by running all the background tasks. (Message queue must be running first)'

    def handle(self, *args, **options):
        s = Process(target=call_command, args=('runserver',))
        p = Process(target=call_command, args=('processing_daemon',))
        h = Process(target=call_command, args=('host_daemon',))
        a = Process(target=call_command, args=('alert_daemon',))
        s.start()
        sleep(0.5)
        p.start()
        h.start()
        a.start()
        s.join()
        p.join()
        h.join()
        a.join()
        return 0
