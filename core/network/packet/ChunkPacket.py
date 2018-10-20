from .PacketStream import *
from core.Util import nice_hex
import struct 

class ChunkPacket(PacketStream):
	
	def __init__(self, stream):
		self.stream = stream
		stream.recv = self.on_recv
		self.len = 0
		self.buf = bytearray()
		self.recv=None
		
	def on_recv(self, pkt):
		if self.len == 0 and len(pkt) >= 2:
			#  print('on len', pkt)
			self.len = struct.unpack('>h', pkt[:2])[0]
			pkt = pkt[2:]
			
		self.buf += pkt
		while self.buf and len(self.buf) >= self.len:
			m = min(self.len, len(self.buf))
			data = bytes(self.buf[:m])
			self.buf = self.buf[m:]
			
			if self.recv:
				self.recv(data)
				
			self.len -= m
			if self.len == 0 and self.buf:
				self.len = self.buf.pop(0)

	def send(self, pkt):
		chunk = None
		try:
			chunk = struct.pack('>h', len(pkt)) + pkt
		except:
			print('chunk fail')
			return
		
		#  print('sending chunk: ', nice_hex(chunk))
		self.stream.send(chunk)

	@staticmethod
	def chunks_from_list(lst):
		chunks=bytes()
		for i in lst:
			chunks += bytes([len(i)]) + i
		return chunks
		
	@staticmethod
	def list_from_chunks(chunks):
		chunks = bytearray(chunks)
		_len=0
		lst = []
		while(chunks):
			_len = chunks.pop(0)
			lst.append(chunks[:_len])
			chunks = chunks[_len:]
		return lst
