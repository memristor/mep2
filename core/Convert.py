import struct

# conversions
def to_uint16(x): return x + 2**16 if x < 0 else x
def to_int16(x): return x - 2**16 if x > 2**15 else x
def to_int32(x): return x - 2**32 if x > 2**31 else x

# packing
def p8(x): return bytes([x + 2**8 if x < 0 else x])
def p32(x): return struct.pack('>i', x)
def p16(x): return struct.pack('>H', to_uint16(x))
# loading
def l8(x, idx): return x[idx]
def l16(x, idx): return struct.unpack('>h', x[idx:idx+2])[0] # return to_int16( (x[idx] << 8) | x[idx+1] );
def l32(x, idx): return struct.unpack('>i', x[idx:idx+4])[0]
