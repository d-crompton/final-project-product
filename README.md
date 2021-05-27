# Network Device Scanner
## Final Year Project by Danny Crompton

The purpose of this software is to allow home users to scan their home network for 
potentially malicious devices or device activity.  

The program has been written almost all in **Python**, with the exception of **HTML** being 
used to format email alerts sent to the User.

Please note that it is necessary to obtain the permission of the owner of a network
before running the program on it. This program was developed to allow remote workers and parents
to protect their home network and is not intended for malicious purposes.

To start the program, Users must run the _**Main.py**_ file.

#### Program Classes and Structure
This section is a breakdown of the different Python files and directories contained in the program.
###### Main.py
The Main.py file is used to start the program, it creates an object for and displays the 
_Legal Notice_ window.
###### File_Handler.py
The File Handler file contains the functions for reading from and writing to the 
Trusted and Suspicious Device, and Blacklisted Domain .txt files. Allowing the User to save data
between sessions.
###### Email_Handler.py
The Email Handler files contains the _EmailHandler_ class which is used to create and send emails
to the address the User enters in the _Email Input_ window. The class allows the results of the
network device scan to be sent or an alert if a blacklisted domain is encountered whilst traffic sniffing.
###### Traffic_Sniff_Class.py
The _TrafficSniffer_ class contains functions that allow the domains a target device is visiting via
HTTP to be retrieved. This is done through the combination of threading, ARP spoofing and packet sniffing.
###### WService.py
The _WService_ class is used to handle Windows Services and is used in the _Traffic Sniffer Class_
to enable IP routing so the target device does not lose internet access. The code in this file and the 
_enable_windows_iproute_ in the Traffic Sniffer class were not my own and originally can be found 
[here](https://github.com/x4nth055/pythoncode-tutorials/blob/master/scapy/arp-spoofer/services.py).  

The code is being used under their MIT License.
##### Devices Folder
The _Device_ class and its two sub-classes _Trusted_Device_ and _Suspicious_Device_
are throughout the program to create device objects. These store the device information
about each device and use getter functions to provide these details when needed.
##### Files Folder
This folder has been created to contain the currently absent _blacklist_, _suspect_ and _trusted.txt_ files that store
the User's defined blacklist, previously found suspicious devices and designated trusted devices respectively.  

The .txt files stored in this folder are created by the _File Handler_ class.
##### Icons Folder
This folder contains the .png files used to represen different devices in the Scanner, Trusted Devices and Suspicious Devices windows.

These icons are royalty free images taken from [flaticons.net](https://flaticons.net/).

##### Windows Folder
###### Legal_Notice.py
The Legal Notice window is displayed by the _Main.py_ script and is the first window 
the User wil see. It is  a remainder to only use the device when authorised to do so.
###### Email_Input.py
The Email Input window appears after the User has clicked confirm on the Legal Notice or if they
edit their email from the _Scanner Window_. This window takes an email address
from the User to which reports or alerts are sent.
###### Scanner_Window.py
The Scanner Window is the main window around which the majority of the program revolves.
On this window the User may scan their network for devices, each of which will
appear on this window. The User will decide whether each device is trusted or not and can
open each device's _Info Window_. Additionally, the User can open the _Trusted Devices_, 
_Suspicious Devices_ and _Blacklist_ windows from here.
###### Device_Info_Window.py
The Device Information window is accessible by a button associated with each device on the Scanner Window or
Trusted and Suspicious device windows. This window lists
device details such as IP address, MAC address, Operating System and Manufacturer.
The User may also remove the device from its current list and if the MAC is available,
open the _Traffic Sniffer_ window.
###### Device_Traffic_Window.py
This window is accessible via the Information window of a device from which the program
can retrieve a MAC address. This window uses the _Traffic Sniff Class_ to retrieve and display
domains the device is communicating with. Domains that are on the 
blacklist are highlighted in red and cause the User to be notified by an email.
###### Trusted_Devices_Window.py
Accessible from the Scanner Window, the Trusted Devices window reads the _trusted.txt_ file and
displays the devices stored in it.
###### Suspicious_Devices_Window.py
Similarly to the _Trusted Devices Window_, this window is accessible from the main Scanner window
and displays the devices stored in the _suspect.txt_ file.
###### Blacklist_window.py
The Blacklist window reads from the _blacklist.txt_ file and displays the list of domains the
User has added previously. The User can add new domains to the list or remove existing ones
from this window.