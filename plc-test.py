import snap7,time
import struct

from snap7.util import *
from snap7.snap7types import *
plc=snap7.client.Client()
plc.connect("192.168.0.1",rack=0,slot=1)


#读取浮点数
#参数分别为0x84,DB号，从第几个浮点数开始读，读多少个浮点数，e为第e个浮点数（从0开始算）

def readfloat(a,b,c,d,e):
    r=plc.read_area(a,b,c*4,d*4)
    print(get_real(r,e*4))
readfloat(0x84,1,0,10,9)


#写入浮点数
#将float数转为四字节数组
def floatToBytes(f):
    bs = struct.pack("f",f)
    return (bs[3],bs[2],bs[1],bs[0])
#a为0x84，b为DB号，c为第几个float数(从0开始算），f为待写入的数
def writefloat(a,b,c,f):
    bb=floatToBytes(f)          
    plc.write_area(a,b,c*4,bytearray([bb[0], bb[1], bb[2], bb[3]]))    #写入浮点数
writefloat(0x84,1,8,90999)


#读取布尔量，一次最少读8个布尔量，等于1个字节
# a为0X84，b为DB号，c为从第几个字节开始读，d为读多少个字节
# e为获取第几个字节，f为获取第几个位
def readbool(a,b,c,d,e,f):
    t=plc.read_area(0x84,2,0,2)
    return get_bool(t,e,f)

print(readbool(0x84,2,0,1,0,6))



#写入布尔量
# a为0X84，DB为DB号，c为从第几个字节开始读，d为读多少个字节
# e待修改的那个位的索引,f为要修改成的值
def writebool(a,DB,start,len,index,value):
    t=plc.read_area(a,DB,start,len)   #读取DB3从第0个字节开始，连续的1个字节
    p=str(bin(t[0])[2:].zfill(8))
    q=p[::-1]
    qw=list(q)
    qw[index]=value
    r=''.join(qw)
    xx=int(r[::-1],2)
    y=bytearray([xx])  #将这4个十进制数转化为bytearray，一个十进制数代表8个布尔量
    plc.write_area(a,DB,start,y)      #将bytearray写入DB3，从0开始写入
writebool(0x84,2,0,1,4,"1")          #