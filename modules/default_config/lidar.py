from modules.sensors.Lidar import *
from modules.processors.LidarProcessor import *
lidar = Lidar(tune_angle=-180+10, packet_stream=_core.get_module('Can').get_packet_stream(0x80007e00))
_core.add_module([lidar, LidarProcessor()])
