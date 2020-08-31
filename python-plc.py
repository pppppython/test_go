import snap7,time
import struct

from snap7.util import *
from snap7.snap7types import *
plc=snap7.client.Client()
plc.connect("192.168.0.1",rack=0,slot=1)
#读数据
#while 1:




#读取浮点数
s=plc.read_area(0x84,1,0,8)    #从DB1的第0个字节开始，连续读取8个字节，一个浮点数占4个字节
#print(get_real(s,0))           #打印第一个浮点数
#print(get_real(s,4))           #打印第二个浮点数



#写入浮点数

#将float数转为四字节数组
def floatToBytes(f):
    bs = struct.pack("f",f)
    return (bs[3],bs[2],bs[1],bs[0])

b=floatToBytes(999.8)          
print(b[1])
plc.write_area(0x84,1,8,bytearray([b[0], b[1], b[2], b[3]]))    #写入浮点数




'''
#读取布尔量

t=plc.read_area(0x84,2,0,2)   #读取DB2从第0个字节开始，连续的2个字节
print(get_bool(t,0,1))      #打印第0个字节（从0开始）的第1位
#print(get_bool(t,1,0))       #打印第1个字节（从0开始）的第0位
'''




#写入布尔量
#plc.write_area(0x84,3,0,t)      #将DB2的前两个字节的值，写入DB3
'''
ss=""
for i in str(bin(245)):
    if i=="0":
        ss=ss+1
    if i="1":
'''

s1=str(bin(245))

s2=s1[2:]
print(s2)
ss=s2[::-1]
print(ss)



'''
y=bytearray([32,255,255,255])  #将这4个十进制数转化为bytearray，一个十进制数代表8个布尔量
plc.write_area(0x84,3,0,y)      #将bytearray写入DB3
'''