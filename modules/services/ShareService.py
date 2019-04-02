SHARE_MESSAGE = 1
SHARE_ENTITY = 2
SHARE_EVENT = 3
SHARE_STATE = 4

import json, asyncio
from core.Entities import Entity
from core.Util import *
from core.network.packet.ChunkPacket import *
class ShareService:
	
	def __init__(self, name='share', packet_stream=None):
		self.name = name
		self.states = {}
		self.set_packet_stream(packet_stream)
		
	def on_recv(self, pkt):
		if not pkt: return
		if pkt[0] == SHARE_MESSAGE:
			msg=pkt[1:].decode()
			_core.service_manager.emit('message', msg)
		elif pkt[0] == SHARE_EVENT:
			pass
		elif pkt[0] == SHARE_ENTITY:
			return
			ent = json.loads(pkt[1:])
			#  print('rcv entity', ent['type'])
			_core.entities.add_entity(ent['type'], ent['name'], ent['polygon'], ent['point'], ent['duration'])
			
		elif pkt[0] == SHARE_STATE:
			p=json.loads(pkt[1:])
			self.states[ p[0] ] = p[1]
			_core.emit('share:state_change', p[0], p[1])
			print('rcv state', p)
			
	def set_packet_stream(self, ps):
		if ps:
			self.ps = ChunkPacket(ps)
			self.ps.recv = self.on_recv
		
	async def loop(self):
		while True:
			await asyncio.sleep(0.5)
			ent = Entity('friendly_robot', _core.robot, _core.get_position(),
				polygon_square_around_point(_core.get_position()[:2], 300), 0.2)
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(ent.__dict__).encode())
			
	def on_new_entity(self,ent):
		if ent.type != 'static' and ent.type != 'friendly_robot':
			if _core.debug >= 1: print('share entity', ent.type)
			#  self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(ent.__dict__).encode())
		
	def run(self):
		asyncio.ensure_future(self.loop())
		_core.listen('entity:new', self.on_new_entity)
		
	def get_state(self, state_name):
		return self.states[state_name]
		
	@_core.asyn2
	def set_state(self, state_name, value):
		self.states[state_name] = value
		p=json.dumps((state_name, self.states[state_name])).encode()
		self.ps.send(bytes([SHARE_STATE]) + p)
		
	@_core.do
	def send_msg(self, msg):
		if _core.debug >= 1:
			print('sending:', msg)
		self.ps.send(bytes([SHARE_MESSAGE]) + msg.encode())
		
	def export_cmds(self, namespace=''):
		p=_core.export_ns()
		_core.export_ns(namespace)
		_core.export_cmd('get_state', self.get_state)
		_core.export_cmd('set_state', self.set_state)
		_core.export_cmd('send_msg', self.send_msg)
		_core.export_ns(p)
		
