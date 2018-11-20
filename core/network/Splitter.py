from .Stream import Stream
class Splitter:
	def __init__(self, ps):
		self.ps = ps
		self.ps.recv = self.on_recv
		self.streams = []
		
	def on_recv(self,pkt):
		for i in self.streams:
			if i.recv:
				i.recv(pkt)
		
	def get(self):
		s = Stream(self.ps.send)
		self.streams.append(s)
		return s
