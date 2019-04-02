from core.schedulers.BasicScheduler import BasicScheduler
from core.schedulers.SimulationScheduler import SimulationScheduler

_core.task_manager.set_scheduler(BasicScheduler('weight'))

#### Testing UDP
from core.network.Udp import Udp
u=Udp(ip='127.0.0.1', local_port=0, port=5000)
_core.add_module([u])
p=u.get_packet_stream()
def msg(m): print('msg:',m)
p.recv = msg
####

if not hasattr(State, 'ip'):
	State.ip = '0.0.0.0'

from modules.default_config import share
share.ip = State.ip

@_core.export_cmd
@_core.do
def bad():
	print('fail')
	exit(-1)
	
State.strat_init=_State()
State.init=_State()

@_core.listen('message')
def msg(m):
	print(m)

State._shared=[]
@_core.listen('state:init')
def on_state(st, value=None, name=None, ishared=True, **kwargs):
	print('init state', name, kwargs)
	if 'shared' in kwargs and kwargs['shared']:
		st.shared = True
		State._shared.append(st)
		# set_state(name, value)

@_core.listen('state:change')
def st_change(st, old, new):
	print('st ch:',old,new)
	if hasattr(st, 'shared') and st.shared:
		_core.get_module('share').set_state(st.name, new)

@_core.listen('share:state_change')
def st_change2(name,new):
	n = next((i for i in State._shared if i.name == name), None)
	if n: n._set(new,report=1)
	

@_core.init_task
def init_task():
	State.init.val = 'initialized'
	_e._print('init config.py')
