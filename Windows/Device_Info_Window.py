# Window that appears when a User presses an information button
# Accessible from Scanner, Trusted Device and Suspicious Device windows
from tkinter import *
from Windows import Device_Traffic_Window, Trusted_Devices_Window, Suspicious_Devices_Window
import File_Handler


class DeviceInfoWindow:
    # Constructor
    def __init__(self, device, email, source, router):
        # Variables used to return to the correct window
        self.device = device
        self.email = email
        self.source = source  # Window the User originated from
        self.router = router  # Used in traffic sniffing
        # Creating window
        self.root = Tk()
        self.root.title("Device Information")
        self.root.geometry("300x260")
        self.root.resizable(0, 0)  # Disables Maximum button
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        title_lbl = Label(self.root, text="Device Information")
        title_lbl.grid(row=0, padx=(10, 5), sticky="WE")
        # Check whether device is Trusted or not, using to make title
        if device.get_category() == "trusted":
            name_lbl = Label(self.root, text=device.get_name())
        elif device.get_category() == "suspicious":
            name_lbl = Label(self.root, text="Suspicious Device")
        else:  # Else added to prevent issues
            name_lbl = Label(self.root, text="Device")
        name_lbl.grid(row=1, padx=(10, 5), sticky="WE")
        mac_text = "MAC Address: " + device.get_mac()  # MAC Address Label
        mac_lbl = Label(self.root, text=mac_text, anchor="w").grid(row=2, padx=(10, 5), sticky="W")
        last_ip_text = "Last IP Address: " + device.get_last_ip()  # IP Address Label
        last_ip_lbl = Label(self.root, text=last_ip_text, anchor="w").grid(row=3, padx=(10, 5), sticky="W")
        os_text = "Operating System: " + device.get_os()  # OS Label
        os_lbl = Label(self.root, text=os_text, anchor="w").grid(row=4, padx=(10, 5), sticky="W")
        manu_text = "Manufacturer: " + device.get_manufacturer()  # Manufacturer Label
        manu_lbl = Label(self.root, text=manu_text, anchor="w").grid(row=5, padx=(10, 5), sticky="W")
        type_text = "Device Type: " + device.get_type()  # Device Type - assigned by Nmap
        type_lbl = Label(self.root, text=type_text, anchor="w").grid(row=6, padx=(10, 5), pady=(0, 10), sticky="W")
        # Remove from.. buttons - adjust text depending on whether device is trusted or not
        if device.get_category() == "trusted":
            remove_txt = "Remove from Trusted Devices"
        elif device.get_category() == "suspicious":
            remove_txt = "Remove from Suspicious Devices"
        else:
            remove_txt = "Remove Device"
        remove_button = Button(self.root, text=remove_txt, bg="#669999", command=self.remove_button)
        remove_button.grid(row=7, padx=10, pady=(0, 5), sticky="WE")
        # Button to open Device Traffic Window - does not appear if the device does not have a MAC
        r = 0  # Used to add correct number of rows after the Device Traffic button
        if device.get_mac() != "Mac Address not Available":
            traffic_button = Button(self.root, text="See Device Traffic", bg="#669999",
                                    command=lambda device=device: self.traffic_button(device))
            traffic_button.grid(row=8, padx=10, pady=(0, 5), sticky="WE")
            r += 1
        return_button = Button(self.root, text="Return", bg="#669999", command=self.return_button)
        return_button.grid(row=8 + r, padx=10, pady=(0, 5), sticky="WE")
        # Mainloop, no code after this
        self.root.mainloop()

    # Button Functions
    def remove_button(self):
        # Loads the existing trusted file and creates a list to replace it
        if self.device.get_category() == "trusted":
            curr_device_list = File_Handler.load_trusted_file()
        elif self.device.get_category() == "suspicious":
            curr_device_list = File_Handler.load_suspicious_file()
        new_device_list = []
        # Check whether the device has a mac address or not, if so loop using the MAC, if not use manufacturer and IP
        if self.device.get_mac() != "Mac Address not Available":
            # Loop through devices in current list, writing them into the new list IF they are not the current device
            for d in curr_device_list:
                if d.get_mac() == self.device.get_mac():
                    continue  # If device is present in existing list, ignore it
                elif d.get_mac() is not self.device.get_mac():
                    new_device_list.append(d)
        # If a MAC address is not available, check whether the device's last IP and last manufacturer match
        elif self.device.get_mac() == "Mac Address not Available":
            for d in curr_device_list:
                if d.get_last_ip() == self.device.get_last_ip():
                    if d.get_manufacturer() == self.device.get_manufacturer():
                        continue  # If devices appear to be the same, do not write it into the new list
                    else:
                        new_device_list.append(d)  # Write to the new list
                        continue  # Move onto the next device 'd'
                else:
                    new_device_list.append(d)
        # Once the loop has finished, rewrite to the appropriate text file list
        if self.device.get_category() == "trusted":
            File_Handler.write_trust_file(new_device_list)
        elif self.device.get_category() == "suspicious":
            File_Handler.write_suspicious_file(new_device_list)
        # After file has written, return to the previous window
        self.return_button()

    # Button that opens the Traffic Sniffer window
    def traffic_button(self, device):
        device_info_window = Device_Traffic_Window.DeviceTrafficWindow(device, self.router, self.email)

    # Button that closes this window, and returns the window the User originally came from
    def return_button(self):
        # Closes the window and returns to the window the User was originally on
        if self.source == "trusted_devices_window":
            self.root.destroy()
            trusted_window = Trusted_Devices_Window.TrustedDevicesWindow(self.email, self.router)
        elif self.source == "suspicious_devices_window":
            self.root.destroy()
            suspicious_window = Suspicious_Devices_Window.SuspiciousDevicesWindow(self.email, self.router)
        else:  # If the User opened the window from the main scanner window, then the window is just closed
            self.root.destroy()
