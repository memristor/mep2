from core.Convert import *
import binascii
class ColorSensor:
	def __init__(self, name, id, packet_stream=None):
		self.ps = None
		self.id = id
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
	
	
	def on_recv(self, pkt):
		if len(pkt) >= 8:
			self.value = (lu16l(pkt,0), lu16l(pkt,2), lu16l(pkt,4), lu16l(pkt,6))
			self.future.set_result( self.rgb_to_hsv( self.value ) )
			#self.future.set_result( self.value  )

	def export_cmds(self, ns=''):
		with _core.export_ns(ns):
			_core.export_cmd('color', self.color)
		
	@_core.module_cmd
	def color(self):
		self.ps.send(bytes([self.id]))

	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps

	def rgb_to_hsv(self, r, g, b):
		r /= 255
		g /= 255
		b /= 255

		_max = max(r, g, b)
		_min = min(r, g, b)
		h=s=v = _max

		d = _max - _min
		s = 0 if _max == 0 else d / _max

		if _max == _min:
			h = 0
		else:
			if _max == r:
				h = (g - b) / d + (6 if g < b else 0)
			elif _max == g:
				h = (b - r) / d + 2
			elif _max == b:
				h = (r - g) / d + 4
			h /= 6;
		return [ h * 255, s * 255, v * 255 ]
