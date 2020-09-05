import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton
def pp():
    print("hello")


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 400)
        self.setWindowTitle('plc')

        # 实例化QLineEdit对象，文本输入框
        self.line_edit = QLineEdit(self)


        # 实例化QLabel对象，文本显示
        self.label = QLabel(self)
        # 设置标签的位置和大小
        self.label.setGeometry(0, 90, 200, 20)
        # 连接信号和槽
        self.line_edit.textChanged.connect(self.label.setText)


        #定义按钮
        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close")         #按钮文本
        self.closeButton.setShortcut('Ctrl+D')    #给按钮绑定快捷键
        self.closeButton.clicked.connect(pp)   #给按钮绑定事件
        self.closeButton.setToolTip("Close the widget") #显示提示消息
        self.closeButton.move(100,100)                   #按钮位置

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())