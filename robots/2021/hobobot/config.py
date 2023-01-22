from modules.drivers.Servo import *
from modules.sensors.BinaryInfrared import *
#from modules.sensors.PressureSensor import *
#from modules.sensors.TOFSensor import *
from core.network.Tcp import *
from core.network.Splitter import *

#VELIKIII
_core.debug = 0


######### Pathfinding #########
from modules.default_config import pathfind
###############################

##### Motion #######
from modules.default_config import motion, motion_fix
motion.can.iface = 'can0' 
can=motion.can

'''
# big robot using old curve_rel
a=_e.r.curve_rel
def mod_curve_rel(radius, angle, *args):
	a(radius//2, angle, *args)
with _core.export_ns('r'):
	_core.export_cmd('curve_rel', mod_curve_rel)
'''
####################


from modules.default_config import collision_wait

############ Activator ##################
from modules.default_config import chinch
chinch.addr = 0x80007f11
#########################################

##### Infrared Sensors ####
_core.add_module([
	BinaryInfrared('zadnji levi', (-200,120), (-300,120), packet_stream=can.get_packet_stream(0x80008d14)),
	BinaryInfrared('zadnji desni', (-200,-120), (-300,-120), packet_stream=can.get_packet_stream(0x80008d15)),

	# TODO
	BinaryInfrared('prednji levi', (-200,-120), (-300,-120), packet_stream=can.get_packet_stream(0x80008d20)),
	BinaryInfrared('prednji desni', (-200,-120), (-300,-120), packet_stream=can.get_packet_stream(0x80008d21)),
])
###########################

##### Lidar Sensors #######
from modules.default_config import lidar
###########################



################### SERVOS #######################
servo_id = 0x80006c00
spl = Splitter(can.get_packet_stream(servo_id))
c_servos  = [Servo('c'+str(i), servo_id=i, packet_stream=spl.get()) for i in range(1,6)]

#servo_llift  = Servo('servo_llift', servo_id=21, packet_stream=spl.get())
#servo_rlift = Servo('servo_rlift', servo_id=22, packet_stream=spl.get())
#servo_lfliper = Servo('servo_lfliper', servo_id=25, packet_stream=spl.get())
#servo_rfliper = Servo('servo_rfliper', servo_id=2, packet_stream=spl.get()) 

# export servo commands
servos = [servo_llift, servo_rlift, servo_lfliper, servo_rfliper]
servos += c_servos

for servo in servos:
	servo.export_cmds(servo.name)

_core.add_module(servos)

# communication with gpio interrupt process which have sudo rights
from core.network.packet.SimplePacket import SimplePacket
# sudo python3 /home/memristor/gpio/interrupt2.py is listening at 3500, process which sends interrupts
# this process is ran from /etc/rc.local at boot
tcp_gpio = Tcp(name='gpio_communicator', ip='127.0.0.1', port=3500)
# simple packet with length of 2 bytes (to packetize tcp continual stream)
gp = SimplePacket(2, tcp_gpio.get_packet_stream())
_core.add_module(tcp_gpio)


# interrupt receiever
def gpio_recv(c):
	c=c.decode()

	# spawn thread task independent
	@_core.spawn_side
	def _():
		v=800 # servo speed	
		# 05 = left down, 06 = left up
		up_switch = '06'
		down_switch = '05'
		if c in (up_switch, down_switch):
			v = -v if c == down_switch else v
			# move back a little, to leave switch
			_e.servo_llift.wheelspeed(v)
			_e.sleep(0.15)
			_e.servo_llift.wheelspeed(0)
			# must use _do because _core.spawn is not in _e
			@_e._do
			def _():
				# spawn label from "sidetask" into active task
				@_core.spawn
				def _():
					_e._L('servo_llift')	

					
gp.recv = gpio_recv

@_core.do
def init_servos():
#servo_lfliper.action('Speed', 200)
#	servo_rfliper.action('Speed', 200)

	# init wheel mode
	_e.servo_llift.wheelspeed(0)
	_e.servo_rlift.wheelspeed(0)

@_core.export_cmd
@_core.do
def llift(v):
	_e._reset_label('servo_llift')
	_e._print('servo_llift', v)
	_e.servo_llift.wheelspeed(-1023 if v==1 else 1023)
	# lets use labels for short improvisation of async command (_future)
	if not State.sim:
		_e._sync('servo_llift')
	
@_core.export_cmd
@_core.do
def rlift(v):
	_e._reset_label('servo_rlift')
	_e._print('servo_rlift', v)
	_e.servo_rlift.wheelspeed(1023 if v==1 else -1023)
	# lets use labels for short improvisation of async command (_future)
	if not State.sim:
		_e._sync('servo_rlift')

@_core.export_cmd
@_core.do
def rfliper(v):
	# _e.servo_rfliper.action('GoalPosition', [20,289,424][v])
#return
	_e._print("Poslao desnom servou")
	_e.servo_rfliper.action('GoalPosition', [880,650,575][v])
	_e.sleep(0.7)

@_core.export_cmd
@_core.do
def lfliper(v):
	# _e.servo_lfliper.action('GoalPosition', [921,606,504][v])
#return
	_e._print("Poslao levom servou")
	_e.servo_lfliper.action('GoalPosition', [212,430,500][v])
	_e.sleep(0.7)
#################################################


######## STATIC OBSTACLES #######
_core.entities.add_entity('static', 'zuta_kamenje', [[600, 850], [580, 850], [580, 1000], [600, 1000]])
_core.entities.add_entity('static', 'plava_kamenje', [[-600, 850], [-620, 850], [-620, 1000], [-600, 1000]])
_core.entities.add_entity('static', 'sredina_kamenje', [[0, 700], [20, 700], [20, 1000], [0, 1000]])
#################################



####### Share and Timer ########
from modules.default_config import share, timer
share.port = 6000
timer.end_time = 100
################################


######### addpts ##########
from modules.default_config import lcd
###########################


############### Coordinates ################# Definisane tacke
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
############################################

######## Point Constants ##########
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
# tcp_experiment = Tcp(name='experiment', ip='127.0.0.1', port=8000)
# pt = tcp_experiment.get_packet_stream()
# _core.add_module(tcp_experiment)
# @_core.export_cmd
# @_core.do
# def experiment(v):
	# pt.send(v.encode())
##########################


def init_pids():
	if not State.sim:
		_e.r.conf_set('stuck_distance_max_fail_count',120)
		_e.r.conf_set('stuck_rotation_max_fail_count',100)
		_e.r.conf_set('stuck_rotation_jump',20)
		_e.r.conf_set('stuck_distance_jump',50)
		_e.r.conf_set('wheel_r1', 71.5)
		_e.r.conf_set('wheel_r2', 70.8)
		_e.r.conf_set('wheel_distance', 260.55)
		_e.r.conf_set('pid_d_p', 1.5) 
		_e.r.conf_set('pid_d_d', 75)
		_e.r.conf_set('pid_r_p', 1.5)
		_e.r.conf_set('pid_r_d', 75)
		_e.r.conf_set('pid_d_i', 0.005)
		_e.r.conf_set('pid_r_i', 0.005)
		_e.r.conf_set('enable_stuck', 1)

###### ROBOT INITIAL TASK #######
@_core.init_task
def init_task():
	_e.check_chinch()
	
	init_servos()
	
	init_pids()
	_e.r.send('R')
	_e.r.conf_set('send_status_interval', 0)
	_e.r.speed(30)
	_e.r.accel(1000)
	
	_e.r.conf_set('alpha', 1000)
	_e.chinch()
	timer.start_timer()

