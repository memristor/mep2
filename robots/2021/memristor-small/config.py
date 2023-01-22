#Small robot 2020 config
from core.Util import *
from modules.sensors.BinaryInfrared import *
from modules.sensors.PressureSensor import *
from modules.sensors.ColorSensor import *
from core.network.Tcp import *
from modules.services.ShareService import *
from modules.drivers.Servo import *
from core.network.Splitter import *

_core.set_robot_size(266,175)


######## Rope Activator ############
from modules.default_config import chinch
chinch.addr = 0x7821
####################################


from modules.default_config import motion_fix

#from modules.default_config import sched_sim


######### Pathfinding #########
from modules.default_config import pathfind
###############################


######### Motion and CAN ######
from modules.default_config import motion, timer
timer.end_time = 100
can = motion.can
###############################


######## Response to collision #######
# from modules.default_config import collision_test
from modules.default_config import collision_wait_suspend
#from modules.default_config import collision_wait
collision_wait_suspend.wait_time = 2
######################################

##### Infrared Sensors ####
_core.add_module([
	BinaryInfrared('prednji desni', (0,-50), (400,-50), packet_stream=can.get_packet_stream(0x80007822)),
	BinaryInfrared('prednji levi', (0,50), (400,50), packet_stream=can.get_packet_stream(0x80007824)),
	BinaryInfrared('zadnji desni', (0, -50), (-400, -50), packet_stream=can.get_packet_stream(0x80007823)),
	BinaryInfrared('zadnji levi', (0, 50), (-400, 50), packet_stream=can.get_packet_stream(0x80007825))
])
###########################

####### Lidar Sensor ######
from modules.default_config import lidar
lidar.tune_angle = -100+180-30+20+20
###########################

#### Pressure Sensors ########
pressure = [ 
	PressureSensor('sp1', 1, can.get_packet_stream(0x80007801, 0x80007800)),
	PressureSensor('sp2', 2, can.get_packet_stream(0x80007802, 0x80007800)),
	PressureSensor('sp3', 2, can.get_packet_stream(0x80007803, 0x80007800)),
	PressureSensor('sp4', 1, can.get_packet_stream(0x80007804, 0x80007800)),
	PressureSensor('sp5', 2, can.get_packet_stream(0x80007805, 0x80007800)),
	PressureSensor('sp6', 2, can.get_packet_stream(0x80007806, 0x80007800))
]
_core.add_module( pressure )
for i in pressure: i.export_cmds(i.name)
##############################

##### Color Sensors #####
color = [
	ColorSensor('levi', 6, can.get_packet_stream(0x80007816, 0x80007810)),
	ColorSensor('desni', 0, can.get_packet_stream(0x80007810, 0x80007810)),
	ColorSensor('rezervni', 4, can.get_packet_stream(0x80007814, 0x80007810))
]
_core.add_module( color )
for i in color: i.export_cmds(i.name)
#########################

######## STATIC OBSTACLES #######
_core.entities.add_entity('static', 'zuta_kamenje', [[600, 850], [580, 850], [580, 1000], [600, 1000]])
_core.entities.add_entity('static', 'plava_kamenje', [[-600, 850], [-620, 850], [-620, 1000], [-600, 1000]])
_core.entities.add_entity('static', 'sredina_kamenje', [[0, 700], [20, 700], [20, 1000], [0, 1000]])

# _core.entities.add_entity('pathfind', 'haos_zona', polygon_square_around_point((-495,45), 220))
# _core.entities.add_entity('pathfind', 'haos_zona_zuta', polygon_square_around_point((495,45), 220))
#################################

#################### SERVOS ###################################
servo_id = 0x80008D70
servo_id = 0x80006c00
servo_stream = can.get_packet_stream(servo_id)
spl=Splitter(servo_stream)
###
servo_izvuci_desno = Servo('servo_izvuci_desno', servo_id=1, packet_stream=spl.get())
servo_izvuci_levo = Servo('servo_izvuci_levo', servo_id=2, packet_stream=spl.get())

servo_gore_desno = Servo('servo_gore_desno', servo_id=3, packet_stream=spl.get())
servo_gore_levo = Servo('servo_gore_levo', servo_id=4, packet_stream=spl.get())

