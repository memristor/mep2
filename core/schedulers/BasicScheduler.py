from operator import itemgetter, attrgetter, methodcaller
import asyncio
class BasicScheduler:
	def __init__(self):
		pass
	
	def task_criteria(self, mod):
		score = mod.weight
		return score
		
	def pick_task(self):
		print('scheduler picking new task')
		tasks = []
		for task in self.task_manager.get_tasks():
			print('task', task.name, task.state)
		for task in self.task_manager.get_pending_tasks():
			if hasattr(task.module, 'weight'):
				print(task.module.weight)
				tasks.append(task)
		if tasks:
			tasks=sorted(tasks, key=lambda t: self.task_criteria(t.module), reverse=True)
			for i in tasks:
				if i.module.run() != False:
					self.task_manager.set_task(i.name)
					return True
			self.core.loop.call_later(0.1, self.pick_task)
			return False
		print('no more tasks')
		#  exit(0)
		return False
