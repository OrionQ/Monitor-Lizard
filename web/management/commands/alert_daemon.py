from django.core.management.base import BaseCommand
from web.models import AlertRule, HostTag, Host, Alert, Report
import logging
from time import sleep

class Command(BaseCommand):
    help = 'To notify the tags that are subscribed to the alerts based on the alert rules'

    def handle(self, *args, **options):

        # retrieve all the alert rules from the database
        rules = AlertRule.objects.all()
        
        # look through all the tags that follows the alert rule every 1 second
        while True:
            
            # retrieve all the host tags and the in the alert rules
            for i in rules:
                metric = i.metric
                threshold = i.threshold
                operator = i.operator
                severity = i.severity

                # retreive all the hosts in each host tags for notification preparation
                hosts = i.host_tag.hosts
                for host in hosts.all():
                    # retrieve the reports from the host
                    if Alert.objects.filter(host=host, alert_rule=i,acknowledged_by__isnull=True).exists():
                        continue
                    if operator == 'min':
                        new_report = Report.objects.filter(host=host, metric=metric).latest('time')
                        if new_report.value < threshold:
                            Alert.create(alert_rule=i, report=new_report).save()
                    if operator == 'max':
                        new_report = Report.objects.filter(host=host, metric=metric).latest('time')
                        if new_report.value > threshold:
                            Alert.create(alert_rule=i, report=new_report).save()
            sleep(1)
        return 0

