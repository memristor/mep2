from core.network.Tcp import *
from modules.services.ShareService import *
tcp = Tcp(port=3000)
share = ShareService(packet_stream=tcp.get_packet_stream())
share.export_cmds()
_core.add_module([tcp, share])
