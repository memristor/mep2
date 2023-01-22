# hello world code for driving robot in ROS2

from modules.drivers.movement.ROS2.MotionROS2_minimal import MotionROS2
from modules.sensors.ROS2.ActivatorROS2 import ActivatorROS2

import rclpy
from rclpy.node import Node
rclpy.init()
ros_node = Node('mep2_node')

ros = MotionROS2(ros_namespace='big', ros_node=ros_node)

_core.add_module(ros)
ros.export_cmds()

activator = ActivatorROS2('activator', ros_node)
activator.export_cmds()
_core.add_module(activator)


@_core.init_task
def init_task():
	# _e.wait_activator()
	pass 
	# timer.start_timer()

	

