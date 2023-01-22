# hello world code for driving robot
from modules.default_config import motion
motion.can.iface = 'can0'

@_core.init_task
def _():
	_e.r.conf_set('send_status_interval', 10)
	_e.r.accel(400)
