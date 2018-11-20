class SimulationScheduler:
	def __init__(self):
		pass
	def task_criteria(self, task):
		return task[0]
		
	def pick_task(self):
		print('scheduler picking new task')
		_core.task_manager.print_task_states()
		tasks = _core.task_manager.get_pending_tasks()
		if tasks:
			print('has tasks')
			tasks = [(task.run_simulator(), task) for task in tasks if self.task_manager.set_task(task.name)]
			print([(t[0], t[1].name) for t in tasks])
			if tasks:
				tasks=sorted(tasks, key=self.task_criteria)
				score,task=tasks[0]
				self.task_manager.set_task(task.name)
				return True
			# no tasks found, try later
			_core.loop.call_later(0.1, self.pick_task)
			return False
		# print('no more tasks')
		# exit(0)
		return False

# 120 + 150 = 270
