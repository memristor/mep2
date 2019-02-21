from .PacketStream import *
class SimplePacket(PacketStream):
	
	def __init__(self, pkt_size, stream):
		self.stream = stream
		stream.recv = self.on_recv
		self.pkt_size = pkt_size
		self.buf = bytes()
		self.recv=None
		
	def on_recv(self, pkt):
		self.buf += pkt
		while len(self.buf) >= self.pkt_size:
			data = self.buf[:self.pkt_size]
			self.buf = self.buf[self.pkt_size:]
			if self.recv:
				self.recv(data)

	def send(self, pkt):
		self.stream.send(pkt)

