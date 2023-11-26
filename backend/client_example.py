import socket
import time

ADDRESS = "127.0.0.1"
UDP_PORT = 8001

addr = socket.getaddrinfo(
	ADDRESS, UDP_PORT,
	socket.AF_INET, socket.SOCK_DGRAM)[0]

with socket.socket(*addr[:3]) as s:
	s.connect(addr[4])
	
	s.send(b'hello')