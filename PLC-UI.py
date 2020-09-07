import sys,_thread
import random
import socket
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton,QComboBox
import snap7
from snap7.util import *
from snap7.snap7types import *
from PyQt5.QtGui import QIcon
import time
def pp():
    print("hello")

#读取函数d
def readd():
    plc=snap7.client.Client()
    plc.connect("192.168.0.1",rack=0,slot=1)
    s=plc.read_area(0x84,1,0,20)
    
    xx=''
    for i in range(5):
        xx=xx+str(get_real(s,i*4))+"  "
    print(xx)
    ex.test.setText(xx)
    #self.test.setText(xx)

def print_time( threadName, delay):

    global tcp_server
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server.bind(("192.168.0.3", 5000))
    tcp_server.listen(20)
    global tcp_client
    global tcp_client_address

    print("wait")
    tcp_client, tcp_client_address= tcp_server.accept()
    count = 0
    while count<5:
        send_data1 = "好好的好的，好的，消息已收到好的，消息已收到消息已收到，消息已收到的，消息已收到"+str(random.randint(0,10))
        send_data=send_data1.encode(encoding = "utf-8")
        print("hello world")
        print(sys.getsizeof(send_data))
        tcp_client.send(send_data)
        time.sleep(1)
        #count += 1
        print (time.ctime(time.time()) )

# 创建两个线程


