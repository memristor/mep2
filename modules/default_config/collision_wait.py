from modules.services.CollisionDetector import *
collision_detector=CollisionDetector(wait_time=1, size=[-1500, -1000, 3000, 2000])
_core.add_module([collision_detector])
wait_time=1

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
				_e._sync(ref='main') # stop task main thread
				_e.r.stop() # stop robot
			elif msg=='safe':
				print(col.yellow, 'its safe', col.white)
				_e._wake('main') # we may continue main thread
