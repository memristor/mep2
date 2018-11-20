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
		if self.state != FINISHED:
			self.result = result
			if self.runable != None:
				#  print('waking runable', self.runable.name)
				self.runable.wake()
			for on_done in self.on_done:
				on_done()
			self.on_done.clear()
		self.state = FINISHED
		
	def get_result(self):
		return self.result
	get = get_result
	set = set_result
	
	val = property(get, set)
	
	def get_exception(self):
		return self.exception
	
	def set_exception(self, exception):
		self.exception = exception
		
	def set_runable(self, runable):
		self.runable = runable
		runable.future = self
	
	def set_on_done(self, on_done):
		self.on_done.append(on_done)
		
	def done(self):
		return self.state != PENDING

	
