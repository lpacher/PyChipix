
##################################################
##   minimal test for FPGA/PC UDP connections   ##
##################################################

import socket

from CommandPacket import *

## in case, obtain the local IP address
socket.gethostbyname(socket.gethostname())

# gSOCKET

FPGA_UDP_IP = "192.168.1.10"
FPGA_UDP_PORT = 10000

#MESSAGE = "\x01\x02\x00\x00\00\x00\x00\x00"   # e.g. get firmware version
#MESSAGE = commandPacket("resetFpgaCounters")

MESSAGE = cpuCommandPacket("getFirmwareVersion")


## create IP socket
s = socket.socket(
	socket.AF_INET,         # Internet socket
	socket.SOCK_DGRAM)      # UDP socket


## we don't "connect" to an UDP server, indded we "bind" the socket to receive data on port 10000
s.bind(("192.168.1.1", 10000))



## sending data
s.sendto(MESSAGE, (FPGA_UDP_IP, FPGA_UDP_PORT))



## received data and sender address
rx = s.recvfrom(64)

rxData   = rx[0].encode("hex")
sender = rx[1]  # (IP, port)

print rxData

## check
if( rxData[0:4] != MESSAGE[0:4]) :
	print "Command error!"
else :
	print "OK"


#firmwareVersion = rxData[6:8]
fmrmwareVersion = rx[0][6:8].encode("hex")



print firmwareVersion

## close the socket when done
s.close()

