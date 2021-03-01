from .models import Report, Metric, Host

# The base class host report
# To make a new report:
# 1) Make a class that extends HostReport
# 2) Put it in host_reports/
# 3) Put it in web.management.commands.host_daemon.Command.reports


class HostReport:
    """
    A report sent from the host daemon to the processing daemon over the message queue.
    .guid = the guid of the host that sent the report
    .metrics = a dict of metrics that host has, keyed by metric name
    .polling_interval = how often the report should be sent, in seconds
    """

    polling_interval = None

    def __init__(self, guid=None, metrics=[]):
        assert guid is not None
        self.guid = guid
        self.metrics = metrics

    def generate_report_models(self):
        """
        Generate multiple report models from this report.
        To be used once the report is on the processing daemon!
        """

        reports = []
        host = Host.objects.get(guid=self.guid)
        for metric, value in self.metrics:
            reports.append(Report(metric=Metric.objects.get(
                name=metric), host=host, value=value))
        return reports
