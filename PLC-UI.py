import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton,QComboBox
def pp():
    print("hello")


class Example(QWidget):
    

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 600)
        self.setWindowTitle('plc')

        #文本标签测试
        self.test = QLabel(self)
        self.test.setGeometry(0, 20, 200, 20)
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
        self.plc_ip.setGeometry(70, 70, 200, 20)


        #DB号
        self.dbnumber=QLabel(self)
        self.dbnumber.setGeometry(300,70,200,20)
        self.dbnumber.setText('DB地址')
        #读取数据大小
        self.dblen=QLineEdit(self)
        self.dblen.setGeometry(350, 70, 60, 20)


        #下拉框选择数据类型
         # 实例化QComBox对象
        self.cb = QComboBox(self)
        self.cb.move(450, 70)

        # 单个添加条目
        self.cb.addItem('浮点数')
        self.cb.addItem('布尔量')
        # 多个添加条目
        self.cb.addItems(['字', 'C#', 'PHP'])




        #定义按钮，并绑定事件
        self.closeButton = QPushButton(self)
        self.closeButton.setText("读取")         #按钮文本
        self.closeButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.closeButton.clicked.connect(self.seeet)   #给按钮绑定事件
        self.closeButton.setToolTip("Close the widget") #显示提示消息
        self.closeButton.move(550,70)                   #按钮位置

        self.show()

    #测试函数
    def seeet(self):
        sex = self.plc_ip.text()
        self.test.setText(sex)

    #读取函数

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())