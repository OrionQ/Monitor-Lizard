from .models import Report, Metric, Host
import configparser
import time

# The base class host report
# To make a new report:
# 1) Make a file in host_reports/
# 2) Make a class that extends HostReport
# 3) Populate _probes with the probes you want


class HostReport:
    """
    A report sent from the host daemon to the processing daemon over the message queue.
    .guid = the guid of the host that sent the report
    ._probes = a list of probes this report can send
    .metrics = a dict of metrics that report will send, keyed by metric name
    """
    _probes = []

    def __init__(self, guid=None):
        assert guid is not None
        self.guid = guid
        self.metrics = {}
        polling_config = self.get_metric_polling_config()
        print(polling_config)

        for probe in self._probes:
            if (self.should_send(polling_config, probe)):
                probe = probe()
                self.metrics[probe.name] = probe.measure()
                polling_config.set('last_poll', probe.name, str(time.time()))

        self.save_metric_polling_config(polling_config)

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

    def get_metric_polling_config(self):
        config = configparser.ConfigParser()
        config.read('host_report_config.ini')
        if not config.has_section('last_poll'):
            config.add_section('last_poll')
        if not config.has_section('polling_intervals'):
            config.add_section('polling_intervals')
        return config

    def save_metric_polling_config(self, config):
        with open('host_report_config.ini', 'w') as configfile:
            config.write(configfile)

    def should_send(self, polling_config, probe):
        """Calculate whether the report should poll the corresponding metric, according to its data in the polling_config"""
        return True

# The probe base class
# To make a new probe:
# 0) Make sure there exists a cooresponding metric
# 1) Make a new Report to put it on (see above) or choose an existing report
# 2) Define a name (must be unique) and default_polling_interval
# 3) Define the measure method. The measure method will only actually run when the probe is polled for data


class Probe:
    name = None
    default_polling_interval = None

    def measure(self):
        return None
