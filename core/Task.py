from contextlib import contextmanager
from .Chain import *
from .Chain import _listen, _unlisten
from .Debug import *
from .Future import *
from .Util import Event

import asyncio


RUNNING = 'running'
WAITING = 'waiting'
SUSPENDED = 'suspended'
DONE = 'done'
PENDING = 'pending'
LEAVING = 'leaving'

runnable_id = 0

def _not(func):
    def not_func(*args, **kwargs):
        return not func(*args, **kwargs)
    return not_func
    
class Runnable:
	def __init__(s, cmd, commands=None, state=RUNNING, ip=0, name='some_runable'):
		# global runable ids
		global runnable_id
		s.name = name
		s.id = runnable_id
		runnable_id += 1
		
		# command name
		assert type(cmd) is Command, 'Runnable(cmd) => cmd must be type Command'
		s.cmd = cmd
		s.cmd.runnables.append(s)
		
		s.labels = s.cmd.labels
		# labels it passed and its timestamp
		s.passed_labels = []
		#  s.label_syncs = []
		s.listeners = []
		
		# support sync commands
		s.wake_on_done = []
		s.on_done = []
		s.future = None
		
		# optionally given function which generates commands
		if callable(commands):
			cmds=Chain()
			with save_cm(cmds):
				commands()
			s.commands = cmds.commands
			#  print('commands from func', s.commands)
		else:
			# can use given list or otherwise cmd commands
			s.commands = commands if commands != None else cmd.commands
		
		s.state = state
		
		# instruction pointer
		s.ip = ip
	
	def redo(s):
		#  print('cmd: ', s.get_current_command().name, s.cmd.state, s.cmd.name, id(s.cmd))
		#  print('\x1b[33mget current cmd:\x1b[0m', s.get_current_command().params)
		#  s.ip -= 1
		if not s.overflow():
			s.get_current_command().state = 0
			s.wake()
		
	def overflow(s):
		return s.ip >= len(s.commands)
		
	def remove_listeners(s):
		for i in s.listeners:
			i.stop() # stop listening
		s.listeners.clear()
	
	def get_current_command(s):
		return s.commands[s.ip]
		
	def run_on_done(s):
		print('runnable', s.id, 'is done')
		for i in s.wake_on_done:
			i.wake()
		for i in s.on_done:
			i()
		if s.future:
			#TODO: set result on _return or return future
			s.future.set_result(1)
			
		s.on_done.clear()
		s.wake_on_done.clear()
		
	def wake(s):
		if s.state == WAITING:
			s.state = RUNNING
	
	def wait_signal(s):
		s.state = WAITING
		
	def inc_ip(s):
		s.ip += 1
		
	def set_ip(s,ip):
		s.ip = ip
		
	def __repr__(s):
		global tl
		tl += 1
		msg = tabs() + '----'+\
			tabs() + 'Runnable'+\
			tabs() + 'ip: ' + str(s.ip)+\
			tabs() + 'state: ' + s.state+\
			tabs() + 'cmd: ' + str(s.cmd) +\
			tabs() + 'running: ' + str(s.commands) +\
			tabs() + '----\n'
		tl -= 1
		return msg

import core.State

@contextmanager
def disabler(name):
	_unlisten(name)
	yield
	_listen(name)
	
state_var = {}
def state(name, val=None):
	global state_var
	if val:
		state_var[name] = val
	elif name in state_var:
		return state_var[name]
	else:
		return False

sync_funcs = {
	'disabler': disabler,
	'state': state
}



