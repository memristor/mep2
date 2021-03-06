from .Debug import *
from core.Constants import *
from .Future import Future
from .Util import _not, pick, col
from .CommandList import *
import traceback

class Thread(CommandList):
	num_instances = 0
	def __init__(s, cmd: Command, commands=None, state=RUNNING, sim_time=0, ip=0, name=None):
		assert type(cmd) == Command, 'Thread(cmd) => cmd must be type Command'
		super().__init__(commands if commands is not None else cmd)
		
		# identification
		Thread.num_instances += 1 # counting how much threads were created
		s.id = Thread.num_instances # for distinguishing
		s.name = 'thread'+str(s.id) if not name else name
		
		# simulation
		s.sim_time=StateBase(sim_time)
		s.sim_duration=StateBase(0)
		s.sim_func=StateBase(None)
		
		# linkage
		s.parent=StateBase(None)
		s.cmd = cmd # command it started thread
		s.cmd.threads.append(s)
		
		# labels it passed and its time
		s.passed_labels = StateBase([])
		s.listeners = [] # we said we don't use listeners in sim mode, maybe later
		
		s.on_done = StateBase([])
		
		# exec states
		# s.sync_flag = 0
		s.sync_flag = StateBase(0)
		s.state = StateBase(state)
		s.cmd_state = StateBase(0)
		s.ip = StateBase(ip)
	
	# for heap sort, just prevent crash
	def __lt__(s,v): return False
	
	def get_active_threads(s):
		return [i for i in s.cmd.threads if i.state.val != DONE]
	
	@property
	def future(s):
		ip=s.ip.get()
		return s.commands[ip].future if ip < len(s.commands) else None
	
	def top(s):
		a=s
		while a.cmd.name[-1] != CMD_SPAWN:
			a=a.parent.get()
		return a
	
	def redo(s):
		s.cmd_state.set(0)
		# print('redo')
		s.wake()
	
	def overflow(s):
		return s.ip.get() >= len(s.commands)
	
	def get_current_command(s):
		return s.commands[s.ip.val]
	
	def run_on_done(s):
		if _core.debug >= 2: print('runa done:',s.name)
		
		s.cancel()
		for done_func in s.on_done.val:
			# debug
			done_func()
		
		if s.parent.val:
			# print('run_on_done, parent', s.name, s.cmd.get_name())
			if s.cmd.get_name() in (CMD_DO, CMD_IF):
				# debug
				s.parent.val.wake(SYNC_DO)
			
			if s in s.parent.val.cmd.threads:
				s.parent.val.cmd.threads.remove(s)
		# _core.emit('thread:done', s.name)
		# remove/disable listeners
		for el in s.listeners: el.ref_count = 0
		
		# threads went out of scope
		for th in s.cmd.threads:
			if th != s: th.kill()
		
		s.on_done.clear()
	
	
	
	def set_future(s, f):
		f.thread = s
		s.future = f
	
	def kill(s):
		if s.state.get() != DONE:
			s.run_on_done()
			s.state.set(DONE)

	'''
	SYNC_UNCOND = 1 # pause/continue
	SYNC_DO = 2 # none
	SYNC_FUTURE = 4 # none
	SYNC_THREAD = 8 # will pause/continue
	SYNC_EVENT = 16 # will pause and continue
	SYNC_FORCE = 32 # no pause, no cancel just block/unblock thread
	'''
	
	def wake(s, sync_flag, waker_thread=None):
		if (s.sync_flag.val & sync_flag) == 0: return
		# print('wake', s.name, 'sync_flag', sync_flag)
		sflag = s.sync_flag.val = s.sync_flag.val & ~sync_flag
		if sflag == 0:
			if Task.is_sim:
				if waker_thread: s.sim_time.val = waker_thread.sim_time.val
				Task.sim_push_event(s)
			s.state.set(RUNNING)
			if s.overflow(): s.state.set(DONE)
		elif sflag == SYNC_DO:
			# recursively go down and pause every do
			a = s.future.thread
			a.wake(sync_flag, waker_thread)
			
		if sflag == SYNC_FUTURE:
			s.resume()
			
	def sync(s, sync_flag, t=None):
		if s.sync_flag.val & sync_flag == sync_flag: return
		# print('sync', s.name, sync_flag)
		sflag = s.sync_flag.val
		
		if sync_flag == SYNC_FUTURE:
			t.set_thread(s)
		if sync_flag == SYNC_DO:
			t.parent.val = s
		if sync_flag == SYNC_THREAD:
			# add thread to list
			pass
		if sync_flag == SYNC_EVENT:
			pass
		if sync_flag == SYNC_UNCOND:
			# pausing
			if not (sflag & SYNC_UNCOND):
				
				if sflag & (SYNC_THREAD | SYNC_EVENT):
					# do nothing
					pass

				elif (sflag & (SYNC_DO | SYNC_FUTURE)):
					s.pause()
					
					if sflag & SYNC_DO:
						# recursively go down and pause every do
						a = s.future.thread
						print('1 fut from', s.future.cmd.name)
						if a:
							a.sync(sync_flag)
			else:
				return
		s.sync_flag.val = sflag | sync_flag
		s.state.set(WAITING)
	
	def pause(s):
		cmd = s.get_current_command()
		print('pausing ', cmd.name)
		if not cmd.future.paused() and not cmd.future.done():
			cmd.future.pause()
			# call pause interface
			if cmd.is_async_command() and '_pause' in cmd.func_interfaces:
				s.async_call_func(cmd, 1)
	
	def resume(s):
		cmd = s.get_current_command()
		if cmd.future.paused():
			cmd.future.resume()
			
			# call unpause interface
			if cmd.is_async_command():
				# print('cmd resume')
				s.async_call_func(cmd, 2 if '_pause' in cmd.func_interfaces else 0)
				s.cmd_state.set(1)
	
	def cancel(s):
		if s.future and not s.future.cancelled(): 
			s.future.cancel()
			cmd = s.get_current_command()
			# if not hasattr(cmd, 'func_interfaces'):
				# print(cmd.name, 'has no func_interfaces')
			if cmd.is_async_command():
				func, cmd.func_interfaces = Task.exported_cmds[cmd.name]
			# print(cmd.name)
			if cmd.is_async_command() and '_pause' in cmd.func_interfaces:
				s.async_call_func(cmd, 4) # 4 = cancel
	
	def async_call_func(s, cmd, pause=0):
		f = cmd.future
		func, cmd.func_interfaces = Task.exported_cmds[cmd.name]
		
		kwargs = cmd.kwargs
		if '_pause' in cmd.func_interfaces:
			kwargs['_pause'] = pause
		kwargs['_future'] = f
		s.sync(SYNC_FUTURE, f)
		sim_mode = '_sim' in cmd.func_interfaces
		if sim_mode: kwargs['_sim'] = Task.is_sim
		return func(*cmd.args, **kwargs)
	
	def inc_ip(s):
		s.ip.inc()
	
	def set_ip(s,ip):
		s.ip.set(ip)
	
	def print_commands(s):
		with inc_tab():
			msg = tabs() + '----'+\
				tabs() + 'Thread'+\
				tabs() + 'ip: ' + str(s.ip.get())+\
				tabs() + 'state: ' + s.state.get()+\
				tabs() + 'cmd: ' + str(s.cmd.print_command()) +\
				tabs() + 'running: ' + str(s.commands) +\
				tabs() + '----\n'
		return msg

	def __repr__(s):
		return s.name+'('+s.state.val+') '

