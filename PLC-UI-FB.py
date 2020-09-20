# -*- coding:utf-8 -*-
import sys,os,random,codecs,threading,socket,time,struct
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QPainter,QColor,QFont,QPen,QPolygon,QImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton,QComboBox
import snap7
from snap7.util import *
from snap7.snap7types import *
from PyQt5.QtGui import QIcon

global clo
clo=False
def pp():
    print("hello")

#将float数转为四字节数组
def floatToBytes(f):
    
    bs = struct.pack("f",f)
    return (bs[3],bs[2],bs[1],bs[0])
#写入浮点数
def writefloat(a,b,c,f):
    bb=floatToBytes(f)
    global plc        
    plc.write_area(a,b,c*4,bytearray([bb[0], bb[1], bb[2], bb[3]]))    

#写入布尔量
# a为0X84，DB为DB号，c为从第几个字节开始读，d为读多少个字节
# e待修改的那个位的索引,f为要修改成的值
def writebool(a,DB,start,len,index,value):
    global plc
    print("hhhhhhhhhhello world")
    t=plc.read_area(a,DB,start,len)   #读取DB3从第0个字节开始，连续的1个字节
    
    p=str(bin(t[0])[2:].zfill(8))
    q=p[::-1]
    qw=list(q)
    qw[index]=value
    r=''.join(qw)
    xx=int(r[::-1],2)
    y=bytearray([xx])  #将这4个十进制数转化为bytearray，一个十进制数代表8个布尔量
    plc.write_area(a,DB,start,y)      #将bytearray写入DB3，从0开始写入

#读取函数d
def readd():
    plc=snap7.client.Client()
    plc.connect("192.168.0.1",rack=0,slot=1)
    s=plc.read_area(0x84,1,0,20)
    
    xx=''
    for i in range(5):
        xx=xx+str(get_real(s,i*4))+"  "
    ex.test.setText(xx)
    


##使用TCP向go服务器发送消息，并接收前端消息
def print_time( threadName, delay):

    global tcp_server
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    #tcp_server.bind(("192.168.0.3", 5000))
    tcp_server.bind(("0.0.0.0", 5000))
    tcp_server.listen(20)
    global tcp_client
    global tcp_client_address

    print("wait")
    ex.statusBar().showMessage("开启了TCP服务器，监听本机5000端口",9000)
    global xxxx   #允许接收前端消息的标志位
    xxxx=False
    tcp_client, tcp_client_address= tcp_server.accept()  #程序会在这一步等待客户端连接，有客户端连接后，才会继续运行下去
    #_thread.start_new_thread(js, ("Thread-2", 4, ) )     #开启一个线程，用于接收go服务器发来的消息
    
    count = 0
    while count<5:
        xxxx=True
        #tcp_client, tcp_client_address= tcp_server.accept()
        send_data1 = "好好的好的，好的，消息已收到的，消息已收到"+str(random.randint(0,10))
        global gdata

        send_data=gdata.encode(encoding = "utf-8")
        #print(gdata)
        gdata=""
        #print(sys.getsizeof(send_data))
        tcp_client.send(send_data)
        time.sleep(0.2)
        global clo
        if clo:
            break

       
               

