import asyncio, socket
from .packet.PacketStream import PacketStream
from core.Util import asyn

		
class TcpClient(asyncio.Protocol):
	def __init__(self, name='tcpclient', ip='localhost', port=5005, packet_size=16):
		self.ip = ip
		self.name = name
		self.port = port
		self.packet_streams = []
		self.clients = []
		self.messages=[]
		self.packet_size = packet_size
		self.future = None
		self.client_tcp = None
		self.transport = None
	
	@asyn
	def wait_client(self):
		pass
	
	def send(self, msg):
		if self.client_tcp != None:
			self.client_tcp.send(msg)
		
	def get_packet_stream(self, addr=None):
		ps = PacketStream()
		ps.addr = addr
		ps.send = self.send
		self.packet_streams.append(ps)
		return ps
		
		
	async def connect(self):
		print('server listening')
		try:
			_,_ = await self.core.loop.create_connection(lambda: self, self.ip, self.port)
		except:
			print('failed to connect to server')
			#  raise
		
		print('client connected')
		if self.future != None:
			self.future.set_result(1)


	def run(self):
		asyncio.ensure_future(self.connect())
		
	def connection_made(self, transport):
		print('connection made')
		self.transport = transport
		
	def data_received(self, data):
		for i in self.packet_streams:
			if i.recv:
				i.recv(data)
		# print('tcp client data received: {}'.format(data.decode()))

	def send(self, data):
		if self.transport:
			self.transport.write(data)

	def connection_lost(self, exc):
		print('Connection lost with the server...', self.transport.get_extra_info('peername'))
		
