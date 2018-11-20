import asyncio
import socket
import struct
import sys
import binascii
import time
from .packet.PacketStream import *


class Can:

	def __init__(self, iface='can0', addr=0, debug=0):
		self.name = 'Can'
		self.addr = addr
		self.can_frame_fmt = "=IB3x8s"
		self.use_eff = 0x80000000
		#  self.debug = debug
		self.debug = 0
		self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
		self.s.setblocking(0)
		self.packet_streams=[]
		self.s.bind((iface,))
	
	def get_packet_stream(self, addr=None):
		ps = PacketStream()
		ps.addr = addr
		def wsend(pkt):
			if type(pkt) is str:
				pkt = pkt.encode('utf-8')
			self.send(pkt, addr=ps.addr)
		ps.send = wsend
		self.packet_streams.append(ps)
		return ps
		
	def ext(self,tf):
		self.use_eff = 0x80000000 if tf else 0

	def _build_can_frame(self, can_id, data):
		can_dlc = len(data)
		data = data.ljust(8, b'\x00')
		return struct.pack(self.can_frame_fmt, can_id | self.use_eff, can_dlc, data)

	def _dissect_can_frame(self,frame):
		can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, frame)
		return (can_id, can_dlc, data[:can_dlc])

	def set_addr(self, a):
		self.addr = a
		
	def send(self, binary, addr=None):
		if addr == None:
			addr = self.addr
		frame = self._build_can_frame(addr, binary)
		self.s.send(frame)
		
	async def read(self):
		while True:
			frame = self._dissect_can_frame(await self.loop.sock_recv(self.s, 16))
			for i in self.packet_streams:
				if i.recv != None and (i.addr == None or (i.addr != None and frame[0] == i.addr)):
					i.recv(frame[2])
	
	def run(self):
		asyncio.ensure_future(self.read())
		self.loop = self.core.loop
