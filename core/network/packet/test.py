from UartPacket import *
import binascii
ps=PacketStream()
def s(x):
	print(binascii.hexlify(x))
ps.send = s

up = UartPacketProtocol(ps)
up.send(b'hello')


msg=binascii.unhexlify('3ccc6804656c6c6f3ccc6804656c6c')

def on_rcv(s):
	print('mSG:',s)
up.recv = on_rcv

ps.recv(msg)
ps.recv(b'\x6f')



