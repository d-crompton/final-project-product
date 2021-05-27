# Appears after the Email Input window, and will be the centre of the other windows after that point
# Allows the User to scan the network for devices and displays them
import socket
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import nmap
from PIL import Image, ImageTk
import Email_Handler
import File_Handler
from Devices import Device, Trusted_Device, Suspicious_Device
from Windows import Trusted_Devices_Window, Suspicious_Devices_Window, Blacklist_Window, Email_Input, Device_Info_Window


class ScannerWindow:
    # Constructor
    def __init__(self, email):
        # Class Variables
        self.device_frame_row = 0  # Sets the current device row to 0, used in loop adding devices to frame
        self.device_frame_used_height = 0  # Used to update the occupied space of device frame (used in scrolling)
        self.email = email  # Passed to and from the "Devices" windows
        self.router = None  # When a device with IP .1 is found, this is identified as the router and used in sniffing
        self.icon_list = []  # Used to store icons
        # Defining Device List variables to be used and prepapring them
        self.trusted_devices = []
        self.suspicious_devices = []
        self.found_trusted = []  # Used in email
        self.found_suspicious = []  # used in email
        self.prepare_device_lists()
        self.check_for_router()
        # Creating Root Window
        self.root = Tk()
        self.root.title("Network Device Scanner")
        self.root.geometry("500x530")
        self.root.resizable(0, 0)  # Disables Maximum button
        # Set two Columns for structure
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        # Adding Widgets
        button_bg = "#669999"  # Background Colour for Buttons
        # Passed in email, and button to return and change the email
        self.email = email  # Self property used with email function later
        curr_email_text = "Email: " + self.email
        email_lbl = Label(self.root, text=curr_email_text, pady=0).grid(row=0, column=0, pady=0, sticky="W")
        email_button = Button(self.root, text="Change Email", bg=button_bg, command=self.open_email_input)
        email_button.grid(row=0, column=1, sticky="E")
        # Title Label
        title_lbl = Label(self.root, pady=0, text="Home Network Scanner")
        title_lbl.grid(row=1, columnspan=2, pady=(0, 10), sticky="WE")
        # Scan Button
        scan_btn = Button(self.root, text="Scan Network", width=50, padx=5, pady=5, bg=button_bg,
                          command=self.scan_button)
        scan_btn.grid(row=2, columnspan=2)
        # Progress Bar
        bar_style = ttk.Style()
        bar_style.theme_use('default')
        bar_style.configure("black.Horizontal.TProgressbar", background=button_bg)
        self.progress_bar = Progressbar(self.root, length=450, s="black.Horizontal.TProgressbar")
        self.progress_bar['value'] = 0
        self.progress_bar.grid(row=3, columnspan=2, padx=10, pady=5, sticky="WE")
        # Frame in which Canvas and Device Frame will go to allow Scrollbar
        self.outer_canvas_frame = Frame(self.root, height=300, width=450)
        self.outer_canvas_frame.grid(row=4, columnspan=2, sticky="NSEW", padx=10)
        self.outer_canvas_frame.grid_columnconfigure(0, weight=1)
        self.outer_canvas_frame.grid_rowconfigure(0, weight=1)
        self.outer_canvas_frame.grid_propagate(0)
        # Canvas - Device Frame will go in this
        self.device_frame_canvas = Canvas(self.outer_canvas_frame, bg="#f0f0f5",
                                          highlightbackground="black", highlightthickness=1)
        self.device_frame_canvas.grid(sticky="NSEW")
        self.device_frame_canvas.grid_rowconfigure(0, weight=1)
        self.device_frame_canvas.grid_columnconfigure(0, weight=1)
        # Scroll bar
        self.scrollbar = Scrollbar(self.outer_canvas_frame, orient="vertical", command=self.device_frame_canvas.yview)
        # self.device_frame_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="NSE")
        # Device Frame - Where found devices are displayed
        self.device_frame = Frame(self.device_frame_canvas, width=self.device_frame_canvas.winfo_width())
        # Created window is used to add Device Frame into the Canvas widget, used instead of .grid
        self.device_frame_canvas.create_window((0, 0), window=self.device_frame, anchor="nw")
        self.device_frame.columnconfigure(0, weight=1)
        self.device_frame_canvas.bind('<Configure>',  # Allow the Canvas' height to be scrollable
                                      lambda e: self.device_frame_canvas.configure(
                                          scrollregion=self.device_frame_canvas.bbox("all"))
                                      )
        self.device_frame_canvas.configure(yscrollcommand=self.scrollbar.set)  # Links up canvas and scrollbar activity
        # Buttons at bottom
        trusted_btn = Button(self.root, text="Trusted Devices", width=30, pady=5, bg=button_bg,
                             command=self.open_trusted_window)
        trusted_btn.grid(row=5, pady=(5, 10))
        suspect_btn = Button(self.root, text="Suspicious Devices", width=30, pady=5, bg=button_bg,
                             command=self.open_suspicious_window)
        suspect_btn.grid(row=5, column=1, pady=(5, 10))
        blacklist_btn = Button(self.root, text="Blacklisted Sites", width=30, pady=5, bg=button_bg,
                               command=self.open_blacklist_window)
        blacklist_btn.grid(row=6, columnspan=2)
        # Main Loop - No code after this
        self.root.mainloop()

    """
        CLASS FUNCTIONS
    """
    # SCAN BUTTON AND ASSOCIATED FUNCTIONS
    def scan_button(self):
        # Setting initial parameters
        self.prepare_device_lists()
        # Clear Device Frame for new scan results to be added
        for child in self.device_frame.winfo_children():
            child.destroy()
            self.root.update()
        self.progress_bar['value'] = 5  # Update progress bar to show scan is started, program is working
        self.device_frame_used_height = 0
        # Initial scan to get available hosts' IPs
        nm = nmap.PortScanner()
        try:
            quick_scan = nm.scan(hosts=self.get_ip_range(), arguments='-F')
            hosts = nm.all_hosts()
            progress_per_host = (95 / len(hosts))  # How much the progress bar increases per device
        except nmap.PortScannerError:
            print("Port Scanner Error")
            warning = tkinter.messagebox.showwarning("Port Scan Error",
                                                     "Unable to scan network, please check network connection")
            return  # Exit function if unable to scan
        # OS Scan of each of the devices found - then compare them with the Device Lists
        for host in hosts:
            curr_device = self.os_scan_obj_func(host)  # device obj with details retrieved from scan
            # Check whether the device is in either list
            if self.check_dev_list(curr_device, self.trusted_devices) is not False:
                self.add_new_device_frame(self.check_dev_list(curr_device, self.trusted_devices), "trusted")
            elif self.check_dev_list(curr_device, self.suspicious_devices) is not False:
                self.add_new_device_frame(self.check_dev_list(curr_device, self.suspicious_devices), "suspicious")
            else:
                # Displays pop up prompting whether they want to add to trusted or suspicious devices list.
                self.pop_up_new_dev(curr_device)
            # Update the progress bar, end of this devices' iteration
            self.update_progress(progress_per_host)
        # Configure scrollbar after#
        self.root.update()
        self.device_frame_canvas.configure(scrollregion=self.device_frame_canvas.bbox("all"))
        # Update lists
        File_Handler.write_trust_file(self.trusted_devices)
        File_Handler.write_suspicious_file(self.suspicious_devices)
        # Show pop-up to let the User know
        tkinter.messagebox.showinfo("Network Scan", "Scan finished")
        email_handler = Email_Handler.EmailHandler(self.email, "Network Scan Results")
        email_handler.send_email(email_handler.generate_network_scan_body(self.found_trusted, self.found_suspicious))

    # Clears the Device arrays and reloads the lists from the text files
    def prepare_device_lists(self):
        # Opening files and filling "local" device lists
        self.trusted_devices = File_Handler.load_trusted_file()
        self.suspicious_devices = File_Handler.load_suspicious_file()
        # Clear 'Found' lists for new scan
        self.found_trusted = []
        self.found_suspicious = []

    # Check for the Router (.1 IP) to be used in traffic sniffing later on
    def check_for_router(self):
        for device in self.trusted_devices:
            if device.get_last_ip().split(".")[3] == "1":
                self.router = device
                return
        for device in self.suspicious_devices:
            if device.get_last_ip().split(".")[3] == "1":
                self.router = device
                return

    # Get device's IP address then use it to generate range for Nmap quick scan
    def get_ip_range(self):
        # Get current device's IP
        host_dev = socket.gethostname()
        dev_ip = socket.gethostbyname(host_dev)
        # Create range from this - XXX.XXX.XXX.XXX/24
        split_ip = dev_ip.split('.')
        return split_ip[0] + "." + split_ip[1] + "." + split_ip[2] + ".1/24"

    # Runs an nmap scan for the device's IP and then creates a device object with the details it returns
    def os_scan_obj_func(self, host):
        nm = nmap.PortScanner()
        os_scan = nm.scan(hosts=host, arguments='-O -F')
        # Try to get device details from scan results, provide X not Available to avoid errors
        try:  # MAC Address
            mac = os_scan['scan'][host]['addresses']['mac']
        except KeyError:  # Error if the dictionary key is not available
            mac = "Mac Address not Available"
        try: # Manufacturer
            manufacturer = os_scan['scan'][host]['vendor'][mac]
        except KeyError:
            manufacturer = "Manufacturer not Available"
        try:  # Operating System
            op_sys = os_scan['scan'][host]['osmatch'][0]['name']  # 'os' is already used by Python
        except KeyError:
            op_sys = "OS not Available"
        except IndexError:
            op_sys = "OS not Available"
        try:  # Type - this is assigned by Nmap's OS Scan
            dev_type = os_scan['scan'][host]['osmatch'][0]['osclass'][0]['type']
        except KeyError:
            dev_type = "Type Unknown"
        except IndexError:
            dev_type = "Type Unknown"
        # Return a Device object with these details to be used in the rest of the scan button code
        returned_device = Device.Device(host, mac, manufacturer, op_sys, dev_type)
        # Check whether the IP address is .1 and is so assign as the router - used in the traffic sniffing functions
        if host.split('.')[3] == "1":
            self.router = returned_device
        return returned_device

    # Checks whether the argument device is in the argument list, merged into one function to avoid repeating code
    def check_dev_list(self, curr_device, dev_list):
        for device in dev_list:
            # Start by checking whether the new device and existing devices' MACs match
            if device.get_mac() == curr_device.get_mac():
                # Further confirm whether the manufacturers are the same - in case MACs are unavailable for both
                if device.get_manufacturer() == curr_device.get_manufacturer():
                    # Then confirm whether the OSes are the same
                    if device.get_os() == curr_device.get_os():
                        # Last check is whether the current IP is the same as the stored IP, if not then update
                        if device.get_last_ip() != curr_device.get_last_ip():
                            device.set_last_ip(curr_device.get_last_ip())
                        # If all details match, return the device ending the loop
                return device
        # Runs if the return device hasn't been reached
        return False

    # Function handling the pop-up that appears when a unknown device is found
    def pop_up_new_dev(self, device):
        # Creating and displaying the Pop-Up message asking if User wants to trust device
        pop_up_message = "Do you want to add the following device to your Trusted Devices?:\n" + \
                         "MAC Address: " + device.get_mac() + "\n" + \
                         "IP Address: " + device.get_last_ip() + "\n" + \
                         "Manufacturer: " + device.get_manufacturer() + "\n" + \
                         "OS: " + device.get_os() + "\n" + \
                        "Device Type: " + device.get_type()
        trust_input = tkinter.messagebox.askquestion("New Device Found", pop_up_message)
        # Handling the response from the User
        if trust_input == "yes":  # User wants to trust device, add device to the Trusted Devices list
            name_question_input = tkinter.messagebox.askquestion("New Device Found",
                                                                 "Do you want to give the trusted device a name?")
            if name_question_input == "yes":
                device_name = tkinter.simpledialog.askstring(title="New Device Found",
                                                             prompt="Enter the name for the new device")
            elif name_question_input == "no":
                device_name = "Trusted Device"  # If User doesn't give a name, just assign default name
            # Create new Trusted Device and add it to the local list, to be written into the file's list at the end
            new_trusted_dev = Trusted_Device.TrustedDevice(device.get_last_ip(), device.get_mac(),
                                                           device.get_manufacturer(), device.get_os(),
                                                           device.get_type(), device_name)
            self.trusted_devices.append(new_trusted_dev)
            self.found_trusted.append(new_trusted_dev)
            self.add_new_device_frame(new_trusted_dev, "trusted")  # Create frame for device
        elif trust_input == "no":  # User suspects device, add device to the Suspicious Devices list
            new_suspicious_dev = Suspicious_Device.SuspiciousDevice(device.get_last_ip(), device.get_mac(),
                                                                    device.get_manufacturer(), device.get_os(),
                                                                    device.get_type())
            self.suspicious_devices.append(new_suspicious_dev)
            self.found_suspicious.append(new_suspicious_dev)
            self.add_new_device_frame(new_suspicious_dev, "suspicious")

    # Add progress to the progress bar, avoiding redundant code
    def update_progress(self, progress):
        self.progress_bar['value'] += progress

    # Add found devices' details to the Device Frame, category determines whether its bg is green (trusted) or red
    def add_new_device_frame(self, device, category):
        # Check whether device is trusted or not to decide bg colour, also decide whether it has a name or not
        if category == "trusted":
            frame_bg = '#adebad'  # Light Green
            device_name = device.get_name()
            # Add device to found trusted devices for email
            self.found_trusted.append(device)
        elif category == "suspicious":
            frame_bg = "#ffb3b3"  # Red
            device_name = "Suspicious Device"
            # Add device to found suspicious devices for email
            self.found_suspicious.append(device)
        # Create frame for this device
        frame = Frame(self.device_frame, bg=frame_bg, highlightbackground="black", highlightthickness=1)
        frame.grid(column=0, row=self.device_frame_row, sticky="WE")
        frame.grid_columnconfigure(0, weight=6, uniform="a")  # Col with labels
        frame.grid_columnconfigure(1, weight=2, uniform="a")  # Col with Icon
        frame.grid_columnconfigure(2, weight=2, uniform="a")  # Col with buttons
        name_lbl = Label(frame, text=device_name, bg=frame_bg, width=38, anchor='w').grid(row=0, column=0, sticky="W")
        host_lbl = Label(frame, text=device.get_last_ip(), bg=frame_bg).grid(row=1, column=0, sticky="W")
        manu_lbl = Label(frame, text=device.get_manufacturer(), bg=frame_bg, anchor='w')
        manu_lbl.grid(row=2, column=0, sticky="W")
        # Creating Icon label
        try:  # Try used in case of icon FileNotFoundError
            icon_path = "Icons/" + device.get_type() + ".png"
            self.icon_list.append(ImageTk.PhotoImage(Image.open(icon_path)))
            icon_lbl = Label(frame, image=self.icon_list[-1], bg=frame_bg)
            icon_lbl.grid(row=0, rowspan=3, column=1, sticky="WE")
        except FileNotFoundError:  # If icon file cannot be found, create a blank label
            icon_lbl = Label(frame, bg=frame_bg).grid(row=0, rowspan=3, column=1, sticky="WE")
        info_btn = Button(frame, width=8, text="Info",
                          command=lambda curr_device=device: self.open_info_window(
                              curr_device, self.email, "scanner"))
        info_btn.grid(row=0, column=2, rowspan=3, pady=5, sticky="NESW")
        # Update the height of the containing devices frame - used in scrolling
        self.device_frame_used_height += frame.winfo_height()
        if self.device_frame_used_height > self.device_frame.winfo_height():
            self.device_frame.config(height=self.device_frame_used_height)
        self.device_frame.update_idletasks()  # Causes window to update with new device frame
        self.device_frame_row += 1

    # ===========================
    # NAVIGATION BUTTON FUNCTIONS
    def open_info_window(self, device, email, source):
        device_info_window = Device_Info_Window.DeviceInfoWindow(device, email, source, self.router)

    def open_trusted_window(self):
        self.root.destroy()
        trusted_window = Trusted_Devices_Window.TrustedDevicesWindow(self.email, self.router)

    def open_suspicious_window(self):
        self.root.destroy()
        suspicious_window = Suspicious_Devices_Window.SuspiciousDevicesWindow(self.email, self.router)

    def open_blacklist_window(self):
        blacklist_window = Blacklist_Window.BlacklistWindow()

    def open_email_input(self):
        self.root.destroy()
        email_window = Email_Input.EmailInputWindow()