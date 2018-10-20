from core.Core import *
from core.Util import *
from core.schedulers.BasicScheduler import *
from modules.drivers.motion.Motion import *
from modules.sensors.BinaryInfrared import *

from modules.sensors.Lidar import *
from modules.processors.LidarProcessor import *

from modules.services.CollisionDetector import *
from core.network.Can import *
from core.network.Uart import *
from core.network.TcpClient import *
from core.network.TcpServer import *
from core.network.packet.SimplePacket import *
from modules.sensors.Activator import *
from modules.services.ShareService import *
import core.State as State
from modules.drivers.Servo import *
from core.network.Splitter import *

from .Actuator import Actuator


print('robot configured')

#  sim = False
sim = True

core = Core()
core.set_robot_size(300,300)

### communication
if sim:
	can = Can('can1')
else:
	can = Can()

core.add_module(can)

if not sim:
	uart = Uart()
else:
	uart = can
ps = uart.get_packet_stream()
core.add_module(uart)
###


###### Motion driver ###
motion = Motion()
motion.set_packet_stream(can.get_packet_stream(0x80000000 | 600))
core.add_module(motion)
core.export_ns('r')
motion.export_cmds()
core.export_ns('')
######################

sched = BasicScheduler()
core.task_manager.set_scheduler(sched)

col = CollisionDetector(1, size=[-1500, -1000, 3000, 2000])
core.add_module(col)


####### Chinch ##################
activator = Activator('pin activator', packet_stream=can.get_packet_stream(0x80008d11))
core.add_module(activator)
core.export_ns('')
core.export_cmd('chinch', activator.wait_activator)
#################################

##### Infrared ####
ir1 = BinaryInfrared('back middle', (0,0), (-500,0))
ir1.set_packet_stream(can.get_packet_stream(0x80008d12))
core.add_module(ir1)

ir2 = BinaryInfrared('back left', (0,0), (-500,0))
ir2.set_packet_stream(can.get_packet_stream(0x80008d16))
core.add_module(ir2)

#  ir5 = BinaryInfrared('back corner', (0,0), (-500,0))
#  ir5.set_packet_stream(can.get_packet_stream(0x80008d15))
#  core.add_module(ir5)
cube_det = BinaryInfrared('block detection', (0,0), (0,0))
cube_det.set_packet_stream(can.get_packet_stream(0x80008d15))

ir3 = BinaryInfrared('front1', (0,0), (500,0))
ir3.set_packet_stream(can.get_packet_stream(0x80008d14))
core.add_module(ir3)

ir4 = BinaryInfrared('front2', (0,0), (500,0))
ir4.set_packet_stream(can.get_packet_stream(0x80008d13))
core.add_module(ir4)
##################

####### CAMERA ######
cam_cols = ['yellow', 'green', 'black', 'blue', 'orange']
cam_tcp = TcpServer(name='camera tcp server', port=5000)
core.add_module(cam_tcp)

cam_ps = SimplePacket(5, cam_tcp.get_packet_stream())
State.camera = False
def on_cam_recv(pkt):
	d = pkt.decode()
	cols = [cam_cols[int(i)] for i in d.split(',')]
	State.camera = True
	State.combination = cols
	print('camera:',cols)

cam_ps.recv = on_cam_recv
#############################



@asyn2
def pump(x, v):
	if x == 0:
		can.send(bytes([v,v,v,0,v]), 0x6c10+x)
	else:
		can.send(bytes([v]), 0x6c10+x)
core.export_ns('')
core.export_cmd('pump', pump)

####### LCD driver #######
if not sim:
	from modules.drivers.LCD import LCD
	lcd=LCD()
	core.add_module(lcd)
State.points = 0
State.small_points = 0
@do
def addpts(e,pts):
	print('\x1b[31mgot ',pts, 'points\x1b[0m')
	State.points += pts
	print('current points', State.points, State.small_points, State.points + State.small_points)
	if not sim:
		lcd.show_pts(State.points + State.small_points)
