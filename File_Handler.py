# This class is intended to handle any files operations (opening, loading devices, writing to)
# Created to avoid repeating code across multiple windows, and make windows' code easier to read
from Devices import Trusted_Device, Suspicious_Device
import os


# Loading and Writing Trusted File
# Retrieves the devices stored on the trusted file, creating a trusted device object from each line
def load_trusted_file():
    trusted_devices = []  # Array to store loaded devices into, return this array
    try:
        # Attempt to open if file exists
        trust_file = open("Files\\trusted.txt", "r+")
        # If file appears, locally store devices
        trust_file.seek(0)  # Puts marker at the start of the file
        for line in trust_file:  # Loop through file's lines
            adj_line = line[:-1]  # Remove the \n from the end
            device = adj_line.split(',')  # Turn into an array
            trusted_devices.append(
                Trusted_Device.TrustedDevice(device[0], device[1], device[2], device[3], device[4], device[5])
            )  # Add to local list of trusted devices
        trust_file.close()
    except FileNotFoundError:
        # Open in write mode to create file, if not available
        trust_file = open("Files\\trusted.txt", "w+")
        trust_file.close()  # File not needed until the end of the scan loop
    return trusted_devices


def write_trust_file(trusted_devices):
    # Open trust file for writing, not using Try as being written in write+
    trust_file = open("Files\\trusted.txt", "w+")
    for device in trusted_devices:
        trust_file.write(device.get_last_ip() + "," +
                         device.get_mac() + "," +
                         device.get_manufacturer() + "," +
                         device.get_os() + "," +
                         device.get_type() + "," +
                         device.get_name() + "\n")
    trust_file.flush()  # Flush and fsync, writes lists without waiting for buffer
    os.fsync(trust_file.fileno())
    trust_file.close()


# Loading and Writing Suspicious File
def load_suspicious_file():
    suspicious_devices = []  # Array to locally store loaded devices, function returns this array
    try:
        # Attempt to open in append, if file exists
        sus_file = open("Files\\suspect.txt", "r+")
        # If file appears, locally store devices
        sus_file.seek(0)  # Puts marker at start of file
        for line in sus_file:
            adj_line = line[:-1]
            device = adj_line.split(',')
            suspicious_devices.append(
                Suspicious_Device.SuspiciousDevice(device[0], device[1], device[2], device[3], device[4])
            )  # Add to local list of suspicious devices
        sus_file.close()
    except FileNotFoundError:
        # Open in write mode to create file, if not
        sus_file = open("Files\\suspect.txt", "w+")
        sus_file.close()  # File not needed until the end of the scan loop
    return suspicious_devices


def write_suspicious_file(suspicious_devices):
    # Open suspect file for writing
    suspicious_file = open("Files\\suspect.txt", "w+")
    for device in suspicious_devices:
        suspicious_file.write(device.get_last_ip() + "," +
                              device.get_mac() + "," +
                              device.get_manufacturer() + "," +
                              device.get_os() + "," +
                              device.get_type() + "," + "\n")
    suspicious_file.flush()
    os.fsync(suspicious_file.fileno())
    suspicious_file.close()


# Loading and Writing Blacklist
def load_blacklist_file():
    blacklisted_sites = []
    try:
        blacklist_file = open("Files\\blacklist.txt", "r+")
        blacklist_file.seek(0)
        for line in blacklist_file:
            adj_line = line[:-1]  # Removes \n from the end
            blacklisted_sites.append(adj_line)
        blacklist_file.close()
    except FileNotFoundError:
        blacklist_file = open("Files\\blacklist.txt", "w+")
        blacklist_file.close()
    return blacklisted_sites


def write_blacklist_file(blacklisted_sites):
    blacklist_file = open("Files\\blacklist.txt", "w+")
    for site in blacklisted_sites:
        blacklist_file.write(site + "\n")
    blacklist_file.flush()
    os.fsync(blacklist_file.fileno())
    blacklist_file.close()
