
import socket, time

from CommandPacket import *

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("192.168.1.1",10000))


tx = s.sendto(cpuCommandPacket("getFirmwareVersion"),("192.168.1.10",10000))
print s.recvfrom(64)[0].encode("hex")


tx = s.sendto(commandPacket("doSpiOperation", 0x70000),("192.168.1.10",10000))

time.sleep(0.5)

tx = s.sendto(commandPacket("doSpiOperation", 0xF0000),("192.168.1.10",10000))

print s.recvfrom(64)[0].encode("hex")
print s.recvfrom(64)[0].encode("hex")


"""

## reset FPGA
s.sendto("\x01\x01\x00\x00\x40\x10\x00\x00",
	("192.168.1.1",10000))

print s.recvfrom(64)[0].encode("hex")


## reset CHIPIX
s.sendto("\x01\x01\x00\x00\x41\x00\x00\x00",
	("192.168.1.1",10000))

print s.recvfrom(64)[0].encode("hex")


## start ADC
s.sendto("\x01\x01\x00\x00\x4A\x07\x00\x00",
	("192.168.1.1",10000))

print s.recvfrom(64)[0].encode("hex")



## read ADC
s.sendto("\x01\x01\x00\x00\x4A\x0F\x00\x00",
	("192.168.1.1",10000))

print s.recvfrom(64)[0].encode("hex")



## get FW version
s.sendto("\x01\x02\x00\x00\x00\x00\x00\x00",("192.168.1.1",10000))

print s.recvfrom(64)[0][6:8].encode("hex")

"""