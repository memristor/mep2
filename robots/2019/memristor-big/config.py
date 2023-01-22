from modules.drivers.Servo import *
from modules.sensors.BinaryInfrared import *
from modules.sensors.PressureSensor import *
from modules.sensors.TOFSensor import *
from core.network.Tcp import *
from core.network.Splitter import *

#VELIKIII
_core.debug = 0


##### Motion #######
from modules.default_config import motion, motion_fix
motion.can.iface = 'can0' 
can=motion.can

# big robot using old curve_rel
a=_e.r.curve_rel
def mod_curve_rel(radius, angle, *args):
	a(radius//2, angle, *args)
with _core.export_ns('r'):
	_core.export_cmd('curve_rel', mod_curve_rel)
####################


from modules.default_config import collision_wait

############ Activator ##################
from modules.default_config import chinch
chinch.addr = 0x80007f11
#########################################

##### Infrared Sensors ####
_core.add_module([
	BinaryInfrared('zadnji levi', (-200,120), (-300,120), packet_stream=can.get_packet_stream(0x80007f22)),
	BinaryInfrared('zadnji desni', (-200,-120), (-300,-120), packet_stream=can.get_packet_stream(0x80007f21)),
	BinaryInfrared('prednji levi', (60, 100), (300,100), packet_stream=can.get_packet_stream(0x80007f10)),
	BinaryInfrared('prednji desni', (60, -100), (300, -100), packet_stream=can.get_packet_stream(0x80007f0f)),
])
###########################

##### Lidar Sensors #######
from modules.default_config import lidar
###########################

##### TOF Sensors ######
tof = TOFSensor()
tof.export_cmds('tof')
_core.add_module( tof )
########################

########### Pumps ###################
@_core.export_cmd
@_core.do
def pump(x, v):
	can.send(bytes([v])*5, 0x6c10) if x == 0 else can.send(bytes([v]), 0x6c10+x)
#####################################

################### SERVOS #######################
servo_id = 0x80008d00
spl = Splitter(can.get_packet_stream(servo_id))
servo_rlift  = Servo('servo_rlift', servo_id=25, packet_stream=spl.get()) # izvuceno 211; medjupozicija 465; uvucano 537
servo_llift = Servo('servo_llift', servo_id=24, packet_stream=spl.get()) # uvuceno 459; izv 843; medju 577
servo_lfliper = Servo('servo_lfliper', servo_id=23, packet_stream=spl.get()) # 
servo_rfliper = Servo('servo_rfliper', servo_id=22, packet_stream=spl.get()) # 

# export servo commands
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
#################################################


######## STATIC OBSTACLES #######
_core.entities.add_entity('static', 'rampa', [[-1050,500], [-35,500], [-35, 368], [45,352], [41, 536], [1055,516], [1089, 992], [-1041, 964], [-1050, 500]])
_core.entities.add_entity('static', 'accelerator', [[-999,-932], [991, -944], [991, -1000], [-991,-1000]])
#################################


######### Pressure Sensors ############
pressure = [ PressureSensor('pressure'+str(i), i, can.get_packet_stream(0x80007800+i, 0x80007800)) for i in range(9) ]
# export pressure sensor commands
_core.add_module(pressure)
for i in pressure: i.export_cmds(i.name)

@_core.export_cmd
def pressure(i): # i - pump num
	i2 = [0, 3, 4, 1, 8, 2, 0, 8, 2, 0][i % 10]
	a = getattr(_e, 'pressure%d' % i2).picked()
	return a
#######################################

######################## LIFT ###################################
from modules.drivers.motion.Motion import *
lift_drv = Motion(name='lift', packet_stream=can.get_packet_stream(0x80000259))
lift_drv.export_cmds('lift_drv')
_core.add_module(lift_drv)

lift_positions1 = {
	'accel': 50000+77000+15000,
	'goldenium': 400000+77000+15000,
	'pri_vrhu': 1700000+77000+15000,
	'sredina': 1977000+15000, #1 860 000
	'dole': 1920000 + 8000*11 + 4000
}

lift_positions2 = {
	'accel': 50000,
	'goldenium': 400000,
	'pri_vrhu': 1700000,
	'sredina': 1800000, #1 860 000
	'dole': 1880000
}

lift_drv.set_lift_positions(1, lift_positions1)
lift_drv.set_lift_positions(2, lift_positions2)

@_core.do
def init_lift():
	lift_drv.conf_set('init_dir1', -1)
	lift_drv.conf_set('init_dir2', -1)
	lift_drv.conf_set('debug_encoders', 0)
	lift_drv.conf_set('speed1', 300)# bilo 100
	lift_drv.conf_set('speed2', 300)#bilo 100
	_e.lift_drv.prepare_lift()
	_e.lift_drv.conf_set('speed1', 450)# bilo 100
	_e.lift_drv.conf_set('speed2', 450)#bilo 100

_core.export_cmd('lift', lift_drv.lift)
#################################################################



####### Share and Timer ########
from modules.default_config import share, timer
share.port = 6000
timer.end_time = 100
################################


######### addpts ##########
from modules.default_config import lcd
###########################


############### Coordinates ################
@_core.export_cmd
def coord(c):
	zuta = {
		'prilaz_rampi': (1265,500),
		
		'start_plavi' :	(1250-50,110),
		'start_zeleni': (1250-50,-390),
		'start_crveni': (1250-50,-520),
		
		'slot_2_1': (795,355+15-5-6+8-5-2),
		'slot_2_1_obratno': (795+4,355+15-5-6+7-5-4-2),
		'slot_2_2': (698-2,355+15-5-6+7-5-2-1+2+2-4+2+2),
		'slot_2_2_obratno': (698+2+200,355+15-5-6+7-5-4-7+2+2),
		'slot_2_poslednje': (698+2+300,355+15-5-6+7-5-4-7+2+2),
		
		'priprema_akcelerator_1': (0,-550),
		'priprema_akcelerator_2_1': (80,-788),
		'priprema_akcelerator_2_2': (-100,-782),
	}
	ljubicasta = {
		'prilaz_rampi': (-1265,500),
		
		'start_plavi': (-1250+50,110),#bilo 1180
		'start_zeleni': (-1250+50,-390),
		'start_crveni': (-1250+50,-520),
	
		'slot_2_1': (-795,355+15-5-6+8-5-2),
		'slot_2_1_obratno': (-795-4,355+15-5-6+7-5-4-2),
		'slot_2_2': (-698+2,355+15-5-6+7-5-2-1+2+2-4+2+2),
		'slot_2_2_obratno': (-698-2-200,355+15-5-6+7-5-4-7+2+2),
		'slot_2_poslednje':(-698-2-300,355+15-5-6+7-5-4-7+2+2),
	
		'priprema_akcelerator_1': (0,-550),
		'priprema_akcelerator_2_1': (-80,-788),
		'priprema_akcelerator_2_2': (100,-782),
	}
	
	if State.color == 'zuta':
		return zuta[c]
	else:
		return ljubicasta[c]
############################################

######## Point Constants ##########
State.color_vaga_bodovi = {'crveni': 4, 'plavi': 12, 'zeleni': 8, False: 0}
State.color_elem_bodovi = {'crveni': 6, 'plavi': 6, 'zeleni': 6, False: 0}
State.akcelerator_bodovi = 10
State.startno_polje_bodovi = 1
State.startno_polje_bonus = 5
###################################



######## Round End Task #########
@_core.listen('round:end')
def round_end():
	for i in range(1,10):
		_e.pump(i,0)
	_e.r.motoroff()
#################################

######## Remote Start Option ######
def start_remotely():
	@_e._on('message')
	def go(m): 
		_e._label('go')
	_e._sync('go')
###################################

###### Experiment ########
tcp_experiment = Tcp(name='experiment', ip='127.0.0.1', port=8000)
pt = tcp_experiment.get_packet_stream()
_core.add_module(tcp_experiment)
@_core.export_cmd
@_core.do
def experiment(v):
	pt.send(v.encode())
##########################

@_core.do
def init_servos():
	servo_rlift.action('Speed',500)
	servo_llift.action('Speed', 500)
	servo_lfliper.action('Speed', 200)
	servo_rfliper.action('Speed', 200)

def init_pids():
	if not State.sim:
		_e.r.conf_set('stuck_distance_max_fail_count',120)
		_e.r.conf_set('stuck_rotation_max_fail_count',50)
		_e.r.conf_set('stuck_rotation_jump',20)
		_e.r.conf_set('stuck_distance_jump',50)
		_e.r.conf_set('wheel_r1', 72.768)
		_e.r.conf_set('wheel_r2', 72.11807159)
		_e.r.conf_set('wheel_distance', 276.621)
		_e.r.conf_set('pid_d_p', 3.0)
		_e.r.conf_set('pid_d_d', 140.0)
		_e.r.conf_set('pid_r_p', 3.0)
		_e.r.conf_set('pid_d_i', 0.025)
		_e.r.conf_set('pid_r_i', 0.025)
		_e.r.conf_set('pid_r_d', 140.0)
		_e.r.conf_set('enable_stuck', 1)

###### ROBOT INITIAL TASK #######
@_core.init_task
def init_task():
	State.pumpe = [_State(0) for i in range(10)]
	
	_e.check_chinch()
	
	init_servos()
	_e.rlift(0)
	_e.llift(0)
	init_lift()
	
	init_pids()
	_e.r.send('R')
	_e.r.conf_set('send_status_interval', 100)
	_e.r.speed(30)
	_e.r.accel(500)
	
	_e.r.conf_set('alpha', 1000)
	_e.chinch()
	timer.start_timer()
	_e.experiment('H')
