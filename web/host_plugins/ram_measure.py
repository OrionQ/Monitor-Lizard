import psutil
from web.host_plugin import HostPlugin, Probe

# Measurements of the cpu to be sent


class RamUsage(Probe):
    category = 'ram'
    name = 'ram_usage'
    metric_type = 'Integer'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return psutil.virtual_memory().percent


class ProbePlugin(HostPlugin):
    _probes = [
        RamUsage,
    ]
