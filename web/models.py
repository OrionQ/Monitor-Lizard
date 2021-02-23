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
    tags = models.ManyToManyField('HostTag')

    class Meta:
        indexes = [
            models.Index(fields=['guid']),
        ]


class HostTag(models.Model):
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
    metric = models.ForeignKey(Metric, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True)
    value = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]


class Team(models.Model):
    """A group of users"""
    name = models.TextField()
    users = models.ManyToManyField('User')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class User(models.Model):
    """Users who receive notifications"""
    name = models.TextField()
    notification_email = models.EmailField(null=True, blank=True)
    notification_phone = models.CharField(max_length=20, null=True, blank=True)
    teams = models.ManyToManyField(Team)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
