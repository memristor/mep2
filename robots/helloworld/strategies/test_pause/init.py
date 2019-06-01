def run():
	r.setpos(0,0,0)
	@_spawn
	def _():
		with _while(1):
			sleep(2)
			
			@_do
			def stopping():
				motion = _core.get_module('Motion')
				fut = motion.future
				_print('stopping')
				r.softstop()
				@_do
				def after_softstop():
					_print('after_softstop')
					motion.future = fut
			_sync(1, ref='main')
			
			sleep(1)
			_wake('main')
			
	@_do
	def _():
		r.forward(1000)
		r.turn(720)
		r.curve_rel(300, -360)
		r.curve(400, 400, 360)
