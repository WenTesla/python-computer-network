from scapy.all import *
from scapy.layers.inet import IP, TCP, in4_chksum, UDP, ICMP
import struct

# packet = IP(dst='10.11.12.13',src='10.11.12.15')/TCP(dport= 8080, sport= 8000)
packet = IP(dst='10.11.12.13',src='localhost')/TCP(dport= 8080, sport= 8000)


scapy_packet = IP(raw(packet))
scapy_packet.show()
checksum_scapy = scapy_packet[TCP].chksum
print('添加负载数据后scapy计算的校验和是：%04x(%s)'%(checksum_scapy,str(checksum_scapy)))
# 设置为0
packet[TCP].chksum=0
# 重新构造
packet_raw =raw(packet)
#
tcp_raw=packet_raw[20:]
chksum = in4_chksum(socket.IPPROTO_TCP,packet[IP],tcp_raw)

print("验证计算IP首部校验和：%04x(%s)"%(checksum_scapy,str(checksum_scapy)))
if(checksum_scapy==chksum):
    print("正确")
else:
    print('不正确')

# loop 参数默认为0，如果它的值不是0，那么数据包将一直循环发送，直到按CTRL-C为止。
# count 可用于设置要发送的数据包的确切数量。
# inter 可用于设置每个数据包之间的秒数。
# send(scapy_packet, inter=2, loop=1)
send(scapy_packet, inter=2)