from web.host_plugin import HostPlugin, Probe
from socket import gethostname, gethostbyname

# Measurements of the network to be sent
class HostName(Probe):
    category = 'network'
    name = 'host_name'
    metric_type = 'String'
    default_polling_interval = 60*60
    
    @staticmethod
    def measure():
        return gethostname()
    
class IPAddress(Probe):
    category = 'network'
    name = 'ip_address'
    metric_type = 'String'
    default_polling_interval = 60*60
    
    @staticmethod
    def measure():
        return gethostbyname(gethostname())
    
class ProbePlugin(HostPlugin):
    _probes = [
        HostName,
        IPAddress,
    ]