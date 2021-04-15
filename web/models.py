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

    def __str__(self):
        return f"Metric: {self.category} {self.name} (self.metric_type)"

    class Meta:
        indexes = [
            models.Index(fields=['category', 'name']),
        ]


class Host(models.Model):
    """A host that reports to the MonitorLizard system"""
    guid = models.UUIDField()
    tags = models.ManyToManyField('HostTag')
    name = models.TextField()

    def __str__(self):
        return f"Host: {self.name} {self.guid}"

    class Meta:
        indexes = [
            models.Index(fields=['guid', 'name']),
        ]


class HostTag(models.Model):
    """A collection of hosts"""
    hosts = models.ManyToManyField(Host, blank=True)
    name = models.TextField()
    registration_key = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Host Tag: {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['registration_key']),
        ]


class Report(models.Model):
    """A report from a host containing the value of a specific metric"""
    time = models.DateTimeField(auto_now=True)
    metric = models.ForeignKey(Metric, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True)
    value = models.JSONField()

    def __str__(self):
        return f"{self.time} report of {self.metric.name} for {self.host.guid}"

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]


class Team(models.Model):
    """A group of users"""
    name = models.TextField()
    users = models.ManyToManyField('User')

    def __str__(self):
        return f"Team: {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class User(models.Model):
    """Users who receive notifications"""
    name = models.TextField()
    notification_email = models.EmailField(null=True, blank=True)
    notification_phone = models.CharField(max_length=20, null=True, blank=True)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return f"User: {self.name}"

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
    host_tag = models.ForeignKey(HostTag, on_delete=models.SET_NULL, null=True)

    # Team to be notified of alert
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    # Metric to watch
    metric = models.ForeignKey(Metric, on_delete=models.SET_NULL, null=True)
    threshold = models.JSONField()
    operator = models.TextField(choices=ALERT_OPERANDS)
    severity = models.PositiveSmallIntegerField('Alert Severity (0 highest)')

    def __str__(self):
        return f"Alert rule: {self.team.name} watching {self.metric.name} of {self.host_tag.name}"


class Alert(models.Model):
    """Alerts that have been thrown"""

    # Alert rule that threw this alert
    alert_rule = models.ForeignKey(
        AlertRule, on_delete=models.SET_NULL, null=True)

    # Save properties of alert rule, in case it changes or is deleted
    host_tag = models.ForeignKey(HostTag, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    metric = models.ForeignKey(Metric, on_delete=models.SET_NULL, null=True)
    threshold = models.JSONField()
    operator = models.TextField(choices=AlertRule.ALERT_OPERANDS)

    # Report that tripped this alert
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)

    # Save properties of report, for when it's deleted
    time = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True)
    value = models.JSONField()

    notes = models.TextField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Alert: {self.team.name} alerted about {self.metric.name} on {self.host.guid}"

    @classmethod
    def create(cls, alert_rule=None, report=None):
        assert alert_rule is not None and report is not None
        alert = cls(alert_rule=alert_rule, host_tag=alert_rule.host_tag, team=alert_rule.team, metric=alert_rule.metric, threshold=alert_rule.threshold,
                    operator=alert_rule.operator, report=report, time=report.time, host=report.host, value=report.value)
        return alert

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]
