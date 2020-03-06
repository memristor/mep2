_sim_mode=False
_sim_time=0
level=0
class State:
	sim=0
	sensor_sim=0
	recompile=0
	known=set()

	@staticmethod
	def is_sim():
		return _sim_mode != False

	@staticmethod
	def get(par):
		State.known.add(par)
		return par if hasattr(State, par) else None
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

inst_leader = None
inst = None
class _State:
	states={}
	def __init__(self, value=None, name=None, ishared=True, local=True, **kwargs):
		self.name = name
		if local:
			if ishared and inst != inst_leader:
				self.inst = inst_leader[len(inst)]
				inst.append(self.inst)
				if _core.debug:
					print('using shared state')
			else:
				# new instance
				self.inst = StateBase(value, name)
				if inst: inst.append(self.inst)
		else:
			if name in self.states:
				self.inst = self.states[name]
			else:
				self.inst = StateBase(value, name)
				self.states[name] = self.inst
		if _core.debug >= 3: print('initing state')
		_core.emit('state:init', self, value, name, **kwargs)
		
	@_core.do
	def set(self, value):
		self._set(value)
		
	def _set(self, value, report=True):
		old = self.inst.get()
		if old != value:
			self.inst.set(value)
			if report: _core.emit('state:change', self, old, value)
	
	def get(self):
		return self.inst.get()

	val = property(get, set)

	def __call__(self):
		return self.inst.val

	@_core.do
	def inc(self):
		old = self.inst.get()
		_core.emit('state:change', self, old, old+1)
		return self.inst.inc()
