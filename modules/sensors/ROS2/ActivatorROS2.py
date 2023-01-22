import asyncio
from std_msgs.msg import Int8

class ActivatorROS2:
	def __init__(self, name, ros_node):
		self.ps = None
		self.name = name
		self.future = None
		self.ros_node = ros_node
		self.ros_node.create_subscription(Int8, '/match_start_status', self._match_start_notif, 1)
	
	def _match_start_notif(self, match_status):
		print('match start notif', match_status.data)
		if match_status.data == 2:
			print('match start')
			self.future.set_result(2) # match starts
	
	@_core.module_cmd
	def wait_activator(self):
		print('waiting activator')
		pass
		
	def export_cmds(self):
		_core.export_cmd('wait_activator', self.wait_activator)
