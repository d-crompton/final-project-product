# Suspicious Devices - Child of Device
from Devices import Device


class SuspiciousDevice(Device.Device):
    # Constructor
    def __init__(self, last_ip, mac, manufacturer, os, dev_type):
        super().__init__(last_ip, mac, manufacturer, os, dev_type)
        self.category = "suspicious"

    # Additional Function
    def get_category(self):
        return self.category
