from core.Util import *
from core.network.packet.SimplePacket import *
from modules.drivers.Servo import *
from modules.sensors.BinaryInfrared import *

# sim = False
sim = True

_core.set_robot_size(300,300)
from modules.default_config import motion, timer, chinch, share, collision_wait_suspend
can = _core.get_module('Can')

##### Infrared ####
_core.add_module([
	BinaryInfrared('back middle', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d12)),
	BinaryInfrared('back left', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d16)),
	BinaryInfrared('front1', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d14)),
	BinaryInfrared('front2', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d13))])
cube_det = BinaryInfrared('block detection', (0,0), (0,0), packet_stream=can.get_packet_stream(0x80008d15))
##################

####### CAMERA ######
from core.network.Tcp import *
cam_tcp = Tcp(name='camera tcp server', port=5000)
_core.add_module(cam_tcp)

cam_cols = ['yellow', 'green', 'black', 'blue', 'orange']
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
'''
if not sim:
	from modules.drivers.LCD import LCD
	lcd=LCD()
	_core.add_module(lcd)
'''
State.points = _State(0)
State.small_points = _State(0)

@_core.export_cmd
@_core.do
def addpts(pts):
	if not sim:
		print(col.red,'got ',pts, 'points',col.white)
		State.points.val += pts
		print('current points', State.points.val, State.small_points.val, State.points.val + State.small_points.val)
		lcd.show_pts(State.points.val + State.small_points.val)
##########################

######## SHARE SERVICE ######
@_core.listen('share:state_change')
def share_state_change(name, new_val):
	if name == 'small_points':
		print('received points from small', share.get_state('small_points'), new_val)
		print(col.red,'small ', new_val, 'points',col.white)
		State.small_points = new_val
		print('current points', State.points.val, State.small_points.val, State.points.val + State.small_points.val)
		if not sim: lcd.show_pts(State.points.val + State.small_points.val)
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
@_core.export_cmd
@_core.do
def pump(x, v):
	can.send(bytes([v,v,v,0,v]), 0x6c10) if x == 0 else can.send(bytes([v]), 0x6c10+x)
from .Actuator import Actuator
act = Actuator(sim=sim)
_core.add_module([act])
##################

_core.export_cmd('cube_detected', lambda: cube_det.detected)

#### PID
@_core.init_task
def init_task():
	_e.r.conf_set('send_status_interval', 100)
	_e.r.conf_set('wheel_distance', 255.2) #248.47
	_e.r.conf_set('wheel_r1', 63.67) #61.92
	_e.r.conf_set('wheel_r2', 64)
	
	if not sim:
		_e.r.conf_set('pid_d_p', 3.7)
		_e.r.conf_set('pid_d_d', 100)
		_e.r.conf_set('pid_r_p', 4.0)
		_e.r.conf_set('pid_r_d', 150)
		_e.r.conf_set('pid_r_i', 0.013)
	_e.r.speed(40)
	_e.r.accel(600)
	_e.r.conf_set('accel', 600)
	_e.r.conf_set('alpha', 600) #650
	
	if not sim:
		# _e.prepare_lift()
		_e._print('initialized')
		act.initialize()
		_e._print('rot')
		# _e.rotate(0)
		_e._print('ready')
	else:
		_e.sleep(3)
	_e.send_msg('small_go')
	_e._print('started')
	timer.start_timer()


