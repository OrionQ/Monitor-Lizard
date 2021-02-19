from django.db import models

# Models for the MonitorLizard web application


class Metric(models.Model):
    """A Quantity measured on a host machine"""
    METRIC_TYPES = (
        ('int', 'Integer'),
        ('float', 'Floating'),
        ('array', 'List'),
    )
    category = models.TextField()
    name = models.TextField()
    metric_type = models.TextField(choices=METRIC_TYPES)
    description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'name']),
        ]


class Host(models.Model):
    """A host that reports to the MonitorLizard system"""
    guid = models.UUIDField()

    class Meta:
        indexes = [
            models.Index(fields=['guid']),
        ]


class HostTags(models.Model):
    """A collection of hosts"""
    hosts = models.ManyToManyField(Host)
    name = models.TextField()
    registration_key = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['registration_key']),
        ]


class Report(models.Model):
    """A report from a host containing the value of a specific metric"""
    time = models.DateTimeField()
    metric = models.ForeignKey(Metric, on_delete=models.SET_NULL)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]
