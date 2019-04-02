from contextlib import contextmanager
from .Debug import *

class CommandList:
	def __init__(self, commands=None):
		self.commands=[]
		self.labels=[]
		if commands:
			if callable(commands):
				with self.save(self):
					commands()
			elif isinstance(commands, CommandList):
				self += commands
			elif type(commands) is list:
				self.commands += commands
		
	def __add__(self, o):
		# add an offset to labels
		self.labels += [(l[0] + len(self.commands) if type(l[0]) is int else l[0], 
						l[1] + len(self.commands), l[2]) for l in o.labels]
		self.commands += o.commands
		
	def add_label(self, label_name):
		self.labels.append( (label_name, len(self.commands), None) )
		
	def add_block(self, block_range):
		self.labels.append( block_range )
	
	def add_cmd(self, cmd):
		self.commands.append(cmd)
		
	def clear(self):
		self.commands.clear()
		self.labels.clear()
		
	@staticmethod
	@contextmanager
	def save(cl):
		_save = CommandList.current
		CommandList.current = cl
		yield
		CommandList.current = _save
		
	@staticmethod
	def new():
		CommandList.current = CommandList()
		return CommandList.current
	@staticmethod
	def set(cmdlist): CommandList.current = cmdlist
	@staticmethod
	def get(): return CommandList.current
	@staticmethod
	def get_pos(): return len(CommandList.current)

# ----- meta cmds ------

CMD_DO = '_do'
CMD_IF = '_if'
CMD_ELIF = '_elif'
CMD_ELSE = '_else'
CMD_END_IF = '_end_if'
CMD_WHILE = '_while'
CMD_LABEL = '_label'
CMD_SYNC = '_sync'
CMD_SPAWN = '_spawn'
CMD_TASK_DONE = '_task_done'
CMD_TASK_STOP = '_task_stop'
CMD_TASK_SUSPEND = '_task_suspend'
CMD_RETURN = '_return'
CMD_ON = '_on'
CMD_LISTEN = '_listen'
CMD_UNLISTEN = '_unlisten'
CMD_WAIT = '_wait'
CMD_GOTO = '_goto'
CMD_REF = '_ref'
CMD_THIS = '_this'
CMD_WAKE = '_wake'
CMD_EMIT = '_emit'
CMD_WHILE = '_while'
CMD_PICK_BEST = '_pick_best'
CMD_WAKE = '_wake'
CMD_REDO = '_redo'
CMD_PARALLEL = '_parallel'
CMD_RESET_LABEL = '_reset_label'
class Command(CommandList):
	def __init__(s, name='', params={}, command_list=None):
		super().__init__(command_list)
		s.name=name
		s.params=params
		s.args = ()
		s.kwargs={}
		s.threads = []

	def print_command(s):
		with inc_tab():
			msg = tabs() + '=========='+\
				tabs() + 'Command ' + str(s.name) +\
				tabs() + 'commands: ' + str(s.commands) +\
				tabs() + '==========='+tabs()
		return msg
		
	def __repr__(s):
		return str(s.name)
def gen_cmd(name, *args, **kwargs):
	if type(name) is not tuple: name = ('', name)
	cmd = Command(name)
	cmd.kwargs = dict(kwargs)
	cmd.args = args
	cmd.params = kwargs
	
	# generate future and make <-> link
	from core.Future import Future
	future = Future()
	future.cmd = cmd
	cmd.future = future
	
	CommandList.get().add_cmd(cmd)
	return future
	
def gen_cmd_func(name, index, *args, **kwargs):
	import types
	g=gen_cmd(name, *args, **kwargs)
	if not args or type(args[0]) != types.FunctionType:
		def set_func(func): 
			g.cmd.args = list(g.cmd.args)
			g.cmd.args.insert(index, func)
		g.call = set_func
	return g

def put_cmd(cmd):
	CommandList.get().add_cmd(cmd)
	return cmd.future

