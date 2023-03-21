import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title('协议编译器')

root.geometry('450x500')

root['background'] = "#C9C9C9"

# 创建左侧树

tree = ttk.Treeview(root)  # #创建树状对象
# #一级目录
treeF1 = tree.insert("", 0, "应用层", text="应用层", values=("F1"))  # #创建一级树目录
treeF2 = tree.insert("", 1, "传输层", text="传输层", values=("F2"))
treeF3 = tree.insert("", 2, "网络层", text="网络层", values=("F3"))
treeF4 = tree.insert("", 3, "网络接入层", text="网络接入层", values=("F3"))

# #二级目录
treeF1_1 = tree.insert(treeF1, 0, "HTTP", text="HTTP", values=("F1_1"))  # #将目录帮到菜单treeF1
treeF1_2 = tree.insert(treeF1, 1, "DNS", text="DNS", values=("F1_2"))
treeF2_1 = tree.insert(treeF2, 0, "TCP", text="TCP", values=("F2_1"))  # #将目录帮到菜单treeF2
treeF2_2 = tree.insert(treeF2, 1, "UDP", text="UDP", values=("F2_2"))
treeF3_1 = tree.insert(treeF3, 0, "IP", text="IP", values=("F3_1"))  # #将目录帮到菜单treeF3
treeF3_2 = tree.insert(treeF3, 1, "ICMP", text="ICMP", values=("F3_2"))
treeF3_3 = tree.insert(treeF3, 2, "ARP", text="ARP", values=("F3_3"))
treeF4_1 = tree.insert(treeF4, 0, "MAC帧", text="MAC帧", values=("F4_3"))
# 设置水平起始位置相对于窗体水平距离的0.01倍，垂直的绝对距离为80，并设置高度为窗体高度比例的0.5倍，宽度为80
tree.place(relheight=1, width=100)
frm = ttk.Frame(root, padding=300)
# frm.place(relheight=1,width=200)

# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# mainloop() 方法将所有控件显示出来，并响应用户输入直到程序终结
root.mainloop()
