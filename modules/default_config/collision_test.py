from modules.services.CollisionDetector import *
wait_time=1

@_core.listen('config:done')
def exec_config():
	collision_detector = CollisionDetector(wait_time=wait_time, size=[-1500, -1000, 3000, 2000])
	_core.add_module([collision_detector])	
	
	@_core.task_setup_func
	def on_task_start():
		
		@_e._listen('collision', _name='on_collision', _repeat='replace')
		def listen_collision(msg):
			if msg == 'danger':
				print(col.yellow, 'got collision', col.white)
			elif msg=='safe':
				print(col.yellow, 'its safe', col.white)
