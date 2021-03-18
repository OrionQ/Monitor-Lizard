from time import time
from .models import Metric

# The base class host plugin
# To make a new host plugin:
# 1) Make a file in host_plugins/
# 2) Make a class that extends HostPlugin
# 3) Populate _probes with the probes you want


class HostPlugin:
    """
    Measure probes that should be measured
    ._probes = a list of probes this report can send
    """
    _probes = []

    @classmethod
    def measure(cls, last_polls=None, polling_config=None):
        assert last_polls is not None and polling_config is not None
        metrics = {}

        for probe in cls._probes:
            if (cls.probe_should_send(probe, polling_config, last_polls)):
                metrics[probe.name] = probe.measure()
                last_polls[probe.name] = time()

        return metrics

    @classmethod
    def generate_metrics(cls):
        metrics = []
        for probe in cls._probes:
            metrics.append(probe.generate_metric())
        return metrics

    @staticmethod
    def probe_should_send(probe, polling_config, last_polls):
        """Calculate whether the report should poll the corresponding metric, according to its data in the polling_config"""
        return True


# The probe base class
# To make a new probe:
# 0) Make sure there exists a cooresponding metric
# 1) Make a new HostPlugin to put it on (see above) or choose an existing report
# 2) Define a name (must be unique and match metric) and default_polling_interval
# 3) Define the measure method. The measure method will only actually run when the probe is polled for data


class Probe:
    category = None
    name = None
    metric_type = None
    description = None
    default_polling_interval = None

    @staticmethod
    def measure():
        return None

    @classmethod
    def generate_metric(cls):
        assert cls.category is not None and cls.name is not None and cls.metric_type is not None
        return Metric(category=cls.category, name=cls.name, metric_type=cls.metric_type, description=cls.description)
