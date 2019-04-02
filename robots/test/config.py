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

@_core.export_cmd
@_core.do
def bad():
	print('fail')
	exit(-1)
	
State.strat_init=_State()
State.init=_State()

@_core.init_task
def init_task():
	State.init.val = 'initialized'
	_e._print('init config.py')
