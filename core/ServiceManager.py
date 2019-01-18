class Listener:
	def __init__(s, evt_name, callback, emitter, args, kwargs):
		s.evt_name, s.callback, s.emitter, s.args, s.kwargs = evt_name, callback, emitter, args, kwargs
		s._once = False
		
	def stop(s): # destroy
		s.emitter._remove_listener(s)
	
class Emitter:
	def __init__(s, evt_name):
		s.listeners=[]
		s.evt_name = evt_name
		
	def _add_listener(s, listener):
		s.listeners.append(listener)
		s.on_new_listener(listener)
		
	def _remove_listener(s, listener):
		if listener in s.listeners:
			s.listeners.remove(listener)
			s.on_lose_listener(listener)
		
	def on_new_listener(s, listener): pass # override
	def on_lose_listener(s, listener): pass # override
		
	def emit(s, *params, listener=None, **kwargs):
		for l in s.listeners:
			l.callback(*params, **kwargs)
			if l._once: l.stop()

class ServiceManager(Emitter):
	def __init__(s):
		super().__init__('')
		s.emitters = {}
		s.listener_map = {}
	def _find_emitter(s, evt_name):
		return s.emitters[evt_name] if evt_name in s.emitters else s
	
	def on_new_listener(s, listener):
		if listener.evt_name not in s.listener_map:
			s.listener_map[listener.evt_name] = [listener]
			return
		s.listener_map[listener.evt_name].append(listener)
		
	def on_lose_listener(s, listener):
		s.listener_map[listener.evt_name].remove(listener)
		
	def listen(s, evt_name, callback, *args, **kwargs):
		emitter = s._find_emitter(evt_name)
		if not emitter: return
		l = Listener(evt_name, callback, emitter, args, kwargs)
		emitter._add_listener(l)
		return l
		
	def listen_once(s, *args, **kwargs):
		l = s.listen(*args, **kwargs)
		l._once = True
		return l
		
	def emit(s, evt_name, *params, **kwargs):
		emitter = s._find_emitter(evt_name)
		if emitter == s:
			if evt_name in s.listener_map:
				for l in s.listener_map[evt_name]:
					l.callback(*params, **kwargs)
		else:
			# find foreigner emitter, and emit with it
			emitter.emit(*params)
		
	def register(s, evt_name, service=None):
		emitter = s._find_emitter(evt_name)
		if type(emitter) is Emitter: raise Exception('event already registered')
		service = service or Emitter
		e = service(evt_name)
		s.emitters[evt_name] = e
		
		e.evt_name = evt_name
		e.listeners=[]
		e.event_manager = s
		
		e.listeners   += [x for x in s.listeners if x.evt_name == evt_name]
		s.listeners = [x for x in s.listeners if x.evt_name != evt_name]
		return e
