PENDING='pending'
FINISHED='finished'
class Future:
	def __init__(self, runable=None):
		self.result = None
		self.exception = None
		self.runable = runable
		self.state = PENDING
		self.on_done = []
		
	def set_result(self, result):
		self.result = result
		self.state = FINISHED
		if self.runable != None:
			#  print('waking runable', self.runable.name)
			self.runable.wake()
		for i in self.on_done:
			i()
		self.on_done.clear()
		
	def set_exception(self, exception):
		self.exception = exception
		
	def set_runable(self, runable):
		self.runable = runable
		runable.future = self
	
	def set_on_done(self, on_done):
		self.on_done.append(on_done)
		
	def done(self):
		return self.state != PENDING

	
