import os
import sys
import importlib
import asyncio
from .Task import *
		
class TaskManager:
	def __init__(self, core): # fix this interdependency issue somehow maybe?
		self.current_task = None
		self.current_sim_task = None
		self.tasks = []
		self.core = core
		self.core_funcs_exported = False
		Task.service_manager = core.service_manager
		self.scheduler=None
		self.init_task = None
		self.exported_cmds = None
		
	def get_current_task(self):
		return self.current_task
	
	def _export_core_functions(self):
		if self.core_funcs_exported:
			return
		#  self.core_funcs_exported = True
		
		for e in self.core.exported_cmds:
			for k,v in self.core.exported_cmds[e].items():
				Task.export_cmd(e, k, v)
		Task.export_meta_cmds()
		
		
	
	def set_scheduler(self, scheduler):
		self.scheduler = scheduler
		self.scheduler.core = self.core
		self.scheduler.task_manager = self
		
	def schedule_task(self):
		if self.scheduler:
			self.scheduler.pick_task()
		
	def get_tasks(self):
		return self.tasks # returns by reference, don't change it (pls)
	
	def get_pending_tasks(self):
		return list(filter(lambda t: t.state == PENDING, self.tasks))
	
	def has_task(self, name):
		task = self.get_task(name)
		return task != None
		
	def get_task(self,name):
		task = next((t for t in self.tasks if t.name == name), None)
		return task
		
	def get_exported_commands(self):
		if self.core_funcs_exported:
			return self.exported_cmds
			
		self._export_core_functions()
		t = type('',(),{})
		for e in self.core.exported_cmds:
			if e == '':
				# global namespace
				for k,v in Task.exported_wrappers[e].items():
					setattr(t, k, v)
			else:
				# namespaced
				o = type('',(),{})
				for k,v in Task.exported_wrappers[e].items():
					setattr(o, k,v)
				setattr(t, e, o)
		
		# synchronous cmds
		for k,v in self.core.sync_cmds.items():
			setattr(t, k, v)
		
		# from Task
		for k,v in sync_funcs.items():
			setattr(t, k, v)
		self.exported_cmds = t
		return t
	
	def _export_cmds_to_module(self,module):
		self._export_core_functions()
		for e in self.core.exported_cmds:
			if e == '':
				for k,v in Task.exported_wrappers[e].items():
					setattr(module, k, v)
			else:
				o = type('',(),{})
				for k,v in Task.exported_wrappers[e].items():
					setattr(o, k,v)
				setattr(module, e, o)
		for k,v in self.core.sync_cmds.items():
			setattr(module, k, v)
			
		for k,v in sync_funcs.items():
			setattr(module, k, v)
	
	def fullstop(self):
		self.current_task = None
	
	def set_task(self, name):
		self.core_funcs_exported = True
		task = next((t for t in self.tasks if t.name == name), None)
		if task != None:
			module = task.module
			
			
			if name == 'init' and self.init_task:
				task.prepend_func = self.init_task
			print('running task\x1b[33m', name,'\x1b[0m')
			self.current_task = task
			
			def run_this():
				# run default func
				if self.core.task_setup_func:
					self.core.task_setup_func()
					
				task.module.run()
			def on_task_done():
				self.current_task.state = DONE
				print('task state:', self.current_task.state)
				self.current_task = None
				
				self.schedule_task()
			self.current_task.run_task(run_this, on_task_done)
			
		else:
			if name == 'init':
				def empty_func():
					pass
				self.add_task_func(name, self.init_task if self.init_task else empty_func)
				
			if self.scheduler:
				self.schedule_task()
			print('task', name, 'does not exist')
			#  raise Exception('task', name, 'does not exist')

	def load_tasks(self, robot_name, strategy_name):
		tasks_dir = 'robots/'+robot_name+'/strategies/'+strategy_name
		sys.dont_write_bytecode = True
		print('loading strategy:\x1b[32m', strategy_name,'\x1b[0m')
		for i in os.listdir(tasks_dir):
			fullpathname = os.path.join(tasks_dir, i)
			if os.path.isfile(fullpathname):
				if fullpathname.endswith('.py'):

					task_name = i[:-3]
					task = importlib.import_module(fullpathname[:-3].replace('/','.'))
					
					self._export_cmds_to_module(task)
					print('loading task\x1b[33m', task_name,'\x1b[0m')
					self.tasks.append(Task(task_name, task))
	
	def set_init_task(self, task_func):
		self.init_task = task_func
	
	def add_task_func(self, name, task_func):
		t=type('',(),{})
		t.run = task_func
		self.tasks.append(Task(name, t))
		return t
		
	
	def run_cycle(self):
		if self.current_task != None:
			self.current_task.run_cycle()
			#  print(self.current_task)
			if self.current_task and self.current_task.state == SUSPENDED:
				prev = self.current_task
				self.schedule_task()
				prev.state = PENDING
				if not self.current_task or self.current_task == prev:
					self.schedule_task()

