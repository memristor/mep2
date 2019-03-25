# hello world code for driving robot
from modules.default_config import motion	
from modules.drivers.Servo import *

from modules.sensors.PressureSensor import *
from core.network.Splitter import *
motion.can.iface = 'can0'
can=motion.can
#VELIKIII
	
@_core.export_cmd
@_core.do
def pump(x, v):
	can.send(bytes([v])*5, 0x6c10) if x == 0 else can.send(bytes([v]), 0x6c10+x)
#exit(0)

#### SERVOS ####

servo_id = 0x80008d00
spl = Splitter(can.get_packet_stream(servo_id))
servo_rlift  = Servo('servo_rlift', servo_id=25, packet_stream=spl.get()) # izvuceno 211; medjupozicija 465; uvucano 537
servo_llift = Servo('servo_llift', servo_id=24, packet_stream=spl.get()) # uvuceno 459; izv 843; medju 577

servo_lfliper = Servo('servo_lfliper', servo_id=23, packet_stream=spl.get()) # 
servo_rfliper = Servo('servo_rfliper', servo_id=22, packet_stream=spl.get()) # 
servos = [servo_lfliper, servo_rfliper, servo_rlift, servo_llift]
for i in servos: i.export_cmds(i.name)
_core.add_module(servos)

@_core.export_cmd
@_core.do
def rlift(v):
	_e.servo_rlift.action('GoalPosition', [537, 465, 211][v])

@_core.export_cmd
@_core.do
def llift(v):
	_e.servo_llift.action('GoalPosition', [459, 577, 843][v])

@_core.export_cmd
@_core.do
def lfliper(v):
	_e.servo_lfliper.action('GoalPosition', [543, 248, 68][v])  #537, 465, 211

@_core.export_cmd
@_core.do
def rfliper(v):
	_e.servo_rfliper.action('GoalPosition', [423, 710, 888][v])


pressure = [ PressureSensor('pressure'+str(i), i, can.get_packet_stream(0x80007800+i, 0x80007800)) for i in range(9) ]

_core.add_module(pressure)
for i in pressure: i.export_cmds(i.name)

@_core.export_cmd
def pressure(i):
	a = getattr(_e, 'pressure%d' % i).picked()
	return a
#ZEKI DODAO

############### LIFT ###########
from modules.drivers.motion.Motion import *
spl=Splitter(can.get_packet_stream(601))
lift_drv = Motion(name='lift', packet_stream=spl.get())
lift_drv.export_cmds('lift_drv')
_core.add_module(lift_drv)
State.lift_fut=[None]*2
def lift_recv(p):
	if p[0] == 0x40 and State.lift_fut[0]:
		State.lift_fut[0].set_result(1)
	elif p[0] == 0x21 and State.lift_fut[1]:
		State.lift_fut[1].set_result(1)
spl.get().recv=lift_recv

lift_positions = {
	'accel': 50000,
	'golden': 400000,
	'pri_vrhu': 1700000,
	'sredina': 1800000
}

@_core.export_cmd
def lift(l, pos, up=0, _future=None):
	if State.sim: _future.set_result(1)
	l = min(1, max(0, l))
	if not State.lift_fut[l]: 
		lift_drv.conf_set('encoder'+str(l)+'_max', 1860000)
	State.lift_fut[l] = _future
	if pos in lift_positions:
		pt = lift_positions[pos]
	elif type(pt) is int:
		pt = pos
	lift_drv.conf_set('setpoint'+str(l), pt - 200000 * up)
###########################

###### ROBOT DEFAULT INITIAL TASK #######


@_core.init_task
def init_task():
	servo_rlift.action('Speed',500)
	servo_llift.action('Speed', 500)
	servo_lfliper.action('Speed', 250)
	servo_rfliper.action('Speed', 250)
	_e._print('initialized task')
	_e.lift_drv.send('/') # initialize lift
	_e.r.send('R')
	_e.r.conf_set('send_status_interval', 80)
	if not State.sim:
		_e.r.conf_set('wheel_r1', 72.768)
		_e.r.conf_set('wheel_r2', 72.11807159)
		_e.r.conf_set('wheel_distance', 276.621)
		_e.r.conf_set('pid_d_p', 3.0)
		_e.r.conf_set('pid_d_d', 140.0)
		_e.r.conf_set('pid_r_p', 3.0)
		_e.r.conf_set('pid_r_d', 140.0)
		_e.r.conf_set('enable_stuck', 1)
	_e.r.speed(30)
	_e.r.accel(1000)
