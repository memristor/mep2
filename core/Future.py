from .State import StateBase
from core.Constants import *

class FuturePending:
	def __repr__(self):
		return 'FuturePending'
	pass

class Future:
	def __init__(self, thread=None):
		self.result = StateBase(None)
		self.exception = StateBase(None)
		self._thread = StateBase(thread)
		self.state = StateBase(PENDING)
		self.on_done = StateBase([])
		self.on_cancel = StateBase([])
		self.on_pause = StateBase([])
		
		self.call = None
	
	def __call__(self, *args, **kwargs): # for immediate use
		if self.call: self.call(*args, **kwargs)
		
	def set_result(self, result):
		# print('fut set result')
		if not self.done():
			self.result.val = result
			# wake waiting thread
			if self.thread != None:
				# print('fut set result', self)
				# import traceback
				# traceback.print_stack()
				self.thread.wake(SYNC_FUTURE)
			# on_done callback
			for on_done in self.on_done.val:
				# print('fut (set_result) on done', self) 
				on_done()
			self.clear()
			self.state.val = DONE
		
	def get_result(self):
		return (self.result.val if self.done() else FuturePending()) if type(self.result.val) != Future else self.result.val.val
		
	# get <=> get_result, set <=> set_result aliases
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
	
	def set_on_pause(self, on_pause):
		self.on_pause.append(on_pause)
	
	def pause(self):
		for func in self.on_pause.val: func(pause=True)
		self.state.val = PAUSED
		return
		'''
		if self.on_pause.val:
			for func in self.on_pause.val: func(pause=True)
			self.state.val = PAUSED
		else:
			self.cancel()
		'''
			
	def resume(self):
		if self.paused():
			self.state.val = PENDING
			for func in self.on_pause.val: func(pause=False)
	
	def paused(self):
		return self.get_state() == PAUSED
		
	def cancelled(self):
		return self.get_state() in (CANCELLED,DONE)
	
	def clear(self):
		self.on_done.clear()
		self.on_cancel.clear()
	
	def reset(self):
		self.state.val = PENDING
		self.clear()
	
	def cancel(self):
		if self.state.val in (PENDING, PAUSED):
			self.state.val = CANCELLED
			for func in self.on_cancel.val: func()
			
			self.on_cancel.clear()
			self.on_pause.clear()
			
	def get_state(self):
		return self.state.val
		
	def done(self):
		return self.state.val == DONE
