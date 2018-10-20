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
		self.core.add_module(self.tcp)
		self.core.entities.on_new_entity.append(self.on_new_entity)
		asyncio.ensure_future(self.loop())
		
	def on_new_entity(self, ent):
		jobj = {'response':'entity',
				'entity':ent.__dict__}
					#  'type': ent.type,
					#  'name': ent.name,
					#  'polygon': ent.polygon})
		self.send_json(jobj)
		#  print('on new entity: ', jstr)
		
	def send_entities(self):
		for ent in self.core.entities.get_entities():
			#  print('sending entity')
			jobj = {'response': 'entity',
					'entity': ent.__dict__}
			self.send_json(jobj)
		
	def on_recv(self, pkt):
		#  print('introspect', pkt)
		pkt = pkt.decode()
		#  print('should decode', pkt)
		#  if not pkt:
			#  return
		
		try:
			j = json.loads(pkt)
		except:
			print('introspection json fail')
			return
			
		if j['request'] == 'entities':
			#  print(pkt)
			#  lst = ChunkPacket.list_from_chunks(pkt[1:])
			
			# send static obstacles
			#  if lst[0].decode() == 'static':
			#  print('looking for ents of type:', j['type'])
			for ent in self.core.entities.get_entities(j['type']):
				#  print('sending entity')
				jobj = {'response': 'entity',
						'entity': ent.__dict__}
				self.send_json(jobj)
		elif j['request'] == 'sensor':
			data = self.core.sensors.get_sensor_data(j['type'], j['length'])
			d = [i.abs2 for i in data]
			
			print('sending sensor data',len(d))
			self.send_json({'response': 'sensor', 'type': j['type'], 'data': d})
		elif j['request'] == 'put_entity':
			pt = j['point']
			self.core.entities.add_entity('robot', 'robot', polygon_square_around_point(pt, 300), point=pt, duration=j['duration'])
			
	def send_json(self, jobj):
		m = bytes([3, ord('J')]) + json.dumps(jobj).encode()
		#  print('sj',m)
		self.ps.send(m)
		
	async def loop(self):
		while 1:
			await asyncio.sleep(0.1)
			p=self.core.position
			pkt = struct.pack('>3h', *p, self.core.angle )
			#  print('sending:',pkt)
			#  self.send_json({'hhehe':'haha'})
			self.ps.send( bytes([3]) + b'PI' + pkt )