# 接收前端消息的线程
def js():
    print("开启接收线程")
    global plc
    global dbn
    global n11                      #浮点数个数
    global n22                      #布尔量个数   n222=int(int(n22)/8) 
    global tcp_client
    global xxxx
    global pz
    z22=int(n22)                   #布尔量个数转为int
    pzlong=len(pz)
    while True:
        if xxxx:
            while True:
                if clo:
                    break
                data= tcp_client.recv(1024).decode('utf-8') 
                #打印前端消息
                ex.rr.setText(data)
                print(data.split('+', 1 )) # 以+为分隔符，分隔成两个
                  
                h=pz.index(data.split('+', 1 )[0])              #阀门在配置表内的索引
                if h<=int(n11):                               #说明应该写入浮点数
                    writefloat(0x84,int(dbn),h+1,float(data.split('+', 1 )[1]))
                else:
                    #writebool(0x84,int(dbn),start,len,index,value)         #写入布尔量

                    try:
                        npt=int(n11)*4       #计算浮点数所占字节
                        k1=int((h-z22)/8)   #计算待写入的值在哪一个字节里面
                        k2=(h-z22)%8-1        #计算待写入的值在所属字节的第几位，余数从1开始，索引从0开始，所以要-1
                        print(k2)
            
                        if k2==0:
                            writebool(0x84,int(dbn),npt+k1-1,1,7,data.split('+', 1 )[1]) #db，db号，start，long，value
                        if k2>0:
                            #print("hello world")
                            writebool(0x84,int(dbn),npt+k1,1,k2-1,data.split('+', 1 )[1])
                    except:
                        pass










                #writebool(a,DB,start,len,index,value)         #写入布尔量
                #writefloat(a,b,c,f)                           #写入模拟量
                time.sleep(1)

                if clo:
                    break
            break

