import struct

import scapy
from scapy.compat import raw
from scapy.layers.inet import IP, TCP, ICMP, UDP
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import send, sendp, sr1


# 处理校验和
def IP_headchecksum(IP_head):
    checksum = 0
    headlen = len(IP_head)
    if headlen % 2 == 1:
        IP_head += b"\0"
    s = 0
    while s < headlen:
        # struct.unpack(fmt, string),fmt是格式字符串,string可以理解为字节流，或字节数组，
        # 该函数用于将字节流转换成python数据类型，返回一个元组,
        temp = struct.unpack('!H', IP_head[s:s + 2])[0]
        checksum = checksum + temp
        s = s + 2
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    return ~checksum & 0xffff


# 程序开始
Protocol = int(input("请输入协议名称 1：ARP协议， 2：IP协议， 3：ICMP协议， 4：TCP协议， 5：UDP协议 \n"))
#  处理协议

# ARP 报文
if Protocol == 1:
    # ARP_op = int(input("请输入op: \n"))
    ARP_hwsrc = input("请输入源MAC地址：\n")
    # 94:08:53:3C:58:5B
    # 08:00:27:97:d1:f5
    ARP_hwdst = input("请输入目的MAC地址：\n")
    # 2c:56:dc:d3:ab:db
    ARP_psrc = input("请输入源IP地址：默认为本地ip \n")
    if ARP_psrc is None or len(ARP_psrc) == 0:
        ARP_psrc = "127.0.0.1"
        print("源IP地址为:", ARP_psrc)
    # 127.0.0.1
    # 192.168.31.1
    ARP_pdst = input("请输入目的IP地址：\n")
    # 192.168.31.247
    eth = Ether()
    eth.dst = 'ff:ff:ff:ff:ff:ff'
    arp = ARP(op='is-at', hwsrc=ARP_hwsrc, psrc=ARP_psrc, hwdst=ARP_hwdst,
              pdst=ARP_pdst)
    # 包装
    eth_arp = eth / arp
    print((eth / arp).show())
    sendp(eth / arp)
    exit()

# IP协议
if Protocol == 2:
    eth = Ether()
    IP_version = int(input("请输入version: \n"))
    IP_src = input("请输入源IP地址：\n")
    # 127.0.0.1
    IP_dst = input("请输入目的IP地址：\n")
    # 43.138.126.75
    data = input("要发送的信息：\n")
    ip = IP(version=IP_version, dst=IP_dst, src=IP_src)
    eth_ip_data = eth / ip / data
    eth_ip_data.show()
    # -todo 计算校验和
    sendp(eth_ip_data, count=1)
    exit()
# ICMP报文
if Protocol == 3:
    ICMP_dst = input("请输入目的IP地址：\n")
    ICMP_type = int(input("请输入类型：\n"))
    a = IP(dst=ICMP_dst) / ICMP(type=ICMP_type)
    """type = echo-request"""
    ans = sr1(a)
    a.show()
    exit()
#     TCP报文
if Protocol == 4:
    # 添加Ip的部分
    TCP_src_ip = input("请输入源ip,回车即默认为本地ip\n")
    if TCP_src_ip is None or len(TCP_src_ip) == 0:
        TCP_src_ip = "127.0.0.1"
    print("源ip为:", TCP_src_ip)
    TCP_dst_ip = input("请输入目的ip,回车默认为43.138.126.75\n")
    if TCP_dst_ip is None or len(TCP_dst_ip) == 0:
        TCP_dst_ip = "43.138.126.75"
    print("目的ip为:", TCP_dst_ip)
    print("正在构造ip包")
    ip = IP(dst=TCP_dst_ip, src=TCP_src_ip)
    # 添加端口号
    TCP_src_port = int(input("请输入源端口号：\n"))
    TCP_dst_port = int(input("请输入目的端口号：\n"))
    # 构造TCP部分
    tcp = TCP(dport=TCP_dst_port, sport=TCP_src_port)
    ip_tcp = ip / tcp
    # 把数据包转换成byte，这时候会自动计算校验和
    packet = IP(raw(ip_tcp))
    # 发送数量
    send_count = input("设置要发送的数据包的确切数量,默认为1 \n")
    if send_count is None or len(send_count) == 0:
        send_count = 1
    send_count = int(send_count)
    packet.show()
    send(packet, count=send_count)
    exit()

# ip_packet_payload.show()
# 把数据包转换成byte，这时候会自动计算校验和
# x = raw(ip_packet_payload)
# ipraw = IP(x)
# ipraw.show()
# checksum_scapy = ipraw[IP].chksum
# print('添加负载数据后scapy计算的校验和是：%04x(%s)' % (checksum_scapy, str(checksum_scapy)))


# 构造UDP报文
if Protocol == 5:
    print("构造UDP报文")
    # 添加Ip的部分
    UDP_src_ip = input("请输入源ip,回车即默认为本地ip\n")
    if UDP_src_ip is None or len(UDP_src_ip) == 0:
        UDP_src_ip = "127.0.0.1"
    print("源ip为:", UDP_src_ip)
    UDP_dst_ip = input("请输入目的ip,回车默认为43.138.126.75\n")
    if UDP_dst_ip is None or len(UDP_dst_ip) == 0:
        UDP_dst_ip = "43.138.126.75"
    print("目的ip为:", UDP_dst_ip)
    print("正在构造ip包")
    ip = IP(dst=UDP_dst_ip, src=UDP_src_ip)
    # 添加端口号
    UDP_src_port = int(input("请输入源端口号：\n"))
    UDP_dst_port = int(input("请输入目的端口号：\n"))
    # 构造TCP部分
    udp = UDP(dport=UDP_dst_port, sport=UDP_src_port)
    # 组装
    ip_udp = ip / udp
    packet = IP(raw(ip_udp))
    # 发送数量
    send_count = input("设置要发送的数据包的确切数量,默认为1 \n")
    if send_count is None or len(send_count) == 0:
        send_count = 1
    send_count = int(send_count)
    packet.show()
    send(packet, count=send_count)
    exit()

else:
    print("你输入的序号不对，请重新输入:")
