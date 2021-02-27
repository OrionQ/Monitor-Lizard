from .models import Report, Metric, Host

# All of the reports a host may want to send


class HostReport:
    """
    A report sent from the host daemon to the processing daemon over the message queue.
    .guid = the guid of the host that sent the report
    .metrics = a dict of metrics that host has, keyed by metric name
    """

    def __init__(self, guid=None, metrics=[]):
        assert guid is not None
        self.guid = guid
        self.metrics = metrics

    def persist(self):
        """
        Generate report models from this report and save to the db.
        Only use this once the report is on the processing daemon!
        """

        reports = []
        host = Host.objects.get(guid=self.guid)
        for metric, value in self.metrics:
            reports.append(Report(metric=Metric.objects.get(
                name=metric), host=host, value=value))
        Report.objects.bulk_create(reports)


class BasicReport(HostReport):
    """A basic report that just sends cpu usage and temp. Basically an example report"""

    def __init__(self, guid=None, cpu_usage=None, cpu_temperature=None):
        HostReport.__init__(self, guid, {
            'CPU Usage': cpu_usage,
            'CPU Temp': cpu_temperature,
        })
