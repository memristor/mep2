_sim_mode=False
_sim_time=0
level=0
class State: pass
class StateBase:
	def __init__(self, value=None, name=None):
		self.name = name
		self._val = [value]
		self.last_sim = 1
		
	def _set(self, value):
		if level > 0:
			self.last_sim = _sim_mode
			d=level+1 - len(self._val)
			if d != 0:
				self._val = self._val[:level+1] if d < 0 else self._val + [self._val[-1]] * d
			# print('level:',level,d, self._val)
		self._val[level] = value
	
	def _get(self):
		return self._val[0] if _sim_mode != self.last_sim else self._val[-1]
		
	set=_set
	get=_get
	
	val = property(get, set)
	
	def inc(self):
		self.set(self.get()+1)
	
	# list operations
	def append(self, value):
		self.set(self.get() + [value])

	def remove(self, value):
		self.set([i for i in self.get() if i != value])
	
	def clear(self):
		self.set([])

	def __repr__(self):
		return 'StateBase:'+str(self.get())

class _State(StateBase):
	on_init=None
	def __init__(self, value=None, name=None):
		super().__init__(value,name)
		if _State.on_init: _State.on_init()
		
	@_core.do
	def set(self, value):
		return super().set(value)
		
	val = property(StateBase.get, set)
	
	def __call__(self):
		return self.val

	@_core.do
	def inc(self):
		return super().inc()
