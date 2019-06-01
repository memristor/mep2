from core.Convert import *
import time, asyncio
if not State.sim:
	import modules.sensors.tofsensor.VL53L0X as VL53L0X

class TOFSensor:
	def __init__(self, name='TOFSensor', packet_stream=None):
		self.ps = None
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
		self.active_sensor = 0
		if not State.sim:
			self.tof = VL53L0X.VL53L0X()
		self.timing = [None]*8
		
	def change_sensor(self, sensor_num):
		if sensor_num != None:
			VL53L0X.i2cbus.write_byte(0x70, 1<<sensor_num)
			self.active_sensor = sensor_num
		return self.active_sensor
	
	@_core.asyn2
	def start_measuring(self, sensor_num=None):
		if State.sim: return
		sensor_num = self.change_sensor(sensor_num)
		self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
		# self.tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
		self.timing[sensor_num] = self.tof.get_timing()
		
	@_core.asyn2
	def stop_measuring(self, sensor_num=None):
		if State.sim: return
		sensor_num = self.change_sensor(sensor_num)
		self.tof.stop_ranging()
		self.timing[sensor_num] = None
		
	async def _measure(self, sensor_num=None, wait=False):
		sensor_num = self.change_sensor(sensor_num)
		if wait:
			await asyncio.sleep(self.timing[sensor_num]/1000000.0)
		self.distance = self.tof.get_distance()
		self.future.val = self.distance

	@_core.module_cmd
	def measure(self, sensor_num=None):
		sensor_num = self.change_sensor(sensor_num)
		print('measuring tof', sensor_num, 'timing:',self.timing[sensor_num])
		if self.timing[sensor_num] == None:
			self.start_measuring(sensor_num)
		asyncio.ensure_future(self._measure())
		
	# def on_recv(self, pkt):
		# if len(pkt) >= 4:
			# self.value = lu16l(pkt,0)
			# self.future.set_result( self.value < 0x0400 )
			#self.future.set_result( self.value  )

	def export_cmds(self, ns=''):
		with _core.export_ns(ns):
			_core.export_cmd('measure', self.measure)
			_core.export_cmd('stop', self.stop_measuring)
			_core.export_cmd('start', self.start_measuring)
		
	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
