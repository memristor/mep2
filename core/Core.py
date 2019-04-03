import asyncio
from .Util import Transform, rot_vec_deg, mul_pt, col, pick, point_distance, sub_pt
import functools
class Core():
	debug=2
	def __init__(self, robot):
		self.robot=robot
		self.quit = False
		self.unique_cnt = 0
		import builtins
		
		# check if its already initialized anywhere
		builtin_core = '_core'
		if hasattr(builtins, builtin_core): return
		
		# core instance is available everywhere in whole python environment
		setattr(builtins, builtin_core, self)

		from .Sensors import Sensors
		from .Entities import Entities
		from .ServiceManager import ServiceManager
		from .Introspection import Introspection
		from .TaskManager import TaskManager
		
		self.service_manager = ServiceManager()
		self.sensors = Sensors()
		self.entities = Entities()
		self.task_manager = TaskManager()
		self.introspection = Introspection()
		
		import signal
		def on_interrupt(a,b): 
			self.introspection.close()
			self.emit('kill')
			exit(0)
		signal.signal(signal.SIGINT, on_interrupt)
		
		self.state = {'direction':1, 'state':'I'}
		self.modules = []
		self.transform = Transform(([0,0],0),([0,0],0))
		
		self.robot_size = [300,300]
		
		setattr(builtins, '_e', self.task_manager.exports)
		
		# forward funcs from task_manager for convenience
		self.set_task_setup_func = self.task_manager.set_task_setup_func
		self.task_setup_func = self.task_manager.set_task_setup_func
		self.set_init_task = self.task_manager.set_init_task
		self.init_task = self.task_manager.set_init_task
		self.has_task = self.task_manager.has_task
		self.set_task = self.task_manager.set_task
		self.export_cmd = self.task_manager.export_cmd
		# self.export_ns = self.task_manager.export_ns
		self.get_current_task = self.task_manager.get_current_task
		self.set_scheduler = self.task_manager.set_scheduler
		self.get_scheduler = self.task_manager.get_scheduler
		
		self.block = self.task_manager.block
		self.notify = self.task_manager.notify
		
		class ExportNS:
			def __call__(self, ns=None):
				if ns is None: return _core.task_manager.export_ns()
				self.old = _core.task_manager.export_ns()
				_core.task_manager.export_ns(ns)
				return self
			def __enter__(self): pass
			def __exit__(self, *args): _core.task_manager.export_ns(self.old)
		
		self.export_ns = ExportNS()
		
		self.emit = self.service_manager.emit
		self.listen_once = self.service_manager.listen_once
		self.export_cmds()
		
		from core.State import StateBase, State, _State
		self.position = StateBase(value=[0,0]) # robot position
		self.angle = StateBase(value=0) # robot angle
		setattr(builtins,'State', State)
		State.conf=type('config',(),{})()
		setattr(builtins,'_State', _State)
		import core.Task
		core.Task.StateBase = StateBase
	
	def listen(self, name, func=None):
		l=self.service_manager.listen
		return (lambda func: l(name, func)) if not func else l(name, func)
		
	def on(self, name, func=None):
		l=self.service_manager.listen_once
		return (lambda func: l(name, func)) if not func else l(name, func)
	
	def set_position(self, x,y,o):
		self.position.set([x,y])
		self.angle.set(o)
	
	def look_vector(self, s=1):
		return rot_vec_deg([s,0], self.get_position()[2])
		
	def vector_to(self, pt):
		return sub_pt( pt, self.get_position()[:2] )
		
	def distance_to(self, pt):
		return point_distance( self.get_position()[:2], pt )
	
	def move_dir_vector(self):
		return mul_pt( self.look_vector(), self.state['direction'] )
	
	def add_module(self, module):
		if not module: return
		if type(module) == list:
			for i in module:
				self.add_module(i)
			return
		if module not in self.modules:
			self.modules.append(module)
		else:
			raise Exception('module ', module.name, 'already exists')
		
	def get_module_names(self):
		return [x.name for x in self.modules]
		
	def get_modules(self):
		return self.modules
		
	def get_module(self, name):
		return next((mod for mod in self.modules if mod.name == name), None)
		
	def load_strategy(self, strategy_name):
		self.task_manager.load_tasks(self.robot, strategy_name)
	
	def fullstop(self):
		for module in self.modules:
			if hasattr(module, 'fullstop'):
				module.fullstop()
		self.task_manager.fullstop()
		self.emit('round:end')
		self.quit = True
		
	def expose_task_commands(self):
		import inspect
		frm = inspect.stack()[1]
		mod = inspect.getmodule(frm[0])
		print('called from:',mod.__name__)
		self.task_manager.expose_task_commands(mod)
	
	def unique_num(self):
		self.unique_cnt += 1
		return self.unique_cnt
		
	def export_cmds(self):
		
		@self.export_cmd('sleep')
		def sleep_cmd(s,_sim=False, _future=None):
			if _sim: return s
			# print('sleeping')
			c=self.loop.call_later(s, lambda: _future.set_result(1))
			_future.on_cancel.append(c.cancel)
		
		from contextlib import contextmanager
		
		@_core.export_cmd
		@_core.do
		def _next_cmd():
			_e._goto(1, ref='main')
		
		@_core.export_cmd
		@contextmanager
		def disabled(name):
			# with gen_block((lambda: _e._unlisten(name)), (lambda: _e._listen(name))):
			_e._unlisten(name)
			yield
			_e._listen(name)
		
		@_core.export_cmd
		@_core.do
		def print_threads():
			print( 'print_threads', _core.task_manager.get_current_task().main_branch.cmd.threads )
		
		@_core.export_cmd
		@contextmanager
		def _while(cond):
			l = '__local'+str(_core.uniq_num())
			l2 = l+'skip'
			_e._L(l)
			fut=_e._ref()
			def _els(): _e._goto(l2, ref=fut)
			_e._if(cond, _else=_els )
			yield
			_e._goto(l)
			_e._L(l2)
			
		@_core.export_cmd
		@_core.do
		def _print(*args):
			if not _e._sim: print(*args)
		
		@_core.export_cmd
		@_core.do
		def _emit(*args, **kwargs):
			_core.service_manager.emit(*args, **kwargs)
		
	def get_position(self):
		return self.position.get() + [self.angle.get()]
	
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
		self.emit('config:done')
		self.loop = asyncio.get_event_loop()
		self.introspection.run()
		# run all modules
		for i in self.modules: 
			if hasattr(i, 'run'): i.run()
		print('loaded modules:', '\n\t' + '\n\t'.join([col.yellow + x.name + col.white + ' : class ' + type(x).__name__ for x in self.get_modules()]))
		
	def start_strategy(self):
		self.task_manager.setup_init_task()
		self.task_manager.set_task('init')
	
	async def main_loop(self):
		while not self.quit:
			await asyncio.sleep(0.00005)
			# await asyncio.sleep(0)
			self.task_manager.run_cycle()
	
	## runs main_loop
	def run(self):
		self.loop = asyncio.get_event_loop()
		# run main loop
		self.loop.run_until_complete(self.main_loop())
	
	def spawn(self, *args, **kwargs):
		return self.task_manager.get_current_task().spawn(*args, **kwargs)
	
	########################## DECORATORS #########################
	def do(self, f=None, **kwargs2):
		if f:
			@functools.wraps(f)
			def wrapper(*args, **kwargs):
				return _e._do(f, *args, **kwargs)
			return wrapper
		else:
			def fn(f):
				@functools.wraps(f)
				def wrapper(*args, **kwargs):
					return _e._do(f, *args, **kwargs2, **kwargs)
				return wrapper
			return fn

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
			inst = args[0]
			if _future:
				# _future = s.block(inst.name, _future)
				# if not _future: return
				inst.future = _future
				# if class has on_cancel method, call it when cancelling future
				if hasattr(inst, 'on_cancel'):
					inst.future.set_on_cancel(inst.on_cancel)
				import time
				inst.future.time = time.monotonic()
			return f(*args, **kwargs)
		return wrapper