def wrap_gen(name): return lambda *args, **kwargs: gen_cmd(name, *args, **kwargs)
def wrap_gen_func(name, index=0): return lambda *args, **kwargs: gen_cmd_func(name, index, *args, **kwargs)

def _label(label_name):
	CommandList.get().add_label(label_name)
	gen_cmd(CMD_LABEL, label_name)

####### IF #######
TAG_IF = '_if'
TAG_ELSE = '_else'
TAG_ELIF = '_elif'

class Block:
	def __init__(self):
		self.active = False
	def start(self):
		if not self.active:
			self.cl = CommandList.get()
		self.active = True
		return CommandList.new()
	def stop(self):
		self.active = False
		cmds = CommandList.get()
		CommandList.set(self.cl)
		return cmds
	def __enter__(self):
		pass
	def __exit__(self, *exc):
		self.stop()

class BlockParallel(Block):
	def __init__(self):
		super().__init__()
	
	def __exit__(self, *exc):
		cmds = self.stop()
		for i in cmds.commands:
			def f(a):
				put_cmd(a)
			c = gen_cmd(CMD_SPAWN, f, i)
		
	def _parallel(self):
		self.start()
		return self

class BlockPickBest(Block):
	def __init__(self):
		super().__init__()
	
	def __exit__(self, *exc):
		cmds = self.stop()
		fut = gen_cmd(CMD_PICK_BEST)
		fut.cmd += cmds
		
	def _pick_best(self):
		self.start()
		return self
		
class BlockIf(Block):
	def __init__(self):
		super().__init__()
		self.state = 0
		self.elifs = []
		self.cmd = None

	def _if(self, condition_func, _then=None, _else=None):
		if _then == _else == None:
			self.state = TAG_ELIF
			fut = gen_cmd(CMD_IF, _then=None, _else=None)
			self.cmd = fut.cmd
			self.cmd.params[TAG_ELIF] = [[condition_func,self.start()]]
		else:
			e = [[condition_func, _then]]
			gen_cmd(CMD_IF, _elif=e, _else=_else)
		return self
		
	def _elif(self, condition_func):
		assert self.cmd, 'no active if'
		# alloc
		self.cmd.params[TAG_ELIF] += [[condition_func,self.start()]]
		return self
	
	def _else(self):
		assert self.cmd, 'no active if'
		self.state = TAG_ELSE
		self.cmd.params[TAG_ELSE] = self.start()
		return self
	
	def _end_if(self):
		self.stop()
		self.state = 0
		self.cmd = None

@contextmanager
def gen_block(_enter,_exit):
	blk_start = CommandList.get_pos()
	yield
	CommandList.get().add_block((blk_start, CommandList.get_pos(), (_enter,_exit)))

# __while = BlockWhile()
_if = BlockIf()
_pb = BlockPickBest()
_parallel = BlockParallel()

meta_funcs = {
	CMD_LABEL: _label,
	'_L': _label,
	CMD_IF: _if._if,
	CMD_ELIF: _if._elif,
	CMD_ELSE: _if._else,
	CMD_END_IF: _if._end_if,
	
	CMD_PICK_BEST: _pb._pick_best,
	CMD_PARALLEL: _parallel._parallel
}

cmds=[CMD_RETURN, CMD_TASK_SUSPEND, CMD_TASK_DONE, CMD_GOTO, CMD_RESET_LABEL,
CMD_WAKE, CMD_UNLISTEN, CMD_EMIT, CMD_REF, CMD_THIS, CMD_WAKE, CMD_SYNC, CMD_REDO]
for i in cmds: meta_funcs[i] = wrap_gen(i)
cmds_func=[(CMD_DO, 0), (CMD_SPAWN,0), (CMD_LISTEN, 1), (CMD_ON, 1)]
for i,idx in cmds_func: meta_funcs[i] = wrap_gen_func(i,idx)
