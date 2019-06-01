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

	@_core.export_cmd
	def chinch2():
		@_e._on('message')
		def go_msg(msg):
			if msg == 'go':
				_e._goto('go', ref='main')
		_e.chinch()
		_e._L('go')
		_e.send_msg('go')
