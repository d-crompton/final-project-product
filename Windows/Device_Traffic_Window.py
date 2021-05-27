from tkinter import *
import tkinter.messagebox
import Traffic_Sniff_Class
import File_Handler
import Email_Handler


class DeviceTrafficWindow:
    # Constructor
    # Target Device is the device which we are monitoring
    # Host Device will be the router (device on .1 IP) that we are impersonating
    def __init__(self, target_device, host_device, email):
        # Creating Variables used
        self.target_device = target_device
        self.host_device = host_device
        self.blacklisted_sites = File_Handler.load_blacklist_file()
        self.email = email
        # Creating Window
        self.root = Tk()
        self.root.title("Network Traffic Sniffer")
        self.root.geometry("400x400")
        self.root.resizable(0, 0)  # Disables Maximum button
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        title_lbl = Label(self.root, text="Network Traffic Sniffer")
        title_lbl.grid(row=0, sticky="WE")
        device_sub_title_lbl = Label(self.root, text="Device Information").grid(row=1, sticky="W", padx=(5, 0))
        # If Device is trusted, display its name, add a row adjustment
        row_adj = 0  # Row Adjustment - caused by name label
        if target_device.get_category() == "trusted":
            row_adj = 1
            device_name_lbl = Label(self.root, text="Device Name: " + target_device.get_name())
            device_name_lbl.grid(row=2, sticky="W", padx=(5, 0))
        # Remaining labels
        ip_lbl = Label(self.root, text="Current IP: " + target_device.get_last_ip())
        ip_lbl.grid(row=2+row_adj, sticky="W", padx=(5, 0))
        mac_lbl = Label(self.root, text="MAC Address: " + target_device.get_mac())
        mac_lbl.grid(row=3+row_adj, sticky="W", padx=(5, 0))
        os_lbl = Label(self.root, text="Operating System: " + target_device.get_os(), anchor="w")
        os_lbl.grid(row=4+row_adj, sticky="W", padx=(5, 0))
        manu_lbl = Label(self.root, text="Manufacturer: " + target_device.get_manufacturer())
        manu_lbl.grid(row=5+row_adj, sticky="W", padx=(5, 0))
        type_lbl = Label(self.root, text="Device Type: " + target_device.get_type())
        type_lbl.grid(row=6+row_adj, sticky="W", padx=(5, 0))
        sniff_button = Button(self.root, text="Sniff Traffic", bg="#669999", command=self.sniff_button)
        sniff_button.grid(row=7+row_adj, sticky="WE", padx=10, pady=5)
        # Create Frame to put sniffing results in
        self.results_frame = Frame(self.root, bg="#f0f0f5", height=170, width=260,
                                   highlightbackground="black", highlightthickness=1)
        self.results_frame.grid(row=8+row_adj, sticky="NWSE", padx=10, pady=10)
        self.results_frame.grid_propagate(0)  # Prevent children re-shaping frame
        # Mainloop
        self.root.mainloop()

    def sniff_button(self):
        # Clear the existing domain list
        for child in self.results_frame.winfo_children():
            child.destroy()
        # Create Sniffer Class and run function
        sniffer = Traffic_Sniff_Class.TrafficSniffer(self.target_device.get_last_ip())
        domains = sniffer.sniffing_function(self.target_device.get_last_ip(),
                                            self.target_device.get_mac(),
                                            self.host_device.get_last_ip())
        curr_row = 0
        flagged_domains = []
        for domain in domains:
            if domain in self.blacklisted_sites:
                flagged_domains.append(domain)
                domain_label = Label(self.results_frame, text=domain, fg="#ff0000").grid(row=curr_row, sticky="W")
            else:
                domain_label = Label(self.results_frame, text=domain).grid(row=curr_row, sticky="W")
            curr_row += 1
        tkinter.messagebox.showinfo("Network Scan", "Scan finished")
        if len(flagged_domains) >= 1:
            email_handler = Email_Handler.EmailHandler(self.email, "Activity with Blacklisted Domain")
            email_handler.send_email(email_handler.generate_sniff_body(self.target_device, flagged_domains))