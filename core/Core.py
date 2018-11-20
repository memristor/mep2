
import asyncio
from .Util import Transform, rot_vec_deg, mul_pt, col, pick
import functools
class Core():
	def __init__(self, robot):
		self.robot=robot
		self.quit = False
		
		import builtins
		# check if its already initialized anywhere
		builtin_core = '_core'
		if builtin_core in builtins.__dict__:
			return
		# core instance is available everywhere in whole python environment
		builtins.__dict__[builtin_core] = self
		# builtins.__dict__['Core'] = self

		from .Sensors import Sensors
		from .Entities import Entities
		from .ServiceManager import ServiceManager
		from .Introspection import Introspection
		from .TaskManager import TaskManager
		
		self.service_manager = ServiceManager()
		self.sensors = Sensors()
		self.entities = Entities()
		self.task_manager = TaskManager()
		
		self.state = {'direction':1, 'state':'I'}
		self.modules = []
		self.transform = Transform(([0,0],0),([0,0],0))
		
		self.sync_cmds = {}
		self.robot_size = [200,100]
		
		self.introspection = Introspection()
		self.introspection.run()
		
		self._export_ns = ''

		self.exported_cmds={'':{}}
		self.export_cmds()
		builtins.__dict__['_e'] = type('',(),{})
		
		# forward funcs from task_manager for convenience
		self.get_exported_commands = self.task_manager.get_exported_commands
		self.set_task_setup_func = self.task_manager.set_task_setup_func
		self.task_setup_func = self.task_manager.set_task_setup_func
		self.set_init_task = self.task_manager.set_init_task
		self.init_task = self.task_manager.set_init_task
		self.has_task = self.task_manager.has_task
		self.set_task = self.task_manager.set_task
		
		self.task_manager.init_sync_funcs()
		
		from core.State import StateBase, State, _State
		self.position = StateBase(value=[0,0]) # robot position
		self.angle = StateBase(value=0) # robot angle
		builtins.__dict__['State'] = State
		builtins.__dict__['_State'] = _State
		import core.Task
		core.Task.StateBase = StateBase
	
	def set_position(self, x,y,o):
		self.position.set([x,y])
		self.angle.set(o)
	
	def look_vector(self):
		return rot_vec_deg([1,0], self.get_position()[2])
	
	def move_dir_vector(self):
		return mul_pt( self.look_vector(), self.state['direction'] )
	
	def add_module(self, module):
		if type(module) == list:
			for i in module:
				self.add_module(i)
			return
		if module not in self.modules:
			self.modules.append(module)
		
	def get_module_names(self):
		return [x.name for x in self.modules]
		
	def get_modules(self):
		return self.modules
		
	def load_strategy(self, strategy_name):
		tm = self.task_manager
		tm.load_tasks(self.robot, strategy_name)
		tm.setup_init_task()
		tm.set_task('init')
		
	def fullstop(self):
		for module in self.modules:
			if hasattr(module, 'fullstop'):
				module.fullstop()
		self.task_manager.fullstop()
		self.quit = True
	
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
		func_args = co.co_varnames[:co.co_argcount+co.co_kwonlyargcount]
		if '_future' in func_args:
			if ns not in self.exported_cmds:
				self.exported_cmds[ns] = {}
			self.exported_cmds[ns][cmd] = func
		else:
			self.sync_cmds[cmd] = func
	
	def export_cmds(self):
		def sleep_cmd(s,_sim=False,_future=None):
			if _sim: return s
			self.loop.call_later(s, lambda: _future.set_result(1))
		self.export_cmd('sleep', sleep_cmd)
		
	def get_position(self):
		return self.position.get() + [self.angle.get()]
	
	def get_vector(self):
		pass
	
	def set_robot_size(self, x,y):
		self.robot_size = [x,y]
	
	def load_config(self):
		import os, sys, importlib
		conf_dir = 'robots/' + self.robot
		sys.dont_write_bytecode = True
		for i in os.listdir(conf_dir):
			fullpathname = os.path.join(conf_dir, i)
			if os.path.isfile(fullpathname):
				if fullpathname.endswith('config.py'):
					print('loading config for robot: ['+col.green, self.robot, col.white+']')
					config_filename = fullpathname[:-3].replace('/','.')
					config_module = importlib.import_module(config_filename)
					
		print('loaded modules:', '\n\t' + '\n\t'.join([col.yellow + x.name + col.white + ' : class ' + type(x).__name__ for x in self.get_modules()]))
	
	async def main_loop(self):
		while not self.quit:
			await asyncio.sleep(0.001)
			self.task_manager.run_cycle()
	
	## runs main_loop
	def run(self):
		def on_interrupt(a,b):
			exit(0)
		
		import signal
		signal.signal(signal.SIGINT, on_interrupt)
		
		self.loop = asyncio.get_event_loop()
		
		# run all modules
		for i in self.modules:
			i.core = self
			if hasattr(i, 'run'):
				# print('running',i.name)
				i.run()
		# run main loop
		self.loop.run_until_complete(self.main_loop())
	
	# decorators
	def do(self, f):
		self.get_exported_commands()
		@functools.wraps(f)
		def wrapper(*args, **kwargs):
			return _e._do(f, *args, **kwargs)
		return wrapper

	def asyn2(s,f):
		@functools.wraps(f)
		def wrapper(*args, _future=None, **kwargs):
			ret=f(*args, **kwargs)
			if _future: _future.set_result(ret)
			return ret
		return wrapper
		
	def module_cmd(s,f):
		@functools.wraps(f)
		def wrapper(*args, _future=None, **kwargs):
			# set future to class instance
			cls = args[0]
			cls.future = _future
			if cls.future:
				import time
				cls.future.time = time.monotonic()
			return f(*args, **kwargs)
		return wrapper
