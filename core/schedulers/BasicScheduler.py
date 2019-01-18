from core.Util import get_task_param
class BasicScheduler:
	def __init__(self, mode='weight'):
		self.mode=mode
	
	def task_criteria(self, task):
		return get_task_param(task, self.mode)
		
	def pick_task(self, tasks):
		tasks = [task for task in tasks if hasattr(task.module, self.mode)]
		if tasks:
			tasks=sorted(tasks, key=self.task_criteria, reverse=(self.mode == 'weight'))
			for task in tasks:
				if _core.task_manager.set_task(task.name):
					# successfully picked task
					return True
		return False