# export commands for each servo (for async control)
servos = [servo_izvuci_desno, servo_izvuci_levo, servo_gore_desno, servo_gore_levo]
for i in servos: i.export_cmds(i.name)
_core.add_module(servos)

@_core.export_cmd
@_core.do
def levo_izvuci(v):
	_e.servo_izvuci_levo.action('GoalPosition', 283 if v == 1 else 601)

@_core.export_cmd
@_core.do
def desno_izvuci(v):
	_e.servo_izvuci_desno.action('GoalPosition', 261 if v == 1 else 570)

@_core.export_cmd
@_core.do
def levo_visina(v):
	_e.servo_gore_levo.action('GoalPosition', [30,350,471][v])

@_core.export_cmd
@_core.do
def desno_visina(v):
	# _e.servo_lfliper.action('GoalPosition', [921,606,504][v])
	_e.servo_gore_desno.action('GoalPosition', [999,700,540][v])

####################################################################

######## Pumps ########
c=can
@_core.export_cmd
@_core.do
def pump(x,v):
	if State.is_sim():
		return
	c.send(bytes([v]) * 5, 0x6c10) if x == 0 else c.send(bytes([v]), 0x6c10+x)
#######################

_core.debug=0

####### Robot Communication ########
from modules.default_config import share,lcd
lcd.init_master()
share.ip = '127.0.0.1' if State.sim else '192.168.1.52'
share.port = 6000
####################################

##### Camera ########
import socket

@_core.export_cmd
def cam_read():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.1.131", 7777))
	msg = s.recv(1024)
	s.close()
	msg = json.loads(msg)

	return msg
#####################


@_core.listen('kill')
def on_kill():
	motion = _core.get_module('Motion')
	motion.stop()

###### round end task ######
@_core.listen('round:end')
def round_end():
	for i in range(1,10):
		_e.pump(i,0)
	_e.r.motoroff()
##########################

######## COORDS ###############

# Definisane tacke
@_core.export_cmd
def coord(c):
	plava = {
		'vetrokazi': (1360, 850),
		'nase_case' : (1360, 720),
		'srednje_blize': (700, -850),
		'srednje_dalje': (-700, -850),
		'mala_luka': (-300, 600),
		'velika_luka': (1000, -200),
		'marina_sever': (1300, -750),
		'marina_jug': (1300, 350),
		'aktivacija_tornja': (1200, -850)

	}
	zuta = {
		'vetrokazi': (-1360, 850),
		'nase_case' : (-1360, 720),
		'srednje_blize': (-700, -850),
		'srednje_dalje': (700, -850),
		'mala_luka': (300, 600),
		'velika_luka': (-1000, -200),
		'marina_sever': (-1300, -750),
		'marina_jug': (-1300, 350),
		'aktivacija_tornja': (-1200, -850)

	}
		
	if State.color == 'zuta':
		return zuta[c]
	else:
		return plava[c]

# coord constants
State.slot1lj = [ (0,0)  ]
State.slot2lj = [ (0,0+i*100) for i in range(6) ]
State.slot1z = [ (0,0+i*100) for i in range(3) ]
State.slot2z = [ (0,0) ]
#################################3


###### ROBOT DEFAULT INITIAL TASK #######

def servo_init():
	servo_izvuci_desno.action('Speed', 250)
	servo_izvuci_levo.action('Speed', 250)
	servo_gore_desno.action('Speed', 250)
	servo_gore_levo.action('Speed', 250)
	
def pids():
	# _e.r.conf_set('stuck_distance_max_fail_count',120)
	# _e.r.conf_set('stuck_rotation_max_fail_count',50)
	return


	
def init_task():
	_e.check_chinch()
	print('Servo speed set')
	
	_e.r.send('R')
	servo_init()
	_e.sleep(0.1)
	_e.r.conf_set('send_status_interval', 10)
	#_e.r.conf_set('send_status_interval', 0)
	_e.r.conf_set('enable_stuck', 0)
	_e._print('init task loaded')
	
	pids()

	_e.r.accel(700)
	_e.r.speed(100)
	

	_e.chinch()
	
	timer.start_timer()


_core.init_task(init_task)
##############################
