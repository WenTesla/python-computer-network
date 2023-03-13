from scapy.all import *
from scapy.layers.inet import IP, TCP, in4_chksum, UDP, ICMP
import struct
from scapy.layers.dns import DNS
from scapy.layers.l2 import Ether, ARP

# 43.138.126.75

# Get the UDP checksum computed by Scapy
# packet = IP(dst='10.11.12.13',src='10.11.12.15')/UDP(dport = 8080, sport= 8000)
packet = IP(dst='192.168.43.121',src='localhost')/UDP(dport = 8080, sport= 8000)
# 自动添加校验和
packet = IP(raw(packet))
packet.show()
checksum_scapy = packet[UDP].chksum # 38108
# %x是以16进制输出。04的意思是一共4位，位数不足的，左侧用0补齐。
print('添加负载数据后scapy计算的校验和是：%04x(%s)'%(checksum_scapy,str(checksum_scapy)))

send(packet, inter = 2, loop = 1)
