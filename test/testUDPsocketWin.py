import socket
import time

global UDP_IP
UDP_IP = "192.168.1.10"
global UDP_PORT
UDP_PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("192.168.1.1", 10000))


# SENDING TEST #

mess_to_send = '\x01\x01\x00\x00\x10\x20\x00\xc0'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))

time.sleep(1)

mess_to_send = '\x01\x01\x00\x00\x10\x20\x04\xc0'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))

time.sleep(1)

mess_to_send = '\x01\x01\x00\x00\x10\x20\x08\x40'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))

time.sleep(1)

mess_to_send = '\x01\x01\x00\x00\x10\x20\x00\x00'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))
mess_to_send = '\x01\x01\x00\x00\x10\x20\x04\x00'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))
mess_to_send = '\x01\x01\x00\x00\x10\x20\x08\x00'
s.sendto(mess_to_send,(UDP_IP, UDP_PORT))

# RECEIVING TEST #

s.settimeout(0.5)

# receive data from socket

d = s.recvfrom(64)
x = d[0].encode("hex")
print x
