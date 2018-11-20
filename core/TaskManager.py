
import asyncio
from core.Task import *

class TaskManager:
	def __init__(self):
		self.current_task = None
		self.tasks = []
		self.core_funcs_exported = False
		
		self.scheduler=None
		self._init_task = None
		self.cached_exported_cmds = None
		self._task_setup_func = None
		
		self.exported_cmds = {}
		self.exported_wrappers = {'':{}}
		
		from core.schedulers.BasicScheduler import BasicScheduler
		self.set_scheduler(BasicScheduler())
		
	
	def init_sync_funcs(self):
		self.sync_funcs = {}
		
		@contextmanager
		def disabled(name):
			_e._unlisten(name)
			yield
			_e._listen(name)
		
		@_core.do
		def _print(*args):
			if not _e._sim:
				print(*args)
			
		self.sync_funcs.update({
			'disabled': disabled, 
			'disabler': disabled, # alias for disabled
			'_print': _print
		})

	def export_cmd(self, ns, name, func):
		if ns not in self.exported_wrappers:
			self.exported_wrappers[ns] = {}
		export_name = ns+'.'+name
		self.exported_cmds[export_name] = func
		
		from .CommandList import wrap_gen
		w = wrap_gen(export_name)
		
		self.exported_wrappers[ns][name] = w
		return w

	def set_scheduler(self, scheduler):
		self.scheduler = scheduler
		self.scheduler.task_manager = self
		
	def schedule_task(self):
		if self.scheduler:
			self.scheduler.pick_task()
	
	def get_current_task(self):
		return self.current_task
		
	def get_tasks(self):
		return self.tasks
	
	def get_pending_tasks(self):
		return list(filter(lambda t: t.state.get() in (PENDING,DENIED), self.tasks))
	
	def has_task(self, name):
		task = self.get_task(name)
		return task != None
		
	def get_task(self,name):
		task = next((t for t in self.tasks if t.name == name), None)
		return task
		
	def get_exported_commands(self):
		if self.core_funcs_exported:
			return self.cached_exported_cmds
			
		t = type('',(),{})
		self._export_cmds_to_module(t)
		self.cached_exported_cmds = t
		import builtins
		builtins.__dict__['_e'] = t
		return t
	
	def _export_core_functions(self):
		if self.core_funcs_exported:
			return
		#  self.core_funcs_exported = True
		
		for e in _core.exported_cmds:
			for k,v in _core.exported_cmds[e].items():
				self.export_cmd(e, k, v)
				
	def _export_cmds_to_module(self, module):
		self._export_core_functions()
		
		for k,v in meta_chain_funcs.items():
			self.exported_wrappers[''][k] = v
			
		for e in _core.exported_cmds:
			if e == '':
				o = module
			else:
				o = type('',(),{})
				setattr(module, e, o)
			for k,v in self.exported_wrappers[e].items():
				setattr(o, k, v)
				
		for k,v in _core.sync_cmds.items(): setattr(module, k, v)
		for k,v in self.sync_funcs.items(): setattr(module, k, v)
	
	def fullstop(self):
		self.current_task = None
		
	def set_task_setup_func(self, func):
		self._task_setup_func = func
	
	def print_task_states(self):
		states={
			'pending': col.yellow + ' PENDING' + col.white,
			'done': col.green + 'DONE' + col.white,
			'suspended': col.red + 'SUSPENDED' + col.white,
			'denied': col.red + 'DENIED' + col.white
		}
		for task in _core.task_manager.get_tasks():
			print('task', task.name, states[task.state.get()])
	
	def setup_init_task(self):
		name='init'
		task = next((t for t in self.tasks if t.name == name), None)
		if not task:
			task = self.add_task_func(name, lambda: None)
		task.prepend_func = self._init_task
		
	def set_task(self, name):
		self.core_funcs_exported = True
		if not name:
			self.current_task = None
			return
		task = next((t for t in self.tasks if t.name == name), None)
		if task:
			print('running task', col.yellow, name, col.white)
			self.current_task = task
			
			def run_this():
				# run default func
				if self._task_setup_func:
					self._task_setup_func()
				ret=task.module.run()
				if ret == False:
					return False
				
			def on_task_done():
				print('task state:', self.current_task.state.get())
				self.current_task = None
				self.schedule_task()
				
			ret = self.current_task.run_task(run_this, on_task_done)
			if ret == False:
				self.current_task = None
			else:
				import builtins
				builtins.__dict__['_e'] = self.current_task.module
			return self.current_task
		else:
			raise 'task ' + name + ' doesnt exist'

	def load_tasks(self, robot_name, strategy_name):
		import os, sys, importlib
		strategy_folder_name = 'strategies'
		tasks_dir = 'robots/' + robot_name + '/' + strategy_folder_name + '/' + strategy_name
		sys.dont_write_bytecode = True
		print('loading strategy:', col.yellow, strategy_name, col.white)
		for i in os.listdir(tasks_dir):
			fullpathname = os.path.join(tasks_dir, i)
			if os.path.isfile(fullpathname):
				if fullpathname.endswith('.py'):
					task_name = i[:-3]
					task_path = fullpathname[:-3].replace('/','.')
					task_module = importlib.import_module(task_path)
					instances = task_module._instances if '_instances' in task_module.__dict__ else 1
					print(col.blue + 'loading task',col.yellow, task_name, col.white)
					for i in range(instances):
						task_module = importlib.import_module(task_path)
						self._export_cmds_to_module(task_module)
						self.add_task_func(task_name + ('#'+str(i) if instances > 1 else ''), task_module, i)
	
	def init_task(self, task_func):
		self._init_task = task_func
	set_init_task = init_task
	
	def add_task_func(self, name, task_func, instance=0):
		import types
		if type(task_func) != types.ModuleType:
			t=type('',(),{'run': task_func})
		else:
			t=task_func
			t.__dict__['_i'] = instance
		task = Task(name, t, instance)
		task.exported_cmds = self.exported_cmds
		self.tasks.append(task)
		return task
	
	def run_cycle(self):
		if self.current_task != None:
			self.current_task.run_cycle()
			# print('run_cycle: cur task', self.current_task)
			if self.current_task and self.current_task.state.get() == SUSPENDED:
				# print(col.red, 'cur is suspended', col.white)
				prev = self.current_task
				# try next pending task
				self.schedule_task()
				# unsuspend suspended task
				prev.state.set(PENDING)
				
				# if no pending task selected try again suspended task
				print(col.yellow,'trying again suspended task', col.white)
				if not self.current_task or self.current_task == prev:
					self.schedule_task()
