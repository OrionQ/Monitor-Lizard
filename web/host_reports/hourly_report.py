from web.host_report import HostReport

# A report to send hourly from the host


class HourlyReport(HostReport):
    """A report to be sent by every host every hour. Currently only contains cpu_usage and cpu_temperature"""

    polling_interval = 60*60

    def __init__(self, guid=None):
        HostReport.__init__(self, guid, metrics={
            'CPU Usage': self.measure_cpu_usage(),
            'CPU Temp': self.measure_cpu_temperature(),
        }, )

    def measure_cpu_usage(self):
        return None

    def measure_cpu_temperature(self):
        return None
