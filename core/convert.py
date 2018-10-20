
import struct
from math import log10
def conf_float_to_bytes(x, decimals=4):
	x *= pow(10, decimals)
	x = int(x)
	s = 1 if x < 0 else 0
	x = abs(x) & 0xffffffff

#return pack32(( (x << 4) | decimals & 0xf) & 0xffffffff)
	return pack32(x) + bytes([s, decimals])

def conf_bytes_to_float(x):
	num = l32(x,0)
	s = x[4]
	if s == 1:
		num = -num
	dec = float(x[5])
	return float(num) / pow(10, dec)

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
	#  return struct.pack('B', x)
	return bytes([x])

def cx(x):
	return hex(c(x))


def l16(x, idx):
	return to_int16( (x[idx] << 8) | x[idx+1] );
def l32(x, idx):
	return to_int32( (x[idx] << 24) | (x[idx+1] << 16) | (x[idx+2] << 8) | x[idx+3] );

def ls16(x, idx):
	return str(l16(x,idx))

def pack32(x):
	return struct.pack('>i', x)
	
def pack(x):
	return struct.pack('>h', x)

def c(x):
	if x < 0:
		x = x + 2**16
	return hex(x)
