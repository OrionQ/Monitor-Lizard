from web.host_report import HostReport, Probe

# Measurements of the cpu to be sent


class CpuUsage(Probe):
    name = 'cpu_usage'
    default_polling_interval = 60*60

    def measure(self):
        return 60


class CpuTemperature(Probe):
    name = 'cpu_temperature'
    default_polling_interval = 60*60

    def measure(self):
        return 60


class Report(HostReport):
    _probes = [
        CpuUsage,
        CpuTemperature,
    ]
