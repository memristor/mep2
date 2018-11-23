def to_uint16(x):
	if x < 0:
		x = x + 2**16
	return x

def to_int16(x):
	if x > 2**15:
		x = x - 2**16
	return x

def to_int32(x):
	if x > 2**31:
		x = x - 2**32
	return x

import struct

def uchr(x):
	if x < 0:
		x = x + 2**8
	return bytes([x])
p8=uchr

def l16(x, idx):
	# return to_int16( (x[idx] << 8) | x[idx+1] );
	return struct.unpack('>h', x[idx:idx+2])[0]

def l32(x, idx):
	return struct.unpack('>i', x[idx:idx+4])[0]

def pack32(x):
	return struct.pack('>i', x)
p32=pack32

def pack16(x):
	return struct.pack('>h', x)
pack=pack16
p16=pack16
