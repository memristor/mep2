from .PacketStream import *
state_wait_sync = 0
state_wait_header = 1
state_wait_data = 2
sync = 0x3c
class UartPacket(PacketStream):
	
	def __init__(self, stream):
		self.stream = stream
		stream.recv = self.on_recv
		self.state = 0
		self.header = bytes()
		self.data = bytes()
		self.recv=None
		
	def on_recv(self, pkt):
		if self.state == state_wait_sync:
			drop=len(pkt)
			for i,b in enumerate(pkt):
				if b == sync:
					self.state = state_wait_header
					self.header = bytes()
					self.data = bytes()
					drop=i
					break
				else:
					print('not sync: ', b)
			pkt = pkt[drop+1:]
		
		if self.state == state_wait_header:
			need = 3-len(self.header)
			self.header += pkt[:need]
			pkt = pkt[need:]
			if len(self.header) >= 3:
				C = self.header[0]
				T = self.header[1]
				L = self.header[2]
				CH = C >> 4
				if CH != ((T + L) & 0xf):
					print('header bad')
					self.state = state_wait_sync
				else:
					self.state = state_wait_data
			
		if self.state == state_wait_data:
			C = self.header[0]
			L = self.header[2]
			need = L-len(self.data)
			self.data += pkt[:need]
			pkt = pkt[need:]
			need = L-len(self.data)
			if need == 0:
				CP = C & 0xf
				c=0
				for i in self.data:
					c += i
				if CP != (c & 0xf):
					print('data checksum is bad')
					return
				msg = bytes([self.header[1]]) + self.data
				if self.recv:
					self.recv(msg)
				self.state = state_wait_sync
				
				if pkt:
					self.on_recv(pkt)
			
	def send(self, x):
		binary = x
		ptype = binary[0]
		payload = len(binary)-1
		header_checksum = (ptype + payload) & 0xf
		payload_checksum = 0
		for i in binary[1:]:
			payload_checksum += i
		payload_checksum &= 0xf
		checksum = (header_checksum << 4) | payload_checksum
		packet = b'\x3c' + bytes([checksum, ptype, payload]) + binary[1:]
		self.stream.send(packet)
