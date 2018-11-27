_sim_mode=False
_last_sim = 1
_sim_time=0
class State:
	pass

class StateBase:
	
	def __init__(self, value=None, name=None):
		self.name = name
		self._val = value
		self._sim_val = None
		self.last_sim = 1
		
	
	def _set(self, value):
		if _sim_mode == False:
			self._val = value
		else:
			self._sim_val = value
			self.last_sim = _sim_mode
	
	def _get(self):
		return self._val if _sim_mode != self.last_sim else self._sim_val
		
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
		return self.get()

class _State(StateBase):
	on_init=None
	def __init__(self, value=None, name=None):
		super().__init__(value,name)
		if _State.on_init:
			_State.on_init()
	
	@_core.do
	def set(self, value):
		return super().set(value)
		
	val = property(StateBase.get, set)

	@_core.do
	def inc(self):
		return super().inc()
