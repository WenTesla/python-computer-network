import hashlib
import json
import sys
import tkinter
from tkinter import ttk
import socket
import sqlite3
import time
import threading
import _thread


from project2.Message import *
import tkinter.messagebox

global Online


class Server_GUI():  # 类，面向对象的过程
    def __init__(self, window):  # 变量初始化，self是类的变量，代表当前类
        # 连接池
        self.conn = None
        self.window = window
        self.Manage_window = tkinter.Tk()
        self.selectUser = None
        self.delete_iid = None  # 选择用户限定已成空

    def set_init_window(self):  # 加入控件窗口
        self.window.title('服务器')
        self.window.geometry('550x355')  # 定义窗口大小
        self.window.resizable(width=False, height=False)
        self.window.tk.eval('package require Tix')
        self.window.protocol('WM_DELETE_WINDOW', self.window_closing)  # 窗口关闭触发时间，调用关闭窗口运行的函数
        # 消息框
        self.message_group = tkinter.LabelFrame(self.window, text='消息记录', padx=5, pady=5)
        self.message_group.grid(column=0, row=0, columnspan=5)
        self.message_text = tkinter.Text(self.message_group, width=37, height=21, stat='disabled')
        self.message_text.pack()
        # 用户管理框
        self.User_Frame = tkinter.Frame(self.window)
        self.User_Frame.grid(column=5, row=0, padx=5, pady=5, columnspan=5)
        self.UserGroup = ttk.Treeview(self.User_Frame, height=14, show='headings')
        self.UserGroup.pack()
        self.UserGroup["columns"] = ('用户名', 'IP', '端口', '登陆时间')
        self.UserGroup.column('用户名', width=70)
        self.UserGroup.column('IP', width=60)
        self.UserGroup.column('端口', width=60)
        self.UserGroup.column('登陆时间', width=70)
        self.UserGroup.heading('用户名', text='用户名')
        self.UserGroup.heading('IP', text='IP')
        self.UserGroup.heading('端口', text='端口')
        self.UserGroup.heading('登陆时间', text='登陆时间')
        self.UserGroup.bind('<ButtonRelease-1>', self.UserGroup_Click)
        # 鼠标右键菜单
        self.menubar = tkinter.Menu(self.window)
        self.menubar.add_command(label='强制下线', command=self.User_Offline)
        self.UserGroup.bind("<Button-3>", self.showmenu)
        # 启动按钮
        self.StartButton = tkinter.Button(self.window, text='启动', font=('SimHei', 12),
                                          command=self.start)
        self.StartButton.grid(column=3, row=1)
        # 管理用户按钮
        self.ManageButton = tkinter.Button(self.window, text='管理用户', font=('SimHei', 12),
                                           command=self.Manage)
        self.ManageButton.grid(column=6, row=1)
        # 管理用户窗口控件
        self.Manage_window.title('用户管理')
        self.Manage_window.geometry('550x355')
        self.Manage_window.resizable(width=False, height=False)
        self.Manage_window.tk.eval('package require Tix')
        self.Manage_window.protocol('WM_DELETE_WINDOW', self.window_closing)
        self.Manage_window.withdraw()
        self.UserManage_Frame = tkinter.Frame(self.Manage_window)
        self.UserManage_Frame.grid(column=0, row=0, padx=5, pady=5, columnspan=10)
        self.UserManage = ttk.Treeview(self.UserManage_Frame, height=14, show='headings')
        self.UserManage["columns"] = ('用户名', '哈希值', '注册时间')
        self.UserManage.column('用户名', width=140)
        self.UserManage.column('哈希值', width=200)
        self.UserManage.column('注册时间', width=195)
        self.UserManage.heading('用户名', text='用户名')
        self.UserManage.heading('哈希值', text='哈希值')
        self.UserManage.heading('注册时间', text='注册时间')
        self.UserManage.bind('<ButtonRelease-1>', self.UserManage_Click)
        self.UserManage.pack()
        # 管理用户按钮
        self.BackButton = tkinter.Button(self.Manage_window, text='返回', font=('SimHei', 12),
                                         command=self.Manage_window_back)
        self.BackButton.grid(column=3, row=1)
        self.deleteButton = tkinter.Button(self.Manage_window, text='删除', font=('SimHei', 12),
                                           command=self.deleteUser)
        self.deleteButton.grid(column=6, row=1)
        self.ManageButton.config(state='disabled')

    def User_Offline(self):  # 强制踢下线

        Online[self.delete_iid][0].close()  # online是字典

    def UserGroup_Click(self, e):  # 点击获取右边在线用户的名称
        try:
            self.delete_iid = self.UserGroup.selection()[0]
        except:
            return 0

    def showmenu(self, e):  # 右键显示踢人菜单
        self.menubar.post(e.x_root, e.y_root)

    def UserManage_Click(self, event):  # 点击管理用户里面用户处，获取选择用户
        try:
            self.selectUser = self.UserManage.selection()[0]
        except:
            return 0

    def deleteUser(self):  # 删除选择用户用户
        if self.selectUser == None:
            tkinter.messagebox.showinfo("提示", "你还没有选择删除对象!!!")  # 弹窗
            return 0
        else:
            self.UserManage.delete(self.selectUser)  # 在界面删除
            self.cur.execute('delete from User where id = (?)', (self.selectUser,))  # 在数据库删除

    def window_closing(self):  # 窗口关闭
        try:
            self.conn.commit()  # 保存数据库
            self.conn.close()  # 断开数据库连接
            self.Server.close()  # 关闭服务器
            sys.exit(1)  # 程序退出
        except:
            sys.exit(1)

    def Manage_window_back(self):  # 返回按钮
        self.Manage_window.withdraw()  # 隐藏当前窗口
        self.window.deiconify()  # 打开服务器出事窗口

    def Manage(self):  # 点管理用户的触发
        self.window.withdraw()  # 隐藏之前窗口
        self.Manage_window.deiconify()  # 显示管理窗口
        x = self.UserManage.get_children()  # 捕获框里所有内容
        for item in x:
            self.UserManage.delete(item)  # 清理之前框里的数据信息

        self.cur.execute('select * from User')
        User_all = self.cur.fetchall()  # 读取所有用户信息

        for u in User_all:
            self.UserManage.insert("", 'end', iid=u[0], values=(u[1], hash(u[2]), u[3]))  # 往管理用户的框里插入信息

    def start(self):  # 服务器启动程序
        # 日志插入
        self.message_text.config(state='normal')  # 消息记录框先变成normal状态
        self.message_text.insert(tkinter.END, gettime() + ' 服务器启动中\n')  ##消息记录框里插入数据
        self.message_text.config(state='normal')  # 消息记录框先变成normal状态
        self.message_text.insert(tkinter.END, gettime() + ' 服务器启动成功\n')  # 消息记录框里插入数据
        self.message_text.config(state='disabled')  # 消息记录框变成disabled状态
        # 服务器监听端口9090
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化
        self.Host = socket.gethostname()  # 得到当前的服务器名称
        self.Port = 9090
        # address=('',self.Port)
        self.Server.bind(('', self.Port))  # 绑定服务器和端口
        self.Server.listen(10)  # 最大阻塞10个
        print("本地服务器开启:", self.Host, self.Port)
        self.conn = sqlite3.connect('data.db',
                                    check_same_thread=False)  # 连接数据库sqllite是python自带的，前面import data.db 数据库的文件名称，che检查线程
        self.cur = self.conn.cursor()  # 数据库游标
        # self.cur.execute('''Delete TABLE User''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS User(                        id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                                    name TEXT NOT NULL UNIQUE,
                                                                                    password TEXT NOT NULL ,
                                                                                    createTime TIMESTAMP Default (datetime('now', 'localtime')),
                                                                                    lastOnlineTime TIMESTAMP )''')  # 初始化数据库，用户信息表，公聊私聊信息文件都未穿
        self.startThread = self.AcceptConnect(self.message_text, self.UserGroup, self.cur, self.Server,
                                              self.conn)  # 创建接收连接的线程
        self.message_text.config(state='normal')
        self.message_text.insert(tkinter.END, gettime() + ' 数据库连接成功\n')
        self.message_text.config(state='disabled')
        self.startThread.setDaemon = True  # 线程锁,防止变量赋值互相冲突 因为会有多个线程
        self.startThread.start()  # 启动线程
        self.StartButton.config(state='disabled')  # 启动按钮失效
        self.ManageButton.config(state='normal')  # 管理按钮可用

    # 创建接收用户请求的线程类
    class AcceptConnect(threading.Thread):  # 创建接收用户请求的线程，继承线程类
        def __init__(self, text, User, cur, Server, conn):  # 初始化
            threading.Thread.__init__(self)
            self.threadID = 0
            self.name = 'Create_Thread'
            self.Text = text
            self.User = User
            self.Server = Server
            self.cur = cur
            self.conn = conn
            global Online  # 一个用户与相应连接的字典
            Online = {}

        def Message_Processing(self, Message):  # 消息处理
            if Message.IsStateMessage():  # 如果是状态消息，发给在线用户中的所有人
                for i in Online.values():
                    i[0].send(Message.Information().encode('utf-8'))
            elif Message.IsChatMessage():  # 如果是聊天消息
                if Message.way == 'public':  # 如果是公聊，发给所有人
                    for i in Online.values():
                        i[0].send(Message.Information().encode('utf-8'))
                else:
                    print("value:",Message.value)
                    value = Message.value.split('\t', 1)
                    print("value",value)
                    #
                    print("Message:",Message.Information())
                    Online[value[0]][0].send(Message.Information().encode('utf-8'))  # 发给指定对象
            elif Message.IsFilerequest:  # 如果文件请求
                value = Message.value.split('\t', 1)
                if Message.way == 'file_request':  # 给所有人发文件
                    for i in Online.keys():
                        if i != value[0]:
                            Online[i][0].send(Message.Information().encode('utf-8'))
                else:  # 处理对方是接收还是拒绝的消息
                    value = Message.value.split('\t', 1)
                    Online[value[0]][0].send(Message.Information().encode('utf-8'))

        def run(self):  # 执行接收用户请求线程
            while True:
                try:
                    c, addr = self.Server.accept()  # c接收到连接对象，addr是客户端的地址 端口号信息
                except:
                    break
                message = Messages.Message(c.recv(1024).decode())  # 收到消息后解码
                way = message.way  # 消息类型
                value = message.value.split('\t', 1)  # 分割
                # 获取用户名密码
                username = value[0]
                password = value[1]
                if way == 'registered':  # 如果消息类型是注册
                    Time = gettime()  # 获取
                    # 长度判断
                    if len(username) < 3 or len(password) < 5:
                        print("长度错误")
                        # 返回给客户端
                        c.sendall((gettime() + " 账号密码长度不正确").encode("UTF-8"))
                        continue

                    # 加密密码
                    encry_password = EncryPassword(password)
                    # 插入数据
                    try:
                        self.cur.execute("INSERT INTO User(name,password) values(?,?)",
                                         (username, encry_password))  # 数据库装了吗，自带的
                        self.conn.commit()
                    except:
                        print("插入失败")
                        c.sendall("用户名重复".encode("UTF-8"))
                        c.close()
                        continue
                    c.sendall((gettime() + " 注册成功").encode("UTF-8"))
                    self.Text.config(state='normal')
                    self.Text.insert(tkinter.END, gettime() + ' ' + value[0] + ' 用户注册\n')  # 往框里写东西
                    self.Text.config(state='disabled')

                    c.close()  # 断掉连接对象
                elif way == 'login':
                    # 请同学们补充用户登录及用户状态等相关代码
                    # 登录过程中需考虑空密码和错误密码验证
                    # 用户状态中需考虑用户的注册登录信息发送给所有服务器管理的用户，消息记录框中把所有注册登录信息展示出来，右边框中展示
                    # 在线用户名IP端口登录时间等信息，
                    # 其它功能请同学们自行考虑

                    # 加密密码
                    encry_password = EncryPassword(password)
                    self.cur.execute("select * from User where name = ? and password = ?",
                                     (username, encry_password))
                    result = self.cur.fetchall()
                    if len(result) == 0:
                        print("无数据", result)
                        c.sendall((gettime() + " 账号或密码错误").encode("UTF-8"))
                        self.Text.config(state='normal')
                        self.Text.insert(tkinter.END, gettime() + ' ' + username + ' 用户登陆失败\n')
                        self.Text.config(state='disabled')
                        continue
                    else:
                        print("数据为", result)
                        c.sendall((gettime() + " 登录成功").encode("UTF-8"))
                        # GUI插入
                        self.Text.config(state='normal')
                        self.Text.insert(tkinter.END, gettime() + ' ' + username + ' 用户登陆成功\n')
                        self.Text.config(state='disabled')
                        #
                        # self.Message_Processing(Messages.Message(way='Online', Value=username))
                    # 判断状态

                    try:
                        _thread.start_new_thread(self.AcceptMessage,
                                                 (username, c))  # 为登录用户专门创建的线程，处理这个用户发来的消息，公聊私聊、每个用户独有的。
                    except:
                        self.Text.config(state='normal')
                        self.Text.insert(tkinter.END, gettime() + ' ' + value[0] + ' 用户无法登陆\n')
                        self.Text.config(state='disabled')
                else:
                    c.close()

        def AcceptMessage(self, name, connection):  # 处理每个用户登录之后消息发送，接收，公聊，私聊，发文件请求的消息,每一个用户独享

            Online.update({name: (connection,)})
            # 向客户端发送所有已注册用户名单
            # 查表
            self.cur.execute("select name from User")
            # 提交
            self.conn.commit()
            # 获取结果
            result = self.cur.fetchall()
            # 创建字典
            usersDic = {}
            # 分析在线用户数据
            for i in result:
                if i[0] in Online:
                    usersDic[i[0]] = "在线"
                else:
                    usersDic[i[0]] = "离线"
            print(usersDic)
            json_data = json.dumps(usersDic)
            connection.send(json_data.encode('utf-8'))
            time.sleep(1)
            # 发送上线消息
            self.Message_Processing(Messages.Message(way="Online", Value=name))
            while True:
                try:
                    message = Messages.Message(connection.recv(1024).decode())  # 接收消息

                # 用户退出操作
                except ConnectionResetError:  # 如果出现这个异常就会执行下面的操作，用户断开的。
                    # 用户退出
                    del Online[name]
                    connection.close()
                    self.Message_Processing(Messages.Message(way='Offline', Value=name))
                    self.Message_Processing(
                        Messages.Message(way='public', Value=gettime() + ' ' + name + ' 用户退出\n'))
                    self.User.delete(name)
                    self.Text.config(state='normal')
                    self.Text.insert(tkinter.END, gettime() + ' ' + name + ' 用户退出\n')
                    self.Text.config(state='disabled')
                    break
                except ConnectionAbortedError:  # 踢人的时候 报错
                    del Online[name]
                    self.Message_Processing(Messages.Message(way='Offline', Value=name))
                    self.Message_Processing(
                        Messages.Message(way='public', Value=gettime() + ' ' + name + ' 用户退出\n'))
                    self.User.delete(name)
                    self.Text.config(state='normal')
                    self.Text.insert(tkinter.END, gettime() + ' ' + name + ' 用户退出\n')
                    self.Text.config(state='disabled')
                    break
                way = message.way
                value = message.value
                # 以下请补充对公聊、私聊、发送文件请求的的处理
                if way == 'public':  # 公聊信息处理
                    print("处理公聊天")
                    self.Message_Processing(Messages.Message(way=way, Value=value))

                elif way == 'private':  # 私聊信息处理，需要考虑给私聊发送者和接受者双方发消息
                    print("处理私聊信息")
                    self.Message_Processing(Messages.Message(way=way, Value=value))

                elif message.IsFilerequest:  # 文件一对多发
                    print("文件处理")
                    self.Message_Processing(Messages.Message(way=way, Value=value))

            #####


def gettime():  # 返回以可读字符串表示的当地时间
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def EncryPassword(password):  # 加密密码
    SALE = password[:4]  # 设置盐值
    print(str(password).join(SALE))
    md_sale = hashlib.md5((str(password).join(SALE)).encode())  # MD5加盐加密方法二：将password整体插入SALE的每个元素之间
    md5salepwd = md_sale.hexdigest()
    print(md5salepwd)
    return md5salepwd


window = tkinter.Tk()
Server = Server_GUI(window)
Server.set_init_window()
window.mainloop()
