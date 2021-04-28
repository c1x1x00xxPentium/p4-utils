#!/usr/bin/env python3
import argparse
import sys
import socket
import random
import struct
import time
from threading import *

from scapy.all import *

rtr = sys.argv[1]

if rtr.endswith('1'):
    list_of_ips = ["10.0.1.2", "10.2.0.2"]
elif rtr.endswith('2'):
    list_of_ips = ["10.0.1.1", "10.1.0.2"]

# Send packet on real interface
def send(pckt):
    iface = str(rtr)+"-eth0"
    pckt.show()
    sendp(pckt, iface=iface)
    print("sending on interface %s"%iface)

# Send received hello to fake interface
def send_to_fake(pckt):
    pass
    '''iface0 = str(rtr)+"-eth1"
    iface1 = str(rtr)+"-eth1"
    if pckt[IP].src == list_of_ips[0]:
        sendp(pckt, iface = iface0)
    elif pckt[IP].src == list_of_ips[1]:
        sendp(pckt, iface = iface1)'''

# Sniff OSPF packet on fake interface 1
def get_pkt_from_fake_1():
    load_contrib('ospf')
    intf = str(rtr) + "-eth1"
    sniff(iface=str(intf), prn = send)

# Sniff OSPF packet on fake interface 2
def get_pkt_from_fake_2():
    load_contrib('ospf')
    intf = str(rtr) + "-eth2"
    sniff(iface=str(intf), prn = send)

# Sniff received OSPF packets on the real interface and send to the fake interfaces
def get_pkt_from_real():
    pass
    '''load_contrib('ospf')
    intf = str(rtr) + "-eth0"
    sniff(filter = "ip src {} or ip src {}".format(list_of_ips[0],list_of_ips[1]), iface=str(intf), prn = send_to_fake)'''

def main():

    if len(sys.argv)<1:
        print('pass 1 argument: router name')
        exit(1)

    Thread(target = get_pkt_from_fake_1).start()
    Thread(target = get_pkt_from_fake_2).start()
    
    #Thread(target = get_pkt_from_real).start()
    

if __name__ == '__main__':
    main()