core.add_sync_cmd('addpts', addpts)
##########################

######## SHARE SERVICE ######
tcp = TcpServer(port=3000)
core.add_module(tcp)
share = ShareService(packet_stream=tcp.get_packet_stream())
core.add_module(share)
share.export_cmds()
def share_state_change(name, new_val):
	if name == 'points':
		print('received points from small',share.get_state('points'), new_val)
		print('\x1b[31msmall ', new_val, 'points\x1b[0m')
		State.small_points += new_val
		print('current points', State.points, State.small_points, State.points + State.small_points)
		if not sim:
			lcd.show_pts(State.points + State.small_points)

share.on_state_change.append(share_state_change)
#############################

######## STATIC OBSTACLES #######
core.entities.add_entity('static','big_terrain_obstacle',polygon_from_rect([-600,1000-260,1200,260]))
kocke = [[650, -460], [1200, 190], [400, 500], [-650, -460], [-1200, 190], [-400, 500]]

for i,v in enumerate(kocke):
	core.entities.add_entity('static','k'+str(i+1),polygon_square_around_point(v, 58*3))

core.entities.add_entity('static','pole1' ,polygon_square_around_point([1500-80, 860-1000],100), point=[1500-80, 860-1000])
core.entities.add_entity('static','pole2' ,polygon_square_around_point([-(1500-80), 860-1000],100), point=[-(1500-80), 860-1000])
core.entities.add_entity('static','pole3' ,polygon_square_around_point([(1500-600), 1000-60],100), point=[1500-600, 1000-60])
core.entities.add_entity('static','pole4' ,polygon_square_around_point([-(1500-600), 1000-60],100), point=[-(1500-600), 1000-60])
#################################



##### Actuator ###
act = Actuator(uart.get_packet_stream(), sim=sim)
core.add_module(act)
act.export_cmds()
##################



e=core.get_exported_commands()

core.export_ns('')
def build_cubes(color):
	with e.disabler('collision'):
		for i in enumerate(color):
			e.lift(max(1, i[0]))
			e.unload(i[1],i[0] == 0)
		e.lift(3)
		e.unload(e.get_remaining_pump(color))
core.add_sync_cmd('build_cubes', build_cubes)

def cube_detection():
	return cube_det.detected
	
core.add_sync_cmd('cube_detected', cube_detection)

e=core.get_exported_commands()
    





######### BIG pathfind ########
@do
def pathfind(e, x,y,o=1):
	path = pathfinder.pathfind([x,y])
	path = pathfinder.fix_path(path)
	if not path:
		print('no path: ', x,y)
		e._task_suspend()
	else:
		print('pathfinding: ', path)
	#  e.r.speed(80)
	for i in path:
		e.r.goto(*i,o)
		
core.export_ns('')
core.add_sync_cmd('pathfind', pathfind)
###############################

future=None
state=0
def default_cmds():
	def on_collision(msg):
		global state, future
		print('\x1b[33mon collision\x1b[0m')
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
	
#  core.on('stuck', stuck_behavior)
core.set_task_setup_func(default_cmds)

###### TIMER #####
async def timer_task():
	time = 0
	while time < 100:
		await asyncio.sleep(1)
		time+=1
		print('time', time)
		if not core.task_manager.current_task:
			print('no more tasks')
	print('round has ended')
	#  motion.fullstop()
	#  act.fullstop()
	core.fullstop()

@do
def start_timer(e):
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
		# e.prepare_lift()
		e._do(lambda: print('initialized'))
		e._do(act.initialize)
	
		e._do(lambda: print('rot'))
		e.rotate(0)
		e._do(lambda: print('ready'))
		e.chinch()
	else:
		e.sleep(3)
	#  e.sleep(10)
	e.send_msg('small_go')
	e._do(lambda: print('started'))
	#  e.sleep(100)
	start_timer()

core.task_manager.set_init_task(init_task)
