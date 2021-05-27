# Window opened from the Scanner Window - Displays any saved Trusted Devices
# Links to the Device Info window
from tkinter import *
from PIL import Image, ImageTk
import File_Handler
from Windows import Scanner_Window, Device_Info_Window


class TrustedDevicesWindow:
    # Constructor
    def __init__(self, email, router):
        self.email = email  # Used in re-opening the scanner window
        self.router = router  # Passed into the Device Info windows for traffic sniffing
        # Opening List File
        self.devices = File_Handler.load_trusted_file()  # Used to store devices locally
        # Creating Window
        self.root = Tk()
        self.root.title("Trusted Devices")
        self.root.geometry("400x400")
        self.root.resizable(0, 0)  # Disables Maximum button
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        title_lbl = Label(self.root, text="Trusted Devices").grid(row=0, column=0, padx=(10, 5), sticky="WE")
        # Outer Frame - to Contain Canvas (Frame) and Scrollbar
        outer_frame = Frame(self.root, height=310, width=300)
        outer_frame.grid(row=1, column=0, padx=5, pady=(10, 5), sticky="NSEW")
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_propagate(0)
        # Canvas to contain the device list frame
        device_frame_canvas = Canvas(outer_frame, bg="#f0f0f5", highlightbackground="black", highlightthickness=1)
        device_frame_canvas.grid(row=0, sticky="NSEW")
        device_frame_canvas.grid_rowconfigure(0, weight=1)
        device_frame_canvas.grid_columnconfigure(0, weight=1)
        # Scroll Bar
        scrollbar = Scrollbar(outer_frame, orient="vertical", command=device_frame_canvas.yview)
        device_frame_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="NSE")
        # Frame Devices are entered into
        device_frame = Frame(device_frame_canvas, width=device_frame_canvas.winfo_width())
        device_frame_canvas.create_window((0, 0), window=device_frame, anchor="nw")
        device_frame.columnconfigure(0, weight=1)
        device_frame_canvas.bind('<Configure>',
                                 lambda e: device_frame_canvas.configure(
                                     scrollregion=device_frame_canvas.bbox("all")
                                 ))
        device_frame_canvas.configure(yscrollcommand=scrollbar.set)
        # Create Frames for each Device
        row = 0  # Current frame row
        icon_list = []  # Used for icon labels, so different frames using the same images do not override each other
        device_frame_used_height = 0  # Used to adjust canvas for scrolling
        for device in self.devices:
            # Creating Widgets for Device's frame
            bg = "#adebad"  # Light Green Background
            inner_frame = Frame(device_frame, bg=bg, highlightbackground="black", highlightthickness=1)
            inner_frame.grid(row=row, column=0, sticky="WE")
            inner_frame.grid_columnconfigure(0, weight=6, uniform="a")  # Device details
            inner_frame.grid_columnconfigure(1, weight=2, uniform="a")  # Icon
            inner_frame.grid_columnconfigure(2, weight=2, uniform="a")  # Info Window button
            name_label = Label(inner_frame, text=device.get_name(), bg=bg, width=31, anchor='w')
            name_label.grid(row=0, column=0, sticky="W")
            mac_label = Label(inner_frame, text=device.get_mac(), bg=bg).grid(row=1, column=0, sticky="W")
            manufacturer_label = Label(inner_frame, text=device.get_manufacturer(), bg=bg)
            manufacturer_label.grid(row=2, column=0, sticky="W")
            # Creating Icon Label
            try:  # Try used in case of icon FileNotFoundError
                icon_path = "Icons/" + device.get_type() + ".png"
                icon_list.append(ImageTk.PhotoImage(Image.open(icon_path)))
                icon_lbl = Label(inner_frame, image=icon_list[-1], bg=bg).grid(row=0, rowspan=3, column=1, sticky="WE")
            except FileNotFoundError:
                # If icon file cannot be found, create a blank label
                icon_lbl = Label(inner_frame, bg=bg).grid(row=0, rowspan=3, column=1, sticky="WE")
            info_button = Button(inner_frame, text="Info",
                                 command=lambda device=device: self.info_button(device))
            info_button.grid(row=0, rowspan=3, column=2, sticky="NSEW")
            # Update the height of the containing devices frame
            device_frame_used_height += inner_frame.winfo_height()
            if device_frame_used_height > device_frame.winfo_height():
                device_frame.config(height=device_frame_used_height)
            row += 1
        # Return button
        return_btn = Button(self.root, text="Return", bg="#669999", pady=5, command=self.return_button)
        return_btn.grid(row=2, padx=10, pady=(5, 0), sticky="SWE")
        # Assigns the scrollable area to the canvas
        device_frame_canvas.configure(scrollregion=device_frame_canvas.bbox("all"))
        self.root.mainloop()

    # Device Information Window button
    def info_button(self, device):
        self.root.destroy()
        info_window = Device_Info_Window.DeviceInfoWindow(device, self.email, "trusted_devices_window", self.router)

    # Return button press function
    def return_button(self):
        self.root.destroy()
        scanner_window = Scanner_Window.ScannerWindow(self.email)


