#new config
from core.Util import *
from modules.sensors.BinaryInfrared import *
from core.network.Tcp import *
from modules.services.ShareService import *
from modules.drivers.Servo import *
from core.network.Splitter import *
import socket

from modules.default_config import motion, collision_wait, chinch, lidar, timer, pathfind


#  sim = True
sim = False

core = _core
core.set_robot_size(290,160)

can = motion.can

###### WIFI COMM #######
ip_zero = "192.168.43.7"
port = 12345
tcp = Tcp(ip='192.168.43.7', port=3000)
ptcp = tcp.get_packet_stream()
@_core.asyn2
def exp():
	ptcp.send(b'g')
	soc = socket.socket()
	print("Socket successfully created")
	soc.connect((ip_zero, port))
	a = "g"
	soc.send(a.encode())
	soc.close()

core.export_cmd('exp', exp)
#########################


##### Infrared ####

_core.add_module([
	BinaryInfrared('front down right', (110,0), (150,0), packet_stream=can.get_packet_stream(0x80008d11)),
	BinaryInfrared('front down left', (110,0), (150,0), packet_stream=can.get_packet_stream(0x80008d14)),
	BinaryInfrared('front up right', (110,0), (150,0), packet_stream=can.get_packet_stream(0x80008d12)),
	BinaryInfrared('front up left', (110,0), (150,0), packet_stream=can.get_packet_stream(0x80008d13)),
	BinaryInfrared('back down right', (-110,0), (-150,0), packet_stream=can.get_packet_stream(0x80008d17)),
	BinaryInfrared('back down left', (-110,0), (-150,0), packet_stream=can.get_packet_stream(0x80008d15)),
	BinaryInfrared('back up midle', (-110,0), (-150,0), packet_stream=can.get_packet_stream(0x80008d16))])

##################


############ SERVOS ###########
servo_id = 0x80008D70
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
    _e.servo_rfliper.action('GoalPosition', [20,289,424][v]) # 406 da se vrati u pocetni polozaj
#768 i 406
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


######## SHARE SERVICE ########
if not sim:
    tcp = Tcp(ip='192.168.4.1', port=3000)
else:
    tcp = Tcp(ip='127.0.0.1', port=3000)
share = ShareService(packet_stream=tcp.get_packet_stream())
core.add_module(tcp)
core.add_module(share)
share.export_cmds()
##############################

e=_e

#### Send Points to BIG robot #####
share.set_state('points', 0)

@_core.do
def addpts(e,pts):
    _e.set_state('points', pts)
core.export_cmd('addpts', addpts)
#####################################

# e=core.get_exported_commands()
e=_e

###### ROBOT DEFAULT INITIAL TASK #######
def init_task():
    servo_napredgold.action('Speed',200)
    servo_rucica_desno.action('Speed', 250)
    servo_rucica_leva.action('Speed', 250)
    servo_nazadgold.action('Speed', 200)
    servo_lfliper.action('Speed', 200)
    servo_rfliper.action('Speed', 200)

    print('Servo speed set')
    e.r.send(b'R')
    # e.r.conf_set('send_status_interval', 100)
    e.r.conf_set('send_status_interval', 0)
    e.r.conf_set('enable_stuck', 0)
    print('init task loaded 1')
    e._do(lambda: print('init task loaded'))
    e.r.conf_set('wheel_r1', 69)	#levi tocak
    e.r.conf_set('wheel_r2', 69)	#desni tocak
    e.r.conf_set('wheel_distance', 253.71)	#idalno 275.92

    e.r.conf_set('pid_d_p', 3)
    e.r.conf_set('pid_d_d', 100)
    e.r.conf_set('pid_r_p', 1.4)
    e.r.conf_set('pid_r_d', 50)
    e.r.conf_set('pid_r_i', 0)
    e.r.conf_set('pid_d_i', 0)

    e.r.accel(800)		
    #e.chinch()
    # timer.start_timer()

core.task_manager.set_init_task(init_task)
##############################
