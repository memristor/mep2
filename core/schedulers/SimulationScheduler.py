from core.Util import get_task_param, dif
import time
class SimulationScheduler:
	def __init__(self):
		self.ltime = time.time()
		self.ptime = 0
		pass

	def task_criteria(self, task_tuple):
		return task_tuple[0]/get_task_param(task_tuple[1],'point',0.1)
	
	def pick_task(self, tasks):
		now = time.time()
		passed=now-self.ltime
		print('passed:',passed,' - ',self.ptime, ' = ', passed-self.ptime)
		if tasks:
			print('has tasks')
			tasks = [(task.run_simulator(), task) for task in tasks if _core.task_manager.set_task(task.name)]
			print([(t[0], t[1].name) for t in tasks])
			if tasks:
				tasks=sorted(tasks, key=self.task_criteria)
				duration,task=tasks[0]
				if duration != float('inf'):
					_core.task_manager.set_task(task.name)
					self.ltime = time.time()
					self.ptime = duration
					return True
		return False
