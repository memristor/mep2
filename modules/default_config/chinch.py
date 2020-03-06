from modules.sensors.Activator import *
addr = 0x80008d11
@_core.on('config:done')
def run():
	activator = Activator('pin activator', packet_stream=_core.get_module('Can').get_packet_stream(addr))
	_core.add_module(activator)
#activator.export_cmds()
	if State.sim or State.get('dont_use_chinch'):
		@_core.export_cmd
		def check_chinch():
			pass
		@_core.export_cmd
		def chinch():
			pass
	else:
		_core.export_cmd('chinch', activator.wait_activator)
		_core.export_cmd('check_chinch', activator.check_activator)

	
