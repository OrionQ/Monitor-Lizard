from time import time

# The base class host plugin
# To make a new host plugin:
# 1) Make a file in host_plugins/
# 2) Make a class that extends HostPlugin
# 3) Populate _probes with the probes you want


class HostPlugin:
    """
    Measure probes that should be measured
    .guid = the guid of the host that sent the report
    ._probes = a list of probes this report can send
    .metrics = a dict of metrics that report will send, keyed by metric name
    """
    _probes = []

    def measure(self, last_polls=None, polling_config=None):
        assert last_polls is not None and polling_config is not None
        metrics = {}

        for probe in self._probes:
            probe = probe()
            if (self.probe_should_send(probe, polling_config, last_polls)):
                metrics[probe.name] = probe.measure()
                last_polls[probe.name] = time()

        return metrics

    def probe_should_send(self, probe, polling_config, last_polls):
        """Calculate whether the report should poll the corresponding metric, according to its data in the polling_config"""
        return True


# The probe base class
# To make a new probe:
# 0) Make sure there exists a cooresponding metric
# 1) Make a new HostPlugin to put it on (see above) or choose an existing report
# 2) Define a name (must be unique and match metric) and default_polling_interval
# 3) Define the measure method. The measure method will only actually run when the probe is polled for data


class Probe:
    name = None
    default_polling_interval = None

    def measure(self):
        return None
