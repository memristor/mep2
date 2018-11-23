
from core.Util import *
from core.schedulers.BasicScheduler import *
from modules.drivers.motion.Motion import *
from modules.sensors.BinaryInfrared import *

from modules.sensors.Lidar import *
from modules.processors.LidarProcessor import *

from modules.services.CollisionDetector import *
from core.network.Can import *
from core.network.TcpClient import *
from modules.sensors.Activator import *
from modules.services.ShareService import *

from modules.drivers.Servo import *
from core.network.Splitter import *

sim = True
#  sim = False

_core.set_robot_size(290,160)

can = Can('can_small' if sim else 'can0')
_core.add_module(can)

###### MOTION DRIVER #######
motion = Motion(packet_stream=can.get_packet_stream(0x80000258))
motion.export_cmds('r')
_core.add_module(motion)
############################

######## Collision detection service ########
_core.add_module( CollisionDetector(wait_time=1, size=[-1500, -1000, 3000, 2000]) )
###################################

####### Chinch activator ##################
activator = Activator('pin activator', packet_stream=can.get_packet_stream(0x80008d11))
_core.add_module(activator)
_core.export_ns('')
_core.export_cmd('chinch', activator.wait_activator)
############################################

##### Infrared ####
ir2 = BinaryInfrared('back1', (-80,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d13))
ir3 = BinaryInfrared('back2', (-80,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d14))
ir4 = BinaryInfrared('front left', (80,0), (195+100,0), packet_stream=can.get_packet_stream(0x80008d15))
ir5 = BinaryInfrared('front middle', (80,0), (120+100,0), packet_stream=can.get_packet_stream(0x80008d16))
_core.add_module([ir2, ir3, ir4])
##################

############# LIDAR ###########
lidar = Lidar(tune_angle=-180+10, packet_stream=can.get_packet_stream(0x80007e00))
_core.add_module([lidar, LidarProcessor()])
###############################

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
if not sim:
	tcp = TcpClient(ip='192.168.6.1', port=3000)
else:
	tcp = TcpClient(ip='127.0.0.1', port=3000)
share = ShareService(packet_stream=tcp.get_packet_stream())
share.export_cmds()
_core.add_module([tcp,share])
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

##### PATHFINDING ######
from modules.services.PathfinderService import *
pathfinder = PathfinderService()
_core.add_module(pathfinder)

def pathfind(x,y,o=1):
	path = pathfinder.pathfind([x,y])
	#  path = pathfinder.fix_path(path)
	if not path:
		print('no path: ', x,y)
		return False
	else:
		print('pathfinding: ', path)
	for pt in path:
		_e.r.goto(*pt,0)
		# _e.r.move(*i,150,0)
	return True
		
pathfinder.prepare_pathfinder()
_core.export_cmd('pathfind', pathfind)
############################

#### Send Points to BIG robot #####
share.set_state('small_points', 0)

@_core.do
def addpts(pts):
	_e.set_state('small_points', _e.get_state('small_points')+pts)
_core.export_cmd('addpts', addpts)
#####################################

########## TASK INITIALIZATION ##############
future=None
sap=None
state=0
def robot_behavior():
	def on_collision(msg):
		global state, future, sap
		if state == 0 or msg == 'danger':
			print(col.yellow, 'got collision', col.white)
			state = 1
			#  assert motion.future != None
			if motion.future:
				future = motion.future
				motion.future = None
				motion.stop(_future=None)
				
			def sleep_and_suspend():
				global sap,future
				future = None
				# print('suspending')
				_core.task_manager.get_current_task().suspend()
				state = 0
				sap = None
				
			if True and not sap:
				sap = _core.loop.call_later(2, sleep_and_suspend)
		elif state == 1 and msg == 'safe':
			state = 0
			if future:
				future.runable.redo()
			else:
				print('no future')
			if sap:
				sap.cancel()
				sap = None
			print('collision safe')
			
	def on_stuck():
		future = motion.future
		#  motion.future = None
		task = _core.task_manager.get_current_task()
		task.pause()
		#  motion.forward(-100, future=None)
		def wr():
			_e.sleep(2)
			_e._do(task.resume)
		_e._do(wr)
		print('got stuck')
		#  if future:
			#  future.runable.redo()
	
	_e._listen('collision', on_collision)
	#  _e._listen('stuck', on_stuck, _insync=True)	

_core.task_setup_func(robot_behavior)
##########################################

###### TIMER #####
async def timer_task():
	time = 0
	# round_time = 100
	round_time = 200
	while time < round_time:
		await asyncio.sleep(1)
		print('time', time)
		time+=1
	_core.fullstop()
	while True:
		print('round has ended', time)
		await asyncio.sleep(1)
		time+=1

@_core.do
def start_timer():
	asyncio.ensure_future(timer_task())
##################


###### ROBOT DEFAULT INITIAL TASK #######
@_core.init_task
def init_task():
	_e.r.send(b'R')
	_e.r.conf_set('send_status_interval', 100)
	_e.r.conf_set('enable_stuck', 0)
	_e.r.conf_set('wheel_r1', 68.0)
	_e.r.conf_set('wheel_r2', 67.25513)
	_e.r.conf_set('wheel_distance', 252.30)

	if not sim:
		_e.r.conf_set('pid_d_p', 2.75)
		_e.r.conf_set('pid_d_d', 90)
		#  _e.r.conf_set('pid_d_d', 200)
		_e.r.conf_set('pid_r_p', 1.5)
		#  _e.r.conf_set('pid_r_p', 1.2)
		_e.r.conf_set('pid_r_d', 100)

	_e.r.conf_set('pid_r_i', 0.0)
	_e.r.conf_set('accel', 600)
	_e.r.conf_set('alpha', 600)
	
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
	start_timer()
	
##############################
