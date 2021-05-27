"""
This will be the first window to appear, provides a notice advising
the User to only use this on networks they have permission to
"""
from tkinter import *
from Windows import Email_Input


class LegalNoticeWindow:
    # Constructor
    def __init__(self):
        # Creating Window
        self.root = Tk()
        self.root.title("Legal Notice - Home Network Scanner")
        self.root.resizable(0, 0)  # Disables maximum button
        self.root.geometry("350x150")
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(self.root)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="NSEW")
        title_lbl = Label(frame, text="Network Device Scanner")
        title_lbl.grid(row=0, sticky="WE")
        message_lbl = Label(frame, wraplength=300, text="Please ensure you have permission to use this program " +
                            "on the network  you are currently connected to. It is illegal to run this tool "
                            + "without permission of the network's owner.")
        message_lbl.grid(row=1, sticky="WE")
        button = Button(frame, text="Confirm", width=30, pady=5, bg="#669999", command=self.button_press)
        button.grid(row=2, sticky="WE", padx=10, pady=(10,0))
        # Main Loop to display - No code after this
        self.root.mainloop()

    # Function runs when button is pressed - Closes this window, opens the next
    def button_press(self):
        self.root.destroy()
        Email_Input.EmailInputWindow()
