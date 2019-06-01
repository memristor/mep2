motion='Motion'

@_core.on('config:done')
def run():
	
	@_core.task_setup_func
	def foreach_task():
		
		# _core.expose_task_commands()
		mod = _core.get_module(motion)
		
		r = getattr(_e, mod.namespace)
		
		@_e._listen('motion:error')
		def on_error():
			# _e._sync(1, ref='main')
			# _e._wake('main')
			print('motion:error')
			
		@_e._listen('motion:glitch_blocked')
		def on_glitch():
			pos = _core.get_position()
			# _e._sync(1, ref='main')
			# _e._wake('main')
			print('glitch blocked')
			on_reset(pos)
			
		def on_reset(pt):
			print('got reset', pt)
			fut = mod.future
			mod.future=None
			_e._sync(1, ref='main')
			@_e._do
			def _(): mod.future=None
			r.reset()
			r.setpos(*pt)
			
			@_e._do
			def after_softstop():
				# _e._print('after_softstop')
				mod.future = fut
			_e._wake('main')
			# _core.task_manager.get_current_task().list_threads()
		
		_e._listen('motion:reset', on_reset)
