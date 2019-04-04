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
#from modules.default_config import motion, collision_wait_redo, chinch, lidar, timer, pathfind
from modules.default_config import motion, chinch, lidar, timer, pathfind
#from modules.default_config import collision_wait
lidar.tune_angle = -100+180-30+20+20
# from modules.default_config import motion, chinch, lidar, timer

chinch.addr = 0x7821

core = _core
core.set_robot_size(290,160)
can = motion.can

# 1. testiranje senzora da ne detektuje teren
# 2. strategije za boje terena
# 3. bodovi
# 4. podela taskova na delove

# motion bug
# pathfinding
# camera
# experiment
# tof

##### Infrared ####
_core.add_module([
	BinaryInfrared('prednji desni', (0,-50), (300,-50), packet_stream=can.get_packet_stream(0x80007822)),
	BinaryInfrared('prednji levi', (0,50), (300,50), packet_stream=can.get_packet_stream(0x80007824)),
	BinaryInfrared('zadnji desni', (0, -50), (-300, -50), packet_stream=can.get_packet_stream(0x80007823)),
	BinaryInfrared('zadnji levi', (0, -50), (-300, 50), packet_stream=can.get_packet_stream(0x80007825))
])
##################

#### Pressure ########
pressure = [ 
 PressureSensor('napredp', 1, can.get_packet_stream(0x80007801, 0x80007800)),
 PressureSensor('nazadp', 2, can.get_packet_stream(0x80007802, 0x80007800)) ]
_core.add_module( pressure )
for i in pressure: i.export_cmds(i.name)
######################

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
_core.entities.add_entity('static', 'rampa', [[-1050,500], [-35,500], [-35, 368], [45,352], [41, 536], [1055,516], [1089, 992], [-1041, 964], [-1050, 500]])
_core.entities.add_entity('static', 'accelerator', [[-999,-932], [991, -944], [991, -1000], [-991,-1000]])
#################################

#################### SERVOS ###################################
servo_id = 0x80008D70
servo_id = 0x80006c00
servo_stream = can.get_packet_stream(servo_id)
spl=Splitter(servo_stream)
###################
servo_rucica_desno = Servo('servo_rucica_desno', servo_id=1, packet_stream=spl.get())
servo_rucica_leva = Servo('servo_rucica_leva', servo_id=2, packet_stream=spl.get())

servo_rfliper = Servo('servo_rfliper', servo_id=9, packet_stream=spl.get())
servo_lfliper = Servo('servo_lfliper', servo_id=7, packet_stream=spl.get())

servo_napredgold = Servo('servo_napredgold', servo_id=3, packet_stream=spl.get())
servo_nazadgold = Servo('servo_nazadgold', servo_id=5, packet_stream=spl.get())

servos = [servo_rucica_desno, servo_rucica_leva, servo_rfliper, servo_lfliper, servo_napredgold, servo_nazadgold]
for i in servos: i.export_cmds(i.name)
_core.add_module(servos)

@_core.do
def rrucica(v):
	_e.servo_rucica_desno.action('GoalPosition', 283 if v == 1 else 601)

@_core.do
def lrucica(v):
	_e.servo_rucica_leva.action('GoalPosition', 261 if v == 1 else 570)

@_core.do
def rfliper(v):
	# _e.servo_rfliper.action('GoalPosition', [20,289,424][v])
	_e.servo_rfliper.action('GoalPosition', [162,370,471][v])
	
@_core.do
def lfliper(v):
	# _e.servo_lfliper.action('GoalPosition', [921,606,504][v])
	_e.servo_lfliper.action('GoalPosition', [821,615,507][v])

@_core.do
def nazgold(v):
	_e.servo_napredgold.action('GoalPosition', [150,330,674][v]) #674 je donji polozaj, 300 je bio najvisi

@_core.do
def napgold(v):
	_e.servo_nazadgold.action('GoalPosition', [87,450,380,550][v])
####################################################################3
c=can
@_core.export_cmd
@_core.do
def pump(x,v):
	c.send(bytes([v]) * 5, 0x6c10) if x == 0 else c.send(bytes([v]), 0x6c10+x)

core.export_ns('')
core.export_cmd('rrucica', rrucica)
core.export_cmd('lrucica', lrucica)
core.export_cmd('rfliper', rfliper)
core.export_cmd('lfliper', lfliper)
core.export_cmd('napgold', napgold)
core.export_cmd('nazgold', nazgold)

_core.debug=0
from modules.default_config import share,lcd
share.ip = '192.168.1.144'
share.port = 6000

tcp_experiment = Tcp(name='experiment', ip='127.0.0.1', port=8000)
pt = tcp_experiment.get_packet_stream()
_core.add_module(tcp_experiment)
@_core.export_cmd
@_core.do
def experiment(v):
	pt.send(v.encode())

###### ROBOT DEFAULT INITIAL TASK #######
def init_task():
	servo_napredgold.action('Speed', 200)
	servo_rucica_desno.action('Speed', 250)
	servo_rucica_leva.action('Speed', 250)
	servo_nazadgold.action('Speed', 200)
	servo_lfliper.action('Speed', 500)
	servo_rfliper.action('Speed', 500)

	print('Servo speed set')
	_e.r.send('R')
	_e.sleep(0.1)
	_e.r.conf_set('send_status_interval', 100)
	#_e.r.conf_set('send_status_interval', 0)
	_e.r.conf_set('enable_stuck', 0)
	print('init task loaded 1')
	_e._do(lambda: print('init task loaded'))
	_e.r.conf_set('wheel_r1', 63.041126)	#levi tocak 70.1920648macak i bela menjali
	_e.r.conf_set('wheel_r2', 63.12501522)	#desni tocak 69.04025833 bela i macak menjali
	_e.r.conf_set('wheel_distance',255.17)	#idalno 275.92 252.917866401 
	#bela dodao 0.1
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
	_e.send_msg('go')
	timer.start_timer()
	_e.experiment('H')

# senzor pritiska
# \x01 ili \x02 7800 => recv 7801, 7802 ( xx 0c => ne drzi, xx 02 => drzi )
# 2 - zadnja
# 1 - prednja

_core.init_task(init_task)
##############################
