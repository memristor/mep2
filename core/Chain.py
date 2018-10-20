from contextlib import contextmanager
from .Debug import *
# maybe no need for chain class but just a list of commands

class Chain:
	def __init__(self):
		self.commands=[]
		self.labels=[]
		self.on_cancel=None
		
	def __add__(self, o):
		# add an offset to labels
		self.labels += [(l[0], l[1] + len(self.commands)) for l in o.labels]
		self.commands += o.commands
current_chain = Chain()
POSITIONAL_ARGS = '*pos*'

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

class Command:
	def __init__(s,name='',params={}, command_chain=Chain()):
		s.name=name
		s.params=params
		s.args = ()
		s.kwargs={}
		s.commands = Chain().commands + command_chain.commands
		s.labels = command_chain.labels
		assert s.commands is not current_chain.commands
		s.overrides=[]
		s.state = 0
		s.runnables = []
		# s.cond_func=None
		# s.func=None
	def __repr__(s):
		global tl
		tl += 1
		msg = tabs() + '----'+\
			tabs() + 'Command ' + s.name +\
			tabs() + 'params: ' + str(s.params.keys()) +\
			tabs() + 'commands: ' + str(s.commands) +\
			tabs() + '----\n'
		tl -= 1
		return msg

@contextmanager
def save_cm(r):
	global current_chain
	save = current_chain
	current_chain = Chain()
	yield
	r += current_chain
	current_chain = save

# robot imported commands
# {'cmd_name':(func, meta), ...}
# {'move': (func, {'module_trace':}}
chain_funcs = {}

def new_chain():
	global current_chain
	current_chain = Chain()
	
def set_chain(c):
	global current_chain
	current_chain = Chain()
	current_chain.commands = c

def get_chain():
	global current_chain
	return current_chain


#  f=open('output.py','w')
#  from .Util import Transform
#  transform = Transform(([80,-350],0), ([1260,-350],180))

from core.Future import Future
def gen_cmd(name, *args, **kwargs):
	global current_chain
	cmd = Command(name)
	cmd.args = args
	#  print('gen_cmd', cmd.name, cmd.args)
	
	#  if cmd.name == 'r.goto':
		#  cmd.args = list(cmd.args)
		#  pos = transform.transform(cmd.args[:3])
		#  if len(cmd.args) > 2:
			#  pos.append(cmd.args[2])
		#  f.write(cmd.name +'('+ ', '.join(str(int(p)) for p in pos) + ')\n')
	#  if cmd.name == 'r.setpos':
		#  f.write(cmd.name + '\n')
	
	cmd.kwargs = dict(kwargs)
	kwargs[POSITIONAL_ARGS] = args
	cmd.params = kwargs
	cmd.future = Future()
	cmd.future.cmd = cmd
	current_chain.commands.append(cmd)
	return cmd.future

def _task_suspend():
	gen_cmd(CMD_TASK_SUSPEND)
	
def _return():
	gen_cmd(CMD_RETURN)

def _do(func, *args, **kwargs):
	return gen_cmd(CMD_DO, func, *args, **kwargs)

def _spawn(func, *args, **kwargs):
	return gen_cmd(CMD_SPAWN, func, *args, **kwargs)

def _label(label_name):
	current_chain.labels.append( (label_name, len(current_chain.commands)) )
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
	
def _goto(label_name):
	gen_cmd(CMD_GOTO, label_name)

####### IF #######
IF_NONE = 0
IF_ELIF = 1
IF_ELSE = 2
a_if = IF_NONE
a_start_idx = 0


TAG_IF = '_if'
TAG_ELSE = '_else'
TAG_ELIF = '_elif'

# modules use this to export funcs
def add_command(cmd_name, func_cb):
	chain_funcs[cmd_name] = ({},func_cb)

def wrap_gen(name, func):
	def wrapper(*args, **kwargs):
		gen_cmd(name, *args, **kwargs)
	return wrapper
	
def wrap_funcs(funcs):
	wrapped = {}
	for i in funcs:
		wrapped[i] = wrap_gen(i, funcs[i])
	return wrapped

def _if(condition_func, _then=None, _else=None):
	global a_if, a_start_idx, current_chain
	if _then == None and _else == None:
		a_if = IF_ELIF
		a_start_idx = len(current_chain.commands)
		fut = gen_cmd(CMD_IF, _then=None, _else=None)
		fut.cmd.params[TAG_ELIF] = [[condition_func,None]]
		#  print('if cmd', current_chain.commands[a_start_idx])
	else:
		#  print('genif')
		e = [[condition_func, _then]]
		#  print(e)
		gen_cmd(CMD_IF, _elif=e, _else=_else)
	
# not tested
def _elif(condition_func):
	global a_if, a_start_idx, current_chain
	assert a_if == IF_IF, 'no active if'
	# if a_if != IF_IF:

	cmd = current_chain.commands[a_start_idx-1]
	
	# past condition
	# pop if
	elsif = current_chain.commands[a_start_idx:]
	del current_chain.commands[a_start_idx:]
	cmd.params[TAG_ELIF][-1][1] = elsif
	
	# alloc new condition
	cmd.params[TAG_ELIF] += [[condition_func,]]

# not tested
def _else():
	global a_if, a_start_idx, current_chain
	assert a_if == IF_IF, 'no active if'
	a_if = IF_ELSE

# not tested
def _end_if():
	global a_if, a_start_idx, current_chain
	assert a_if == IF_ELIF and a_if != IF_ELSE, 'no active if'
	
	
	cmd = current_chain.commands[a_start_idx]
	if a_if == IF_ELSE:
		els = current_chain.commands[a_start_idx:]
		del current_chain.commands[a_start_idx:]
		cmd.commands += els
	else:
		# pop if
		elsif = current_chain.commands[a_start_idx+1:]
		del current_chain.commands[a_start_idx+1:]
		#  print(cmd, cmd.params)
		cmd.params[TAG_ELIF][-1][1] = elsif
	a_if = IF_NONE
	
########## /IF ##########


# task calls these functions
meta_chain_funcs = {
	CMD_IF: _if,
	CMD_ELSE: _else,
	CMD_END_IF: _end_if,
	CMD_DO: _do,
	CMD_SPAWN: _spawn,
	CMD_LABEL: _label,
	CMD_SYNC: _sync,
	CMD_ON: _on,
	CMD_LISTEN: _listen,
	CMD_UNLISTEN: _unlisten,
	CMD_TASK_SUSPEND: _task_suspend,
	CMD_RETURN: _return,
	CMD_NEXT_CMD: _next_cmd,
	CMD_GOTO: _goto,
	CMD_TASK_DONE: _task_done
}
