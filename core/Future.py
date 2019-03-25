PENDING='pending'
FINISHED='finished'
CANCELLED='cancelled'
from .State import StateBase
class Future:
	def __init__(self, thread=None):
		self.result = StateBase(None)
		self.exception = StateBase(None)
		self._thread = StateBase(thread)
		self.state = StateBase(PENDING)
		self.on_done = StateBase([])
		self.on_cancel = StateBase([])
		
		self.call = None
	
	def __call__(self, *args, **kwargs): # for immediate use
		if self.call: self.call(*args, **kwargs)
		
	def set_result(self, result):
		# print('fut set result')
		if not self.done():
			self.result.val = result
			if self.thread != None:
				# print('waking thread:', self.thread.name)
				self.thread.wake()
			for on_done in self.on_done.val: on_done()
			self.clear()
			self.state.val = FINISHED
		
	def get_result(self):
		return self.result.val
	get = get_result
	set = set_result
	
	val = property(get, set)
	
	@property
	def thread(self):
		return self._thread.val
	
	def get_exception(self):
		return self.exception
	
	def set_exception(self, exception):
		self.exception = exception
		
	def set_thread(self, thread):
		self._thread.val = thread
	
	def set_on_done(self, on_done):
		self.on_done.append(on_done)
	
	def set_on_cancel(self, on_cancel):
		self.on_cancel.append(on_cancel)
	
	def clear(self):
		self.on_done.clear()
		self.on_cancel.clear()
		
	def reset(self):
		self.state.val = PENDING
		self.clear()
	
	def cancel(self):
		if self.state.val != CANCELLED:
			self.state.val = CANCELLED
			# print('canncel fut', self.on_cancel)
			for on_cancel in self.on_cancel.val: on_cancel()
			self.on_cancel.clear()
			
	def done(self):
		return self.state.val != PENDING
