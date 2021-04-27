from random import randrange
from django.core.management.base import BaseCommand
import web.models as models
from uuid import uuid4

class Command(BaseCommand):
    help = 'THIS WILL WIPE YOUR DATABASE. Creates randomized demo data for presentations and UI testing. Populate Probes first.'

    def handle(self, *args, **options):
        testHost = []
        models.Host.objects.all().delete()
        models.HostTag.objects.all().delete()
        for i in range(5):
            testHost.append(models.Host(guid=uuid4()))
            testHost[i].save()
        testTag1 = models.HostTag.objects.create(name="US-East")
        testTag1.hosts.add(models.Host.objects.get(guid=testHost[0].guid))
        testTag1.hosts.add(models.Host.objects.get(guid=testHost[1].guid))
        testTag2 = models.HostTag.objects.create(name="Dubai")
        testTag2.hosts.add(models.Host.objects.get(guid=testHost[2].guid))
        testTag2.hosts.add(models.Host.objects.get(guid=testHost[3].guid))
        testTag3 = models.HostTag.objects.create(name="Gregs Test Box")
        testTag3.hosts.add(models.Host.objects.get(guid=testHost[4].guid))
        metrics = models.Metric.objects.all()
        models.Report.objects.all().delete()
        reports = []
        for h in testHost:
            for m in metrics:
                val = 50
                for i in range(100):
                    reports.append(models.Report(metric=m, host=models.Host.objects.get(guid=h.guid), value=str(val)))
                    val = val + randrange(-5,5)
                    val = val if val <= 100 else 95
                    val = val if val >= 0 else 5
        models.Report.objects.bulk_create(reports)
        models.User.objects.all().delete()
        user = models.User.objects.create(name="user")
        models.Team.objects.all().delete()
        team = models.Team.objects.create(name="alertees")
        team.users.add(user)
        models.AlertRule.objects.all().delete()
        alertRule0 = models.AlertRule.objects.create(metric=metrics[0], host_tag=testTag1, team=team, operator=models.AlertRule.ALERT_OPERANDS[0], threshold="40", severity=0)
        alertRule1 = models.AlertRule.objects.create(metric=metrics[2], host_tag=testTag1, team=team, operator=models.AlertRule.ALERT_OPERANDS[1], threshold="40", severity=1)
        alertRule2 = models.AlertRule.objects.create(metric=metrics[1], host_tag=testTag1, team=team, operator=models.AlertRule.ALERT_OPERANDS[0], threshold="99", severity=2)
        models.Alert.objects.all().delete()
        models.Alert.objects.create(host=models.Host.objects.get(guid=testHost[0].guid), alert_rule=alertRule0, host_tag=testTag1, operator="Maximum", threshold="40", value="55", team=team, metric=metrics[0])
        models.Alert.objects.create(host=models.Host.objects.get(guid=testHost[1].guid), alert_rule=alertRule1, host_tag=testTag1, operator="Minimum", threshold="20", value="0", team=team, metric=metrics[2])
        models.Alert.objects.create(host=models.Host.objects.get(guid=testHost[2].guid), alert_rule=alertRule0, host_tag=testTag2, operator="Maximum", threshold="40", value="46", team=team, metric=metrics[0])
        models.Alert.objects.create(host=models.Host.objects.get(guid=testHost[3].guid), alert_rule=alertRule1, host_tag=testTag2, operator="Minimum", threshold="20", value="0", team=team, metric=metrics[2])
        models.Alert.objects.create(host=models.Host.objects.get(guid=testHost[4].guid), alert_rule=alertRule2, host_tag=testTag3, operator="Maximum", threshold="99", value="100", team=team, metric=metrics[1])
        return  0