from core.Core import *
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

core = Core()
core.set_robot_size(290,160)

can = Can()
core.add_module(can)

###### MOTION DRIVER #######
motion = Motion(packet_stream=can.get_packet_stream(0x80000258))
core.export_ns('r')
core.add_module(motion)
motion.export_cmds()
############################

sched = BasicScheduler()
core.task_manager.set_scheduler(sched)

######## Collision detection service ########
col = CollisionDetector(wait_time=1, size=[-1500, -1000, 3000, 2000])
core.add_module(col)
###################################

####### Chinch activator ##################
activator = Activator('pin activator', packet_stream=can.get_packet_stream(0x80008d11))
core.add_module(activator)
core.export_ns('')
core.export_cmd('chinch', activator.wait_activator)
############################################

##### Infrared ####
'''
ir1 = BinaryInfrared('front', (0,0), (10,0))
ir1.set_packet_stream(can.get_packet_stream(0x80008d11))
core.add_module(ir1)
'''

ir2 = BinaryInfrared('back1', (-80,0), (-500,0))
ir2.set_packet_stream(can.get_packet_stream(0x80008d13))
core.add_module(ir2)

ir3 = BinaryInfrared('back2', (-80,0), (-500,0))
ir3.set_packet_stream(can.get_packet_stream(0x80008d14))
core.add_module(ir3)

ir4 = BinaryInfrared('front left', (80,0), (195+100,0))
ir4.set_packet_stream(can.get_packet_stream(0x80008d15))
core.add_module(ir4)

ir5 = BinaryInfrared('front middle', (80,0), (120+100,0))
ir5.set_packet_stream(can.get_packet_stream(0x80008d16))
core.add_module(ir5)
##################

############# LIDAR ###########
lidar_id = 0x80007e00
lidar = Lidar(tune_angle=-180+10, packet_stream=can.get_packet_stream(lidar_id))
core.add_module(lidar)
core.add_module(LidarProcessor())
###############################


############# SERVOS ###########
servo_id = 0x00008D70
servo_stream = can.get_packet_stream(servo_id)
spl=Splitter(servo_stream)
servo_klapna = Servo('klapna', servo_id=3, packet_stream=spl.get())
servo_cev = Servo('cev', servo_id=5, packet_stream=spl.get())
servo_cev2 = Servo('cev2', servo_id=20, packet_stream=spl.get())
servo_prekidac = Servo('prekidac', servo_id=1, packet_stream=spl.get())
servo_pcelica = Servo('prekidac', servo_id=7, packet_stream=spl.get())

@asyn2
def klapna(v):
	servo_klapna.action('GoalPosition', 85 if v == 1 else 225)
	
@asyn2
def cev2(v):
	servo_cev2.action('GoalPosition', 130 if v == 0 else 200)

@asyn2
def cev(v):
	servo_cev.action('GoalPosition', 805 if v == 0 else 703)

@asyn2
def prekidac(v):
	servo_prekidac.action('GoalPosition', 272 if v == 0 else 0)

@asyn2
def pcelica(v):
	servo_pcelica.action('GoalPosition', 815 if v == 1 else (600 if v == 2 else 221))
##################

@asyn2
def turbina(x):
	can.send(bytes([x]), 0x8d53)
	pass

core.export_ns('')
core.export_cmd('cev', cev)
core.export_cmd('cev2', cev2)
core.export_cmd('klapna', klapna)
core.export_cmd('pcelica', pcelica)
core.export_cmd('prekidac', prekidac)
core.export_cmd('turbina', turbina)



######## SHARE SERVICE ########
if not sim:
	tcp = TcpClient(ip='192.168.6.1', port=3000)
else:
	tcp = TcpClient(ip='127.0.0.1', port=3000)
share = ShareService(packet_stream=tcp.get_packet_stream())
core.add_module(tcp)
core.add_module(share)
share.export_cmds()
##############################

##### PATHFINDING ########
from modules.services.PathfinderService import *
pathfinder = PathfinderService()
core.add_module(pathfinder)
##########################

######## STATIC OBSTACLES #######
core.entities.add_entity('static','big_terrain_obstacle',polygon_from_rect([-600,1000-260,1200,260]))
#  kocke = [[650, -460+1], [1200, 190-1], [400, 500+1], [-650, -460-1], [-1200, 190+1], [-400, 500-1]]
kocke = [[650, -460], [1200, 190], [400, 500], [-650, -460], [-1200, 190], [-400, 500]]

for i,v in enumerate(kocke):
	core.entities.add_entity('static','k'+str(i+1),polygon_square_around_point(v, 58*3))

