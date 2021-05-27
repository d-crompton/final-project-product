# Appears after the legal notice
# Takes a User's email, and passes it to the Main Scanner Window
from tkinter import *
import tkinter.messagebox
import re
from Windows import Scanner_Window


class EmailInputWindow:
    # Constructor
    def __init__(self):
        # Creating Window
        self.root = Tk()
        self.root.title("Please Enter Your Email - Network Device Scanner")
        self.root.geometry("300x130")
        self.root.resizable(0, 0)
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(self.root)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="NSEW")
        lbl1 = Label(frame, text="Please enter an Email").grid(row=0, sticky="WE")
        lbl2 = Label(frame, text="Scanner alerts will be sent to this address").grid(row=1, sticky="WE")
        self.input_txt = Entry(frame)
        self.input_txt.grid(row=2, padx=10, sticky="WE")
        submit_btn = Button(frame, text="Submit", width=30, pady=5, bg="#669999", command=self.submit_button)
        submit_btn.grid(row=3, pady=10)
        # Main Loop - No Code after this
        self.root.mainloop()

    # Function runs when submit button is pressed
    def submit_button(self):
        # Define regular expression - used to check whether email format is correct
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        email = self.input_txt.get().strip()  # Retrieve value from text field
        # Check if User's input is valid
        if email == "":  # Check if it's blank
            warning = tkinter.messagebox.showwarning("No Email", "Please enter an email address")
        elif email != "" and re.search(regex, email) is None:  # Check if it's not blank, but an invalid email address
            warning = tkinter.messagebox.showwarning("Invalid Email", "Please enter a valid address")
        elif email != "" and len(email) > 254:  # Check if the email is below the
            warning = tkinter.messagebox.showwarning("Invalid Email", "Email entered is too long")
        else:  # If the box isn't blank nor invalid according to regex, it passes
            # Closing current window, opening the other
            self.root.destroy()
            scanner_window = Scanner_Window.ScannerWindow(email)
