from core.Util import *
from core.schedulers.BasicScheduler import *

from core.network.Can import *
from core.network.Uart import *
from core.network.TcpClient import *
from core.network.TcpServer import *
from core.network.packet.SimplePacket import *
from core.network.Splitter import *

from modules.services.CollisionDetector import *
from modules.sensors.Activator import *
from modules.services.ShareService import *
from modules.drivers.Servo import *

from modules.drivers.motion.Motion import *
from modules.sensors.BinaryInfrared import *
from modules.sensors.Lidar import *
from modules.processors.LidarProcessor import *

from .Actuator import Actuator

#  sim = False
sim = True

_core.set_robot_size(300,300)

### CAN and Uart Communication
can = Can() if not sim else Can('can_big')
_core.add_module(can)
uart = Uart() if not sim else can
###

###### Motion driver ###
motion = Motion(packet_stream=can.get_packet_stream(0x80000258))
motion.export_cmds('r')
_core.add_module(motion)
######################

_core.task_manager.set_scheduler( BasicScheduler() )
_core.add_module( CollisionDetector(wait_time=1, size=[-1500, -1000, 3000, 2000]) )

####### Chinch ##################
activator = Activator('pin activator', packet_stream=can.get_packet_stream(0x80008d11))
_core.add_module(activator)
_core.export_cmd('chinch', activator.wait_activator)
#################################

##### Infrared ####
ir1 = BinaryInfrared('back middle', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d12))
ir2 = BinaryInfrared('back left', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d16))
ir3 = BinaryInfrared('front1', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d14))
ir4 = BinaryInfrared('front2', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d13))
_core.add_module([ir1,ir2,ir3,ir4])
cube_det = BinaryInfrared('block detection', (0,0), (0,0), packet_stream=can.get_packet_stream(0x80008d15))
##################

####### CAMERA ######
cam_cols = ['yellow', 'green', 'black', 'blue', 'orange']
cam_tcp = TcpServer(name='camera tcp server', port=5000)
_core.add_module(cam_tcp)

cam_ps = SimplePacket(5, cam_tcp.get_packet_stream())
State.camera = False
def on_cam_recv(pkt):
	d = pkt.decode()
	cols = [cam_cols[int(i)] for i in d.split(',')]
	State.camera = True
	State.combination = cols
	print('camera:', cols)

cam_ps.recv = on_cam_recv
#############################

####### LCD driver #######
if not sim:
	from modules.drivers.LCD import LCD
	lcd=LCD()
	_core.add_module(lcd)
State.points = _State(0)
State.small_points = _State(0)

@_core.do
def addpts(pts):
	print(col.red,'got ',pts, 'points',col.white)
	State.points.val += pts
	print('current points', State.points.val, State.small_points.val, State.points.val + State.small_points.val)
	if not sim:
		lcd.show_pts(State.points.val + State.small_points.val)
_core.export_cmd('addpts', addpts)
##########################

######## SHARE SERVICE ######
tcp = TcpServer(port=3000)
share = ShareService(packet_stream=tcp.get_packet_stream())
share.export_cmds()
_core.add_module([tcp, share])
def share_state_change(name, new_val):
	if name == 'small_points':
		print('received points from small', share.get_state('small_points'), new_val)
		print(col.red,'small ', new_val, 'points',col.white)
		State.small_points = new_val
		print('current points', State.points.val, State.small_points.val, State.points.val + State.small_points.val)
		if not sim:
			lcd.show_pts(State.points.val + State.small_points.val)

share.on_state_change.append(share_state_change)
#############################

######## STATIC OBSTACLES #######
_core.entities.add_entity('static','big_terrain_obstacle',polygon_from_rect([-600,1000-260,1200,260]))
cube_obstacles = [[650, -460], [1200, 190], [400, 500], [-650, -460], [-1200, 190], [-400, 500]]

for i,v in enumerate(cube_obstacles):
	_core.entities.add_entity('static','k'+str(i+1),polygon_square_around_point(v, 58*3))

poles=[ [1500-80, 860-1000], [-(1500-80), 860-1000], [(1500-600), 1000-60], [-(1500-600), 1000-60] ]
for i,v in enumerate(poles):
	_core.entities.add_entity('static','pole'+str(i), polygon_square_around_point(v,100), point=v)
#################################

##### Actuator ###
@_core.do
def pump(x, v):
	can.send(bytes([v,v,v,0,v]), 0x6c10) if x == 0 else can.send(bytes([v]), 0x6c10+x)

_core.export_cmd('pump', pump)

act = Actuator(uart.get_packet_stream(), sim=sim)
_core.add_module(act)
act.export_cmds()
##################

_core.export_cmd('cube_detected', lambda: cube_det.detected)

e=_core.get_exported_commands()

######### BIG pathfind ########
@_core.do
def pathfind(x,y,o=1):
	path = pathfinder.pathfind([x,y])
	path = pathfinder.fix_path(path)
	if not path:
		print('no path: ', x,y)
		e._task_suspend()
	else:
		print('pathfinding: ', path)
	for i in path:
		e.r.goto(*i,o)

_core.export_cmd('pathfind', pathfind)
###############################

future=None
state=0
def default_cmds():
	def on_collision(msg):
		global state, future
		print(col.yellow, 'on collision', col.white)
		if state == 0 and msg == 'danger':
			print('got collision')
			state = 1
			if motion.future:
				future = motion.future
				motion.future = None
				motion.stop(future=None)
		elif state == 1 and msg == 'safe':
			state = 0
			if future:
				future.runable.redo()
				print('resuming')
			print('collision safe')
		
	e._listen('collision', on_collision)
	def rep():
		e.sleep(2)
		e._next_cmd()
	#e._listen('stuck', rep)
#  _core.on('stuck', stuck_behavior)
_core.set_task_setup_func(default_cmds)

###### TIMER #####
async def timer_task():
	time = 0
	while time < 100:
		await asyncio.sleep(1)
		time+=1
		print('time', time)
		if not _core.task_manager.current_task:
			print('no more tasks')
	print('round has ended')
	_core.fullstop()

@_core.do
def start_timer():
	asyncio.ensure_future(timer_task())
##################

#### PID
def init_task():
	e.r.conf_set('send_status_interval', 100)
	e.r.conf_set('wheel_distance', 255.2) #248.47
	e.r.conf_set('wheel_r1', 63.67) #61.92
	e.r.conf_set('wheel_r2', 64)
	
	if not sim:
		e.r.conf_set('pid_d_p', 3.7)
		e.r.conf_set('pid_d_d', 100)
		e.r.conf_set('pid_r_p', 4.0)
		e.r.conf_set('pid_r_d', 150)
		e.r.conf_set('pid_r_i', 0.013)
	
	e.r.conf_set('accel', 600)
	e.r.conf_set('alpha', 550) #650
	
	#  wait_activator()
	#  e.sleep(10)
	
	if not sim:
		e.prepare_lift()
		e._print('initialized')
		act.initialize()
		e._print('rot')
		e.rotate(0)
		e._print('ready')
		e.chinch()
	else:
		e.sleep(3)
	#  e.sleep(10)
	e.send_msg('small_go')
	e._print('started')
	#  e.sleep(100)
	start_timer()

_core.set_init_task(init_task)
