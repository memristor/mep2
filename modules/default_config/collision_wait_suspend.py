from modules.services.CollisionDetector import *
collision_detector=CollisionDetector(name='CollisionDetector', wait_time=1, size=[-1500, -1000, 3000, 2000])
_core.add_module([collision_detector])
wait_time=1


@_core.do
def stop_pause():
	motion = _core.get_module('Motion')
	fut = motion.future
	motion.future=None
	_e._sync(1, ref='main')
	@_e._do
	def _():
		motion.future=None
		
	_e._repeat('block2')
	if fut:
		# haaard stop
		# for i in range(5):
			# _e.r.stop()
			# _e.sleep(0.1)
		_e._print('stopping', fut)
		save = _e.r.accel()
		@_e._do
		def _():
			_e.r.accel(300)
			_e.sleep(0.01)
			v=_e.r.accel()
			@_e._do
			def _():
				_e._print('save:', save.val, v.val)
			_e.r.softstop()
			_e.r.accel(save.val)
		
	# _e.r.stop()
	@_e._do
	def after_softstop():
		_e._print('after_softstop')
		motion.future = fut
		# _e.sleep(3)
	_e._print('replace')
	_e._repeat('replace')

@_core.listen('task:done')
def task(t):
	print('task is done:',t)
@_core.listen('config:done')
def exec_config():

	@_core.task_setup_func
	def behaviour():
		# using _repeat='replace' because while waiting for wait_time, opponent may get out of our way
		# so execution of sleep and whole listener will immediatelly cancel and get replaced with new one (it will then do _wake('main') and robot continues moving)
		@_e._listen('collision', _name='on_collision', _repeat='replace')
		def on_collision(msg):
			if msg == 'danger':
				print(col.yellow, 'got collision', col.white)
				stop_pause()
				
				_e.sleep(wait_time)
				_e._repeat('block2')
				
				@_e._do
				def forw_after_leave():
					@_core.on('task:after_leave')
					def _():
						pt1 = _core.get_point()
						pt2 = add_pt(_core.get_point(), mul_pt(_core.move_dir_vector(), -200-150))
						print('in_line', pt1, pt2)
						ents = _core.entities.get_entities_in_line(pt1, pt2)
						print('col susp:',ents)
						if not ents:
							_e.r.forward(int(-_core.state['direction'] * 200))
					
				
				_e._task_suspend() # suspend task
				_e._repeat('replace')
			elif msg=='safe':
				_e._print(col.yellow, 'safe', col.white)
				_e._wake('main') # we may continue main thread

		@_e._do
		def resend_state():
			collision_detector.resend_state()
