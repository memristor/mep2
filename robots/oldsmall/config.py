
from core.Util import *
from core.schedulers.SimulationScheduler import *
from modules.drivers.motion.Motion import *
from modules.sensors.BinaryInfrared import *

from core.network.Can import *
from core.network.Tcp import *
from modules.sensors.Activator import *
from modules.services.ShareService import *

from modules.drivers.Servo import *
from core.network.Splitter import *

sim = True
#  sim = False

_core.set_robot_size(290,160)

# _core.task_manager.set_scheduler( SimulationScheduler() )

from modules.default_config import motion, timer, chinch, share, lidar, collision_pathfind
can=_core.get_module('Can')
can.iface='can1' if sim else 'can0'

##### Infrared ####
_core.add_module([
	BinaryInfrared('back1', (-80,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d13)), 
	BinaryInfrared('back2', (-80,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d14)),
	BinaryInfrared('front left', (80,0), (195+100,0), packet_stream=can.get_packet_stream(0x80008d15)),
	BinaryInfrared('front middle', (80,0), (120+100,0), packet_stream=can.get_packet_stream(0x80008d16))])
###################


############# SERVOS ###########
servo_stream = can.get_packet_stream(0x00008D70)
servo_streams=Splitter(servo_stream)

servo_klapna = Servo('klapna', servo_id=3, packet_stream=servo_streams.get())
servo_cev = Servo('cev', servo_id=5, packet_stream=servo_streams.get())
servo_cev2 = Servo('cev2', servo_id=20, packet_stream=servo_streams.get())
servo_prekidac = Servo('prekidac', servo_id=1, packet_stream=servo_streams.get())
servo_pcelica = Servo('pcelica', servo_id=7, packet_stream=servo_streams.get())
_core.add_module([servo_klapna, servo_cev, servo_cev2, servo_prekidac, servo_pcelica])

_core.export_ns('')
@_core.export_cmd
@_core.do
def klapna(v):
	servo_klapna.action('GoalPosition', 85 if v == 1 else 225)

@_core.export_cmd
@_core.do
def cev2(v):
	servo_cev2.action('GoalPosition', 130 if v == 0 else 200)

@_core.export_cmd
@_core.do
def cev(v):
	servo_cev.action('GoalPosition', 805 if v == 0 else 703)

@_core.export_cmd
@_core.do
def prekidac(v):
	servo_prekidac.action('GoalPosition', 272 if v == 0 else 0)

@_core.export_cmd
@_core.do
def pcelica(v):
	servo_pcelica.action('GoalPosition', 815 if v == 1 else (600 if v == 2 else 221))

@_core.export_cmd
@_core.do
def turbina(x):
	can.send(bytes([x]), 0x8d53)
##################

######## SHARE SERVICE ########
# if not sim:
	# tcp = Tcp(ip='192.168.6.1', port=3000)
# else:
	# tcp = Tcp(ip='127.0.0.1', port=3000)
# share = ShareService(packet_stream=tcp.get_packet_stream())
# share.export_cmds()
# _core.add_module([tcp,share])
##############################

######## STATIC OBSTACLES #######
_core.entities.add_entity('static','big_terrain_obstacle',polygon_from_rect([-600,1000-260,1200,260]))
cube_obstacles = [[650, -460], [1200, 190], [400, 500], [-650, -460], [-1200, 190], [-400, 500]]

for i,v in enumerate(cube_obstacles):
	_core.entities.add_entity('static','k'+str(i+1),polygon_square_around_point(v, 58*3))

poles=[ [1500-80, 860-1000], [-(1500-80), 860-1000], [(1500-600), 1000-60], [-(1500-600), 1000-60] ]
for i,v in enumerate(poles):
	_core.entities.add_entity('static','pole'+str(i), polygon_square_around_point(v,100), point=v)
#################################

#### Send Points to BIG robot #####
share.set_state('small_points', 0)

@_core.do
def addpts(pts):
	_e.set_state('small_points', _e.get_state('small_points')+pts)
_core.export_cmd('addpts', addpts)
#####################################

_core.entities.remove_entity('k5')

###### ROBOT DEFAULT INITIAL TASK #######
@_core.init_task
def init_task():
	print('running init task')
	_e.r.send(b'R')
	_e.r.speed(50)
	_e.r.accel(250)
	_e.r.conf_set('send_status_interval', 10)
	_e.r.conf_set('enable_stuck', 0)
	_e.set_state('small_points', 0)
	if not sim:
		_e.r.conf_set('pid_d_p', 2.75)
		_e.r.conf_set('pid_d_d', 90)
		_e.r.conf_set('pid_r_p', 1.5)
		_e.r.conf_set('pid_r_d', 100)

	_e.r.conf_set('accel', 250)
	_e.r.conf_set('alpha', 250)
	
	### GO MSG ###
	def listen_msg(msg):
		print('listen msg', msg)
		if msg == 'small_go':
			_e._label('go')
		if msg == 'continue':
			_e._label('continue')
	_e._listen('message', listen_msg)
	_e._print('waiting go signal')
	#_e._sync('go')
	_e._print('go go go')
	##############
	if not sim:
		_e.chinch()
	else:
		_e.sleep(3)
	timer.start_timer()
	
##############################