class ListenerRecord:
	def __init__(s, name, cmd=None):
		s.name=name
		s.disabled=False
		s.cmd=cmd
		s.children=[]

class ListenInstance:
	def __init__(s, callb, ref_count, once):
		s.callback=callb
		s.ref_count=ref_count
		s.once=once

class Task:
	is_sim=False
	last_sim = 0
	task_num = 0
	meta_commands = {}
	
	def __init__(s, name, module, instance=0):
		s.meta_commands = None
		s.instance=instance
		s.name = name
		Task.sim_heap = StateBase()
		s.state = StateBase(PENDING)
		s.module = module
		s.module._sim = False
		s.names = {}
	
		s.evt_type = {}
		s.evt_name = {}
	def disable(s):
		s.state.val = DISABLED
	
	def add_thread(s,r):
		s.branches.append(r)
		if s.is_sim: s.sim_push_event(r)
		return r
	
	def run_task(s, task_func=None, on_task_done_cb=None):
		s.fut_queue = []
		CommandList.new()
		ret = task_func() if task_func else s.module.run()
		if ret == False: return False
		
		s.on_task_done = [on_task_done_cb] if on_task_done_cb else []
		s.state.set(PENDING)
		
		cmd = Command(CMD_DO, command_list=CommandList.get())
		s.main_branch = Thread(cmd, name='main')
		s.names['main'] = s.main_branch
		s.branches = StateBase([s.main_branch])
		s.passed_labels = StateBase([])
		s.label_syncs = StateBase([])
		
		return True
	
	def suspend(s):
		s.stop_task(SUSPENDED)
	
	###### block & notify #######
	def block(s, queue_id, future):
		el = next((a for a in s.fut_queue if a[0] == queue_id), None)
		print('calling block', el, s.fut_queue)
		tup = (queue_id, future)
		s.fut_queue.append( tup )
		print('calling block after', s.fut_queue)
		def on_cancel():
			print('cancelling ', tup)
			# if s.fut_queue[0] == tup:
				# s.notify(queue_id)
			if tup != s.fut_queue[0] and tup in s.fut_queue:
				s.fut_queue.remove( tup ) 
		future.set_on_cancel(on_cancel)
		
		if el:
			print('BLOCKED', s.fut_queue)
			return False
		else:
			return future
	
	def notify(s, queue_id):
		el = next((a for a in s.fut_queue if a[0] == queue_id), None)
		print('notify', s.fut_queue)
		if el:
			s.fut_queue.remove(el)
			el = next((a for a in s.fut_queue if a[0] == queue_id), None)
			if el:
				print('REDOING')
				s.fut_queue.remove(el)
				el[1].thread.redo()
	##############################
	
	
	def get_ref(s, ref, default=None):
		if type(ref) is Future: return ref.thread if ref.thread else default
		ret=s.names[ref] if ref in s.names else default
		# print('get ref:', type(ref), type(ret))
		return ret
	
	def stop_task(s, new_state=DONE):
		# print('finishing task')
		for b in s.branches.get():
			if b.state.get() != DONE:
				b.cancel()
		
		_core.emit('task:done', s.name)
		Task.task_num += 1
		prev_on_task_done = s.on_task_done
		def new_state_func():
			# clear event listeners
			s.destroy_event()
			s.state.set(new_state)
			for fnc in prev_on_task_done: fnc()
		if (s.state.get() == LEAVING and new_state != SUSPENDED) or new_state == DONE:
			new_state_func()
		else:
			def leaving_task():
				_core.emit('task:leave')

				print('staring task leave')
				if hasattr(s.module, 'leave'):
					s.module.leave()

				_core.emit('task:after_leave')
			s.run_task(leaving_task, new_state_func)
			s.state.set(LEAVING)
	
	##### RUNABLES CYCLE ######
	def run_thread(s,r):
		if r.overflow():
			r.state.val = DONE
		elif r.state.val in (RUNNING, LEAVING):
			s.run_command(r)
		
		if r.state.val == DONE:
			r.run_on_done()
			# print('removing branch:',r.name)
			s.branches.remove(r)
	
	def run_cycle(s):
		# print('runnin', s.name)
		b = s.branches.get()
		tn = s.task_num
		
		# debug
		# rs = [a for a in b if a.state.get() != WAITING]
		# if rs: print(rs)
			
		for r in b:
			if s.task_num != tn:
				break
			if r.state.get() != WAITING:
				# print(r.name, 'run_cycle', [a.name for a in b])
				# s.list_threads()
				s.run_thread(r)
		
		if s.main_branch.state.get() == DONE and s.state.get() != DONE:
			s.stop_task(DONE)
	################################
	
	
	############## SIMULATOR ############
	@staticmethod
	def sim_push_event(r):
		import heapq
		heapq.heappush(Task.sim_heap.get(), (r.sim_time.val, r))
	
	@contextmanager
	def simulator(s):
		import core.State as State
		if State.level == 0:
			Task.last_sim += 1
			State._sim_mode = Task.last_sim
			_e._sim = s.module._sim = Task.is_sim = True
		State.level+=1
		yield
		State.level-=1
		if State.level == 0:
			State._sim_mode = _e._sim = s.module._sim = Task.is_sim = False
	
	def run_simulator(s, thread=None, max_sim_time=0, max_cpu_clock=0):
		import time
		time_start=time.clock()
		if not thread: thread = s.main_branch
		with s.simulator():
			# import core.State as State
			# print('sim level:', State.level)
			import heapq
			for b in s.branches.val:
				if b.state.val == WAITING:
					if s.is_async_command( b.get_current_command() ):
						b.cmd_state.val = 0
						b.state.val = RUNNING
			Task.sim_heap.val = sorted([(b.sim_time.val, b) for b in s.branches.val if b.state.val == RUNNING])
			# print('start sim:', [(b.name, b.state.val, b.get_current_command()) for b in s.branches.val])
			while s.state.get() == PENDING:
				# print('sim heap:',len(s.sim_heap.val), [(i[0], i[1].name) for i in s.sim_heap.val])
				if not s.sim_heap.get(): return float('inf')
				sim_time, r = heapq.heappop(s.sim_heap.val)
				if r.state.get() == WAITING:
					if r.sim_func.val:
						r.sim_duration.val = r.sim_func.val(r.sim_time.val, r.sim_duration.val)
						if r.sim_duration.val == 0:
							r.future.set_result(1)
						else:
							r.sim_time.val += r.sim_duration.val
							s.sim_push_event(r)
					else:
						r.future.set_result(1)
				else:
					s.run_thread(r)
					if r == thread and r.state.get() == DONE: break
			if s.state.get() == SUSPENDED: return float('inf')
			return thread.sim_time.val
	########################################
	
	def cmd_meta_command(self, cmd, r):
		if not Task.meta_commands:
			Task.meta_commands = {
				CMD_DO: Task.cmd_do,
				CMD_GOTO: Task.cmd_goto,
				CMD_IF: Task.cmd_if,
				CMD_LABEL: Task.cmd_label,
				CMD_LISTEN: Task.cmd_listen,
				CMD_ON: Task.cmd_listen,
				CMD_RETURN: Task.cmd_return,
				CMD_SPAWN: Task.cmd_spawn,
				CMD_SYNC: Task.cmd_sync,
				CMD_TASK_DONE: Task.cmd_task_done,
				CMD_TASK_SUSPEND: Task.cmd_task_suspend,
				CMD_REF: Task.cmd_ref,
				CMD_UNLISTEN: Task.cmd_unlisten,
				CMD_PICK_BEST: Task.cmd_pick_best,
				CMD_WAKE: Task.cmd_wake,
				CMD_REDO: Task.cmd_redo,
				CMD_RESET_LABEL: Task.cmd_reset_label,
				CMD_REPEAT: Task.cmd_repeat
				}
		Task.meta_commands[cmd.name[-1]](self, cmd, r)

	def list_threads(s):
		print('running threads:')
		for th in s.branches.get():
			print('\tthread:', th.name)
	
	### EXEC ###
	def run_command(s, r):
		cmd = r.get_current_command()
		# print(s.name, r.name, 'runable ', r, 'doing cmd', cmd)
		# s.list_threads()
		# traceback.print_stack()
		# print(r.name, 'doing cmd', cmd)
		if cmd.is_meta_command():
			s.cmd_meta_command(cmd,r)
			if s.is_sim and r.state.get() == RUNNING: s.sim_push_event(r)
		else:
			s.cmd_async_command(cmd, r)
	
	def cmd_async_command(s, cmd, r):
		# if (r.cmd_state.get() == 1 and not s.is_sim) or r.cmd_state.get() == 2: # command finished
		if r.cmd_state.get() == 1: # command finished
			r.inc_ip()
			r.cmd_state.set(0)
			if s.is_sim: s.sim_push_event(r)
		else: # command starting
			r.cmd_state.set(1)
			f = cmd.future
			f.reset()
			f.set_thread(r)
			ret = r.async_call_func(cmd)
			
			if s.is_sim:
				if ret is False:
					r.sim_time.val = float('inf')
					s.stop_task()
				r.sim_duration.val = 0
				if type(ret) == tuple:
					r.sim_duration.val, r.sim_func.val = ret
				elif type(ret) in (int, float):
					r.sim_duration.val, r.sim_func.val = ret, None
				r.sim_time.val += r.sim_duration.val
				# r.cmd_state.set(2)
				if s.is_sim and not f.done(): s.sim_push_event(r)
	
	def cmd_pick_best(s, cmd, r):
		# print(col.yellow, 'cmd pick best', r.name, r.cmd_state.val, col.white)
		if r.cmd_state.get() == 1:
			r.inc_ip()
			r.cmd_state.set(0)
		else:
			r.cmd_state.set(1)
			r.sync(SYNC_FORCE)
			best=(float('inf'),None)
			# import core.State as State
			# print('pick best', State.level, cmd.commands)
			for c in cmd.commands:
				rn = s.add_thread(
					Thread(cmd, commands=[c], sim_time=r.sim_time.val, name='pick_best_thread')
				)
				t=s.run_simulator(thread=rn)
				rn.kill()
				# print('pbest',t)
				if t < best[0]: best=(t,c)
			if best[0] != float('inf'):
				rn = s.add_thread(
					# pick best possible command
					Thread(cmd, [best[1]], sim_time=r.sim_time.val, name='picked_best_thread')
				)
				r.sync(SYNC_DO, rn)
			r.wake(SYNC_FORCE)
	
	def cmd_redo(s, cmd, r):
		# r.kill()
		ref=pick('ref', cmd.kwargs, None, 0)
		rn=s.get_ref(ref, None) if ref else r
		
		if rn.parent.val:
			rn.parent.val.redo()
		else:
			r.set_ip(0)
			r.cmd_state.val = 0
			return
		# rn.cancel()
		rn.kill()
		# print(r.id, 'is done')
		r.inc_ip()
		
	def cmd_do(s, cmd, r):
		if r.cmd_state.get() == 1:
			r.inc_ip()
			r.cmd_state.set(0)
			cmd.future.set(cmd.ret)
		else:
			kwargs = cmd.kwargs.copy()
			name=pick('_name', kwargs)
			atomic=pick('_atomic', kwargs)
			
			if not cmd.future.paused() or atomic:
				cmd.clear()
				with CommandList.save(cmd):
					cmd.ret=cmd.args[0](*cmd.args[1:], **kwargs)
				
				if not cmd.commands:
					r.inc_ip()
					cmd.future.set(cmd.ret)
					return
					
				rn = s.add_thread(Thread(cmd, sim_time=r.sim_time.val, 
					name=name if name else 'thread' + str(_core.unique_num())))
				cmd.future.set_thread(rn)
				cmd.future.reset()
				rn.parent.set(r)
			else:
				# print('was paused')
				rn = cmd.future.thread
				rn.redo()
			
			if name: s.names[name] = rn
			r.sync(SYNC_DO, rn)
			r.cmd_state.set(1)
	
	def cmd_spawn(s, cmd, r):
		ref=pick('ref', cmd.kwargs, delete=False)
		rn = r
		if ref: rn = s.get_ref(ref)
		s.spawn(cmd=cmd, r=rn)
		r.inc_ip()
	
	def cmd_if(s,cmd,r):
		rn = None
		# if woken up
		if r.cmd_state.get() == 1:
			r.inc_ip()
			r.cmd_state.set(0)
		else:
			done=False
			for i in cmd.params[TAG_ELIF]:
				condition_func, commands = i
				if (type(condition_func) is int and condition_func > 0) or \
				   (callable(condition_func) and condition_func()):
					done = True
					rn = s.add_thread(Thread(cmd, commands, sim_time=r.sim_time.val))
					break
					
			if not done and TAG_ELSE in cmd.params:
				rn = s.add_thread(Thread(cmd, cmd.params[TAG_ELSE]))
			
			# enter sync waiting state
			if rn != None:
				r.sync(SYNC_DO, rn)
				r.cmd_state.set(1)
			else:
				r.inc_ip()
	
	def cmd_ref(s, cmd, r):
		cmd.future.set_thread(r)
		r.inc_ip()
	
	def cmd_label(s, cmd, r):
		label_name = cmd.args[0]
		
		# print('cmd_label label', label_name, r.labels)
		if not any(l for l in s.passed_labels.get() if l[0] == label_name):
			s.passed_labels.append((label_name, r.sim_time.val))
		
		# wake all threads syncing on label
		cond=lambda tpl: tpl[1] == label_name and (tpl[0] in (r, None))
		for i in filter(cond, s.label_syncs.get()):
			if _core.debug: print('sync finished')
			i[2](r)
		s.label_syncs.set(list(filter(_not(cond), s.label_syncs.get())))
		r.inc_ip()
		# print('cmd_label',r.name, r.state.val, r.ip.val)
	
	def cmd_reset_label(s, cmd, r):
		lbl = cmd.args[0] if cmd.args else None
		if lbl:
			r.passed_labels.val = [i for i in r.passed_labels.val if i[0] != lbl]
			s.passed_labels.val = [i for i in s.passed_labels.val if i[0] != lbl]
		else:
			r.passed_labels.clear()
			s.passed_labels.clear()
		r.inc_ip()
	
	def cmd_sync(s, cmd, r):

		c = cmd.args[0] if cmd.args else None # future or label
		
		ref = pick('ref', cmd.kwargs, None, 0)
		rn = s.get_ref(ref, None) if ref else r
		evt = pick('event', cmd.kwargs, None, 0)
		# print('syncing ', ref, rn)
		
		if not rn:
			if _core.debug: print('sync has no reference!')
			r.inc_ip()
			return
		
		if type(c) is Future: # wait for future to be resolved
			c = [c]
		
		if type(evt) is str: # sync event (_sync(event='motion:stuck'))
			_core.on(evt, lambda:rn.wake(SYNC_EVENT))
		
		elif type(c) is str: # _sync('label') wait for label to be consumed
			label_name = c
			# check if already passed
			passed = next((l for l in s.passed_labels.get() if l[0] == label_name), False)
			if passed: return
			# setting hook
			def on_label(waker): rn.wake(SYNC_LABEL, waker)
			s.label_syncs.append((None, label_name, on_label))
			if _core.debug: print('[', rn.name, '] waiting label sync', label_name)
			rn.sync(SYNC_LABEL)
			
		elif type(c) is list: # wait for threads in list to die
			cmd.wake_counter=len(c)
			for i in c:
				r2=s.get_ref(i)
				if not r2 or not r2.future or r2.future.done():
					cmd.wake_counter-=1
					continue
				def on_done():
					cmd.wake_counter-=1
					if cmd.wake_counter <= 0: rn.wake(SYNC_THREAD, r2)
				r2.on_done.append(on_done)
		
		elif type(c) is int: # wait unconditionally
			rn.sync(SYNC_UNCOND)
			
		elif c is None: # wait for active child threads to die
			c = r.get_active_threads()
			if _core.debug >= 2:
				print(r.name, 'active threads', r.cmd.threads)
			cmd.wake_counter=len(c)-1
			
			if cmd.wake_counter <= 0:
				rn.inc_ip();
				return
				
			for i in c:
				if i == r: 
					if _core.debug >= 2:
						print('skipping ',r)
					continue
				r2=i
				# test if invalid or already done
				if not r2 or not r2.future or r2.future.done():
					cmd.wake_counter-=1
					continue
					
				if cmd.wake_counter <= 0:
					rn.inc_ip();
					return

				def on_done():
					cmd.wake_counter-=1
					if _core.debug >= 2:
						print('sync dec', cmd.wake_counter, r.cmd.threads)
					if cmd.wake_counter <= 0: rn.wake(SYNC_THREAD, r2)
				r2.on_done.append(on_done)
				
				rn.sync(SYNC_THREAD, r2)
		
		if _core.debug: print('thread [', rn.name, '] is waiting')
		# r.cmd_state.set(1)
		r.inc_ip()
			
			
	def spawn(s, *args,  cmd=None, future=None, r=None, **kwargs):
		# print(s.name, 'spawning')
		if not cmd:
			CommandList.new()
			cmd=gen_cmd(CMD_SPAWN, *args, **kwargs).cmd
		
		if not r: r=s.main_branch
		kwargs=cmd.kwargs.copy()
		name=pick('_name', kwargs)
		cmd.clear()
		
		with CommandList.save(cmd):
			cmd.ret=cmd.args[0](*cmd.args[1:], **kwargs)
		
		if cmd.commands:
			rn = s.add_thread(
				Thread(cmd, sim_time=r.sim_time.val, name=(name if name else None))
			)
			#print('spawning thread', rn.name,rn.state.get())
			r.cmd.threads.append(rn)
			rn.parent.set(r)
			
			if future:
				def on_done():
					nonlocal future
					future.set_result(1)
				rn.on_done.append(on_done)
				
			if name: s.names[name] = rn
			cmd.future.set_thread(rn)
		elif future:
			future.set_result(1)
		
		return cmd.future
	
	# listener changing policy
	def cmd_repeat(s, cmd, r):
		
		rec = r.top().cmd.record
		rep = rec.repeat
		rec.repeat = cmd.args[0]
		if rep != cmd.args[0]:
			if rep == 'block2' and hasattr(rec, 'block2'):
				s.run_listener(rec.block2)
				del rec.block2
		r.inc_ip()
	
	def run_listener(s, ctx):
		record, el, args, kwargs = ctx
		threads = record.cmd.threads
		if record.repeat == 'replace':
			for rn in threads: rn.kill()
		fut=s.spawn(el.callback, *args, cmd=None, r=None, **kwargs, _name='listener:'+record.name)
		if fut.thread: threads.append(fut.thread)
		fut.cmd.record = record
		
	def on_listener_event(s, record, *args, **kwargs):
		# print('listening: ', record, *args)
		parent = record.cmd.parent
		if hasattr(parent, 'paused') and parent.paused:
			if _core.debug >= 1.5:
				print('on listener event: paused')
			return
		if s.is_sim: return
		tr = record.type_record
		if tr.disabled or record.disabled: return
		# print('before', [i.deleted for i in record.children])
		# print('-- got evt', tr.name, record.name, *args)
		s.handled=False
		for el in reversed(record.children):
			if el.ref_count == 0:
				# print('rem ', el)
				record.children.remove(el)
				# print('after rem',record.children)
				continue
			# print('cmds:',id(CommandList.get()), CommandList.get().name, el[0])
			threads = record.cmd.threads = [r for r in record.cmd.threads if r.state.get() != DONE]
			# print('got evt: ', tr.name, record.name, *args, len(threads))
			res = False;
			fut=None
