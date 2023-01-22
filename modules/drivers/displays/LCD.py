class LCD:
	def __init__(self):
		self.name='lcd'
		from .lcd.lcddriver import lcd
		self.lcd = lcd()
		
	def show_pts(self, p):
		self.lcd.clear()
		self.lcd.display_string(str(p), 0)
