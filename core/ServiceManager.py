# very simple event propagation

class Listener:
	def __init__(s, evt_name, callback, emitter, args, kwargs):
		s.state = 1
		s._once = False
		s.evt_name = evt_name
		s.emitter = emitter
		s.callback = callback
		s.args = args
		s.kwargs = kwargs
		
	def pause(s):
		pass
		
	def resume(s):
		pass
		
	def stop(s): # destroy
		s.emitter._on_lose_listener(s)
		#  if type(s.emitter) == Emitter:
			#  s.emitter.listeners.remove(s)
		#  else:
			#  s.emitter.unbound_listeners.remove(s)
	
class Emitter:
	def __init__(s, evt_name, event_manager):
		s.evt_name = evt_name
		s.listeners=[]
		s.event_manager = event_manager
	
	## private: don't use directly
	def _on_new_listener(s, listener):
		s.listeners.append(listener)
		s.on_new_listener(listener)
	
	def _on_lose_listener(s, listener):
		#  if listener in s.listeners:
		s.listeners.remove(listener)
		s.on_lose_listener(listener)
	##
	
	def on_new_listener(s, listener):
		pass
		
	def on_lose_listener(s, listener):
		pass
		
	def emit(s, *params, listener=None):
		for l in list(s.listeners):
			l.callback(*params)
			if l._once:
				#  print('lst once')
				l.stop()
		
	def stop(s): # destroy
		#  print('stop', s.event_manager.emitters)
		s.event_manager.emitters.remove(s)

class ServiceManager(Emitter):
	def __init__(s):
		super().__init__('',s)
		#  s.unbound_listeners = []
		s.emitters = []
		
	def _find_emitter(s, evt_name, default=None):
		return next((e for e in s.emitters if e.evt_name == evt_name), s if default == None else default)
	
	#  def on_new_listener(s, listener):
		#  s.unbound_listeners.append(listener)
	
	#  def on_lose_listener(s, listener):
		#  s.unbound_listeners.remove(listener)
		
	# public:
	def listen(s, evt_name, callback, *args, **kwargs):
		emitter = s._find_emitter(evt_name)
		print('adding listener', evt_name)
		l = Listener(evt_name, callback, emitter, args, kwargs)
		#  if emitter != None:
		emitter._on_new_listener(l)
		#  else:
			#  s.unbound_listeners.append(l)
		return l
	def listen_once(s, evt_name, callback, *args, **kwargs):
		emitter = s._find_emitter(evt_name)
		
		l = Listener(evt_name, callback, emitter, args, kwargs)
		l._once = True
		#  if emitter != None:
		emitter._on_new_listener(l)
		#  else:
			#  s.unbound_listeners.append(l)
		return l
		
	# should i use?
	def emit(s, evt_name, *params):
		for l in s.listeners:
			if l.evt_name == evt_name:
				l.callback(*params)
		emitter = s._find_emitter(evt_name)
		if type(emitter) == Emitter:
			emitter.emit(*params)
		
	def register(s, evt_name, service=None):
		emitter = s._find_emitter(evt_name)
		if type(emitter) == Emitter:
			raise Exception("emitter event already taken")
		#  print(emitter)
		if service == None:
			service = Emitter
		e = service(evt_name, s)
		
		e.listeners += [x for x in s.listeners if x.evt_name == evt_name]
		s.listeners[:] = [x for x in s.listeners if x.evt_name != evt_name]
		
		s.emitters.append(e)
		return e
