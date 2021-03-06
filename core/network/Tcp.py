from core.network.packet.PacketStream import PacketStream
import asyncio

class Tcp(asyncio.Protocol):
	def __init__(self, name ='tcp', ip='0.0.0.0', port=5005, mode='client'):
		if ip == '0.0.0.0': mode='server'
		self.mode = mode
		self.ip = ip
		self.port = port
		self.name = name
		self.packet_streams = []
		self.clients = []
		self.messages = []
		self.future = None
		self.transport = None
		_core.on('kill', self.close)

	@_core.module_cmd
	def wait_client(self): pass
	
	def error_received(self, err): 
		print('error:',err)
	
	@staticmethod
	def get_free_port(start, count):
		import socket
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		for port in range(start,start+count):
			try:
				sock.bind(('', port))
				sock.close()
				return port
			except OSError:
				pass
		return False
	
	def get_packet_stream(self):
		ps=PacketStream(self.send)
		self.packet_streams.append(ps)
		return ps
			
	def run(self):
		
		if self.mode == 'client':
			async def connect():
				try:
					_,_ = await _core.loop.create_connection(lambda: self, self.ip, self.port)
				except:
					_core.loop.call_later(0.5, self.run)
					if _core.debug >= 0.05:
						print(self.name+':', 'failed to connect to server')
					return
				print('client connected')
				if self.future: self.future.set_result(1)
			future = connect()
		else:
			# print('running server')
			future = _core.loop.create_server(lambda: self, self.ip, self.port)
		asyncio.ensure_future( future )
			
	def connection_made(self, transport):
		if self.future: self.future.set_result(1)
		print(self.name, 'connected')
		# _core.emit('tcp:connected', self.ip, self.port)
		self.transport = transport

	def data_received(self, data, addr=None):
		for i in self.packet_streams:
			if i.recv:
				if addr: i.recv(data, addr)
				else: i.recv(data)
		
	def send(self, msg):
		# print('tcp send:',msg)
		if self.transport: self.transport.write(msg)
		
	def connection_lost(self, exc):
		self.transport = None
		print('conn lost', self.name)
		if self.mode == 'client':
			print('reconnecting', self.name)
			self.run()
	
	def close(self):
		if self.transport: self.transport.close()
