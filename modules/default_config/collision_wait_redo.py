from modules.services.CollisionDetector import *
collision_detector=CollisionDetector(wait_time=1, size=[-1500, -1000, 3000, 2000])
_core.add_module([collision_detector])
wait_time=2

@_core.listen('task:done')
def task(t):
	print('task is done:',t)
@_core.listen('config:done')
def exec_config():
	_core.expose_task_commands()
	@_core.task_setup_func
	def behaviour():
		_e._print('starting pf listener')
		# using _repeat='replace' because while waiting for wait_time, opponent may get out of our way
		# so execution of sleep and whole listener will immediatelly cancel and get replaced with new one (it will then do _wake('main') and robot continues moving)
		@_e._listen('collision', _name='on_collision', _repeat='block')
		def on_collision(msg):
			if msg == 'danger':
				print(col.yellow, 'got collision', col.white)
				_e._sync(ref='main') # stop task main thread
				# _e.r.softstop() # stop robot
				_e.r.stop() # stop robot
				'''
				save = _e.r.accel()
				@_do
				def _():
					_e.r.accel(100)
					_e.r.softstop() # stop robot
					_e.r.accel(save.val)
				_e._print('stopping')
				_e.sleep(wait_time)
				_e._print('waited')
				'''
				#r.forward(-_core.state['direction'] * 200)
				_e._do(collision_detector.release)
				_e._wake('main') # we may continue main thread
				sleep(0.1)
				#_e._task_suspend() # suspend task
			elif msg=='safe':
				_e._wake('main') # we may continue main thread
