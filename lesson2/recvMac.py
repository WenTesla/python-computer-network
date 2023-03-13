from scapy.all import *
from scapy.layers.l2 import Ether

captNum = 0


def packet_callback(packet):
    global captNum
    captNum = captNum + 1
    print("捕获到第%d个以太帧" % captNum)
    print("目的MAC地址为: %s" % packet[Ether].dst)
    print("源MAC地址为: %s" % packet[Ether].src)
    print("协议类型为: %s" % packet[Ether].type)
    print("payload为: \n%s" % hexdump(packet[Ether].payload, dump=True))


sniff(prn=packet_callback, count=5)
