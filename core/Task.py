from .Debug import *
from .Future import *
from .Util import Event, _not, pick, col
from .CommandList import *
import asyncio

RUNNING = 'running'
WAITING = 'waiting'
SUSPENDED = 'suspended'
DENIED = 'denied'
DONE = 'done'
PENDING = 'pending'
LEAVING = 'leaving'


class Runnable:
	num_instances = 0
	def __init__(s, cmd, commands=None, state=RUNNING, sim_time=0, ip=0, name='some_runable'):
		s.name = name
		s.id = Runnable.num_instances
		Runnable.num_instances += 1
		s.sim_time=sim_time
		s.sim_duration=0
		s.sim_func=0
		# command name
		assert type(cmd) == Command, 'Runnable(cmd) => cmd must be type Command'
		s.cmd = cmd
		s.cmd.runnables.append(s)
		
		s.labels = s.cmd.labels
		
		# labels it passed and its timestamp
		s.passed_labels = StateBase(value=[])
		#  s.label_syncs = []
		s.listeners = []
		
		# support sync commands
		s.wake_on_done = StateBase(value=[])
		s.on_done = StateBase(value=[])
		s.waiting_for = StateBase()
		s.future = None
		
		# optionally given function which generates commands
		if callable(commands):
			cmds=CommandList()
			result = None
			with save_command_list(cmds):
				commands()
			s.commands = cmds.commands
		else:
			# can use given list or otherwise cmd commands
			s.commands = commands if commands != None else cmd.commands
		
		s.state = StateBase(value=state)
		s.cmd_state = StateBase(value=0)
		
		# instruction pointer
		s.ip = StateBase(value=ip)
	
	def __lt__(s,v):
		return False
	
	def redo(s):
		if not s.overflow():
			s.cmd_state.set(0)
			s.wake()
	
	#TODO: rename function or something
	def overflow(s):
		return s.ip.get() >= len(s.commands)
		
	def remove_listeners(s):
		for el in s.listeners:
			el[1] = True
	
	def get_current_command(s):
		return s.commands[s.ip.get()]
		
	def run_on_done(s):
		for wake_on_done in s.wake_on_done.get():
			# print('WAKE')
			wake_on_done.wake(s)
		for on_done in s.on_done.get():
			# print('ON DONE')
			on_done()
		if s.future:
			#TODO: set result on _return or return future
			s.future.set_result(1)
		s.remove_listeners()
		s.on_done.clear()
		s.wake_on_done.clear()
		
	def wake(s, waker_runable=None):
		if s.state.get() == WAITING:
			if Task.is_sim:
				if waker_runable:
					s.sim_time = waker_runable.sim_time
				Task.sim_push_event(s)
			s.state.set(RUNNING)
			s.waiting_for.set(None)
	
	def wait_signal(s, waiting_for=None):
		s.waiting_for.set(waiting_for)
		s.state.set(WAITING)
		
	def inc_ip(s):
		s.ip.inc()
		
	def set_ip(s,ip):
		s.ip.set(ip)
		
	# def __repr__(s):
		# global tl
		# tl += 1
		# msg = tabs() + '----'+\
			# tabs() + 'Runnable'+\
			# tabs() + 'ip: ' + str(s.ip.get())+\
			# tabs() + 'state: ' + s.state.get()+\
			# tabs() + 'cmd: ' + str(s.cmd) +\
			# tabs() + 'running: ' + str(s.commands) +\
			# tabs() + '----\n'
		# tl -= 1
		# return msg
		
class ListenerRecord:
	def __init__(s, name, cmd=None):
		s.disabled=False
		s.cmd=cmd
		s.children=[]

