from core.Util import asyn
from .packet.PacketStream import PacketStream

import asyncio, socket

class TcpServer(asyncio.Protocol):
	def __init__(self, name ='tcp', port=5005, packet_size=16):
		self.port = port
		self.name = name
		self.packet_streams = []
		self.clients = []
		self.messages = []
		self.packet_size = packet_size
		self.future = None
		self.transport = None
	@asyn
	def wait_client(self):
		pass
		
	def get_packet_stream(self):
		ps = PacketStream()
		ps.send = self.send
		self.packet_streams.append(ps)
		return ps
			
	def run(self):
		print('running server')
		coro = self.core.loop.create_server(lambda: self, '0.0.0.0', self.port)
		asyncio.ensure_future(coro)
	
	def connection_made(self, transport):
		if self.future:
			self.future.set_result(1)
		peername = transport.get_extra_info('peername')
#print('Connection from {}'.format(peername))
		self.transport = transport

	def data_received(self, data):
		# message = data.decode()

		for i in self.packet_streams:
			if i.recv:
				i.recv(data)
		
	def send(self, msg):
		if self.transport:
			self.transport.write(msg)
		
	def connection_lost(self, exc):
#print('Connection lost with the server...', self.transport.get_extra_info('peername'))
		self.transport = None
