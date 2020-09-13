import sys,math
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout
from PyQt5.QtGui import QPainter,QColor,QFont,QPen,QPolygon,QImage
from PyQt5.QtCore import Qt,QRect,QPoint
class DrawDemo(QMainWindow):
    def __init__(self):
        super(DrawDemo, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('demo')
        self.setGeometry(300,300,300,200)
        widget=QWidget()
        self.setCentralWidget(widget)
        layout=QVBoxLayout()
        widget.setLayout(layout)
        self.text='helloword'
        self.size=self.size()
        self.show()
 
 
    def paintEvent(self,event):  #paintEvent 当窗口变化是直接调用，不需要调用函数
        painter=QPainter()
 
        painter.begin(self)
        #设置画笔和字体
        painter.setPen(QColor(2,1,3))
        painter.setFont(QFont('SimSun',12))
 
        '''绘制圆弧'''
        #(1)确定绘制区域
        rect=QRect(0,0,100,100) #前两个值为左上角的坐标，后两个值为宽度和高度
        #(2)在区域绘制图形
        painter.drawArc(rect,0,50*16)  #后面两个参数为为起始的角度，和结束的角度，为什么乘16，因为单位为alen，一度=16alen，也就是50度为50*16
 
        '''绘制圆'''
        rect=QRect(100,0,50,50)
        painter.setPen(Qt.red)
        painter.drawArc(rect,0,360*16)
 
        '''绘制带弦的弧'''
        rect = QRect(200, 0, 50, 50)
        painter.drawChord(rect,1,90*16)
 
        '''绘制扇形'''
        rect = QRect(0,50, 50, 50)
        painter.drawPie(rect,12,76*16)
 
        '''绘制椭圆'''
        painter.drawEllipse(0,100,60,50)   #前两个参数为起始坐标，后两个为宽和高，当后两个参数一样为圆
 
        '''绘制多边形'''
        #绘制一个正方形
        p1=QPoint(100,100)
        p2=QPoint(130,100)
        p3=QPoint(130,130)
        p4=QPoint(100,130)
        polygon=QPolygon([p1,p2,p3,p4])
        painter.drawPolygon(polygon)
 
        '''绘制一个图形'''
        #（1）读取图像
        img=QImage('python.png')
        #（2）进行绘制,对图片的大小压说为原来的二分之一
        rect=QRect(100,100,img.width()/3,img.height()/3)
        painter.drawImage(rect,img)
 
 
 
        painter.end()
 
 
 
 
 
if __name__=='__main__':
    app=QApplication(sys.argv)
    demo=DrawDemo()
    sys.exit(app.exec_())