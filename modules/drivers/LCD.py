from modules.drivers.lcd.lcddriver import lcd
from core.Util import asyn2
class LCD:
	def __init__(self):
		self.name='lcd'
		self.lcd = lcd()
		self.cur_pts = 0
		
	@asyn2
	def addpts(self, p):
		self.cur_pts += p
		self.show_pts(self.cur_pts)
		
	def show_pts(self, p):
		self.lcd.clear()
		self.lcd.display_string(str(p), 0)
		
	def export_cmds(self):
		self.core.export_cmd('addpts', self.addpts)
