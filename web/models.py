from django.db import models

# Models for the MonitorLizard web application


class Metric(models.Model):
    """A Quantity measured on a host machine"""
    METRIC_TYPES = (
        ('int', 'Integer'),
        ('float', 'Floating point'),
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
    time = models.DateTimeField(auto_now=True)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
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


class AlertRule(models.Model):
    """Definitions of alerts and when they should be tripped"""
    ALERT_OPERANDS = (
        ('min', 'Minimum'),
        ('max', 'Maximum'),
    )
    # Host Tag to be watched for the alert
    host_tag = models.ForeignKey(HostTag, on_delete=models.CASCADE)
    # Team to be notified of alert
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # Metric to watch
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    threshold = models.JSONField()
    operator = models.TextField(choices=ALERT_OPERANDS)
    severity = models.PositiveSmallIntegerField('Alert Severity (0 highest)')


class Alert(models.Model):
    """Alerts that have been thrown"""
    time = models.DateTimeField(auto_now=True)
    # Alert rule that threw this alert
    alert_rule = models.ForeignKey(
        AlertRule, on_delete=models.SET_NULL, null=True)
    # Save properties of alert rule, in case it changes or is deleted
    host_tag = models.ForeignKey(HostTag, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    threshold = models.JSONField()
    operator = models.TextField(choices=AlertRule.ALERT_OPERANDS)

    # Report that tripped this alert
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    # Save properties of report, for when it's deleted
    time = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True)
    value = models.JSONField()

    # Team to be notified of alert
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    notes = models.TextField()
    acknowledged_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]
