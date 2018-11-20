from operator import itemgetter, attrgetter, methodcaller
import asyncio

states={
	'pending': '\x1b[33m PENDING\x1b[0m',
	'done': '\x1b[32m DONE\x1b[0m',
	'suspended': '\x1b[31m SUSPENDED\x1b[0m'
}
class BasicScheduler:
	def __init__(self, mode='weight'):
		self.mode=mode
	
	def task_criteria(self, mod):
		score = mod.order if self.mode == 'order' else mod.weight
		return score
		
	def pick_task(self):
		print('scheduler picking new task')
		tasks = []
		for task in self.task_manager.get_tasks():
			print('task', task.name, states[task.state.get()])
		for task in self.task_manager.get_pending_tasks():
			if hasattr(task.module, self.mode):
				tasks.append(task)
		if tasks:
			tasks=sorted(tasks, key=lambda t: self.task_criteria(t.module), reverse=(self.mode == 'weight'))
			for task in tasks:
				if task.module.run() != False:
					self.task_manager.set_task(task.name)
					# successfully picked task
					return True
			# no tasks found, try later
			_core.loop.call_later(0.1, self.pick_task)
			return False
		# print('no more tasks')
		exit(0)
		return False
