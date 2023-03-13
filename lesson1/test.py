from scapy.all import *

pkt = Ether()
pkt.dst = '4C:CC:6A:A3:78:B4'
pkt.src = '4C:CC:6A:A3:77:CA'
pkt.type = 0x8000
sendp(pkt)