#class Example(QWidget):
class Example(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 650)
        self.setWindowTitle('plc')

        exitAction = QAction(QIcon('exit.png'), '&退出', self)       
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出软件')
        exitAction.triggered.connect(self.close)

        bxitAction = QAction(QIcon('exit.png'), '&帮助', self)       
        bxitAction.setShortcut('Ctrl+H')
        bxitAction.setStatusTip('帮助文档')
        bxitAction.triggered.connect(self.close)
 
        #self.statusBar()
        #self.statusBar.setStyleSheet("background-color:gray")
        menubar = self.menuBar()
        aMenu = menubar.addMenu('&菜单')
        aMenu.addAction(exitAction)
        aMenu.addAction(bxitAction)


        
        
        #self.test.setText('测试用')

        #PLC地址
        # 实例化QLabel对象，文本显示
        self.plcip = QLabel(self)
        # 设置文本标签的位置和大小
        self.plcip.setGeometry(0, 70, 200, 20)
        # 通过通道给文本标签赋值
        #self.line_edit.textChanged.connect(self.label.setText)
        str='PLC地址'
        self.plcip.setText(str)

        # 实例化QLineEdit对象，文本输入框,输入PLC的IP地址
        self.plc_ip = QLineEdit(self)
        self.plc_ip.setGeometry(70, 70, 120, 20)


        #DB号常量
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(20,120,200,20)
        self.dbnumber.setText('DB号')
        #DB号输入框
        self.dblen=QLineEdit(self)
        self.dblen.setGeometry(50, 120, 60, 20)

        #读取的字节数
        self.readlen=QLabel(self)
        self.readlen.setGeometry(150,120,200,20)
        self.readlen.setText("读取字节数：")
        #读取长度输入框
        self.read_len=QLineEdit(self)
        self.read_len.setGeometry(250,120,100,20)
        
        #读取数据类型，文本常量
        self.readtype=QLabel(self)
        self.readtype.setGeometry(370,120,200,20)
        self.readtype.setText('DB结构：')

        self.float_n=QLineEdit(self)
        self.float_n.setGeometry(570,120,80,20)

        #下拉框选择数据类型
         # 实例化QComBox对象
        self.t1 = QComboBox(self)
        #self.cb.move(450, 120)
        self.t1.setGeometry(450,120,100,20)

        # 单个添加条目
        self.t1.addItem('浮点数')
        self.t1.addItem('布尔量')
        self.t1.addItems(['字', 'C#', 'PHP'])

        #输入浮点数个数
        self.n1=QLineEdit(self)
        self.n1.setGeometry(570,120,80,20)


        #下拉框选择数据类型
         # 实例化QComBox对象
        self.t2 = QComboBox(self)
        #self.cb.move(450, 120)
        self.t2.setGeometry(680,120,100,20)

        # 单个添加条目
        self.t2.addItem('浮点数')
        self.t2.addItem('布尔量')
        self.t2.addItems(['字', 'C#', 'PHP'])

        #输入浮点数个数
        self.n2=QLineEdit(self)
        self.n2.setGeometry(800,120,80,20)

        



        #定义连接按钮，并绑定事件
        self.conButton = QPushButton(self)
        self.conButton.setText("连接")         #按钮文本
        self.conButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.conButton.clicked.connect(self.conn)   #给按钮绑定事件
        self.conButton.setToolTip("Close the widget") #显示提示消息
        self.conButton.move(570,70)                   #按钮位置

        #定义断开连接按钮，并绑定事件
        self.closeButton = QPushButton(self)
        self.closeButton.setText("断开")         #按钮文本
        self.closeButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.closeButton.clicked.connect(self.discon)   #给按钮绑定事件
        self.closeButton.setToolTip("Close the widget") #显示提示消息
        self.closeButton.move(650,70)                   #按钮位置



        #测试连接，常量文本
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(770,70,200,20)
        self.dbnumber.setText('连接状态：')


        #显示连接状态
        self.state = QPushButton(self)
        self.state.setText("")         #按钮文本
        self.state.move(900,70)                   #按钮位s置
        #self.state.setStyleSheet("background-color:yellow")




        #定义测试按钮，并绑定事件
        self.cButton = QPushButton(self)
        self.cButton.setText("测试")         #按钮文本
        self.cButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.cButton.clicked.connect(readd)   #给按钮绑定事件
        self.cButton.setToolTip("Close the widget") #显示提示消息
        self.cButton.move(550,10)                   #按钮位置

        ##pyqt5定时器，用于读取PLC数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        #开始读取按钮
        self.start = QPushButton(self)
        self.start.setText("开始读取")         #按钮文本
        self.start.move(80,150)                   #按钮位s置
        self.start.clicked.connect(self.startTimer)
        

        #结束读取按钮
        self.end = QPushButton(self)
        self.end.setText("停止读取")         #按钮文本
        self.end.move(180,150)                   #按钮位s置
        self.end.clicked.connect(self.endTimer)
        

        #用于展示读取到的数据
        self.test = QLabel(self)
        self.test.setGeometry(0, 300, 800, 200)
        self.test.setStyleSheet("background-color:gray")

        ##pyqt5定时器，用于创建TCP服务器，并发送数据
        self.tcptimer=QTimer()
        self.tcptimer.timeout.connect(self.tcpsend)
        #开启TCP服务器的按钮
        self.start1 = QPushButton(self)
        self.start1.setText("开启TCP服务器")         #按钮文本
        self.start1.move(0,600)                   #按钮位s置
        self.start1.clicked.connect(self.start2)
        #关闭TCP服务器的按钮
        self.end1 = QPushButton(self)
        self.end1.setText("关闭TCP服务器")         #按钮文本
        self.end1.move(180,600)                   #按钮位s置
        self.end1.clicked.connect(self.stop2)





        self.show()

    #测试函数
    def seeet(self):
        sex = self.plc_ip.text()
        self.test.setText(sex)

    #连接函数
    def conn(self):
        global plc
        plc=snap7.client.Client()
        ip=self.plc_ip.text()     #获取输入的ip地址
        try:
            plc.connect("192.168.0.1",rack=0,slot=1)
            self.state.setStyleSheet("background-color:green")
            self.conButton.setEnabled(False)   #一旦连接成功，连接按钮将被屏蔽
            self.closeButton.setEnabled(True)   #一旦连接成功，断开连接按钮将启用
        except:
            self.state.setStyleSheet("background-color:gray")
    

    ##断开连接
    def discon(self):
        global plc
        plc.disconnect()
        self.conButton.setEnabled(True)   
        self.closeButton.setEnabled(False)   
        self.state.setStyleSheet("background-color:gray")  #修改连接状态
        

    #定时读取函数，并刷新
    def showTime(self):
        
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")

        #dbn=self.dblen.text()      #获取输入的db号
        

        global plc
        try:
            s=plc.read_area(0x84,1,0,20)
            xx=''
            for i in range(5):
                xx=xx+str(get_real(s,i*4))+"  "
            self.test.setText(xx)
        except:
            self.test.setText("连接断开")
            self.state.setStyleSheet("background-color:gray")  #修改连接状态

    #开始读取计时
    def startTimer(self):
        print('lalala')

        ##开始定时读取之前，获取读取参数
        '''
        global dbn,read__len,t11,n11,t22,n22
        dbn=self.dblen.text()      #获取待读取的db号
        read__len=self.read_len.text()              #获取待读取的字节数
        t11=self.t1.text()
        n11=self.n1.text()
        t22=self.t2.text()
        n22=self.n2.text()
        '''
        self.timer.start(1000)
        self.start.setEnabled(False)
        self.end.setEnabled(True)

    #停止读取计时
    def endTimer(self):
        self.timer.stop()
        self.start.setEnabled(True)
        self.end.setEnabled(False)


    #tcp推送函数
    def tcpsend(self):
        pass
        '''
        try:
            tcp_client, tcp_client_address= tcp_server.accept()
            send_data = "好好的好的，好的，消息已收到好的，消息已收到消息已收到，消息已收到的，消息已收到".encode(encoding = "utf-8")
            tcp_client.send(send_data)
        except:
            print("nonono")
        '''
   
    
    def start2(self):
        '''
        #print("开启TCP服务器")
        global tcp_server
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server.bind(("", 8000))
        tcp_server.listen(2)
        global tcp_client, tcp_client_address

        #tcp_client, tcp_client_address= tcp_server.accept()
        # 准备要发送给服务器的数据
        #send_data = "好好的好的，好的，消息已收到好的，消息已收到消息已收到，消息已收到的，消息已收到".encode(encoding = "utf-8")
   
        # 发送数据给客户端
        #tcp_client.send(send_data)
        '''

        _thread.start_new_thread(print_time, ("Thread-1", 2, ) )
        #_thread.start_new_thread(print_time, ("Thread-2", 4, ) )

        self.tcptimer.start(1000)
        self.start1.setEnabled(False)
        self.end1.setEnabled(True)
       
    def stop2(self):
        '''
        # 关闭服务与客户端的套接字， 终止和客户端通信的服务
        #tcp_client.close()
   
        # 关闭服务端的套接字, 终止和客户端提供建立连接请求的服务 但是正常来说服务器的套接字是不需要关闭的，因为服务器需要一直运行。
        tcp_server.close()


        #print("开启TCP服务器")
        '''
        self.tcptimer.stop()
        self.start1.setEnabled(True)
        self.end1.setEnabled(False)


        
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())