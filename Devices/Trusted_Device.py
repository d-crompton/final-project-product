# Trusted Device - Child of Device
from Devices import Device


class TrustedDevice(Device.Device):
    # Constructor
    def __init__(self, last_ip, mac, manufacturer, os, dev_type, name):
        super().__init__(last_ip, mac, manufacturer, os, dev_type)
        self.name = name
        self.category = "trusted"

    # Additional Functions
    # Setter
    def set_name(self, name):
        self.name = name

    # Getters
    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

