from scapy.all import *   #程序中用到了scapy中的函数，所以要加这条语句，表示从scapy包中导入我们需要的函数
from scapy.layers.l2 import Ether

srcMac = input("请输入源MAC地址：\n")  #接收用户的键盘输入
dstMac = input("请输入目的MAC地址：\n")
typeMac = input("请输入协议类型：\n")  #这里接收的是字符串类型，所以在使用时要用int（）函数转换为整型
a = Ether(dst=dstMac, src=srcMac, type = int(typeMac))  #按照用户的输入来构造MAC帧
a.show()  # 按照层次显示报文内容

# 指定MAC帧的负载数据和发送的网络接口卡名称，并通过sendp函数，循环发送二层数据包
#用“/”构造多层数据报文,"56781234"为负载数据，iface为指定要发送数据包的网络接口卡的名称
for i in range(10):
    sendp(a / "56781234", iface="Realtek 8822CE Wireless LAN 802.11ac PCI-E NIC")

