from modules.services.CollisionDetector import *
wait_time=1

@_core.do
def stop_pause():
	motion = _core.get_module('Motion')
	fut = motion.future
	motion.future=None
	_e._sync(1, ref='main')
	_e._print('stopping')
	_e._repeat('block2')
	_e.r.softstop()
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
	collision_detector = CollisionDetector(wait_time=wait_time, size=[-1500, -1000, 3000, 2000])
	_core.add_module([collision_detector])
	
	@_core.task_setup_func
	def behaviour():
		# using _repeat='replace' because while waiting for wait_time, opponent may get out of our way
		# so execution of sleep and whole listener will immediatelly cancel and get replaced with new one (it will then do _wake('main') and robot continues moving)
		@_e._listen('collision', _name='on_collision', _repeat='replace')
		def on_collision(msg):
			if msg == 'danger':
				print(col.yellow, 'got collision', col.white)
				stop_pause()
			elif msg=='safe':
				print(col.yellow, 'its safe', col.white)
				_e._wake('main') # we may continue main thread
