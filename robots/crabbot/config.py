from modules.drivers.Servo import *
from modules.sensors.BinaryInfrared import *
from modules.sensors.PressureSensor import *
from modules.sensors.TOFSensor import *
from core.network.Tcp import *
from core.network.Uart import *
from core.network.Splitter import *

#VELIKIII
_core.debug = 0


######### Pathfinding #########
from modules.default_config import pathfind
###############################

######### Motion #############
from modules.default_config import motion, motion_fix
motion.can.iface = 'can0' 
can=motion.can

# big robot using old curve_rel ?
a=_e.r.curve_rel
def mod_curve_rel(radius, angle, *args):
	a(radius//2, angle, *args)
with _core.export_ns('r'):
	_core.export_cmd('curve_rel', mod_curve_rel)
########################################


from modules.default_config import collision_wait

############ Activator ##################
from modules.default_config import chinch
chinch.addr = 0x80007f11
#########################################

##### Infrared Sensors ####
_core.add_module([
	BinaryInfrared('zadnji levi', (-200,120), (-300,120), packet_stream=can.get_packet_stream(0x00008d15)),
	BinaryInfrared('zadnji desni', (-200,-120), (-300,-120), packet_stream=can.get_packet_stream(0x00008d13)),
	BinaryInfrared('prednji levi', (60, 100), (300,100), packet_stream=can.get_packet_stream(0x00008d12)),
	BinaryInfrared('prednji desni', (60, -100), (300, -100), packet_stream=can.get_packet_stream(0x00008d15)),
])
###########################

##### Lidar Sensors #######
from modules.default_config import lidar
###########################


########### Pumps ###################
@_core.export_cmd
@_core.do
def pump(x, v):
	can.send(bytes([v])*5, 0x6c10) if x == 0 else can.send(bytes([v]), 0x6c10+x)
#####################################

################### SERVOS #######################
servo_id = 0x80006c00
uart = Uart(baud='57142')
uart_stream = uart.get_stream()
spl = Splitter(uart_stream)

def uart_recv(m):
	print('uart recv',m)

spl.get().recv = uart_recv
_core.add_module(uart)

servos = [
	Servo('s_sgl', servo_id=1, packet_stream=spl.get(), raw_packet=True)
	, Servo('s_sgd', servo_id=2 , packet_stream=spl.get(), raw_packet=True)
	, Servo('s_sdl', servo_id=3, packet_stream=spl.get(), raw_packet=True)
	, Servo('s_sdd', servo_id=4, packet_stream=spl.get(), raw_packet=True)
	, Servo('r_fliper', servo_id=23, packet_stream=spl.get(), raw_packet=True)
	, Servo('l_fliper', servo_id=22 , packet_stream=spl.get(), raw_packet=True)
	, Servo('servo_lift', servo_id=10, packet_stream=spl.get(), raw_packet=True)#11
	#, Servo('servo_lift', servo_id=10, packet_stream=spl.get(), raw_packet=True)
]

# export servo commands
for i in servos:
	i.export_cmds(i.name)
_core.add_module(servos)


@_core.do
def init_servos():
	# init wheel mode
	_e.servo_lift.wheelspeed(0)
#_e.servo_rlift.wheelspeed(0)
	pass


@_core.export_cmd
@_core.do
def rfliper(v):
	_e._print("Poslao desnom servou", v)
	_e.r_fliper.action('GoalPosition',[228,550][v])
	_e.sleep(0.7)


@_core.export_cmd
@_core.do
def sgd(v):
	_e._print("Poslao gornjem  desnom servou", v)
	_e.s_sgd.action('GoalPosition', [700,485,300][v])
	_e.sleep(0.7)

@_core.export_cmd
@_core.do
def sgl(v):
	_e._print("Poslao gornjem levom servou", v)
	_e.s_sgl.action('GoalPosition', [0,220,290][v])
	_e.sleep(0.7)


@_core.export_cmd
@_core.do
def sdd(v):
	_e._print("Poslao donjem desnom servou", v)
	_e.s_sdd.action('GoalPosition', [267,500,675][v])
	_e.sleep(0.7)



@_core.export_cmd
@_core.do
def sdl(v):
	_e._print("Poslao donjem levom servou", v)
	_e.s_sdl.action('GoalPosition', [752,510,326][v])
	_e.sleep(0.7)


@_core.export_cmd
@_core.do
def lfliper(v):
	_e._print("Poslao levom servou")
	_e.l_fliper.action('GoalPosition', [212,430,500][v])
	_e.sleep(0.7)




# @_core.export_cmd
# @_core.do
# def dlift(v):
# 	_e._print("Poslao desnom liftu")
# 	_e.servo_rfliper.action('GoalPosition', [880,650,575][v])
# 	_e.sleep(0.7)

########## LIFT ####################
@_core.export_cmd
@_core.do
def lift(v):
	_e._reset_label('servo_lift')
	_e._print('servo_lift', v)
	_e.servo_lift.wheelspeed(-1023 if v==1 else 1023)
	# lets use labels for short improvisation of async command (_future)
	if not State.sim:
		_e._sync('servo_lift')
	
# @_core.export_cmd
# @_core.do
# def rlift(v):
	# _e._reset_label('servo_rlift')
	# _e._print('servo_rlift', v)
	# _e.servo_rlift.wheelspeed(1023 if v==1 else -1023)
	# # lets use labels for short improvisation of async command (_future)
	# if not State.sim:
		# _e._sync('servo_rlift')
# communication with gpio interrupt process which have sudo rights
from core.network.packet.SimplePacket import SimplePacket
# sudo python3 /home/memristor/gpio/interrupt2.py is listening at 3500, process which sends interrupts
# this process is ran from /etc/rc.local at boot
tcp_gpio = Tcp(name='gpio_communicator', ip='127.0.0.1', port=3500)
# simple packet with length of 2 bytes (to packetize tcp continual stream)
gp = SimplePacket(3, tcp_gpio.get_packet_stream())
_core.add_module(tcp_gpio)

# interrupt receiever
def gpio_recv(c):
	c=c.decode()
	c,v = c[:2], c[2]
	# spawn thread task independent
	@_core.spawn_side
	def _():
		v=500	#800	
		up_sw1 = '06'
		down_sw1 = '13'
		# 05 = left down, 06 = left up
		if c in (down_sw1, up_sw1):
			v = -v if c == down_sw1 else v
			# move back a little, to leave switch
			_e.servo_lift.wheelspeed(v)
			_e.sleep(0.15)
			_e.servo_lift.wheelspeed(0)
			# must use _do because _core.spawn is not in _e
			@_e._do
			def _():
				# spawn label from "sidetask" into active task
				@_core.spawn
				def _():
					_e._L('servo_lift')	

					
gp.recv = gpio_recv

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


######## Round End Task #########
@_core.listen('round:end')
def round_end():
	for i in range(1,10):
		_e.pump(i,0)
	_e.r.motoroff()
#################################

def init_pids():
	if not State.sim:
		_e.r.conf_set('stuck_distance_max_fail_count',120)
		_e.r.conf_set('stuck_rotation_max_fail_count',100)
		_e.r.conf_set('stuck_rotation_jump',20)
		_e.r.conf_set('stuck_distance_jump',50)
		_e.r.conf_set('wheel_r1', 72.64)
		_e.r.conf_set('wheel_r2', 72.7)
		_e.r.conf_set('wheel_distance', 259.22)
		_e.r.conf_set('pid_d_p', 1.4)
		_e.r.conf_set('pid_d_d', 70)
		_e.r.conf_set('pid_r_p', 1.4)
		_e.r.conf_set('pid_r_d', 70)
		_e.r.conf_set('pid_d_i', 0.005)
		_e.r.conf_set('pid_r_i', 0.005)
		_e.r.conf_set('enable_stuck', 1)

###### ROBOT INITIAL TASK #######
@_core.init_task
def init_task():
	State.pumpe = [_State(0) for i in range(10)]
	
#	_e.check_chinch()
	
	init_servos()
	
	init_pids()

	_e.r.send('R')
	_e.r.conf_set('send_status_interval', 0)
	_e.r.speed(125)
	_e.r.accel(1000)
	
	_e.r.conf_set('alpha', 1000)
#_e.chinch()

	_e._label('go')
	timer.start_timer()

	

