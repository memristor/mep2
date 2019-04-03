#new config
from core.Util import *
from modules.sensors.BinaryInfrared import *
from modules.sensors.PressureSensor import *
from modules.sensors.ColorSensor import *
from core.network.Tcp import *
from modules.services.ShareService import *
from modules.drivers.Servo import *
from core.network.Splitter import *
import socket

# from modules.default_config import motion, collision_wait, chinch, lidar, timer, pathfind
#from modules.default_config import motion, chinch, lidar, timer#, pathfind
from modules.default_config import motion, collision_wait_redo, chinch, lidar, timer, pathfind
lidar.tune_angle = -100+180-30+20+20
# from modules.default_config import motion, chinch, lidar, timer

chinch.addr = 0x7821

#  sim = True
sim = False

core = _core
core.set_robot_size(290,160)
can = motion.can
'''
##### Infrared ####
_core.add_module([
	BinaryInfrared('prednji desni', (0,-50), (100,-50), packet_stream=can.get_packet_stream(0x80007822)),
	BinaryInfrared('prednji levi', (0,50), (100,50), packet_stream=can.get_packet_stream(0x80007824)),
	BinaryInfrared('zadnji desni', (0, -50), (-100, -50), packet_stream=can.get_packet_stream(0x80007823)),
	BinaryInfrared('zadnji levi', (0, 50), (-100, 50), packet_stream=can.get_packet_stream(0x80007825))
])
##################
'''
#### Pressure ########
pressure = [ 
 PressureSensor('napredp', 1, can.get_packet_stream(0x80007801, 0x80007800)),
 PressureSensor('nazadp', 2, can.get_packet_stream(0x80007802, 0x80007800)) ]
_core.add_module( pressure )
for i in pressure: i.export_cmds(i.name)
#############

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
'''
_core.entities.add_entity('static','big_terrain_obstacle',polygon_from_rect([-600,1000-260,1200,260]))
cube_obstacles = [[650, -460], [1200, 190], [400, 500], [-650, -460], [-1200, 190], [-400, 500]]

for i,v in enumerate(cube_obstacles):
    _core.entities.add_entity('static','k'+str(i+1),polygon_square_around_point(v, 58*3))

poles=[ [1500-80, 860-1000], [-(1500-80), 860-1000], [(1500-600), 1000-60], [-(1500-600), 1000-60] ]
for i,v in enumerate(poles):
    _core.entities.add_entity('static','pole'+str(i), polygon_square_around_point(v,100), point=v)
'''
_core.entities.add_entity('static', 'rampa', [[-1050,500], [-35,500], [-35, 368], [45,352], [41, 536], [1055,516], [1089, 992], [-1041, 964], [-1050, 500]])
_core.entities.add_entity('static', 'accelerator', [[-999,-932], [991, -944], [991, -1000], [-991,-1000]])
#################################

############ SERVOS ###########
servo_id = 0x80008D70
servo_id = 0x80006c00
servo_stream = can.get_packet_stream(servo_id)
spl=Splitter(servo_stream)
######################################################################
servo_rucica_desno = Servo('servo_rucica_desno', servo_id=1, packet_stream=spl.get())
servo_rucica_leva = Servo('servo_rucica_leva', servo_id=2, packet_stream=spl.get())

servo_rfliper = Servo('servo_rfliper', servo_id=9, packet_stream=spl.get())
servo_lfliper = Servo('servo_lfliper', servo_id=7, packet_stream=spl.get())

servo_napredgold = Servo('servo_napredgold', servo_id=3, packet_stream=spl.get())
servo_nazadgold = Servo('servo_nazadgold', servo_id=5, packet_stream=spl.get())

servos = [servo_rucica_desno, servo_rucica_leva, servo_rfliper, servo_lfliper, servo_napredgold, servo_nazadgold]
for i in servos: i.export_cmds(i.name)
_core.add_module(servos)

######################################################################
servo_id = 0x00008D70
#########################
#@_core.asyn2
#def servo_set_speed(x,y):
@_core.do
def rrucica(v):
	_e.servo_rucica_desno.action('GoalPosition', 283 if v == 1 else 601)

@_core.do
def lrucica(v):
	_e.servo_rucica_leva.action('GoalPosition', 261 if v == 1 else 570)

@_core.do
def rfliper(v):
	_e.servo_rfliper.action('GoalPosition', [20,289,424][v])
@_core.do
def lfliper(v):
	_e.servo_lfliper.action('GoalPosition', [921,606,504][v])

@_core.do
def nazgold(v):
	_e.servo_napredgold.action('GoalPosition', [77,300,674][v]) #674 je donji polozaj


@_core.do
def napgold(v):
	_e.servo_nazadgold.action('GoalPosition', 416 if v == 1 else 83)

c=can
@_core.export_cmd
@_core.do
def pump(x,v):
	c.send(bytes([v]) * 5, 0x6c10) if x == 0 else c.send(bytes([v]), 0x6c10+x)

@_core.asyn2
def turbina(x):
	can.send(bytes([x]), 0x8d53)
	pass

core.export_ns('')

core.export_cmd('rrucica', rrucica)
core.export_cmd('lrucica', lrucica)
core.export_cmd('rfliper', rfliper)
core.export_cmd('lfliper', lfliper)
core.export_cmd('napgold', napgold)
core.export_cmd('nazgold', nazgold)

###### ROBOT DEFAULT INITIAL TASK #######
def init_task():
	servo_napredgold.action('Speed',200)
	servo_rucica_desno.action('Speed', 250)
	servo_rucica_leva.action('Speed', 250)
	servo_nazadgold.action('Speed', 200)
	servo_lfliper.action('Speed', 200)
	servo_rfliper.action('Speed', 200)

	print('Servo speed set')
	_e.r.send('R')
	_e.sleep(0.1)
	_e.r.conf_set('send_status_interval', 100)
	#_e.r.conf_set('send_status_interval', 0)
	_e.r.conf_set('enable_stuck', 0)
	print('init task loaded 1')
	_e._do(lambda: print('init task loaded'))
	_e.r.conf_set('wheel_r1', 63)	#levi tocak
	_e.r.conf_set('wheel_r2', 63)	#desni tocak
	_e.r.conf_set('wheel_distance', 253.917866401+0.1)	#idalno 275.92

	_e.sleep(0.01)
	if not State.sim:
		_e.r.conf_set('pid_d_p', 2.2)
		_e.r.conf_set('pid_d_d', 100)
		_e.r.conf_set('pid_r_p', 2.1)
		_e.r.conf_set('pid_r_d', 50)
		_e.r.conf_set('pid_d_i', 0.03)
		_e.r.conf_set('pid_r_i', 0.03)

	
	_e.r.accel(800)
	_e.r.speed(100)
	_e.chinch()
	timer.start_timer()

# senzor pritiska
# \x01 ili \x02 7800 => recv 7801, 7802 ( xx 0c => ne drzi, xx 02 => drzi )
# 2 - zadnja
# 1 - prednja

_core.init_task(init_task)
##############################