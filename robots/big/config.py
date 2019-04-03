# hello world code for driving robot
from modules.default_config import motion,chinch
from modules.drivers.Servo import *
from modules.sensors.BinaryInfrared import *

from modules.sensors.PressureSensor import *
from core.network.Splitter import *
motion.can.iface = 'can0'
can=motion.can

#VELIKIII

from modules.default_config import collision_wait
chinch.addr = 0x8d02

##### Infrared ####
_core.add_module([
	BinaryInfrared('zadnji', (-200,120), (-300,-50), packet_stream=can.get_packet_stream(0x80008d05)),
	BinaryInfrared('prednji levi', (60, 100), (300,50), packet_stream=can.get_packet_stream(0x8008d03)),
	BinaryInfrared('prednji desni', (60, -100), (300, -50), packet_stream=can.get_packet_stream(0x80008d04)),
])
##################
	
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
	_e.servo_lfliper.action('GoalPosition', [682, 389, 239][v])  #537, 465, 211

@_core.export_cmd
@_core.do
def rfliper(v):
	_e.servo_rfliper.action('GoalPosition', [251, 549, 703][v])

######## STATIC OBSTACLES #######
_core.entities.add_entity('static', 'rampa', [[-1050,500], [-35,500], [-35, 368], [45,352], [41, 536], [1055,516], [1089, 992], [-1041, 964], [-1050, 500]])
_core.entities.add_entity('static', 'accelerator', [[-999,-932], [991, -944], [991, -1000], [-991,-1000]])
#################################

pressure = [ PressureSensor('pressure'+str(i), i, can.get_packet_stream(0x80007800+i, 0x80007800)) for i in range(9) ]

_core.add_module(pressure)
for i in pressure: i.export_cmds(i.name)

@_core.export_cmd
def pressure(i): # i - pump num
	i2 = [0, 3, 4, 1, 8, 2, 0, 8, 2, 0][i % 10]
	a = getattr(_e, 'pressure%d' % i2).picked()
	return a
#ZEKI DODAO

############### LIFT ###################
from modules.drivers.motion.Motion import *
spl=Splitter(can.get_packet_stream(0x80000259))
lift_drv = Motion(name='lift', packet_stream=spl.get())
lift_drv.export_cmds('lift_drv')
_core.add_module(lift_drv)
State.lift_fut=[None]*2
def lift_recv(p):
	if p[0] == 0x40:
		if State.lift_fut[1]:
			State.lift_fut[1].set_result(1)
			if _core.debug >= 1: print('lift 2 done')
	elif p[0] == 0x21:
		if State.lift_fut[0]:
			State.lift_fut[0].set_result(1)
			if _core.debug >= 1: print('lift 1 done')
spl.get().recv=lift_recv

lift_positions = {
	'accel': 50000,
	'goldenium': 400000,
	'pri_vrhu': 1700000,
	'sredina': 1800000
}

@_core.export_cmd
def init_lift(_future):
	lift_drv.future = _future
	# motion.motion.future = _future
	if State.sim: _future.set_result(1)
	lift_drv.conf_set('init_dir1', -1)
	lift_drv.conf_set('init_dir2', -1)
	lift_drv.conf_set('debug_encoders', 0)
	lift_drv.conf_set('speed1', 200)# bilo 100
	lift_drv.conf_set('speed2', 200)#bilo 100
	lift_drv.send('/')

@_core.export_cmd
def lift(l, pos, up=0, _future=None):
	if State.sim: _future.set_result(1)
	l = min(2, max(1, l))
	if not State.lift_fut[l-1]: 
		lift_drv.conf_set('encoder'+str(l)+'_max', 1860000)
	p = State.lift_fut[l-1]
	if p and not p.done():
		print('lift unfinished !')
	State.lift_fut[l-1] = _future
	pt = 0
	if pos in lift_positions:
		pt = lift_positions[pos]
	elif type(pos) is int:
		pt = pos
	lift_drv.conf_set('setpoint'+str(l), pt - 200000 * up)
#########################################

###### ROBOT DEFAULT INITIAL TASK #######

from modules.default_config import share, timer
share.port = 6000

_core.debug =1 
######### addpts ##########
@_core.init_task
def _():
		pts = _State(0, name='points', local=0, shared=1)
		@_core.export_cmd
		@_core.do
		def addpts(points):
			print('addpts',points)
			pts.val = pts.val + points
###########################

@_core.init_task
def init_task():
	servo_rlift.action('Speed',500)
	servo_llift.action('Speed', 500)
	servo_lfliper.action('Speed', 350)
	servo_rfliper.action('Speed', 350)
	init_lift()
	_e.lift_drv.conf_set('speed1', 300)# bilo 100
	_e.lift_drv.conf_set('speed2', 300)#bilo 100
	_e._print('initialized task')
	_e.r.send('R')
	_e.r.conf_set('send_status_interval', 100)
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
	@_e._on('message')
	def go(m):
			_e._label('go')
#_e._sync('go')
	_e.chinch()
	timer.start_timer()
