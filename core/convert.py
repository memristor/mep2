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

def to_uchar(x):
	if x < 0:
		x = x + 2**8
	return x

def uchr(x):
	return bytes([x])

def l16(x, idx):
	return to_int16( (x[idx] << 8) | x[idx+1] );

def l32(x, idx):
	return to_int32( (x[idx] << 24) | (x[idx+1] << 16) | (x[idx+2] << 8) | x[idx+3] );

import struct
def pack32(x):
	return struct.pack('>i', x)
	
def pack(x):
	return struct.pack('>h', x)
pack16=pack

def uword16(x):
	return bytes([x >> 8, x & 0xff])
