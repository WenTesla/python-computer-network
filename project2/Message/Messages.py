class Message():#处理消息的格式，状态消息
    way = ''#消息类型
    value = ''#消息值

    _state = ['Online', 'Offline']#私有变量，外部无法访问
    _Operation = ['registered', 'Login']
    _Chat = ['public', 'private']
    _File = ['file_request', 'IP_port']
    # 初始化
    def __init__(self, Messages=None, way=None, Value=None):
        if Messages != None:
            self.MessageStr = Messages#中间有/\t
            self.Data_Processing()
        else:#message赋值 后面两个变量不赋值
            self.way = way
            self.value = Value
            self.MessageStr = self.way + '\t' + self.value

    def Information(self):
        self.MessageStr = self.way + '\t' + self.value
        return self.MessageStr

    def Data_Processing(self):
        FormatMessages = self.MessageStr.split('\t', 1)#way value 分成两个部分
        self.way = FormatMessages[0]
        self.value = FormatMessages[1]

    def IsStateMessage(self):
        return self.way in self._state#对比  in 是对比

    def IsOperationMessage(self):#请补充
        return

    def IsChatMessage(self):#请补充
        return

    def IsFilerequest(self):#请补充
        return

class UserStateMessage(Message):#用户状态消息

    def __init__(self, Messages=None, way=None, Value=None):
        super().__init__(Messages=Messages, way=way, Value=Value)

class ChatMessage(Message):#聊天消息

    def __init__(self, Messages=None, way=None, Value=None):
        super().__init__(Messages=Messages, way=way, Value=Value)
        self.Data_Processing()

    def Data_Processing(self):
        super(ChatMessage, self).Data_Processing()
        if self.way == 'private':
            self.value = self.value.split('\t', 1)

    def Information(self):
        if self.way == 'public':
            self.MessageStr = self.way + '\t' + self.value
            return self.MessageStr
        else:
            self.MessageStr = self.way + '\t' + self.value[0] + '\t' + self.value[1]

class OperationMessage(Message):#操作消息

    def __init__(self, Messages=None, way=None, Value=None):
        super().__init__(Messages=Messages, way=way, Value=Value)
