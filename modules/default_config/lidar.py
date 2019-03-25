from modules.sensors.Lidar import *
from modules.processors.LidarProcessor import *
tune_angle=0
@_core.listen('config:done')
def conf():
	lidar = Lidar(tune_angle=tune_angle, packet_stream=_core.get_module('Can').get_packet_stream(0x80007e00))
	_core.add_module([lidar, LidarProcessor()])
