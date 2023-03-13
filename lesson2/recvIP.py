from scapy.all import *
from datetime import datetime
from scapy.layers.inet import IP, TCP, in4_chksum, UDP
from scapy.layers.l2 import ARP, Ether


dstip = input("请输入目的IP地址:")
capNum = 0
print("开始抓包...")

def packet_callback(packet):
    if packet[IP].dst == dstip:
          
        print("----------------IP协议解析开始-------------")
        print("version:  %s" % packet[IP].version)
        print("ihl:  %s" % packet[IP].ihl)
        print("tos:  %s" % packet[IP].tos)
        print("len：%s" % packet[IP].len)
        print("id:  %s" % packet[IP].id)
        print("flags：%s" % packet[IP].flags)
        print("frag：%s" % packet[IP].frag)
        print("ttl：%s" % packet[IP].ttl)
        print("proto：%s" % packet[IP].proto)
        print("checksum  %s" % packet[IP].chksum)
        print("src：%s" % packet[IP].src)
        print("dst：%s" % packet[IP].dst)
        print("----------------IP协议解析结束-------------\n")
        print("----------------MAC协议解析开始-------------")
        print("目的MAC地址  %s" % packet[Ether].dst)
        print("源MAC地址  %s" % packet[Ether].src)
        print("上层协议类型：%s" % packet[Ether].type)
        print("----------------MAC协议解析结束-------------")



print("开始抓包...")


sniff(filter="ip", prn=packet_callback, count=0)
