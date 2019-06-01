# from core.schedulers.SimulationScheduler import SimulationScheduler
def run():
	# _core.task_manager.set_scheduler(SimulationScheduler())

	@_spawn
	def s():
		# sleep(1)
		@_do
		def _():
			# return
			if not _sim:
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
				print('sim res:',_core.task_manager.get_current_task().run_simulator())
	
	_print('sleeping now')
	sleep(5)
	with _pick_best():
		sleep(10)
		sleep(1)
		@_do
		def _():
			sleep(5)
			print('called')
			with _pick_best():
				sleep(5)
				sleep(3)
				_print('lol')
	_print('sleeping done')
