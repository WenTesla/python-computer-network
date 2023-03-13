from scapy.all import *
from datetime import datetime
from scapy.layers.inet import IP, TCP, in4_chksum, UDP
from scapy.layers.l2 import ARP, Ether


dst = input("请输入目的端口:")
capNum = 0
print("开始抓包...")

def packet_callback(packet):
    if packet[TCP].dport == int(dst):
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
        print("----------------IP协议解析结束-------------")
        print("----------------TCP协议解析开始-------------")
        print("sport: %s" % packet[TCP].sport)
        print("dport: %s" % packet[TCP].dport)
        print("seq：%s" % packet[TCP].seq)
        print("ack：%s" % packet[TCP].ack)
        print("dataofs：%s" % packet[TCP].dataofs)
        print("reserved：%s" % packet[TCP].reserved)
        print("flags：%s" % packet[TCP].flags)
        print("window：%s" % packet[TCP].window)
        print("chksum：%s" % packet[TCP].chksum)
        print("urgptr：%s" % packet[TCP].urgptr)
        print("options：%s" % packet[TCP].options)
        print("----------------TCP协议解析结束-------------")
        print("----------------MAC协议解析开始-------------")
        print("目的MAC地址  %s" % packet[Ether].dst)
        print("源MAC地址  %s" % packet[Ether].src)
        print("上层协议类型：%s" % packet[Ether].type)
        print("----------------MAC协议解析结束-------------")


print("开始抓包...")
# 可以添加过滤以捕获需要的数据包，使用标准的tcpdump / libpcap语法：
sniff(filter="tcp", prn=packet_callback, count=0)
