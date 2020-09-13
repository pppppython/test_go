
binNum = bin(11110000)
binStr = str(binNum)
binStr = binStr[2:]
        #rjust..对应应该有ljust#
reverseStr = binStr.rjust(32, '0')
reverseStr = reverseStr[::-1]

reverseNum = int(reverseStr, 2)
print(reverseNum)