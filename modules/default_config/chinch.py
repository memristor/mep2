from modules.sensors.Activator import *
activator = Activator('pin activator', packet_stream=_core.get_module('Can').get_packet_stream(0x80008d11))
_core.add_module(activator)
_core.export_cmd('chinch', activator.wait_activator)
