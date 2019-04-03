from core.network.Tcp import *
from modules.services.ShareService import *
ip='0.0.0.0'
port = 3000
@_core.on('config:done')
def load():
	tcp = Tcp(name='share tcp', ip=ip, port=port)
	share = ShareService(name='share', packet_stream=tcp.get_packet_stream())
	share.export_cmds()
	_core.add_module([tcp, share])
