from contextlib import contextmanager
from .Debug import *

class CommandList:
	def __init__(self):
		self.commands=[]
		self.labels=[]
		self.on_cancel=None
		
	def __add__(self, o):
		# add an offset to labels
		self.labels += [(l[0], l[1] + len(self.commands)) for l in o.labels]
		self.commands += o.commands

current_command_list = CommandList()

# ----- meta cmds ------

CMD_DO = '_do'
CMD_IF = '_if'
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
CMD_NEXT_CMD = '_next_cmd'
CMD_GOTO = '_goto'
CMD_THIS = '_this'

class Command:
	def __init__(s,name='',params={}, command_list=CommandList()):
		s.name=name
		s.params=params
		s.args = ()
		s.kwargs={}
		s.commands = CommandList().commands + command_list.commands
		s.labels = command_list.labels
		assert s.commands is not current_command_list.commands
		s.overrides=[]
		s.runnables = []
		
	def __repr__(s):
		global tl
		tl += 1
		msg = tabs() + '----'+\
			tabs() + 'Command ' + str(s.name) +\
			tabs() + 'params: ' + str(s.params.keys()) +\
			tabs() + 'commands: ' + str(s.commands) +\
			tabs() + '----\n'
		tl -= 1
		return msg

@contextmanager
def save_command_list(r):
	global current_command_list
	save = current_command_list
	current_command_list = CommandList()
	yield
	r += current_command_list
	current_command_list = save

def new_command_list():
	global current_command_list
	current_command_list = CommandList()
	
def set_command_list(c):
	global current_command_list
	current_command_list = c

def get_command_list():
	global current_command_list
	return current_command_list

from core.Future import Future
def gen_cmd(name, *args, **kwargs):
	global current_command_list
	if type(name) is not tuple:
		name = ('', name)
	cmd = Command(name)

	cmd.kwargs = dict(kwargs)
	cmd.args = args
	cmd.params = kwargs
	
	# generate future and make <-> link
	future = Future()
	future.cmd = cmd
	cmd.future = future
	
	current_command_list.commands.append(cmd)
	return cmd.future

def _this():
	return gen_cmd(CMD_THIS)

def _task_suspend():
	gen_cmd(CMD_TASK_SUSPEND)

#TODO: remove?
def _return():
	gen_cmd(CMD_RETURN)

def _do(func, *args, **kwargs):
	return gen_cmd(CMD_DO, func, *args, **kwargs)

def _spawn(func, *args, **kwargs):
	return gen_cmd(CMD_SPAWN, func, *args, **kwargs)

def _label(label_name):
	current_command_list.labels.append( (label_name, len(current_command_list.commands)) )
	gen_cmd(CMD_LABEL, label_name)
	
def _sync(*args,**kwargs):
	if type(args[0]) is Future or type(args[0]) == str:
		gen_cmd(CMD_SYNC, *args, **kwargs)
	else:
		raise('bad params')
	
def _on(event, callb, **kwargs):
	gen_cmd(CMD_ON, event, callb, **kwargs)
	
def _listen(event, callb=None, **kwargs):
	c = gen_cmd(CMD_LISTEN, event, callb, **kwargs)
	c.listener = None
	return c
	
def _task_done():
	gen_cmd(CMD_TASK_DONE)

def _unlisten(handle):
	gen_cmd(CMD_UNLISTEN, handle)
	
def _next_cmd():
	gen_cmd(CMD_NEXT_CMD)
	
def _goto(*args):
	gen_cmd(CMD_GOTO, *args)

####### IF #######
IF_NONE = 0
IF_ELIF = 1
IF_ELSE = 2
a_if = IF_NONE
a_start_idx = 0

TAG_IF = '_if'
TAG_ELSE = '_else'
TAG_ELIF = '_elif'

def wrap_gen(name):
	def wrapper(*args, **kwargs):
		return gen_cmd(name, *args, **kwargs)
	return wrapper

def _if(condition_func, _then=None, _else=None):
	global a_if, a_start_idx, current_command_list
	if _then == None and _else == None:
		a_if = IF_ELIF
		a_start_idx = len(current_command_list.commands)
		fut = gen_cmd(CMD_IF, _then=None, _else=None)
		fut.cmd.params[TAG_ELIF] = [[condition_func,None]]
		#  print('if cmd', current_command_list.commands[a_start_idx])
	else:
		#  print('genif')
		e = [[condition_func, _then]]
		#  print(e)
		gen_cmd(CMD_IF, _elif=e, _else=_else)
	
# not tested
def _elif(condition_func):
	global a_if, a_start_idx, current_command_list
	assert a_if == IF_IF, 'no active if'
	# if a_if != IF_IF:

	cmd = current_command_list.commands[a_start_idx-1]
	
	# past condition
	# pop if
	elsif = current_command_list.commands[a_start_idx:]
	del current_command_list.commands[a_start_idx:]
	cmd.params[TAG_ELIF][-1][1] = elsif
	
	# alloc new condition
	cmd.params[TAG_ELIF] += [[condition_func,]]

# not tested
def _else():
	global a_if, a_start_idx, current_command_list
	assert a_if == IF_IF, 'no active if'
	a_if = IF_ELSE

# not tested
def _end_if():
	global a_if, a_start_idx, current_command_list
	assert a_if == IF_ELIF and a_if != IF_ELSE, 'no active if'
	
	cmd = current_command_list.commands[a_start_idx]
	if a_if == IF_ELSE:
		els = current_command_list.commands[a_start_idx:]
		del current_command_list.commands[a_start_idx:]
		cmd.commands += els
	else:
		# pop if
		elsif = current_command_list.commands[a_start_idx+1:]
		del current_command_list.commands[a_start_idx+1:]
		#  print(cmd, cmd.params)
		cmd.params[TAG_ELIF][-1][1] = elsif
	a_if = IF_NONE

# task calls these functions
meta_chain_funcs = {
	CMD_IF: _if,
	CMD_ELSE: _else,
	CMD_END_IF: _end_if,
	CMD_DO: _do,
	CMD_SPAWN: _spawn,
	CMD_LABEL: _label,
	'_L': _label,
	CMD_SYNC: _sync,
	CMD_ON: _on,
	CMD_LISTEN: _listen,
	CMD_UNLISTEN: _unlisten,
	CMD_TASK_SUSPEND: _task_suspend,
	CMD_RETURN: _return,
	CMD_NEXT_CMD: _next_cmd,
	CMD_GOTO: _goto,
	CMD_TASK_DONE: _task_done,
	CMD_THIS: _this
}
