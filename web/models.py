from django.db import models


class Metric(models.Model):
    METRIC_TYPES = (
        ('perc', 'Percent'),
        ('count', 'Count'),
        ('bits', 'Bits'),
    )
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    metric_type = models.CharField(max_length=5, choices=METRIC_TYPES)
    description = models.TextField()


class Host(models.Model):
    guid = models.UUIDField()


class HostTags(models.Model):
    hosts = models.ManyToManyField(Host)
    name = models.CharField(max_length=200)
    registration_key = models.CharField(max_length=256)


class Report(models.Model):
    time = models.DateTimeField()
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    host = models.ForeignKey(Host, on_delete=models.PROTECT)
    value = models.JSONField()