core.entities.add_entity('static','pole1' ,polygon_square_around_point([1500-80, 860-1000],100), point=[1500-80, 860-1000])
core.entities.add_entity('static','pole2' ,polygon_square_around_point([-(1500-80), 860-1000],100), point=[-(1500-80), 860-1000])
core.entities.add_entity('static','pole3' ,polygon_square_around_point([(1500-600), 1000-60],100), point=[1500-600, 1000-60])
core.entities.add_entity('static','pole4' ,polygon_square_around_point([-(1500-600), 1000-60],100), point=[-(1500-600), 1000-60])
#################################

e=core.get_exported_commands()


##### PATHFIND ROUTINE ######
@func
def task_start_pathfind(e, x,y,o=1):
	path = pathfinder.pathfind([x,y])
	
	#  path = pathfinder.fix_path(path)
	if not path:
		print('no path: ', x,y)
		return False
		e._task_suspend()
	else:
		print('pathfinding: ', path)
	#  e.r.speed(100)
	#  e.r.tol(50)
	for i in path:
		e.r.goto(*i,0)
		#  e.r.move(*i,150,0)
	return True
		
@do
def pathfind(e,x,y,o=1):
	task_start_pathfind(x,y,o)
pathfinder.prepare_pathfinder()
core.export_ns('')
core.add_sync_cmd('pathfind', task_start_pathfind)
#  core.add_sync_cmd('pathfind', pathfind)
############################

#### Send Points to BIG robot #####
share.set_state('points', 0)

@do
def addpts(e,pts):
	e.set_state('points', pts)
core.add_sync_cmd('addpts', addpts)
#####################################

e=core.get_exported_commands()


future=None
sap=None
state=0
def robot_behavior():
	def on_collision(msg):
		global state, future, sap
		#  print('on collision\x1b[0m', msg)
		#  return
		if state == 0 or msg == 'danger':
			print('\x1b[33mgot collision\x1b[0m', bool(motion.future), sap)
			state = 1
			#  assert motion.future != None
			if motion.future:
				future = motion.future
				motion.future = None
				motion.stop(future=None)
				
			def sleep_and_pathfind():
				global sap,future
				future = None
				print('suspending')
				core.task_manager.get_current_task().suspend()
				state = 0
				sap = None
				
			if True and not sap:	
				sap = core.loop.call_later(3, sleep_and_pathfind)
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
		task = core.task_manager.get_current_task().task_chain
		task.pause()
		#  motion.forward(-100, future=None)
		def wr():
			e.sleep(2)
			e._do(task.resume)
		e._do(wr)
		print('got stuck')
		#  if future:
			#  future.runable.redo()
	
	e._listen('collision', on_collision)
	#  e._listen('stuck', on_stuck, _insync=True)
	

#  core.on('stuck', stuck_behavior)
core.set_task_setup_func(robot_behavior)

###### TIMER #####
async def timer_task():
	time = 0
	while time < 100:
		await asyncio.sleep(1)
		print('time', time)
		time+=1
	print('round has ended')
	motion.fullstop();

@do
def start_timer(e):
	asyncio.ensure_future(timer_task())
##################


###### ROBOT DEFAULT INITIAL TASK #######
def init_task():
	e.r.send(b'R')
	e.r.conf_set('send_status_interval', 100)
	e.r.conf_set('enable_stuck', 0)
	print('init task loaded 1')
	e._do(lambda: print('init task loaded'))
	e.r.conf_set('wheel_r1', 68.0)
	e.r.conf_set('wheel_r2', 67.25513)
	e.r.conf_set('wheel_distance', 252.30)

	if not sim:
		e.r.conf_set('pid_d_p', 2.75)
		e.r.conf_set('pid_d_d', 90)
		#  e.r.conf_set('pid_d_d', 200)
		e.r.conf_set('pid_r_p', 1.5)
		#  e.r.conf_set('pid_r_p', 1.2)
		e.r.conf_set('pid_r_d', 100)

	e.r.conf_set('pid_r_i', 0.0)
	e.r.conf_set('accel', 600)
	e.r.conf_set('alpha', 600)
	
	### GO MSG ###
	def listen_msg(msg):
		print('listen msg', msg)
		if msg == 'small_go':
			e._label('go')
		if msg == 'continue':
			e._label('continue')
	e._listen('message', listen_msg)
	e._do(lambda: print('waiting go signal'))
	#e._sync('go')
	e._do(lambda: print('go go go'))
	##############
	#  e._unlisten('collision')
	#  e.addpts(500)
	#  e.r.softstop()
	#  e.sleep(800)
	if not sim:
		e.chinch()
	else:
		e.sleep(3)
	#  e.send_msg('small_go')
	start_timer()
	
		
core.task_manager.set_init_task(init_task)
##############################
