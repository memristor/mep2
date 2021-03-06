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
else:
	State.ip = '127.0.0.1'

from modules.default_config import share

share.ip = State.ip


from modules.default_config import timer
timer.end_time = 100

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

@_core.listen('round:end')
def _():
	_e._print('round end is run as task')
	

@_core.init_task
def init_task():
	State.init.val = 'initialized'
	_e._print('init config.py')
	timer.start()
