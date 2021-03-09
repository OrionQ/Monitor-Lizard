from web.host_plugin import HostPlugin, Probe

# Measurements of the cpu to be sent


class CpuUsage(Probe):
    name = 'cpu_usage'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return 60


class CpuTemperature(Probe):
    name = 'cpu_temperature'
    default_polling_interval = 60*60

    @staticmethod
    def measure():
        return 60


class ProbePlugin(HostPlugin):
    _probes = [
        CpuUsage,
        CpuTemperature,
    ]
