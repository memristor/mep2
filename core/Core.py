import signal
import importlib
import os, sys
import asyncio

import core.State

from .Sensors import *
from .Entities import *
from .Util import Singleton, Transform, rot_vec_deg, mul_pt_s
from .TaskManager import TaskManager
from .ServiceManager import ServiceManager
from .Introspection import Introspection


class Core(metaclass=Singleton):
	def __init__(self, robot_name=None):
		self.service_manager = ServiceManager()
		self.task_manager = TaskManager(self)
		self.entities = Entities(self)
		self.sensors = Sensors()
		self.sensors.core = self
		self.state = {'direction':1, 'state':'I'}
		self.modules = []
		self.transform = Transform(([0,0],0),([0,0],0))
		self.position = [0,0] # robot position
		self.angle = 0 # robot angle
		self.task_setup_func = None
		self.sync_cmds = {}
		core.State.core = self
		self.quit = False
		self.robot_size = [200,100]
		
		# unused
		self.default_listeners = []
		
		self.introspection = Introspection()
		self.introspection.core = self
		self.introspection.run()
		
		self._export_ns = ''
		if robot_name == None:
			raise Exception('must set robot name')
		self.robot=robot_name

		self.get_exported_commands = self.task_manager.get_exported_commands
		self.exported_cmds={'':{}}
		self.export_cmds()
	
	def set_position(self, x,y,o):
		self.position = [x,y]
		self.angle = o
		
	def look_vector(self):
		return rot_vec_deg([1,0], self.angle)
		
	def move_dir_vector(self):
		return mul_pt_s( rot_vec_deg([1,0], self.angle), self.state['direction'] )
	
	def add_sync_cmd(self, name, func):
		self.sync_cmds[name] = func
	
	def add_module(self, module):
		if module not in self.modules:
			module.core = self
			self.modules.append(module)
		
	def get_module_names(self):
		return [x.name for x in self.modules]
		
	def get_modules(self):
		return self.modules
		
	def load_strategy(self, strategy_name):
		self.task_manager.load_tasks(self.robot, strategy_name)
		
	def fullstop(self):
		for module in self.modules:
			if hasattr(module, 'fullstop'):
				module.fullstop()
		self.task_manager.fullstop()
		self.quit = True
	
	def export_cmd(self, cmd, func):
		if cmd in self.exported_cmds:
			raise 'command must be overriden'
		else:
			ns = self._export_ns
			if ns not in self.exported_cmds:
				self.exported_cmds[ns] = {}
			self.exported_cmds[ns][cmd] = func
			
	def export_ns(self, ns):
		self._export_ns = ns
			
	def sleep_cmd(self,s,future=None):
		def stop_waiting():
			#  print('done waiting')
			future.set_result(1)
		#  print('sleepcmd', s,future)
		self.loop.call_later(s, stop_waiting)
		
	def export_cmds(self):
		self.export_cmd('sleep', self.sleep_cmd)
		
	def get_position(self):
		pass	
	
	def override_cmd(self, cmd, func):
		ns = self._export_ns
		if ns not in self.exported_cmds:
			self.exported_cmds[ns] = {}
		self.exported_cmds[ns][cmd] = func
		
	def set_task_setup_func(self, func):
		self.task_setup_func = func
	
	def set_robot_size(self, x,y):
		self.robot_size = [x,y]
	
	def load_config(self):
		conf_dir = 'robots/' + self.robot
		sys.dont_write_bytecode = True
		for i in os.listdir(conf_dir):
			fullpathname = os.path.join(conf_dir, i)
			if os.path.isfile(fullpathname):
				if fullpathname.endswith('.py'):
					print(fullpathname, i)
				
					#  t = tasks_dir + '.' + i[:-3]
					print('loading config for robot: [\x1b[32m', self.robot, '\x1b[0m]')
					#  filename = i[:-3]
					config_module = importlib.import_module(fullpathname[:-3].replace('/','.'))
					
					#  print('loading task: ', filename)
					#  self.tasks.append(TaskContext(filename, task))
	
	async def main_loop(self):
		while not self.quit:
			await asyncio.sleep(0.005)
			#  print('tick')
			#  self.service_manager.emit('tick')
			self.task_manager.run_cycle()
	
	## runs main_loop
	def run(self):
		
		def on_interrupt(a,b):
			#  self.stop()
			# motion.stop
			exit(0)
		signal.signal(signal.SIGINT, on_interrupt)
		
		self.loop = asyncio.get_event_loop()
		
		# run all modules
		for i in self.modules:
			i.core = self
			if hasattr(i, 'run'):
				i.run()
			
		# run main loop
		self.loop.run_until_complete(self.main_loop())

def do(f):
	e=Core().get_exported_commands()
	def wrapper(*args, **kwargs):
		return e._do(f, e, *args, **kwargs)
	return wrapper
	
def func(f):
	e=Core().get_exported_commands()
	def wrapper(*args, **kwargs):
		return f(e, *args, **kwargs)
	return wrapper
	