class Task:
	is_sim=False
	def __init__(s, name, module, instance=0):
		s.meta_commands = None
		# task context
		s.instance=instance
		s.name = name
		s.state = StateBase(value=PENDING)
		s.module = module
		s.module._sim = False
	
	def add_runnable(s,r):
		s.branches.append(r)
		if s.is_sim:
			s.sim_push_event(r)
		return r
		
	def run_task(s, task_func=None, on_task_done_cb=None):
		new_command_list()
		ret = task_func() if task_func else s.module.run()
		
		if ret == False:
			return False
		
		s.state.set(PENDING)
		cmd = Command(CMD_DO, command_list=get_command_list())
		# [Command, ip]
		s.main_branch = Runnable(cmd, name='main_branch')
		# s.main_branch.labels = get_command_list().labels
		s.branches = StateBase(value=[s.main_branch])
		
		s.on_task_done = Event()
		if on_task_done_cb: s.on_task_done += [on_task_done_cb]
		s.passed_labels = StateBase(value=[])
		s.label_syncs = StateBase(value=[])
		
		s.evt_type = {}
		s.evt_names = {}
		return True
	
	#TODO: remove?
	def pause(self):
		pass
		#  self.main_branch.state = WAITING
	
	def resume(self):
		self.main_branch.state.set(RUNNING)
	
	def suspend(s):
		s.stop_task(SUSPENDED)
	
	def on_listener(s, record, *args, **kwargs):
		# print('listening: ', record, *args)
		parent = record.type_record
		if parent.disabled:
			return
		# TODO: implement common hook
		# print('before', record.children)
		s.handled=False
		for el in reversed(record.children):
			if el[1]:
				# print('rem ', el)
				record.children.remove(el)
				continue
			res=el[0](*args, **kwargs)
			if el[2]:
				record.children.remove(el)
				continue
			if s.handled or res:
				break
		
		if not record.children:
			parent.children.remove(record)
			del s.evt_names[record.name]
		# print('after', record.children)
	
	def stop_task(s, new_state=DONE):
		
		# clear event listeners
		for type_name,type_rec in s.evt_type.items():
			for c in type_rec.children:
				c.listener.stop()
			type_rec.children.clear()
		s.evt_type.clear()
		s.evt_names.clear()
		
		def ch_state():
			print(col.red,'suspended task', col.yellow + s.name + col.white)
			s.state.set(SUSPENDED)
		
		# print('stop task', s.state.get(), new_state)
		# new state:
		# 	DONE => on_task_done
		# 	-	   => suspended
		prev_on_task_done = s.on_task_done
		f = (lambda: (s.state.set(new_state), prev_on_task_done())) if new_state == DONE else ch_state
		# f = s.on_task_done if new_state == DONE else ch_state
		# current state:
		# 	LEAVING => do func now
		# 	- => delay func if "def leave():" present
		if s.state.get() == LEAVING or not hasattr(s.module, 'leave'):
			f()
		else:
			s.run_task(s.module.leave, f)
			s.state.set(LEAVING)
			
	##### RUNABLES CYCLE ######
	def run_runable(s,r):
		if r.ip.get() >= len(r.commands):
			r.state.set(DONE)
			r.run_on_done()
		
		#TODO: in => == RUNNING
		if r.state.get() in (RUNNING, LEAVING):
			s.run_command(r)
		
		if r.state.get() == DONE:
			s.branches.remove(r)
				
	def run_cycle(s):
		if s.main_branch.state.get() in (DONE,SUSPENDED):
			return
		_e._main = s.main_branch.future
		s.module._main = _e._main
		
		b = s.branches.get()
		for r in b: s.run_runable(r)
		
		if not s.is_sim and s.main_branch.state.get() == DONE:
			s.stop_task(DONE)

	@staticmethod
	def sim_push_event(r):
		import heapq
		# print('push evt', type(r), r.sim_time)
		heapq.heappush(Task.sim_heap, (r.sim_time, r))
	
	
	@contextmanager
	def simulator(s):
		import core.State as State
		State._last_sim += 1
		State._sim_mode = State._last_sim
		_e._sim = True
		s.module._sim = True
		Task.is_sim = True
		yield
		State._sim_mode = False
		_e._sim = False
		s.module._sim = False
		Task.is_sim = False
			
	def run_simulator(s, max_sim_time=0, max_cpu_clock=0):
		import time
		time_start=time.clock()
		with s.simulator():
			import heapq
			Task.sim_heap = sorted([(b.sim_time, b) for b in s.branches.get() if b.state.get() == RUNNING])
			while s.main_branch.state.get() != DONE:
				# print('sim heap:',len(s.sim_heap), [(i[0], i[1].name) for i in s.sim_heap])
				if not s.sim_heap:
					return float('inf')
				sim_time, r = heapq.heappop(s.sim_heap)
				if r.state.get() == WAITING:
					if r.sim_func:
						r.sim_duration = r.sim_func(r.sim_time, r.sim_duration)
						if r.sim_duration == 0:
							r.future.set_result(1)
						else:
							r.sim_time += r.sim_duration
							s.sim_push_event(r)
					else:
						r.future.set_result(1)
				else:
					s.run_runable(r)
		return s.main_branch.sim_time

	def do_meta_command(self, cmd, r):
		if not self.meta_commands:
			self.meta_commands = {CMD_DO: self.cmd_do,
			 CMD_GOTO: self.cmd_goto,
			 CMD_IF: self.cmd_if,
			 CMD_LABEL: self.cmd_label,
			 CMD_LISTEN: self.cmd_listen,
			 CMD_ON: self.cmd_listen,
			 CMD_NEXT_CMD: self.cmd_next_cmd,
			 CMD_RETURN: self.cmd_return,
			 CMD_SPAWN: self.cmd_spawn,
			 CMD_SYNC: self.cmd_sync,
			 CMD_TASK_DONE: self.cmd_task_done,
			 CMD_TASK_STOP: self.cmd_task_stop,
			 CMD_TASK_SUSPEND: self.cmd_task_suspend,
			 CMD_THIS: self.cmd_this,
			 CMD_UNLISTEN: self.cmd_unlisten,
			 CMD_WHILE: self.cmd_while}
		self.meta_commands[cmd.name[-1]](cmd, r)
		
	### EXEC ###
	def run_command(s, r):
		tag='run_command'
		cmd = r.get_current_command()
		# dbg(tag, 'cmd: ', cmd)
		# print(cmd.name)
		if cmd.name[-1].startswith('_'):
			s.do_meta_command(cmd,r)
			if s.is_sim and r.state.get() == RUNNING:
				s.sim_push_event(r)
		else:
			if r.cmd_state.get() == 1: # command finished
				r.inc_ip()
				r.cmd_state.set(0)
				if s.is_sim: s.sim_push_event(r)
			else: # command starting
				f = cmd.future
				f.runable = r
				r.future = f
				kwargs = cmd.kwargs
				kwargs['_future'] = f
				r.cmd_state.set(1)
				r.wait_signal()
				# func = s.exported_cmds[cmd.name]
				func = s.exported_cmds[cmd.name]
				# func_args = func.__code__.co_varnames
				# import inspect
				# func_args = list(inspect.signature(func).parameters.keys())
				co = func.__code__
				# func_args = co.co_varnames[:co.co_argcount+co.co_kwonlyargcount]
				import inspect
				func_args = co.co_varnames[:co.co_argcount+co.co_kwonlyargcount] + \
							tuple(inspect.signature(func).parameters.keys())
				sim_mode = '_sim' in func_args
				if sim_mode:
					kwargs['_sim'] = s.is_sim
				
				if s.is_sim:
					if sim_mode: 
						
						ret = func(*cmd.args, **kwargs)
					else:
						ret = 0
					r.sim_duration = 0
					if type(ret) == tuple:
						ret,func2 = ret
						r.sim_func = func2
						r.sim_duration = ret
					elif type(ret) in (int, float):
						r.sim_func = None
						r.sim_duration = ret
					# print('duration: ', r.sim_duration)
					r.sim_time += r.sim_duration
					r.future = f
					if s.is_sim and not f.done(): s.sim_push_event(r)
				else:
					ret = func(*cmd.args, **kwargs)
	
	def cmd_do(s, cmd, r):
		if r.cmd_state.get() == 1:
			r.inc_ip()
			r.cmd_state.set(0)
		else:
			new_command_list()
			
			# exec to generate new commands
			cmd.args[0](*cmd.args[1:], **cmd.kwargs)
			cmd.commands = get_command_list().commands
			#TODO: copy labels too
			cmd.labels = get_command_list().labels
			cmd.future.runable = r
			# if any commands generated in do func
			if cmd.commands:
				rn = s.add_runnable(Runnable(cmd, sim_time=r.sim_time))
				
				# sync
				r.wait_signal(rn)
				rn.wake_on_done.append(r)
				r.cmd_state.set(1)
			else:
				r.inc_ip()
				
	def cmd_spawn(s, cmd, r):
		new_command_list()
		# exec to generate new commands
		cmd.args[0]()
		cmd.commands = get_command_list().commands
		cmd.labels = get_command_list().labels
		rn = s.add_runnable(Runnable(cmd, sim_time=r.sim_time))
		cmd.future.set_runable(rn)
		# move on, while this runable executes in parallel
		r.inc_ip()
		
	def cmd_this(s, cmd, r):
		cmd.future.runable = r
		r.inc_ip()
		
	def cmd_while(s, cmd, r):
		pass
		
	def cmd_if(s,cmd,r):
		rn = None
		# if woken up
		if r.cmd_state.get() == 1:
			r.inc_ip()
			r.cmd_state.set(0)
		else:
			done=False
			# all conditions
			for i in cmd.params[TAG_ELIF]:
				dbg('if', cmd)
				
				# eval condition
				if(i[0]()):
					done = True
					rn = s.add_runnable( Runnable(cmd, i[1], sim_time=r.sim_time) )
					
			if not done and TAG_ELSE in cmd.params:
				rn = s.add_runnable(Runnable(cmd, cmd.params[TAG_ELSE]))
			
			# enter sync waiting state
			if rn != None:
				r.wait_signal()
				rn.wake_on_done.append(r)
				r.cmd_state.set(1)
			else:
				r.inc_ip()
				
	def cmd_label(s, cmd, r):
		label_name = cmd.args[0]
		if not any(l for l in s.passed_labels.get() if l[0] == label_name):
			s.passed_labels.append((label_name, r.sim_time))
		
		# wake all runables syncing on label
		cond=lambda tpl: tpl[1] == label_name and (tpl[0] in (r, None))
		for i in filter(cond, s.label_syncs.get()):
			print('sync finished')
			i[2](r)
		s.label_syncs.set(list(filter(_not(cond), s.label_syncs.get())))
		r.inc_ip()
		
	def cmd_sync(s, cmd, r):
		if r.cmd_state.get() == 1:
			r.inc_ip()
			if cmd.f:
				cmd.f.cancel()
			print('sync done')
			r.cmd_state.set(0)
		else:
			c = cmd.args[0] # future or label
			
			#TODO: remove?
			waiting_forever = True
			if type(c) is Future:
				assert c.runable != None, 'sync future == None'
				
				if len(cmd.args) == 1: # _sync(future)
					def on_done(): r.wake()
					if c.done():
						r.inc_ip()
						return
					else:
						c.set_on_done(on_done)
					waiting_forever = False
				else: # _sync(future, label)
					#TODO: should implement?
					label_name = cmd.args[1]
					if label_name in c.runable.passed_labels.get():
						r.inc_ip()
						return
						
					def on_label(r2):
						r.wake(r2)
						
					s.label_syncs.append((c.runable, label_name, on_label))
					waiting_forever = False
					
			elif type(c) is str: # _sync(label)
				label_name = c
				passed = next((l for l in s.passed_labels.get() if l[0] == label_name), False)
				if passed:
					r.inc_ip()
					return
					
				def on_label(r2): r.wake(r2)
				s.label_syncs.append((None, label_name, on_label))
				waiting_forever = False
				print('waiting sync', label_name)
				
			if waiting_forever:
				raise 'waiting forever'
				
			r.cmd_state.set(1)
			cmd.f = None
			r.wait_signal()

	def cmd_listen(s, cmd, r):
		event_name, callback = cmd.args
		if s.is_sim:
			r.inc_ip()
			return
		# if given only 1 argument, 2nd is None
		if callback == None and type(event_name) is str:
			if event_name in s.evt_type:
				s.evt_type[event_name].disabled = False
			r.inc_ip()
			return
			
		
		# TODO: filter _* kwargs
		listener_name = pick('_name', cmd.kwargs, event_name)
		order=pick('_order', cmd.kwargs, 'top')
		
		
		# TODO: process listener_name if needed
		# if listener_name.startswith('#'):
			
		
		# get type_record
		if event_name in s.evt_type:
			type_record=s.evt_type[event_name]
		else:
			type_record=ListenerRecord(event_name)
			s.evt_type[event_name] = type_record
		
		# get listener_record
		if listener_name in s.evt_names:
			listener_record = s.evt_names[listener_name]
		else:
			listener_record = ListenerRecord(listener_name)
			s.evt_names[listener_name] = listener_record
			# listener_rec -> type_rec
			listener_record.type_record = type_record
			# type_rec << listener_rec
			type_record.children.append(listener_record)
			cmd.args = list(cmd.args)
			cmd.args[1] = lambda *args, **kwargs: s.on_listener(listener_record, *args, **kwargs)
			l = _core.service_manager.listen(*cmd.args, **cmd.kwargs)
			listener_record.listener = l
		
		once = cmd.name[1] != CMD_LISTEN
		
		# TODO: take order into account
		el = [callback, False, once]
		if order == 'top':
			listener_record.children.append(el)
		else:
			listener_record.children.insert(0, el)
		
		# append to runable, use filter later to find and remove runable based hooks
		r.listeners.append(el)
		# s.listeners.append(l) # append to task
		r.inc_ip()

	def cmd_unlisten(s, cmd, r):
		if s.is_sim:
			r.inc_ip()
			return
		reference = cmd.args[0]
		if type(reference) is str:
			s.evt_type[reference].disabled = True
		elif type(reference) is Future:
			reference.cmd.listener.stop()
		r.inc_ip()
		
	def cmd_return(s, cmd, r):
		r.state.set(DONE)
		r.run_on_done()
		
	def cmd_task_done(s, cmd, r):
		s.stop_task()
	
	def cmd_task_suspend(s, cmd, r):
		if s.state != LEAVING:
			s.stop_task(SUSPENDED)
		else:
			print('cannot suspend when leaving')
	
	#TODO: remove?
	def cmd_task_stop(s, cmd, r):
		#  s.state.set(STOP)
		print('task stop cmd')
	
	#TODO: remove?
	def cmd_next_cmd(s, cmd, r):
		s.main_branch.inc_ip()
		s.main_branch.wake()
		r.inc_ip()
		
	def cmd_goto(s, cmd, r):
		if len(cmd.args) == 2:
			future,label=cmd.args
			r2=future.runable
		else:
			label = cmd.args[0]
			r2=r

		if r2.state.get() == DONE:
			r.inc_ip()
			return
		
		if not s.is_sim and r2.future and not r2.future.done():
			r2.future.cancel()
		
		lab=next((l for l in r2.labels if l[0] == label), None)
		
		if lab:
			r2.set_ip(lab[1])
			r2.cmd_state.set(0)
			r2.state.set(RUNNING)
			if not s.is_sim:
				r2.future = r2.get_current_command().future
		if r != r2: r.inc_ip()
	
	def dump_info(s):
		dbg('active', ' num braches:', len(s.branches), 'num waiting: ', len(list(filter(lambda r: r.state.get() == WAITING, s.branches))))

	
