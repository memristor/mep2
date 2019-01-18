# hello world code for driving robot
from core.network.Can import *
from modules.drivers.motion import Motion
# use can0 CAN device for communicating with motion board (virtual or physical)
can = _core.get_module('Can')
if not can:
	can = Can()
# make motion driver instance and give CAN channel with address 0x80000258 
#	0x80000258 is default motion board address
motion = Motion(packet_stream=can.get_packet_stream(0x80000258))
motion.export_cmds('r') # exports commands with namespace 'r' (r.goto, r.conf_set, ...)
# add modules to core 
# 	(they will have their `def run():` functions executed prior to task execution, 
#	but not before config.py execution ends)
_core.add_module([can, motion])
