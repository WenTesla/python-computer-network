from scapy.all import *
from datetime import datetime
from scapy.layers.inet import IP, TCP, in4_chksum, UDP, ICMP
from scapy.layers.l2 import ARP, Ether

capNum = 0
Protocol = int(input("请输入你要查找的protocol：1：ARP协议， 2：IP协议， 3：ICMP协议， 4：TCP协议， 5：UDP协议 \n"))
# MAC
# if Protocol == "mac":
#     dstMac = input("请输入目的MAC地址:")
#     capNum = 0
#     print("开始抓包...")
#
#
#     def mac_callback(packet):
#         if packet[Ether].dst == dstMac:
#             global capNum
#             capNum = capNum + 1
#             ts = "捕获到第" + str(capNum) + "个以太帧"
#             print(ts)
#             print("----------------MAC协议解析开始-------------")
#             print("目的MAC地址  %s" % packet[Ether].dst)
#             print("源MAC地址  %s" % packet[Ether].src)
#             print("上层协议类型：%s" % packet[Ether].type)
#             # print("%s" % hexdump(packet[Ether], dump=True))
#             print("----------------MAC协议解析结束-------------")
#
#
#     sniff(prn=mac_callback, count=0)

# arp
if Protocol == 1:
    # ARP_analysis(packet)
    # print('ARP发送')
    arp_ip = input("请输入目的IP地址:\n")
    capNum = 0
    print("开始抓包...")


    def ARP_callback(packet):
        if packet[ARP].pdst == arp_ip:
            print("----------------ARP协议解析开始-------------")
            print("hwtype:  %s" % packet[ARP].hwtype)
            print("ptype:  %s" % packet[ARP].ptype)
            print("hwlen  %s" % packet[ARP].hwlen)
            print("plen：%s" % packet[ARP].plen)
            print("op:  %s" % packet[ARP].op)
            print("hwsrc：%s" % packet[ARP].hwsrc)
            print("psrc：%s" % packet[ARP].psrc)
            print("hwdst：%s" % packet[ARP].hwdst)
            print("pdst：%s" % packet[ARP].pdst)
            print("----------------ARP协议解析结束-------------")


    sniff(filter="arp", prn=ARP_callback, count=0)
# IP
elif Protocol == 2:
    dstip = input("请输入目的IP地址:")
    capNum = 0
    print("开始抓包...")


    # 头部校验和的计算
    def IP_headchecksum(IP_head):
        # 把校验和字段置为0
        checksum = 0


    def packet_callback(packet):
        if (packet[IP].dst == dstip):
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


    sniff(filter="ip", prn=packet_callback, count=0)
#     ICMP报文
elif Protocol == 3:
    ICMP_dst = input("请输入目的IP地址：\n")
    print("开始抓包")
    def packet_callback(packet):
        if (packet[IP].dst == ICMP_dst):
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
            print("----------------ICMP协议解析开始-------------")
            print("ICMP类型  %s" % packet[ICMP].type)
            print("ICMP-CODE  %s" % packet[ICMP].code)
            print("ICMP校验和：%s" % packet[ICMP].chksum)
            print("ICMPid：%s" % packet[ICMP].id)
            print("ICMPseq：%s" % packet[ICMP].seq)

            print("----------------ICMP协议解析结束-------------")

    sniff(filter="icmp", prn=packet_callback, count=0)
# TCP
elif Protocol == 4:
    tcp_dport = input("请输入目的端口:")
    capNum = 0
    print("开始抓包...")


    def packet_callback(packet):
        if packet[TCP].dport == int(tcp_dport):
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


    sniff(filter="tcp", prn=packet_callback, count=0)

# UDP
elif Protocol == 5:
    dst = input("请输入目的端口:")
    capNum = 0
    print("开始抓包...")


    def packet_callback(packet):
        if packet[UDP].dport == int(dst):
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
            print("----------------UDP协议解析开始-------------")
            print("sport: %s" % packet[UDP].sport)
            print("dport: %s" % packet[UDP].dport)
            print("len：%s" % packet[UDP].len)
            print("chksum：%s" % packet[UDP].chksum)
            print("----------------UDP协议解析结束-------------")
            print("----------------MAC协议解析开始-------------")
            print("目的MAC地址  %s" % packet[Ether].dst)
            print("源MAC地址  %s" % packet[Ether].src)
            print("上层协议类型：%s" % packet[Ether].type)
            print("----------------MAC协议解析结束-------------")


    sniff(filter="udp", prn=packet_callback, count=0)




else:
    print('未知协议类型')