#class Example(QWidget):
class Example(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 700)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('plc')
        self.setWindowIcon(QIcon('./1.ico'))    #设置软件图标

        exitAction = QAction(QIcon('exit.png'), '&退出', self)       
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出软件')
        exitAction.triggered.connect(self.close)

        bxitAction = QAction(QIcon('exit.png'), '&帮助', self)       
        bxitAction.setShortcut('Ctrl+H')
        bxitAction.setStatusTip('帮助文档')  #状态栏提示
        bxitAction.triggered.connect(self.show_child)
        
        self.statusBar().showMessage('状态栏',0)
        self.statusBar().setStyleSheet("background-color:gray")

        menubar = self.menuBar()
        #menubar.setStyleSheet("background-color:gray")
        aMenu = menubar.addMenu('&菜单')
        aMenu.addAction(exitAction)
        
        bMenu = menubar.addMenu('&教程')
        bMenu.addAction(bxitAction)

        #定义测试按钮，并绑定事件
        self.cButton = QPushButton(self)
        self.cButton.setText("测试")         #按钮文本
        self.cButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.cButton.clicked.connect(readd)   #给按钮绑定事件
        self.cButton.setToolTip("Close the widget") #显示提示消息
        self.cButton.move(550,-5)                   #按钮位置
        

        #PLC地址
        # 实例化QLabel对象，文本显示
        self.plcip = QLabel(self)
        # 设置文本标签的位置和大小
        self.plcip.setGeometry(20, 40, 200, 20)
        # 通过通道给文本标签赋值
        #self.line_edit.textChanged.connect(self.label.setText)
        str='PLC地址:'
        self.plcip.setText(str)

        # 实例化QLineEdit对象，文本输入框,输入PLC的IP地址
        self.plc_ip = QLineEdit(self)
        self.plc_ip.setGeometry(90, 40, 120, 20)


        #定义连接按钮，并绑定事件
        self.conButton = QPushButton(self)
        self.conButton.setText("连接")         #按钮文本
        self.conButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.conButton.clicked.connect(self.conn)   #给按钮绑定事件
        self.conButton.setToolTip("Close the widget") #显示提示消息
        self.conButton.move(570,40)                   #按钮位置

        #定义断开连接按钮，并绑定事件
        self.closeButton = QPushButton(self)
        self.closeButton.setText("断开")         #按钮文本
        self.closeButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.closeButton.clicked.connect(self.discon)   #给按钮绑定事件
        self.closeButton.setToolTip("Close the widget") #显示提示消息
        self.closeButton.move(650,40)                   #按钮位置



        #测试连接，常量文本
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(770,40,200,20)
        self.dbnumber.setText('连接状态：')


        #显示连接状态
        self.state = QPushButton(self)
        self.state.setText("")         #按钮文本
        self.state.move(900,40)                   #按钮位s置
        #self.state.setStyleSheet("background-color:yellow")


        #配置读取参数
        self.cs=QLabel(self)
        self.cs.setGeometry(20,80,150,30)
        self.cs.setText('配置读取参数')
        self.cs.setStyleSheet("font: bold; font-size:20px; color: rgb(0,0,0);background-color:gray")

        #DB号常量
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(20,120,200,20)
        self.dbnumber.setText('DB：')
        #DB号输入框
        self.dblen=QLineEdit(self)
        self.dblen.setGeometry(50, 120, 60, 20)

        #读取间隔时间
        self.readlen=QLabel(self)
        self.readlen.setGeometry(140,120,200,20)
        self.readlen.setText("读取周期(毫秒)：")
        #读取长度输入框
        self.read_len=QLineEdit(self)
        self.read_len.setGeometry(260,120,50,20)
        
        #读取数据类型，文本常量
        self.readtype=QLabel(self)
        self.readtype.setGeometry(340,120,200,20)
        self.readtype.setText('DB结构：')

        #self.float_n=QLineEdit(self)
        #self.float_n.setGeometry(570,120,80,20)

        #下拉框选择数据类型
         # 实例化QComBox对象
        self.t1 = QComboBox(self)
        #self.cb.move(450, 120)
        self.t1.setGeometry(400,120,100,20)

        # 单个添加条目
        self.t1.addItem('浮点数个数')
        #self.t1.addItem('布尔量')
        #self.t1.addItems(['字', 'C#', 'PHP'])

        #输入浮点数个数
        self.n1=QLineEdit(self)
        self.n1.setGeometry(520,120,60,20)


        #下拉框选择数据类型
         # 实例化QComBox对象
        self.t2 = QComboBox(self)
        #self.cb.move(450, 120)
        self.t2.setGeometry(630,120,100,20)

        # 单个添加条目
        self.t2.addItem('布尔量个数')
        #self.t2.addItem('布尔量')
        #self.t2.addItems(['字', 'C#', 'PHP'])

        #输入布尔量个数
        self.n2=QLineEdit(self)
        self.n2.setGeometry(750,120,60,20)

    

        ##pyqt5定时器，用于读取PLC数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        #开始读取按钮
        self.start = QPushButton(self)
        self.start.setText("开始读取")         #按钮文本
        self.start.move(20,150)                   #按钮位s置
        self.start.clicked.connect(self.startTimer)
        

        #结束读取按钮
        self.end = QPushButton(self)
        self.end.setText("停止读取")         #按钮文本
        self.end.move(120,150)                   #按钮位s置
        self.end.clicked.connect(self.endTimer)

        #用于展示读取到的数据,浮点数
        self.test = QLabel(self)
        self.test.setGeometry(20, 200, 960, 50)
        self.test.setWordWrap(True)
        #self.test.setStyleSheet("background-color:green")
        self.test.setStyleSheet("font: bold; font-size:30px;background-color: green")

        #用于展示读取到的数据,布尔量
        self.test1 = QLabel(self)
        self.test1.setGeometry(20, 270, 960, 50)
        self.test1.setWordWrap(True)
        #self.test.setStyleSheet("background-color:green")
        self.test1.setStyleSheet("font: bold; font-size:30px;background-color: green")



        #配置写入参数
        self.cs=QLabel(self)
        self.cs.setGeometry(20,340,150,30)
        self.cs.setText('配置写入参数')
        self.cs.setStyleSheet("font: bold; font-size:20px; color: rgb(0,0,0);background-color:gray")



        self.z1 = QComboBox(self)
        #self.cb.move(450, 120)
        self.z1.setGeometry(20,390,80,20)

        #添加条目
        self.z1.addItems(['浮点数', '布尔量'])
 
        #索引
        self.p12=QLabel(self)
        self.p12.setGeometry(120,385,150,30)
        self.p12.setText('索引[1]:')

        #写入第几个浮点数/布尔量
        self.z2=QLineEdit(self)
        self.z2.setGeometry(190,390,100,20)

        #写入的值
        self.p12=QLabel(self)
        self.p12.setGeometry(320,385,150,30)
        self.p12.setText('值:')

        #值
        self.z3=QLineEdit(self)
        self.z3.setGeometry(350,390,100,20)

        #定义写入按钮
        self.w10 = QPushButton(self)
        self.w10.setText("写入·")         #按钮文本
        self.w10.clicked.connect(self.wri)   #给按钮绑定事件
        self.w10.move(550,390) 
        
        #读取配置文件的按钮
        self.w11=QPushButton(self)
        self.w11.setText("读取配置文件")
        self.w11.clicked.connect(self.dq)
        self.w11.move(680,390)


        '''
        #待写入DB号
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(20,380,150,30)
        self.dbnumber.setText('DB：')
        #DB号输入框
        self.writedb=QLineEdit(self)
        self.writedb.setGeometry(50,385,60,20)
        '''


        #主界面提示文本
        self.qqq=QLabel(self)
        self.qqq.setGeometry(20,530,500,20)
        self.qqq.setText('注意：DB块应该是浮点数在前，布尔量在后，且布尔量个数应为8的倍数')
        self.qqq.setStyleSheet("font: bold")

        self.qq=QLabel(self)
        self.qq.setGeometry(20,560,500,20)
        self.qq.setText('注意：开启TCP服务器后，可访问本机5000端口，获取实时数据')
        self.qq.setStyleSheet("font: bold")
        




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

        #接收前端消息r
        self.r=QLabel(self)
        self.r.setGeometry(380,600,200,20)
        self.r.setText('接收前端消息:')
        self.r.setStyleSheet("font: bold")

        #展示前端消息r
        self.rr=QLabel(self)
        self.rr.setGeometry(500,600,200,20)
        self.rr.setText('')
        self.rr.setStyleSheet("font: bold; font-size:20px; color: rgb(241, 70, 62);")
        
        '''
        self.qq=QLabel(self)
        self.qq.setGeometry(320,500,400,100)
        self.qq.setText('开启TCP服务器后，可访问本机5000端口，获取实时数据')
        #self.qq.setStyleSheet("font: bold; font-size:20px; color: rgb(241, 70, 62); background-color: green")
        '''


        #读取配置文件

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
            plc.connect(str(ip),rack=0,slot=1)
            self.state.setStyleSheet("background-color:green")
            self.conButton.setEnabled(False)   #一旦连接成功，连接按钮将被屏蔽
            self.closeButton.setEnabled(True)   #一旦连接成功，断开连接按钮将启用
            #self.s.setStatusTip('退出软件')
            self.statusBar().showMessage('ip：'+ip+"  "+"连接成功",9000)
        except:
            self.state.setStyleSheet("font: bold;background-color:gray")
            self.statusBar().showMessage('ip'+ip+"连接失败",9000)
    

    ##断开连接
    def discon(self):
        try:
            global plc
            plc.disconnect()
            self.conButton.setEnabled(True)   
            self.closeButton.setEnabled(False)   
            self.state.setStyleSheet("background-color:gray")  #修改连接状态
            self.statusBar().showMessage("断开连接")
        except:
            self.statusBar().showMessage("当前未连接任何PLC")
        

    #定时读取函数，并刷新
    def showTime(self):
        
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")

        #dbn=self.dblen.text()      #获取输入的db号
        global plc
        global dbn
        global n11                      #浮点数个数
        global n22                      #布尔量个数
        try:
            n222=int(int(n22)/8)            #布尔量个数/8=字节数
        except:
            self.test.setText("未设置参数")
        
        ttt=""
        try:
            #读取浮点数
            s=plc.read_area(0x84,int(dbn),0,int(n11)*4)   #int(n11)*4=字节数
            p=int(n11)
            xx=''
            for i in range(p):
                xx=xx+str(get_real(s,i*4))+"  "   #前端解析要留意
            self.test.setText(xx)
            
            
        except:
            self.test.setText("连接断开")
            self.state.setStyleSheet("background-color:gray")  #修改连接状态
        try:
            #读取布尔量
            if n222>0:
                t=plc.read_area(0x84,int(dbn),int(n11)*4,n222)  #读取DB2，从第0个字节开始，连续读 n222 个字节
                #tt=get_bool(t,0,0)            #获取读到的数据，获取第0个字节的第01位
                for i in range(n222):
                    for j in range(8):
                        tt=str(get_bool(t,i,j))
                        ttt=ttt+tt+"  "             #前端解析要留意
            global gdata
            gdata=xx+str(ttt)
            
            self.test1.setText(ttt)
            
        except:
            self.test1.setText("连接断开")
            self.state.setStyleSheet("background-color:gray")  #修改连接状态

    #开始读取计时
    def startTimer(self):
        ##开始定时读取之前，获取读取参数
        global dbn
        global n11
        global n22
        
        dbn=self.dblen.text()                       #获取待读取的db号
        read__len=self.read_len.text()              #获取读取周期
        n11=self.n1.text()                          #获取浮点数个数
        n22=self.n2.text()                          #获取布尔量个数，必须位8的倍数
        
        if not read__len:
            read__len=500

        self.timer.start(int(read__len))                       #读取间隔时间，单位毫秒
        self.start.setEnabled(False)
        self.end.setEnabled(True)
        

    #停止读取计时
    def endTimer(self):
        self.timer.stop()
        self.start.setEnabled(True)
        self.end.setEnabled(False)


    #会定时运行的函数
    def tcpsend(self):
        pass
        

   
    
    def start2(self):
        
        #_thread.start_new_thread(print_time, ("Thread-1", 2, ) )
        global t1
        global t2
        global clo
        clo=False

        #创建TCP服务器线程
        t1 = threading.Thread(target=print_time, args=("Thread-1", 2, ))
        t2 = threading.Thread(target=js, args=())
        #开启线程
        t1.start()
        t2.start()
        self.tcptimer.start(1000)
        self.start1.setEnabled(False)
        self.end1.setEnabled(True)
       
    def stop2(self):
        #退出TCP线程的标志位
        global clo
        clo=True
       
        self.tcptimer.stop()
        self.start1.setEnabled(True)
        self.end1.setEnabled(False)
        self.statusBar().showMessage("关闭了TCP服务器",9000)

    #打开子窗口的函数
    def show_child(self):
        self.child_window = Child()
        self.child_window.show()

    #写入数据
    def wri(self):
        global plc
        global dbn
        z11=self.z1.currentText()   #获取将要写入的类型
        try:
            z22=int(self.z2.text())    #获取将要写入第几个,从1开始数
        except:
            self.statusBar().showMessage("参数错误",9000)
        z33=self.z3.text()   #获取将要写入的值
        
        if z11=="浮点数":
            try:
                writefloat(0x84,int(dbn),int(z22)-1,float(z33))
            except:
                self.statusBar().showMessage("参数错误",9000)
        if z11=="布尔量":
            try:
                global n11      #获取布尔量之前有多少个浮点数
                npt=int(n11)*4       #计算浮点数所占字节
                k1=int(z22/8)   #计算待写入的值在哪一个字节里面
                k2=z22%8        #计算待写入的值在所属字节的第几位
            
                if k2==0:
                    writebool(0x84,int(dbn),npt+k1-1,1,7,z33)
                if k2>0:
                    #print("hello world")
                    writebool(0x84,int(dbn),npt+k1,1,k2-1,z33)
            except:
                self.statusBar().showMessage("参数错误",9000)
    
    #读取配置文件的函数
    def dq(self):
        with open("1.txt",encoding="utf-8") as y:
            global pz
            pz=[]
            lines = y.readlines()     
            for line in lines:
                pz.append(line.strip('\n'))    #去掉换行符
            print(pz)



        
        
#定义子窗口
class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("使用教程")
        self.resize(800, 600)
        self.setFixedSize(self.width(), self.height())
        #教程文本
        self.ber=QLabel(self)
        self.ber.setGeometry(50,0,700,500)
       
        
        
        with open("2.txt", encoding="utf-8") as f:
            self.ber.setText(f.read())
        #print(open("2.txt", encoding="gbk").read())
        

        

        
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())