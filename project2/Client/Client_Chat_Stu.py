import hashlib
import json
import os
import time
import tkinter
import tkinter.messagebox
import socket
from project2.Message import *
import _thread
import sys
from tkinter import ttk
import tkinter.filedialog


class Client_GUI():  # 客户端GUI
    def __init__(self, window):  # 初始化客户端

        # 声明GUI组件
        self.filename = None
        self.OnlineUser_text = None
        self.PrivateChat_bool = None
        self.OnlineUser_frame = None
        self.Message_text = None
        self.Register_button = None
        self.Login_button = None
        self.Server_entry = None
        self.Message_group = None
        self.Server_label = None
        self.UserPassword_entry = None
        self.UserPassword_label = None
        self.UserName_entry = None
        self.UserName_label = None
        self.window = window

        # 声明服务器IP
        self.ServerIP = None
        # 端口
        self.port = 9090
        #
        self.state = False
        #
        self.selectUser = None
        #
        self.var = tkinter.IntVar()
        # 定义一个userInfo
        self.userInfo = None

    def set_init_window(self):  # 初始化窗口控件
        # 设置本体
        self.window.title('客户端')
        self.window.geometry('612x355')
        self.window.resizable(width=False, height=False)
        self.window.tk.eval('package require Tix')
        self.window.protocol('WM_DELETE_WINDOW', self.window_closing)
        # 用户名
        self.UserName_label = tkinter.Label(self.window, text='用户名:', font=('SimHei', 12))
        self.UserName_label.grid(column=0, row=0)
        self.UserName_entry = tkinter.Entry(self.window, bd=3, width=10)
        self.UserName_entry.grid(column=1, row=0, columnspan=1)
        # 口令(请补充代码）
        self.UserPassword_label = tkinter.Label(self.window, text='口令:', font=('SimHei', 12))
        self.UserPassword_label.grid(column=2, row=0)
        self.UserPassword_entry = tkinter.Entry(self.window, bd=3, width=10)
        self.UserPassword_entry.grid(column=3, row=0, columnspan=1)
        self.UserPassword_entry.insert(tkinter.END, "123456")
        # 服务器（请补充代码）
        self.Server_label = tkinter.Label(self.window, text='服务器:', font=('SimHei', 12))
        self.Server_label.grid(column=4, row=0)
        self.Server_entry = tkinter.Entry(self.window, bd=3, width=10)
        self.Server_entry.grid(column=5, row=0, columnspan=1)
        # self.Server_entry.insert()
        # 登录按钮
        self.Login_button = tkinter.Button(self.window, text='登录', font=('SimHei', 12), command=self.login)
        self.Login_button.grid(column=6, row=0)
        # 注册按钮（请补充代码）
        self.Register_button = tkinter.Button(self.window, text='注册', font=('SimHei', 12), command=self.registered)
        self.Register_button.grid(column=7, row=0)
        # 消息记录框
        self.Message_group = tkinter.LabelFrame(window, text='消息记录', padx=5, pady=5)
        self.Message_group.grid(column=0, row=1, columnspan=5)
        self.Message_text = tkinter.Text(self.Message_group, width=50, height=20)
        self.Message_text.tag_config("private", foreground="red")
        self.Message_text.tag_config("public", foreground="black")
        self.Message_text.pack()
        # 在线用户框（请补充）
        self.OnlineUser_frame = tkinter.LabelFrame(self.window, text="用户", padx=5, pady=5)
        self.OnlineUser_frame.grid(column=5, row=1, columnspan=5)
        # 树形
        self.User_Group = ttk.Treeview(self.OnlineUser_frame, height=12, show='headings')
        self.User_Group["columns"] = ('用户名', '状态')
        self.User_Group.column('用户名', width=100, anchor="center")
        self.User_Group.column('状态', width=100, anchor="center")
        self.User_Group.heading('用户名', text='用户名')
        self.User_Group.heading('状态', text='状态')
        self.User_Group.bind('<ButtonRelease-1>', self.UserGroup_Click)  # 用于选择用户进行私聊
        self.User_Group.pack()
        # 插入数据
        # 信息输入框（请补充）
        self.InputMessage_entry = tkinter.Entry(self.window, bd=4, width=50)
        self.InputMessage_entry.grid(column=0, row=2, columnspan=5)
        # 私聊选择
        self.PrivateChat_bool = tkinter.Checkbutton(self.window, text='私聊', font=('SimHei', 12), variable=self.var)
        self.PrivateChat_bool.grid(column=5, row=2)
        # 发送信息按钮（请补充）
        self.ChatSendMessage_button = tkinter.Button(self.window, text='发送消息', font=('SimHei', 12),
                                                     command=self.SendMessage)
        self.ChatSendMessage_button.grid(column=6, row=2)
        # 发送文件按钮（请补充）
        self.ChatSendFile_button = tkinter.Button(self.window, text='发送文件', font=('SimHei', 12),
                                                  command=self.file)
        self.ChatSendFile_button.grid(column=7, row=2)
        # 数值初始化
        self.Server_entry.insert(tkinter.END, "127.0.0.1")

    def UserGroup_Click(self, event):  # 获取选择私聊用户名
        try:
            # self.selectUser = self.User_Group.selection()[0]
            # print(self.User_Group.selection())
            foc = self.User_Group.focus()
            val = self.User_Group.set(foc)
            print(val, type(val))
            self.selectUser = val["用户名"]

        except:
            return 0

    # def file(self):  # 发送文件请求
    #     filename = tkinter.filedialog.askopenfilename()  # 打开文件管理器，获取文件名
    #     (_, filename) = os.path.split(filename)  # 上面获取的是绝对路径，只截取文件名
    #     print(self.UserName_entry.get() + '\t' + filename)
    #     messages = Messages.Message(way='file_request',
    #                                 Value=self.UserName_entry.get() + '\t' + filename)  # 构造告诉服务器自己要发文件的消息
    #
    #     try:
    #         self.Client.send(messages.Information().encode('utf-8'))  # 给服务器发送要发文件的消息
    #     except:
    #         tkinter.messagebox.showinfo("提示", "你还没有登陆请重新登陆!!!")

    def file(self):  # 发送文件请求
        self.filename = tkinter.filedialog.askopenfilename()  # 打开文件管理器，获取文件名
        print("file中的:", self.filename)
        # (_, filename) = os.path.split(self.filename)  # 上面获取的是绝对路径，只截取文件名
        messages = Messages.Message(way='file_request',
                                    Value=self.UserName_entry.get() + '\t' + self.filename)  # 构造告诉服务器自己要发文件的消息

        try:
            self.Client.send(messages.Information().encode('utf-8'))  # 给服务器发送要发文件的消息
        except:
            tkinter.messagebox.showinfo("提示", "你还没有登陆请重新登陆!!!")

    def window_closing(self):  # 关闭窗口
        sys.exit(1)

    def registered(self):  # 注册用户
        self.ServerIP = self.Server_entry.get()  # 获取server ip
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化
        try:
            self.Client.connect(("127.0.0.1", self.port))  # socket连接服务器
            self.name = self.UserName_entry.get()  # 获取注册的用户名
            self.password = self.UserPassword_entry.get()  # 获取注册的密码
            if self.name.isdigit():
                tkinter.messagebox.showinfo("注册失败", "用户名不能为数字")
                return
            if self.name == "" or self.password == "":
                tkinter.messagebox.showinfo("注册失败", "用户名或密码不能为空")
                return
            way = 'registered'  # 注册信息
            message = Messages.Message(way=way, Value=self.name + '\t' + self.password).Information()  # 构造注册信息
            self.Client.send(message.encode('utf-8'))  # 发送注册信息
            response = self.Client.recv(1024).decode()
            print('Received response: {response}')
            tkinter.messagebox.showinfo("info", response)
            self.Client.close()  # 发完关闭

        except:
            tkinter.messagebox.showerror("错误", "服务器无法连接")

    def login(self):  # 请补充客户端用户登录
        self.ServerIP = self.Server_entry.get()  # 获取server ip
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化
        try:
            self.Client.connect((self.Server_entry.get(), self.port))  # socket连接服务器
            print("客户端连接服务器成功")
            self.name = self.UserName_entry.get()  # 获取登录的用户名
            self.password = self.UserPassword_entry.get()  # 获取登录的密码
            print(f'您的用户名{self.name} 密码{self.password}')
            if self.name.isdigit():
                tkinter.messagebox.showinfo("登录失败", "用户名不能为数字")
                return
            if self.name == "" or self.password == "":
                tkinter.messagebox.showinfo("登录失败", "用户名或密码不能为空")
                return
            way = 'login'  # 登录信息
            message = Messages.Message(way=way, Value=self.name + '\t' + self.password).Information()  # 构造登录信息
            self.Client.send(message.encode('utf-8'))  # 发送登录信息
            receiveText = self.Client.recv(1024).decode()
            print(receiveText)
            splitedText = receiveText.split(" ")
            if splitedText[2] == "登录成功":
                tkinter.messagebox.showinfo("成功", "登录成功！")
                self.Login_button['state'] = tkinter.DISABLED
                _thread.start_new_thread(self.AcceptMessage, (self.Client,))
            else:
                tkinter.messagebox.showerror("错误", splitedText[2])
                self.Client.close()
        except:
            tkinter.messagebox.showerror("错误", "服务器无法连接")
        #
        print("登录")

    def SendMessage(self, event=None):  # 发送消息
        try:
            if len(self.InputMessage_entry.get()) == 0:
                tkinter.messagebox.showinfo("提示", "消息为空")
                return
            if self.var.get() == 0:  # 没有选择私聊-即选择公聊
                information = 'public' + '\t' + self.InputMessage_entry.get()  # 组装information
                # print(information)
                self.Client.send(information.encode('utf-8'))  # 发送
            else:
                if self.selectUser is None:  # 没有选用户
                    tkinter.messagebox.showinfo("提示", "你还没有私聊对象!!!")
                    return 0
                else:

                    information = 'private' + '\t' + self.selectUser + '\t' + self.InputMessage_entry.get()  # 组装私聊information
                    print("你当前选择的对象为\n" + self.selectUser)
                    # print(self.InputMessage_entry.get())
                    # print(information)
                    self.Client.send(information.encode('utf-8'))  # 发送
        except:
            tkinter.messagebox.showinfo("提示", "你还没有登陆请重新登陆!!!")
        self.InputMessage_entry.delete(0, tkinter.END)  # 清空信息发布窗口

    def AcceptMessage(self, client):  # 请补充接收消息
        # print("用户消息接受")
        msg = client.recv(1024).decode('utf-8')
        print('收到的数据是: ', msg)
        # print('收到的数据类型是: ', type(msg))
        usersDic = json.loads(msg)
        # print(usersDic)
        for (key, value) in usersDic.items():
            # print('key: ', key, 'value: ', value)
            self.User_Group.insert('', 'end', iid=key, values=[key, value])

        while True:
            receiveText = client.recv(1024).decode()
            print("receiveText:\n" + receiveText)
            data = receiveText.split("\t")
            receive_type = data[0]
            receive_data = data[1]
            # admin
            # 112222
            # 接收到用户状态并改变
            if receive_type == "Online":
                self.Message_text["stat"] = "normal"
                self.Message_text.insert("end", receive_data + "用户已上线" + "\n")
                self.Message_text["stat"] = "disable"
                self.User_Group.set(receive_data, column="状态", value="在线")
            elif receive_type == "Offline":
                self.Message_text["stat"] = "normal"
                self.Message_text.insert("end", receiveText + "\n")
                self.Message_text["stat"] = "disable"
                self.User_Group.set(receive_data, column="状态", value="离线")
            # 接收到聊天信息
            if receive_type == "public":
                self.Message_text["stat"] = "normal"
                self.Message_text.insert("end", " • " + receive_data + "\n", 'green-color')
                self.Message_text["stat"] = "disable"
            elif receive_type == "private":
                self.Message_text["stat"] = "normal"
                self.Message_text.insert("end", " " + str(data[1]) + "\n", 'private')
                self.Message_text.insert("end", " • " + str(data[2]) + "\n", 'private')
                self.Message_text["stat"] = "disable"
            # 发送文件
            if receive_type == "IP_port":
                print("IP_port")
                # print(receive_data)

                # print(receiveText[1])
                # 用绝对路径作为参数创建发送线程
                print("self.name::", self.filename)
                # filename IP
                _thread.start_new_thread(self.SendFile, (self.filename, receive_data))

            # 接收到文件发送请求
            elif receive_type == "file_request":
                result = tkinter.messagebox.askokcancel(title="接收确认",
                                                        message="确认接收来自" + receive_data
                                                                + "的“" + receiveText[2] + "”文件吗?")
                self.Message_text["stat"] = "normal"
                self.Message_text.insert("end", receive_data + "发送文件" + "\n")
                self.Message_text["stat"] = "disable"
                # 接受
                if result:
                    fileName = tkinter.filedialog.asksaveasfilename()
                    _thread.start_new_thread(self.AcceptFile, (fileName,))
                    # 自己的id yes/no filename ip
                    messages = Messages.Message(way='IP_port',
                                                Value=receive_data + '\t' + "yes" + '\t' + fileName + '\t' + socket.gethostbyname(
                                                    socket.gethostname()))
                    print(messages.Information())
                    self.Client.sendall(messages.Information().encode("UTF-8"))
                else:
                    self.Message_text["stat"] = "normal"
                    self.Message_text.insert("end", receive_data + "拒绝文件发送" + "\n")
                    self.Message_text["stat"] = "disable"
                    messages = Messages.Message(way='IP_port',
                                                Value="no" + '\t')
                    print(messages.Information())
                    self.Client.sendall(messages.Information().encode("UTF-8"))

    def SendFile(self, filename, IP):  # 发送文件
        # 类型: SOCK_STREAM (使用 TCP 传输控制协议)地址簇 : AF_INET (IPv4)
        # 类型: SOCK_STREAM (使用 TCP 传输控制协议)
        print("sendFile:", filename, IP)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 Socket 地址簇 : AF_INET (IPv4)
        ip_port = (IP, 6969)

        client.connect(ip_port)
        if os.path.isfile(filename):  # 判断文件存在

            size = os.stat(filename).st_size  # 获取文件大小
            client.send(str(size).encode("utf-8"))  # 发送数据长度

            client.recv(1024)  # 接收确认
            print('发送文件')
            m = hashlib.md5()  # 计算MD5校验，确保文件接收是正确的
            f = open(filename, "rb")  # 以只读方式打开文件
            # count = 0
            # for index, line in enumerate(f):
            #     count += 1
            # read_line = 0
            for line in f:  # 文件中一行一行循环的发送
                # read_line += 1
                # processbar['value'] = (float(read_line)/float(count))*100
                client.send(line)  # 发送数据 一行一行
                m.update(line)  # 往MD5中传参数
            f.close()
            # 发送md5值校验
            md5 = m.hexdigest()  # 计算校验值
            client.send(md5.encode("utf-8"))  # 发送md5值
        client.close()

    def AcceptFile(self, filename):  # 接收文件
        # conn, addr = self.server.accept()  # 文件接收连接
        # file_size = int(conn.recv(1024).decode())  # 文件大小
        # process_window = tkinter.Tk()  # 进度条
        # # 下载进度条
        # process_window.title('文件接收')
        # process_window.geometry('200x60')
        # process_window.resizable(width=False, height=False)
        # process_window.tk.eval('package require Tix')  # 测试进度条组件是否可用
        #
        # processbar = tkinter.ttk.Progressbar(process_window, length=150)  # 定义进度条
        # processbar.pack(pady=20)  # 加入进度条
        # processbar['maximum'] = 100  # 进度条最大100
        # _thread.start_new_thread(self.download, (filename, processbar, conn, file_size))  # 开启线程开始下载
        # process_window.mainloop()

        print("AcceptFile")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 6969))
        self.server.listen(10)
        conn, addr = self.server.accept()  # 文件接收连接
        print(conn)
        file_size = int(conn.recv(1024).decode())  # 文件大小
        process_window = tkinter.Tk()  # 进度条
        # 下载进度条
        process_window.title('文件接收')
        process_window.geometry('200x60')
        process_window.resizable(width=False, height=False)
        process_window.tk.eval('package require Tix')  # 测试进度条组件是否可用

        processbar = tkinter.ttk.Progressbar(process_window, length=150)  # 定义进度条
        processbar.pack(pady=20)  # 加入进度条
        processbar['maximum'] = 100  # 进度条最大100
        processbar["value"] = 0
        speedLabel = tkinter.Label(process_window)
        speedLabel.pack()
        startTime = time.time()
        _thread.start_new_thread(self.download, (
            filename, process_window, processbar, speedLabel, conn, file_size, startTime))  # 开启线程开始下载
        process_window.mainloop()

    def download(self, filename, process_window, processbar, speedLabel, conn, file_size, startTime):  # 请补充下载文件
        print("download")
        conn.send("StartFlag".encode("UTF-8"))
        fileToWrite = open(filename, "wb")
        total = 0
        lastTotal = 0
        startTime = startTime
        lastTime = startTime
        speed = 0
        speedDisplayFlag = 1

        while True:
            data = conn.recv(1024)
            total += len(data)
            if speedDisplayFlag % 1000 == 0:
                totalGap = total - lastTotal
                lastTotal = total
            fileToWrite.write(data)
            if speedDisplayFlag % 1000 == 0:
                timeNow = time.time()
                timeGap = timeNow - lastTime
                lastTime = timeNow
                speed = float(totalGap) / float(timeGap) / 1024.0
                speedLabel["text"] = ("传输速度：" + str(speed)[0:8] + "KB/s")
            processbar["value"] = (float(total) / float(file_size)) * 100
            process_window.update()
            speedDisplayFlag += 1
            if total >= file_size:
                break
        if speedDisplayFlag < 1000:
            speedLabel["text"] = "传输速度：" + str(float(total) / 1024.0)[0:8] + "KB/s"
        tkinter.messagebox.showinfo(message="文件接收完成")

        conn.close()


window = tkinter.Tk()
# 初始化方法
client = Client_GUI(window)
#
client.set_init_window()

# 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

window.mainloop()
