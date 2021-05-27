# Used to assemble and send an email for Scan reports
# This example uses Gmail, therefore need to allow less secure apps to use a Gmail account
from email.mime.text import MIMEText
import os
import smtplib


class EmailHandler:
    # Constructor - take email details and run the different functions in the constructor
    def __init__(self, recipient_email, subject):
        self.recipient = recipient_email
        self.subject = subject  # This will either be "Network Scan Results" or "Traffic Sniffing Results"
        # Retrieve email credentials from IDE variables - so when uploading credentials aren't exposed
        try:
            self.email_user = os.environ['MVP_EMAIL']
            self.email_pass = os.environ['MVP_PASS']
        except KeyError:
            print("Unable to get credentials")

    """
        Functions for creating the email body differ between Network Scan and Traffic Sniffer
    """
    def generate_network_scan_body(self, found_trusted, found_supsicious):
        body = "<h2>Network Scan Results</h2>" + \
                    "<p>The following are the results of the last Network Scan</p>" + \
                    "<h3>Trusted Devices</h3>" + \
                    "<table><tr>" + \
                    "<th>Device Name</th><th>IP Address</th><th>MAC Address</th>" + \
                    "<th>Operating System</th><th>Manufacturer</th></tr>"
        # Create table for all the trusted devices
        for device in found_trusted:
            device_row = f"<tr><td>{device.get_name()}</td><td>{device.get_last_ip()}</td>" + \
                         f"<td>{device.get_mac()}</td><td>{device.get_os()}</td>" + \
                         f"<td>{device.get_manufacturer()}</td></tr>"
            body += device_row
        body += "</table>"
        # Create table for all the suspicious devices
        body += "<h3>Suspicious Devices</h3>" + \
                "<table><tr>" + \
                "<th>IP Address</th><th>MAC Address</th>" + \
                "<th>Operating System</th><th>Manufacturer</th></tr>"
        for device in found_supsicious:
            device_row = f"<tr><td>{device.get_last_ip()}</td>" + \
                         f"<td>{device.get_mac()}</td><td>{device.get_os()}</td>" + \
                         f"<td>{device.get_manufacturer()}</td></tr>"
            body += device_row
        body += "</table>"
        # ADD SUSPICIOUS DEVICES
        return body

    def generate_sniff_body(self, device, flagged_domains):
        body = "<h2>Device contacting blacklisted sites</h2>" + \
                "<p>The following device was found communicating with blacklisted domains: </p>" + \
                "<p>"
        if device.get_category() == "trusted":
                body += f"Device Name: {device.get_name()}</br>"
        body += f"Device IP: {device.get_last_ip()}</br>" + \
                f"Device MAC: {device.get_mac()}</br>" + \
                f"Operating System: {device.get_os()}</br>" + \
                f"Manufacturer: {device.get_manufacturer()}</br></p></br>"
        # Listing blacklisted domains
        body += "<h3>Contacted Domains</h3><ul>"
        for domain in flagged_domains:
            body += f"<li>{domain}</li>"
        body += "</ul>"
        return body

    # This function sends an email with one of the bodies generated above via Gmail
    def send_email(self, body):
        # Create Email Message
        msg = MIMEText(body, 'html')  # Define that the body content is HTML
        msg['Subject'] = self.subject
        msg['From'] = self.email_user
        msg['To'] = self.recipient
        # Attempt sending, will return console messages if unable to send
        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # Gmail port
            smtp.starttls()
            smtp.login(self.email_user, self.email_pass)
            send = smtp.sendmail(self.email_user, self.recipient, msg.as_string())
            smtp.quit()
        # Different Exceptions
        except smtplib.SMTPHeloError:  # The Server didn't reply properly to the Helo Greeting
            print("Server didn't respond")
        except smtplib.SMTPAuthenticationError:  # The server didn't accept the Username/Password
            print("The server didn't accept the Username/Password combination")
        except smtplib.SMTPRecipientsRefused:  # The Recipient is not a valid email address
            print("The recipient isn't valid")
