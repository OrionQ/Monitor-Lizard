import psutil
from web.host_plugin import HostPlugin, Probe

# Measurements of the cpu to be sent


class CpuUsage(Probe):
    category = 'cpu'
    name = 'cpu_usage'
    metric_type = 'Integer'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return psutil.cpu_percent()


class CpuTemperature(Probe):
    category = 'cpu'
    name = 'cpu_temperature'
    metric_type = 'Floating point'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return 60


class ProbePlugin(HostPlugin):
    _probes = [
        CpuUsage,
        CpuTemperature,
    ]
