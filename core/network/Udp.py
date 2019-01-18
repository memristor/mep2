import asyncio
from core.network.packet.PacketStream import PacketStream
from core.network.Tcp import Tcp

class Udp(Tcp):
	def __init__(self, name='udp', ip='0.0.0.0', local_port=0, port=5005):
		super().__init__(name,ip,port,mode='udp')
		self.local_port = local_port
		
	def run(self):
		async def get_transport():
			self.transport, _ = await _core.loop.create_datagram_endpoint(lambda: self, local_addr=('0.0.0.0', self.local_port), allow_broadcast=True)
		asyncio.ensure_future( get_transport() )

	datagram_received=Tcp.data_received
	
	def get_packet_stream(self, addr=None):
		ps = PacketStream(lambda msg: self.send(msg, addr if addr else (self.ip, self.port)))
		self.packet_streams.append(ps)
		return ps
		
	def send(self, msg, addr):
		if self.transport: self.transport.sendto(msg, addr)
		
	def broadcast(self, msg, port):
		self.send(msg, ('127.0.0.255', port))
		self.send(msg, ('255.255.255.255', port))
