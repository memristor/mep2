import math
import asyncio
from core.Convert import *
from core.network.packet.PacketStream import *
from core.Util import *

import rclpy
import rclpy.action
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from std_msgs.msg import Int8
from nav2_msgs.action import NavigateToPose
from .robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

class MotionROS2:
	active_actions = []
	
	def __init__(self, name='MotionROS2', ros_namespace='big', ros_node=None):
		self.name = name
		self.debug = 0
		self.ps = None
		self.future=None
		self.disabled = False
		self.timeout = False
		self.namespace = None
		
		self._ros_last_action = None
		
		if not ros_node:
			rclpy.init()
			self.ros_motion_node = Node(name)
		else:
			self.ros_motion_node = ros_node
		
		self.navigator = BasicNavigator(ros_namespace)
		self.navigator.waitUntilNav2Active()
		
	def print_cmd(self, name, *args):
		print(col.yellow, name+':', col.white, *args)
	
	def resolve(self, v=True):
		if self.disabled: return
		if self.future:
			
			if self._ros_last_action:
				active_actions.remove( self._ros_last_action )
				
			self.future.set_result(v)
			self.future = None
	
	def to_ros_pose(self, x,y,r):
		pose = PoseStamped()
		pose.header.frame_id = 'map'
		pose.header.stamp = self.navigator.get_clock().now().to_msg()
		pose.pose.position.x = float(x/1000.0)
		pose.pose.position.y = float(y/1000.0)
		
		theta = math.radians(r)
		pose.pose.orientation.z = math.sin(theta/2)
		pose.pose.orientation.w = math.cos(theta/2)
		return pose
	
	####### RAW COMMANDS #######
	def move_cmd(self, x,y,r=100,dir=1):
		point = [x,y]
		curpos = _core.get_position()[:2]
		theta = vector_orient( sub_pt(point, curpos) )

		self.navigator.goToPose(self.to_ros_pose(x,y, theta))
	#############################
	
	
	def on_cancel(self):
		print('motion cancel')
		self.future = None
		self.cancelling = True
			
	def export_cmds(self, namespace='r'):
		self.namespace = namespace
		with _core.export_ns(namespace):
			_core.export_cmd('move', self.move)
			_core.export_cmd('setpos', self.setpos)
	
	@_core.module_cmd
	def setpos(self, x, y, r):
		self.navigator.setInitialPose( self.to_ros_pose(x,y,r) )
	
	@_core.module_cmd
	def move(self, x,y,r=100,o=1):
		self.print_cmd('moving to',x,y,o)
		x,y=int(x),int(y)
		self.point = [x,y]
		self.move_cmd(x,y,r,o)

	async def timer_task(self):
		while 1:
			if self.navigator.isTaskComplete():
				self.resolve()
			if rclpy.ok():
				rclpy.spin_once(self.ros_motion_node,  timeout_sec=0.1)
			await asyncio.sleep(0.1)

	def run(self):
		self.timer_future = asyncio.ensure_future(self.timer_task())
	
