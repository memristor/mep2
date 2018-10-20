SHARE_MESSAGE = 1
SHARE_ENTITY = 2
SHARE_EVENT = 3
SHARE_STATE = 4

import json,asyncio
from core.Entities import EntityPoint
from core.Util import *
from core.network.packet.ChunkPacket import *
class ShareService:
	
	def __init__(self, packet_stream=None):
		self.name = 'share service'
		self.states = {}
		self.set_packet_stream(packet_stream)
		self.on_state_change = Event()
		
	def on_recv(self, pkt):
		if not pkt:
			return
			
		if pkt[0] == SHARE_MESSAGE:
			msg=pkt[1:].decode()
			self.core.service_manager.emit('message', msg)
		elif pkt[0] == SHARE_EVENT:
			pass
		elif pkt[0] == SHARE_ENTITY:
			return
			ent = json.loads(pkt[1:])
			#  print('rcv entity', ent['type'])
			self.core.entities.add_entity(ent['type'], ent['name'], ent['polygon'], ent['point'], ent['duration'])
			
		elif pkt[0] == SHARE_STATE:
			p=json.loads(pkt[1:])
			self.states[ p[0] ] = p[1]
			self.on_state_change(p[0], p[1])
			print('rcv state', p)
			
	def set_packet_stream(self, ps):
		
		if ps:
			self.ps = ChunkPacket(ps)
			self.ps.recv = self.on_recv
		
	async def loop(self):
		while True:
			await asyncio.sleep(0.5)
			ent = EntityPoint('friendly_robot', self.core.robot, self.core.position,
				polygon_square_around_point(self.core.position, 300), 0.2)
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(ent.__dict__).encode())
			
	def on_new_entity(self,ent):
		if ent.type != 'static' and ent.type != 'friendly_robot':
			print('share entity', ent.type)
			#  self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(ent.__dict__).encode())
		
	def run(self):
		asyncio.ensure_future(self.loop())
		self.core.entities.on_new_entity.append(self.on_new_entity)
		pass
		
	def get_state(self, state_name):
		return self.states[state_name]
		
	@asyn2
	def set_state(self, state_name, value):
		self.states[state_name] = value
		p=json.dumps((state_name, self.states[state_name])).encode()
		self.ps.send(bytes([SHARE_STATE]) + p)
		
	@asyn2
	def send_msg(self, msg):
		print('sending:',msg)
		self.ps.send(bytes([SHARE_MESSAGE]) + msg.encode())
		
	def export_cmds(self):
		self.core.add_sync_cmd('get_state', self.get_state)
		self.core.export_cmd('set_state', self.set_state)
		self.core.export_cmd('send_msg', self.send_msg)
		
