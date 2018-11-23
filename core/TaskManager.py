
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
		self._export_ns=''
		
		self.exports = type('exports', (), {'_sim': False})()
		self.exported_commands = {}
		
		from core.schedulers.BasicScheduler import BasicScheduler
		self.set_scheduler(BasicScheduler())
		
		self.init_export()
		
	
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
	
	
	##### EXPORT #####
	def init_export(self):
		ns=''
		for k,w in meta_chain_funcs.items():
			setattr(self.exports, k, w)
	
	def export_ns(self, ns=None):
		if ns == None: return self._export_ns
		self._export_ns = ns
		
	def export_cmd(self, cmd, func=None):
		ns = self._export_ns
		if not func:
			if type(cmd) == str:
				def wrapper(f):
					self.export_cmd(cmd, f)
					return f
				return wrapper
			else:
				cmd,func=cmd.__name__,cmd
				
		co = func.__code__
		import inspect
		func_args = co.co_varnames[:co.co_argcount+co.co_kwonlyargcount] + tuple(inspect.signature(func).parameters.keys())
		
		is_async = '_future' in func_args
		if is_async:
			from .CommandList import wrap_gen
			ref = (ns,cmd)
			w = wrap_gen(ref)
			self.exported_commands[ref] = func
		else:
			w = func
		o = self.exports
		# export right away to exports
		if ns != '': 
			if hasattr(o, ns):
				o = getattr(o, ns) 
			else:
				no=type(ns, (), {})()
				setattr(o, ns, no)
				o=no
		setattr(o, cmd, w)
			
		return w
	######################
	
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
			task = self.add_task_func(name, lambda: self._init_task)
		
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
						if i > 0:
							del sys.modules[task_path]
							task_module = importlib.import_module(task_path)
						self.add_task_func(task_name + ('#'+str(i) if instances > 1 else ''), task_module, i)
	
	def init_task(self, task_func):
		self._init_task = task_func
	set_init_task = init_task
	
	def add_task_func(self, name, task_func, instance=0):
		import types
		if type(task_func) == types.FunctionType:
			t=type(name,(),{'run':task_func})
		else:
			d=task_func.__dict__
			d.update(self.exports.__dict__)
			d['_i'] = instance
			t=task_func
			
		task = Task(name, t, instance)
		task.exported_cmds = self.exported_commands
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
