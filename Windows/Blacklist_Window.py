# Opened via a button on the Main Scanner Window
# Lists the
from tkinter import *
import tkinter.messagebox
import File_Handler


class BlacklistWindow:
    # Constructor
    def __init__(self):
        # Load blacklisted sites
        self.blacklisted_sites = []
        self.load_blacklist()
        # Creating Window
        self.root = Tk()
        self.root.title("Blacklisted Domains")
        self.root.geometry("400x420")
        self.root.resizable(0, 0)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        # Adding Widgets
        button_bg = "#669999"
        title_lbl = Label(self.root, text="Blacklisted Sites")
        title_lbl.grid(row=0, column=0, columnspan=2, pady=5, sticky="WE")
        submit_lbl = Label(self.root, text="Please enter a website you would like to blacklist below: ")
        submit_lbl.grid(row=1, column=0, sticky="W")
        self.domain_input = Entry(self.root)
        self.domain_input.grid(row=2, column=0, padx=(10, 0), sticky="WE")
        submit_btn = Button(self.root, text="Submit", command=self.submit_button)
        submit_btn.grid(row=2, column=1, padx=(0, 5), sticky="WE")
        # Outer Frame that will hold Canvas, Scrollbar and the Blacklist Frame
        outer_frame = Frame(self.root, width=350, height=280)
        outer_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="NSEW")
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_propagate(0)
        # Canvas to contain blacklist frame
        blacklist_frame_canvas = Canvas(outer_frame, bg="#f0f0f5", highlightbackground="black", highlightthickness=1)
        blacklist_frame_canvas.grid(row=0, sticky="NSEW")
        blacklist_frame_canvas.grid_rowconfigure(0, weight=1)
        blacklist_frame_canvas.grid_columnconfigure(0, weight=1)
        # Scroll Bar
        scrollbar = Scrollbar(outer_frame, orient="vertical", command=blacklist_frame_canvas.yview)
        blacklist_frame_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="NSE")
        # Frame blacklisted sites will be added in to
        self.blacklist_frame = Frame(blacklist_frame_canvas, width=blacklist_frame_canvas.winfo_width())
        blacklist_frame_canvas.create_window((0, 0), window=self.blacklist_frame, anchor="nw")
        self.blacklist_frame.columnconfigure(0, weight=1)
        blacklist_frame_canvas.bind('<Configure>',
                                    lambda e: blacklist_frame_canvas.configure(
                                        scrollregion=blacklist_frame_canvas.bbox("all")
                                    ))
        blacklist_frame_canvas.configure(yscrollcommand=scrollbar.set)
        return_btn = Button(self.root, text="Return", bg=button_bg, padx=5, pady=5, command=self.return_button)
        return_btn.grid(row=4, column=0, columnspan=2, padx=10, sticky="WE")
        self.populate_blacklist_frame()  # After widgets created, this is run to populate it.
        # Mainloop code
        self.root.mainloop()

    # Retrieve the saved blacklist from the text file - uses the File handler
    def load_blacklist(self):
        self.blacklisted_sites = []
        self.blacklisted_sites = File_Handler.load_blacklist_file()

    # Populates the blacklist frame with the sites and delete buttons
    def populate_blacklist_frame(self):
        # Clears the frame
        for child in self.blacklist_frame.winfo_children():
            child.destroy()
        # Loop through the blacklisted sites list and adds frames
        row = 0
        used_frame_height = 0
        for site in self.blacklisted_sites:
            site_frame = Frame(self.blacklist_frame)
            site_frame.grid_columnconfigure(0, weight=3)
            site_frame.grid_columnconfigure(1, weight=1)
            site_frame.grid(row=row, sticky="WE")
            site_lbl = Label(site_frame, text=site, width=40, anchor="w")
            site_lbl.grid(row=0, column=0, sticky="W")
            remove_btn = Button(site_frame, text="X", command=lambda site=site: self.remove_button(site))
            remove_btn.grid(row=0, column=1, sticky="E")
            # Update the height of the blacklist frame for the scrollbar
            used_frame_height += site_frame.winfo_height()
            if used_frame_height > self.blacklist_frame.winfo_height():
                self.blacklist_frame.config(height=used_frame_height)
            self.blacklist_frame.update_idletasks()
            # Move to next row
            row += 1

    # Button to add a new site
    def submit_button(self):
        new_site = self.domain_input.get().strip()  # Removes white space and
        self.domain_input.delete(0, 'end')  # Deletes the contents of the input box
        if new_site == "":  # Check if input is blank
            warning = tkinter.messagebox.showwarning("Empty Field", "Please enter a domain")
        else:
            # Add the new site to the list, rewrite file and then reload the frames
            self.blacklisted_sites.append(new_site)
            File_Handler.write_blacklist_file(self.blacklisted_sites)
            self.load_blacklist()
            self.populate_blacklist_frame()

    #
    def remove_button(self, removed_site):
        updated_sites = []
        # Place all sites (except the one being removed) in a temporary list
        for site in self.blacklisted_sites:
            if site != removed_site:
                updated_sites.append(site)
        # Rewrite saved file with this list
        File_Handler.write_blacklist_file(updated_sites)
        self.load_blacklist()
        self.populate_blacklist_frame()

    # Button closes the window
    def return_button(self):
        self.root.destroy()