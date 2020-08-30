
import snap7

from snap7.util import *
from snap7.snap7types import *
plc=snap7.client.Client()
plc.connect("192.168.0.1",rack=0,slot=1)
s=plc.read_area(0x84,1,0,4)
print(get_real(s,0))
