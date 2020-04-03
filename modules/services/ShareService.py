SHARE_MESSAGE = 1
SHARE_ENTITY = 2
SHARE_EVENT = 3
SHARE_STATE = 4

import json, asyncio
from core.Entities import Entity
from core.Util import *
from core.network.packet.ChunkPacket import *
from core.Debug import dbg
	
class ShareService:
	
	def __init__(self, name='share', packet_stream=None, share_entity=True):
		self.name = name
		self.states = {}
		self._shared = []
		self.block = False
		self.share_entity=share_entity
		self.set_packet_stream(packet_stream)
		_core.listen('state:change', self.on_state_change)
		_core.listen('state:init', self.on_state_init)
	
	def on_state_init(self, st, value=None, name=None, ishared=True, **kwargs):
		# if _core.debug >= 1.1:
		# print('init state', name, kwargs)
		if 'shared' in kwargs and kwargs['shared']:
			st.shared = True
			self._shared.append(st)
		
	def update_state(self, name, new):
		n = next((i for i in self._shared if i.name == name), None)
		if n:
			print('upd state')
			self.block = 1
			n._set(new)
			self.block = 0
		
	def on_state_change(self, st, old, new):
		if State.is_sim():
			return
#print('st ch:', old, new)
		if self.block: return
		if hasattr(st, 'shared') and st.shared:
			print('is shared')
			self.set_state(st.name, new)
				
	def on_recv(self, pkt):
		if not pkt: return
		if pkt[0] == SHARE_MESSAGE:
			msg=pkt[1:].decode()
			_core.service_manager.emit('message', msg)
		elif pkt[0] == SHARE_EVENT:
			pass
		elif pkt[0] == SHARE_ENTITY:
			if not self.share_entity: return
			
			ent = json.loads(pkt[1:])
			if ent['type']!='friendly_robot':
				dbg('share:on_recv:share_entity', ent)
			found_ent = _core.entities.get_entity_by_name(ent['name'])
			
			if found_ent:
				if ent['action'] == 'remove':
					_core.entities.remove_entity(found_ent)
				elif ent['action'] == 'disable':
					_core.entities.disable_entity(found_ent)
				else:
					found_ent.refresh()
			if not found_ent:
				if ent['action'] == 'add':
					_core.entities.add_entity(ent['type'], ent['name'],
						ent['polygon'], ent['point'], ent['duration'])

		elif pkt[0] == SHARE_STATE:
			p=json.loads(pkt[1:])
			self.states[ p[0] ] = p[1]
			self.update_state(p[0], p[1])
			_core.emit('share:state_change', p[0], p[1])
			# print('rcv state', p)
			
	def set_packet_stream(self, ps):
		if ps:
			self.ps = ChunkPacket(ps)
			self.ps.recv = self.on_recv

	async def loop(self):
		while True:
			await asyncio.sleep(0.5)
			ent = Entity('friendly_robot', _core.robot, _core.get_position(),
				polygon_square_around_point(_core.get_position()[:2], 150), 0.2)
			d = ent.__dict__.copy()
			d['action'] = 'add'
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(d).encode())
			
	def on_new_entity(self,ent):
		if ent.type != 'friendly_robot':
			d = ent.__dict__.copy()
			d['action'] = 'add'
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(d).encode())
			dbg('share:new_entity', ent.type, d)
	
	def run(self):
		asyncio.ensure_future(self.loop())
		_core.listen('entity:new', self.on_new_entity)
		_core.listen('entity:remove', self.on_remove_entity)
		_core.listen('entity:disable', self.on_disable_entity)
		
	def on_remove_entity(self, ent):
		if ent.type != 'friendly_robot':
			d = ent.__dict__.copy()
			d['action'] = 'remove'
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(d).encode())
			dbg('share:remove_entity', ent.type, d)
			
	def on_disable_entity(self, ent):
		if ent.type != 'friendly_robot':
			d = ent.__dict__.copy()
			d['action'] = 'disable'
			self.ps.send(bytes([SHARE_ENTITY]) + json.dumps(d).encode())
			dbg('share:disable_entity', ent.type, d)
		
	def get_state(self, state_name):
		return self.states[state_name]
		
	@_core.asyn2
	def set_state(self, state_name, value):
		self.states[state_name] = value
		p=json.dumps((state_name, self.states[state_name])).encode()
		self.ps.send(bytes([SHARE_STATE]) + p)
		dbg('share:set_state', p)
		
	@_core.do
	def send_msg(self, msg):
		# if _core.debug >= 1: print('sending:', msg)
		dbg('share:send_msg', msg)
		self.ps.send(bytes([SHARE_MESSAGE]) + msg.encode())
		
	def export_cmds(self, namespace=''):
		p=_core.export_ns()
		_core.export_ns(namespace)
		_core.export_cmd('get_state', self.get_state)
		_core.export_cmd('set_state', self.set_state)
		_core.export_cmd('send_msg', self.send_msg)
		_core.export_ns(p)
		
