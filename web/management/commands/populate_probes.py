
import json
import re
from os import path
from glob import glob
from time import sleep
from importlib import import_module
from configparser import ConfigParser
from json import JSONEncoder, dumps
import logging
from web.models import Report, Metric, Host
from web.message_queue import MessageQueue
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'To be run on the server. Loads every probe in every plugin as metrics'

    def probePlugins(self):
        """Find and return the probe plugins to load"""
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
        plugins = self.probePlugins()

        metrics = []
        for plugin in plugins:
            for metric in plugin.generate_metrics():
                if not Metric.objects.filter(name=metric.name).exists():
                    metrics.append(metric)

        Metric.objects.bulk_create(metrics)
