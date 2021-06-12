import time
import socket
import bluetooth as bt

def btsend(v):
	s = bt.BluetoothSocket(bt.RFCOMM)
	s.connect(('30:ae:a4:6b:66:86', 1))
	s.send(v)
	s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind(('127.0.0.1', 8000))
s.listen(1)
while 1:
	a,b=s.accept()

	try:
		while 1:
			d=a.recv(1024)

			d = d.decode()
			d = d[0]
			print(d)
			if d in 'HL':
				btsend(d)

	except:
		pass
