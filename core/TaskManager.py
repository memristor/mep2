import asyncio
from core.Task import *

class TaskManager:
	def __init__(self):
		self.current_task = None
		self.tasks = []
		
		self.scheduler=None
		self._init_task = None
		self.cached_exported_cmds = None
		self._export_ns=''
		self._next_task = None
		self.scheduling = None
		
		self.exports = type('exports', (), {'_sim': False})()
		self.exported_commands = {}
		
		from core.schedulers.BasicScheduler import BasicScheduler
		self.set_scheduler(BasicScheduler())
		self.init_export()
		
	def set_scheduler(self, scheduler):
		self.scheduler = scheduler
		
	def schedule_task(self):
		print(col.yellow,'scheduling next task',col.white)
		if self.scheduling: self.scheduling.cancel()
		if self._next_task:
			next_task = self._next_task
			self._next_task = None
			if self.get_task(next_task).state.val != DONE:
				if self.set_task(next_task) != False: return
		_core.task_manager.print_task_states()
		# if self.scheduler and self.get_pending_tasks():
		if self.scheduler:
			r=self.scheduler.pick_task(_core.task_manager.get_ready_tasks())
			if type(r) is str: r=self.set_task(r)
			if not r and self.get_pending_tasks():
				print('failed to pick task')
				self.scheduling = _core.loop.call_later(0.5, self.schedule_task)
			
		if not self.get_pending_tasks():
			_core.emit('strategy:done')
	
	def get_current_task(self):
		return self.current_task
		
	def get_tasks(self):
		return self.tasks
	
	def get_ready_tasks(self):
		return list(filter(lambda t: t.state.get() in (PENDING,DENIED), self.tasks))
		
	def get_pending_tasks(self):
		return list(filter(lambda t: t.state.get() in (PENDING,DENIED,SUSPENDED), self.tasks))
	
	def has_task(self, name):
		task = self.get_task(name)
		return task != None
		
	def get_task(self, name):
		task = next((t for t in self.tasks if t.name == name), None)
		return task
	
	def notify(self, queue_id):
		self.get_current_task().notify(queue_id)
		
	def block(self, queue_id, future):
		return self.get_current_task().block(queue_id, future)
	
	##### EXPORT #####
	def init_export(self):
		ns=''
		for k,w in meta_funcs.items():
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
		from .Util import get_func_args
		func_args = get_func_args(func)
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
		
	def print_task_states(self):
		states={
			'pending': col.yellow + ' PENDING' + col.white,
			'done': col.green + 'DONE' + col.white,
			'suspended': col.red + 'SUSPENDED' + col.white,
			'disabled': col.red + 'DISABLED' + col.white,
			'denied': col.red + 'DENIED' + col.white
		}
		for task in _core.task_manager.get_tasks():
			print('task', task.name, states[task.state.get()])
	
	def setup_init_task(self):
		task = next((t for t in self.tasks if t.name == 'init'), None)
		if not task:
			def run_this(): pass
			self.add_task_func('init', run_this)

	def set_next_task(self, name):
		self._next_task = name

	def set_task(self, name):
		if not name:
			self.current_task = None
			return
		task = next((t for t in self.tasks if t.name == name), None)
		if task:
			if task.state.get() == DONE:
				self.current_task = None
				return False
			print('running task', col.yellow, name, col.white)
			self.current_task = task
			
			def run_this():
				# run default func
				_core.emit('task:new', task.name)
				if task.module.run() is False: return False
			
			def on_task_done():
				if Task.is_sim: return
				state = self.current_task.state.get()
				print('task state:', self.current_task.name, state)
				if self.current_task:
					prev = self.current_task
					self.current_task = None
					if state == DONE:
						self.schedule_task()
					elif state == SUSPENDED:
						print(col.red,'suspended task', col.yellow + prev.name + col.white)
						# print(col.red, 'cur is suspended', col.white)
						# try next pending task
						self.schedule_task()
						# unsuspend suspended task
						prev.state.set(PENDING)
						# if no pending task selected try again suspended task
						# print(col.yellow,'trying again suspended task', col.white)
						if not self.current_task or self.current_task == prev:
							self.schedule_task()
			ret = self.current_task.run_task(run_this, on_task_done)
			if ret == False:
				self.current_task = None
			return self.current_task
		else:
			return False

	def load_tasks(self, robot_name, strategy_name):
		import os, sys, importlib
		strategy_folder_name = 'strategies'
		tasks_dir = 'robots/' + robot_name + '/' + strategy_folder_name + '/' + strategy_name
		sys.dont_write_bytecode = True
		import core.State as st
		print('loading strategy:', col.yellow, strategy_name, col.white)
		for i in os.listdir(tasks_dir):
			fullpathname = os.path.join(tasks_dir, i)
			if os.path.isfile(fullpathname):
				if fullpathname.endswith('.py'):
					task_name = i[:-3]
					task_path = fullpathname[:-3].replace('/','.')
					st.inst_leader = []
					st.inst = st.inst_leader
					task_module = importlib.import_module(task_path)
					instances = task_module._instances if '_instances' in task_module.__dict__ else 1
					print(col.blue + 'loading task',col.yellow, task_name, col.white)
					for i in range(instances):
						if i > 0:
							st.inst = []
							del sys.modules[task_path]
							task_module = importlib.import_module(task_path)
						self.add_task_func(task_name + ('#'+str(i) if instances > 1 else ''), task_module, i)
	
	
	def set_task_setup_func(self, func):
		_core.listen('task:new', lambda task: func() if task != 'init' else None)
		
	def init_task(self, task_func):
		_core.listen('task:new', lambda task: task_func() if task == 'init' else None)
	set_init_task = init_task
	
	def expose_task_commands(self, o):
		o.__dict__.update(self.exports.__dict__)
	
	def add_task_func(self, name, task_func, instance=0):
		import types
		if type(task_func) == types.FunctionType:
			t=type(name,(),{'run':task_func})
			d={}
		else:
			self.expose_task_commands(task_func)
			d=task_func.__dict__
			d['_i'] = instance
			t=task_func
		
		task = Task(name, t, instance)
		if '_disabled' in d and d['_disabled'] == True:
			task.state.set(DISABLED)
		else:
			task.state.set(PENDING)
			
		task.exported_cmds = self.exported_commands
		self.tasks.append(task)
		return task
	
	def run_cycle(self):
		if self.current_task:
			self.current_task.run_cycle()
			# print('run_cycle: cur task', self.current_task)
			
