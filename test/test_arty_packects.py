
from socket import *
import struct

import time

## create UDP socket

#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

## create RAW UDP socket
s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)  # family, type, protocol


payload = "\x01\x01\x00\x00\x10\x20\x00\xC0"

source_port = 4711
destination_port = 10000
length = 8 + len(payload)
checksum = 0


header = struct.pack('!HHHH', source_port, destination_port, length, checksum)

s.sendto(header + data, ("192.168.1.10", 10000) )


"""

count = 0

while( count < 10) :
	s.sendto( "\x01\x01\x00\x00\x10\x20\x00\xC0" , ("192.168.1.10", 10000) )
	time.sleep(0.5)
	s.sendto( "\x01\x01\x00\x00\x10\x20\x00\x00" , ("192.168.1.10", 10000) )
	time.sleep(0.5)
	count = count + 1

#s.sendto( "\x01\x01\x00\x00\x10\x20\x00\xC0" , ("192.168.1.10", 10000) )

"""

s.close()