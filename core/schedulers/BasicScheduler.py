class BasicScheduler:
	def __init__(self, mode='weight'):
		self.mode=mode
	
	def task_criteria(self, task):
		return task.module.order if self.mode == 'order' else task.module.weight
		
	def pick_task(self):
		print('scheduler picking new task')
		_core.task_manager.print_task_states()
		tasks = [task for task in _core.task_manager.get_pending_tasks() if hasattr(task.module, self.mode)]
		if tasks:
			# print('has tasks')
			tasks=sorted(tasks, key=self.task_criteria, reverse=(self.mode == 'weight'))
			for task in tasks:
				if self.task_manager.set_task(task.name):
					# successfully picked task
					return True
			# no tasks found, try later
			_core.loop.call_later(0.1, self.pick_task)
			return False
		# print('no more tasks')
		# exit(0)
		return False
