import psutil
from web.host_plugin import HostPlugin, Probe

# Measurements of the cpu to be sent


class DiskUsage(Probe):
    category = 'disk'
    name = 'disk_usage'
    metric_type = 'Integer'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return psutil.disk_usage()


class ProbePlugin(HostPlugin):
    _probes = [
        DiskUsage
    ]