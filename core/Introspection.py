from core.network.TcpServer import TcpServer
from core.network.packet.ChunkPacket import ChunkPacket
import asyncio, struct
from core.Util import *
import json

class Introspection:
	def __init__(self):
		self.port = 5100

	def run(self):
		self.tcp = TcpServer(name='introspection_tcp', port=self.port)
		self.ps = ChunkPacket( self.tcp.get_packet_stream() )
		self.ps.recv = self.on_recv
		_core.add_module(self.tcp)
		_core.entities.on_new_entity.append(self.on_new_entity)
		asyncio.ensure_future(self.loop())
		
	def send_json(self, jobj):
		m = bytes([3, ord('J')]) + json.dumps(jobj).encode()
		self.ps.send(m)
		
	def send_entity(self, ent):
		jobj = {'response': 'entity', 'entity': ent.__dict__}
		self.send_json(jobj)
		
	def send_entities(self):
		for ent in _core.entities.get_entities():
			self.send_entity(ent)
			
	def on_new_entity(self, ent):
		self.send_entity(ent)
		
	def on_recv(self, pkt):
		if not pkt: return
		pkt = pkt.decode()
		
		try:
			j = json.loads(pkt)
		except:
			print('introspection json fail', pkt)
			return
			
		if j['request'] == 'entities':
			#  print(pkt)
			#  lst = ChunkPacket.list_from_chunks(pkt[1:])
			
			# send static obstacles
			#  if lst[0].decode() == 'static':
			#  print('looking for ents of type:', j['type'])
			for ent in _core.entities.get_entities(j['type']):
				#  print('sending entity')
				jobj = {'response': 'entity', 'entity': ent.__dict__}
				self.send_json(jobj)
		elif j['request'] == 'sensor':
			data = _core.sensors.get_sensor_data(j['type'], j['length'])
			d = [i.abs2 for i in data]
			print('sending sensor data',len(d))
			self.send_json({'response': 'sensor', 'type': j['type'], 'data': d})
		elif j['request'] == 'put_entity':
			pt = j['point']
			_core.entities.add_entity('robot', 'robot', polygon_square_around_point(pt, 300), point=pt, duration=j['duration'])
			
	async def loop(self):
		while 1:
			await asyncio.sleep(0.1)
			p=_core.get_position()
			pkt = struct.pack('>3h', *p )
			self.ps.send( bytes([3]) + b'PI' + pkt )
