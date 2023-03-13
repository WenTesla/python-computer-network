from scapy.all import *
import struct
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, in4_chksum, UDP, ICMP

ip_packet = IP(dst = '10.5.25.24',src = '10.5.25.66')
payload="111111111111"
ip_packet_payload=ip_packet/payload
ip_packet_payload.show()
x = raw(ip_packet_payload)
ipraw = IP(x)
ipraw.show()
checksum_scapy=ipraw[IP].chksum
print('添加负载数据后scapy计算的校验和是：%04x(%s)'%(checksum_scapy,str(checksum_scapy)))


def IP_headchecksum(IP_head):
    checksum = 0
    headlen = len(IP_head)
    if headlen % 2 == 1:
        IP_head += b"\0"
    s = 0
    while s < headlen:
        #struct.unpack(fmt, string),fmt是格式字符串,string可以理解为字节流，或字节数组，
        # 该函数用于将字节流转换成python数据类型，返回一个元组,
        temp = struct.unpack('!H', IP_head[s:s + 2])[0]
        checksum = checksum + temp
        s = s + 2
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    return ~checksum & 0xffff


ip_packet_payload.len=20+len(payload)
ip_packet_payload.chksum=0
ip_packet_payload.ihl=5
ip_packet_payload[IP].show()
print("/n报文长度是：%s" %str(ip_packet_payload.len))
y=raw(ip_packet_payload)
ipString="".join("%02x"%orb(y)for y in y)
#bytearray.fromhex(string) 返回字节序列bytes,string必须是2个字符的16进制的形式。
ipbytes=bytearray.fromhex(ipString)
checksum_changed_self=IP_headchecksum(ipbytes[0:ip_packet_payload.ihl*4])
print("改变数据长度后IP首部的校验和是：%04x(%s)"%(checksum_changed_self,str(checksum_changed_self)))
if(checksum_scapy==checksum_changed_self):
    print("正确")
else:
    print('不正确')
ip_packet.chksum=checksum_changed_self
eth=Ether()
sendp(eth/ip_packet_payload, inter = 2, loop = 1)