class Task:
	exported_cmds = {}
	exported_wrappers = {'':{}}
	service_manager=None
	def __init__(s, name, module):
		# s.commands = commands
		
		# task context
		s.name = name
		s.state = PENDING
		s.module = module
		s.prepend_func = None
	
	def add_runnable(s,r):
		s.branches += [r]
		return r
		
	def run_task(s, task_func=None, on_task_done_cb=None):
		
		s.state = PENDING
		new_chain()
		
		if s.prepend_func:
			s.prepend_func()
			
		if task_func:
			task_func()
		else:
			s.module.run()
			
		cmd = Command(CMD_DO, command_chain=get_chain())
		for i in get_chain().labels:
			print('label', i)
		dbg('new',cmd)
		
		# [Command, ip]
		s.main_branch = Runnable(cmd)
		s.main_branch.name = 'main runable'
		s.branches = [] + [s.main_branch]
		
		s.on_task_done = Event()
		if on_task_done_cb:
			s.on_task_done += [on_task_done_cb]
		# [('lbl_name', time_it_happened), ...]
		#  s.labels = []
		s.passed_labels = []
		s.listeners = []
		s.label_syncs = []
		
	@staticmethod
	def export_cmd(ns, name, func):
		if ns not in Task.exported_wrappers:
			Task.exported_wrappers[ns] = {}
		export_name = ns+'.'+name
		Task.exported_cmds[export_name] = func
		w = wrap_gen(export_name,func)
		Task.exported_wrappers[ns][name] = w
		return w
		
	@staticmethod
	def export_meta_cmds():
		for k,v in meta_chain_funcs.items():
			Task.exported_wrappers[''][k] = v
	
	@staticmethod
	def get_sync_cmds():
		return sync_cmds
		
	def pause(self):
		pass
		#  self.main_branch.state = WAITING
	
	def resume(self):
		self.main_branch.state = RUNNING
	
	def suspend(s):
		s.stop_task(SUSPENDED)
		
	def stop_task(s, new_state=DONE):
		
		for i in s.listeners:
			try:
				core.State.disabled.remove(i.evt_name)
			except:
				pass
			i.stop()
		s.listeners.clear()
		
		
		def ch_state():
			print('task suspended')
			s.state = SUSPENDED
		
		def task_done():
			s.on_task_done()
			print('task ', new_state)
			
		f = s.on_task_done if new_state == DONE else ch_state
		
		if s.state == LEAVING:
			
			f()
		else:
			s.leave_task(f)
		
	def leave_task(self, after_leave=None):
		#  self.state = LEAVING
		if hasattr(self.module, 'leave'):
			self.run_task(self.module.leave, after_leave)
			self.state = LEAVING
		elif after_leave:
			after_leave()
	##### RUNABLES CYCLE ######
	def run_cycle(s):
		tag='run_cycle'
		dbg(tag,tag)
		
		if s.main_branch.state == DONE:
			return
			
		b = [] + s.branches
		c = 0
		num_active = 0
		for r in b:
			#  dbg(tag, c, ' in branch ', r)
			
			if r.ip >= len(r.commands):
				r.state = DONE
				#  print(r.ip, len(r.commands), 'fail done')
				r.run_on_done()
				dbg(tag, 'set state')
			
			if r.state == RUNNING or r.state == LEAVING:
				dbg(tag, '- run cmd')
				s.run_command(r)
			elif r.state == WAITING:
				dbg(tag, r.id, 'still waiting')
			
			# process state
			if r.state == RUNNING:
				num_active += 1
			elif r.state == DONE:
				s.branches.remove(r)
			
		if s.main_branch.state == DONE:
			s.stop_task()
				
			
		c+=1
		#  dbg('active', 'num active:', num_active, ' num braches:', len(s.branches), len(b), 'num waiting: ', 
			#  len(list(filter(lambda r: r.state == WAITING, s.branches))))
				
	### EXEC ###
	def run_command(s, r):
		tag='run_command'
		dbg(tag, r)
		cmd = r.get_current_command()
		dbg(tag, 'cmd: ', cmd)
		pos = cmd.params[POSITIONAL_ARGS]
		if cmd.name.startswith('_'):
			#do
			if cmd.name == CMD_DO:
				
				if cmd.state == 1:
					r.inc_ip()
					cmd.state = 0
				else:
					cmd.commands=[]
					#  set_chain(cmd.commands)
					new_chain()
					
					# exec to generate new commands
					#  print(cmd.args, cmd.kwargs)
					cmd.args[0](*cmd.args[1:], **cmd.kwargs)
					
					cmd.commands = get_chain().commands
					#TODO: copy labels too
					
					# if any commands generated in do func
					if cmd.commands:
						rn = s.add_runnable(Runnable(cmd))
						
						# sync
						r.wait_signal()
						rn.wake_on_done.append(r)
						cmd.state = 1
					else:
						r.inc_ip()

			elif cmd.name == CMD_SPAWN:
				
				cmd.commands=[]
				set_chain(cmd.commands)
				# exec to generate new commands
				pos[0]()
				if cmd.commands:
					rn = s.add_runnable(Runnable(cmd))
					cmd.future.set_runable(rn)
				# move on, while this runable executes in parallel
				r.inc_ip()
				
			#while		
			elif cmd.name == CMD_WHILE:
				# NOT IMPL yet
				pass
				
				
			#if
			elif cmd.name == CMD_IF:
				rn = None
				# if woken up
				if cmd.state == 1:
					r.inc_ip()
					cmd.state = 0
				else:
					done=False
					print('if', 'eval', cmd)
					# all conditions
					for i in cmd.params[TAG_ELIF]:
						dbg('if', cmd)
						
						# eval condition
						if(i[0]()):
							done = True
							#  print('cond true')
							#  print('branchs',len(s.branches))
							rn = s.add_runnable( Runnable(cmd, i[1]) )
							#  print('rnbl', rn)
							#  print('branchs',len(s.branches))
							
					if not done and TAG_ELSE in cmd.params:
						rn = s.add_runnable(Runnable(cmd, cmd.params[TAG_ELSE]))
					
					# enter sync waiting state
					if rn != None:
						r.wait_signal()
						rn.wake_on_done.append(r)
						cmd.state = 1
					else:
						r.inc_ip()
					
			elif cmd.name == CMD_LABEL:
				
				label_name = pos[0]
				
				if label_name not in r.passed_labels:
					r.passed_labels.append(label_name)
				if label_name not in s.passed_labels:
					s.passed_labels.append(label_name)
				
				print('on label', label_name)
				# wake all runables syncing on label
				cond=lambda tpl: tpl[1] == label_name and (tpl[0] == r or tpl[0] == None)
				for i in filter(cond, s.label_syncs):
					print('sync finished')
					i[2]()
				# ridiculus removal from list
				s.label_syncs = [i for i in filter(_not(cond), s.label_syncs)]
				print('cur ip', r.ip)
				r.inc_ip()
				print('after ip', r.ip)
			elif cmd.name == CMD_SYNC:
				if cmd.state == 1:
					r.inc_ip()
					if cmd.f:
						cmd.f.cancel()
					print('sync done')
					cmd.state = 0
				else:
					c = pos[0]
					
					waiting_forever = True
					if type(c) is Future:
						assert c.runable != None, 'sync future runable must not be None'
						if len(pos) == 1:
							def on_done():
								r.wake()
							if c.done():
								r.inc_ip()
								return
							else:
								c.set_on_done(on_done)
							waiting_forever = False
						else:
							label_name = pos[1]
							#  for i in c.runnables:
							
							if label_name in c.runable.passed_labels:
								r.inc_ip()
								return
								
							def on_label():
								r.wake()
								
							s.label_syncs.append((c.runable, label_name, on_label))
							#  l = Task.service_manager.listen_once('label', on_label, r, label_name)
							waiting_forever = False
							
					elif type(c) is str:
						label_name = c
						if label_name in s.passed_labels:
							r.inc_ip()
							return
							
						def on_label():
							r.wake()
							
						s.label_syncs.append((None, label_name, on_label))
						#  l = Task.service_manager.listen_once('label', on_label, None, label_name)
						waiting_forever = False
						print('waiting sync', label_name)
					if waiting_forever:
						raise 'waiting forever'
						
					cmd.state = 1
					cmd.f = None
					if '_timeout' in cmd.kwargs:
						def cancel_sync():
							r.wake()
						cmd.f = asyncio.get_event_loop().call_later(cmd.kwargs['_timeout'], cancel_sync)
					r.wait_signal()
			
			elif cmd.name in (CMD_ON, CMD_LISTEN):

				if cmd.args[1] == None and type(cmd.args[0]) is str:
					try:
						core.State.disabled.remove(cmd.args[0])
					except:
						pass
					r.inc_ip()
					return
					
				orig_func = cmd.args[1]
				listener_name = cmd.args[0] if '_name' not in cmd.kwargs else cmd.kwargs['_name']
				
				def wrapper(*args, **kwargs):
					if cmd.state == 1:
						#  print('bloked')
						return
					
					if listener_name in core.State.disabled:
						return
					
					cmd.commands=[]
					set_chain(cmd.commands)
					
					# exec to generate new commands
					orig_func(*args, **kwargs)
					# if any commands generated in do func
					if cmd.commands:
						rn = Runnable(cmd)
						if '_insync' in cmd.kwargs and cmd.kwargs['_insync']:
							def ch_state():
								cmd.state = 0
							rn.on_done.append(ch_state)
							cmd.state = 1
						s.add_runnable(rn)

					
				# override callback
				cmd.args = list(cmd.args)
				cmd.args[1] = wrapper
				
				
				if cmd.name == CMD_LISTEN:
					l = Task.service_manager.listen(*cmd.args, **cmd.kwargs)
					r.listeners.append(l)
				else:
					l = Task.service_manager.listen_once(*cmd.args, **cmd.kwargs)
				
				s.listeners.append(l)	
				cmd.listener = l
				# start listening
				#  l = (*cmd.args)
				r.inc_ip()
			elif cmd.name == CMD_UNLISTEN:
				if type(cmd.args[0]) is str:
					core.State.disabled.add(cmd.args[0])
				else:
					cmd.args[0].listener.stop()
				r.inc_ip()
			elif cmd.name == CMD_RETURN:
				
				print('runable cmd')
				r.state = DONE
				r.run_on_done()
				r.inc_ip()
				
			elif cmd.name == CMD_TASK_DONE:
				
				print('task done cmd')
				s.stop_task()
				
			elif cmd.name == CMD_TASK_SUSPEND:
				
				#  s.state = SUSPENDED
				print('task suspend cmd')
				if s.state != LEAVING:
					s.stop_task(SUSPENDED)
				else:
					print('cannot suspend when leaving')
				#  r.inc_ip()
				
			elif cmd.name == CMD_TASK_STOP:
				#  s.state = STOP
				print('task stop cmd')
			elif cmd.name == CMD_NEXT_CMD:
				s.main_branch.inc_ip()
				s.main_branch.wake()
				r.inc_ip()
				
			elif cmd.name == CMD_GOTO:
				print('on goto', cmd.args[0], r.ip)
				lab=next((l for l in r.labels if l[0] == cmd.args[0]), None)
				if lab:
					r.set_ip(lab[1])
		else:
			if cmd.state == 1: # command finished
				r.inc_ip()
				cmd.state = 0
				#print('finished\n')
			else: # command starting
				# exported cmds
				#print('should run: ', cmd.name, id(cmd))
				f = Future(r)
				kwargs = cmd.kwargs
				kwargs['future'] = f
				cmd.state = 1
				r.wait_signal()
				Task.exported_cmds[cmd.name](*cmd.args, **kwargs)
		
	
	def dump_info(s):
		dbg('active', ' num braches:', len(s.branches), 'num waiting: ', 
			len(list(filter(lambda r: r.state == WAITING, s.branches))))