#print('got evt', tr.name, record.repeat)
			ctx = (record, el, args, kwargs)
			if threads:
				if record.repeat not in ('block', 'block2'):
					s.run_listener(ctx)
				elif record.repeat == 'block2':
					record.block2 = ctx
			elif not threads:
				s.run_listener(ctx)
			if fut: res=fut.cmd.ret
			
			if el.once:
				record.children.remove(el)
				el.ref_count -= 1
				continue
				
			if s.handled or res:
				break
		
		if not record.children:
			try:
				tr.children.remove(record)
				del s.evt_name[record.name]
			except:
				# print('failed to remove children')
				pass
	
	def cmd_listen(s, cmd, r):
		#print('cmd listen', r.name)
		r.inc_ip()
		if s.is_sim: return
		event_name, callback = cmd.args[0], cmd.args[1] if len(cmd.args) == 2 else None
		
		# listen / unlisten
		# if given only 1 argument, 2nd is None
		if callback == None and type(event_name) is str:
			if event_name in s.evt_type:
				s.evt_type[event_name].disabled = False
			elif event_name in s.evt_name:
				s.evt_name[event_name].disabled = False
			return
		
		kwargs = cmd.kwargs.copy()
		listener_name = pick('_name', kwargs)
		# print('new listener name:', listener_name)
		name=None
		if listener_name: 
			name = listener_name
		else:
			listener_name = event_name
		order=pick('_order', kwargs, 'top')
		repeat=pick('_repeat', kwargs, 'block')
		
		# get type record
		if event_name in s.evt_type:
			tr=s.evt_type[event_name]
		else:
			tr=ListenerRecord(event_name)
			s.evt_type[event_name] = tr
		
		# get listener record
		if listener_name in s.evt_name:
			lr = s.evt_name[listener_name]
		else:
			lr = ListenerRecord(listener_name, cmd)
			s.evt_name[listener_name] = lr
			# listener_rec -> type_rec
			lr.type_record = tr
			# type_rec << listener_rec
			tr.children.append(lr)
			args = list(cmd.args)
			args[1] = lambda *args, **kwargs: s.on_listener_event(lr, *args, **kwargs)
			l = _core.service_manager.listen(*args, **cmd.kwargs)
			lr.listener = l
			lr.repeat=repeat
			cmd.threads=[]
			cmd.parent = r.cmd
		
		once = cmd.name[1] != CMD_LISTEN
		
		# take order into account
		el = ListenInstance(callback, 1, once)
		if order == 'top': lr.children.append(el)
		else: lr.children.insert(0, el)
		r.listeners.append(el)
	
	def destroy_event(s, evt_type=None, evt_name=None):
		if s.is_sim: return
		if evt_type == evt_name == None: # remove all events
			for lr in s.evt_name.values(): lr.listener.stop()
			s.evt_name.clear()
			s.evt_type.clear()
		elif evt_name:
			if type(evt_name) is ListenerRecord:
				lr=evt_name
				evt_name=lr.name
				if evt_name in s.evt_name: del s.evt_name[evt_name]
			elif evt_name in s.evt_name:
				lr=s.evt_name[evt_name]
			lr.listener.stop()
			lr.type_record.children.remove(lr)
		elif evt_type and evt_type in s.evt_type:
			for c in s.evt_type[evt_type].children: 
				s.destroy_event(evt_name=c)
			del s.evt_type[evt_type]
	
	def cmd_unlisten(s, cmd, r):
		r.inc_ip()
		if s.is_sim: return
		dest=pick('destroy', cmd.kwargs, delete=False)
		if cmd.args:
			reference = cmd.args[0]
			
			if reference not in s.evt_type: return
				
			if type(reference) is str:
				if dest:
					s.destroy_event(evt_type=reference)
				else:
					s.evt_type[reference].disabled = True
			elif type(reference) is Future:
				if dest: s.destroy_event(evt_name=reference.listener)
				reference.listener.disabled = True
		else:
			reference = cmd.kwargs['_name']
			if reference in s.evt_name:
				s.evt_name[reference].disabled = True
	
	def cmd_return(s, cmd, r):
		ref=pick('ref', cmd.kwargs, delete=False)
		r.inc_ip()
		if ref:
			r=s.get_ref(ref)
			if not r: raise Exception('_return ref= reference not found')
		if r.cmd.future: r.cmd.future.set_result(cmd.args[0] if cmd.args else 1)
		r.state.set(DONE)
		r.run_on_done()
	
	def cmd_task_done(s, cmd, r):
		if s.state != LEAVING:
			next_task = cmd.args[0] if cmd.args else None
			if next_task:
				_core.task_manager.get_task(next_task).state.val = PENDING
				_core.task_manager.set_next_task(next_task)
			s.stop_task()
		else:
			raise Exception('cannot finish task while leaving task')
	
	def cmd_task_suspend(s, cmd, r):
		next_task = cmd.args[0] if cmd.args else None
		if next_task:
			_core.task_manager.get_task(next_task).state.val = PENDING
			_core.task_manager.set_next_task(next_task)
		s.stop_task(SUSPENDED)
	
	def cmd_wake(s, cmd, r):
		rn = s.get_ref(cmd.args[0])
		rn.wake(SYNC_UNCOND)
		r.inc_ip()
	
	def cmd_goto(s, cmd, r):
		# print('entering goto cmd',cmd.args, r.name)
		kwargs=cmd.kwargs
		ref=pick('ref', kwargs, 0, 0)
		if ref:
			r2=s.get_ref(ref)
			if not r2: raise Exception('goto reference is invalid')
		else:
			r2=r
		label = cmd.args[0] if cmd.args else None
		
		if r2.state.get() == DONE:
			r.inc_ip()
			return
		
		if not s.is_sim and r2.future and not r2.future.done():
			r2.cancel()
		
		# find label to jump to
		offset=pick('offset', kwargs, 0, 0)
		if label is None:
			lab = (0, r2.ip.get())
		elif type(label) is int:
			lab = (0, r2.ip.get())
			offset = label
		else:
			lab=next((l for l in r2.labels if l[0] == label), None)
		# print('LAB:',lab, r2.labels)
		
		if lab:
			if not s.is_sim and not r2.overflow(): # cancelation
				r2.cancel()
			r2.set_ip( min(len(r2.commands), max(0, lab[1]+offset)) )
			r2.cmd_state.set(0)
			r2.state.set(RUNNING)
		
		elif r == r2:
			raise Exception('no label to jump to')
		if r != r2: r.inc_ip()
	
