import time,math

class col:
	yellow='\x1b[33m'
	green='\x1b[32m'
	red='\x1b[31m'
	blue='\x1b[34m'
	white='\x1b[0m'

def _not(func):
	def not_func(*args, **kwargs):
		return not func(*args, **kwargs)
	return not_func

def get_task_param(task,name,default=0):
	if not hasattr(task.module,name):
		return default
	v=getattr(task.module,name)
	import types
	if type(v) is types.FunctionType:
		return v()
	return v

def get_attr(t, v):
	return v if hasattr(t,v) else None

def get_func_args(func):
	co = func.__code__
	import inspect
	return co.co_varnames[:co.co_argcount+co.co_kwonlyargcount] +\
		tuple(inspect.signature(func).parameters.keys())
		
def inspect_function(func):
	args = get_func_args(func)
	return [i for i in ('_future', '_sim', '_pause') if i in args]
			
def pick(k,kw,default=None, delete=True):
	c=default
	if k in kw:
		c=kw[k]
		if delete: del kw[k]
	return c
	
td=time.time()
def dif(p=False):
	global td
	now=time.time()
	d=now-td
	if p: print('dif:',d)
	td=now
	return d
	
def load_boost_cpp_module(path, name=None):
	import platform, importlib, os, inspect
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	_name = mod.__name__
	if name is None:
		name = path
	# bin/<machine>/<module_name>.so
	module_path = _name + '.bin.' + platform.machine() + '.' + name
	mod_path = _name.replace('.','/')
	def _compile():
		try:
			module = importlib.import_module(module_path)
		except:
			print(col.yellow, 'compiling module:', col.white, path)
			os.system('make -C ' + mod_path)
			module = importlib.import_module(module_path)
		return module
	if State.recompile:
		os.remove( module_path.replace('.','/') + '.so' )
	module = _compile()
	
	return module

def simple_hash(v):
	h=5381
	if type(v) is bytes:
		# print('hashing', nice_hex(v))
		for i in v: 
			h = (h*33 + i) & 0xffff
	else:
		for i in v: h = (h*33 + ord(i)) & 0xffff
	# print('hash is',h)
	return int(h) & 0xffff

# vector rotation
def rot_vec(vec, rad):
	# sin(a+b) = asin(a)cos(b) + acos(a)sin(b)
	# cos(a+b) = acos(a)cos(b) - asin(a)sin(b)
	#
	# x2 = xcos(b) - ysin(b)
	# y2 = ycos(b) + xsin(b)
	c = math.cos(rad)
	s = math.sin(rad)
	return [vec[0]*c - vec[1]*s, vec[0]*s + vec[1] * c]

def rot_vec_deg(vec, deg):
	return rot_vec(vec, math.radians(deg))
rot_pt = rot_vec_deg

def rot_pt_around(pt, around_pt, deg):
	return add_pt( rot_vec_deg(sub_pt( pt, around_pt ), deg), around_pt )

def vector_from_orient(orient_deg, length):
	return rot_vec_deg([length,0], orient_deg)

def in_range(v, min_val, max_val):
	return v >= min_val and v <= max_val

#  import numpy as np
from operator import add,sub,mul

def perp(a):
	b = [-a[1], a[0]]
	return b

def det(p1,p2):
	# x1 y1
	# x2 y2
	# x1y2 - x2y1
	return p1[0] * p2[1] - p2[0]*p1[1]

def dot(a,b):
	return a[0]*b[0] + a[1]*b[1]

def add_pt(p1,p2):
	return list(map(add, p1, p2))
	
def sub_pt(p1,p2):
	return list(map(sub, p1, p2))

def mul_pt(p,scalar):
	return list(map(lambda a: a*scalar, p))
mul_pt_s = mul_pt

def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def seg_intersect(A,B,C,D):
	# Return true if line segments AB and CD intersect
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def is_in_rect(pt, rect):
	px,py=pt
	x,y,w,h=rect
	ret= in_range(px, x, x+w) and in_range(py, y, y+h)
	return ret
	
def get_seg_intersect_pt(a1,a2, b1,b2) :
	da = sub_pt(a2, a1)
	db = sub_pt(b2, b1)
	dp = sub_pt(a1, b1)
	dap = perp(da)
	denom = dot( dap, db )
	num = dot( dap, dp )
	return add_pt( mul_pt_s(db, (num / denom)), b1 )

def is_intersecting_rect(p1,p2, rect):
	x,y,w,h = rect
	segs=[((x,y), (x+w,y)), ((x+w,y),(x+w,y+h)),
		  ((x+w,y+h), (x,y+h)), ((x,y), (x,y+h))]
	for s in segs:
		if seg_intersect(p1,p2,*s):
			return True
	return False

def is_intersecting_poly(p1, p2, poly):
	if seg_intersect(p1,p2, poly[0], poly[-1]):
		return True
	for i in range(1,len(poly)):
		if seg_intersect(p1,p2, poly[i-1], poly[i]):
			return True
	return False
is_seg_intersecting_poly = is_intersecting_poly

def is_poly_intersecting_poly(poly1, poly2):
	if is_intersecting_poly(poly1[0], poly1[-1], poly2):
		return True
	for i in range(len(poly1)-1):
		if is_intersecting_poly(poly1[i],poly1[i+1], poly2):
			return True
	return False

def is_point_in_poly(pt, poly):
	c = False
	j = len(poly)-1
#print(pt,poly)
	for i,p1 in enumerate(poly):
		p2 = poly[j]
		if p1 == pt: return False
		if (p1[1] >= pt[1]) != (p2[1] >= pt[1]):
			x = (pt[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
			if x - pt[0] >= 0:
				c = not c
		j = i
	return c
	
def is_poly_inside_poly(poly1, poly2):
	return not is_poly_intersecting_poly(poly1, poly2) and is_point_in_poly(polygon_midpoint(poly1), poly2)

def polygon_square_around_point(point, rect_size):
	x,y = point
	a,b = (rect_size/2, rect_size/2) if type(rect_size) is int else (rect_size[0]/2, rect_size[1]/2)
	return [(x-a,y-b), (x+a,y-b), (x+a,y+b), (x-a,y+b)]

def rect_around_point(point, rect_size):
	a,b = (rect_size/2, rect_size/2) if type(rect_size) is int else (rect_size[0]/2, rect_size[1]/2)
	return [point[0]-a, point[1]-b, a*2, b*2]

def polygon_rotate(poly, deg):
	center=polygon_midpoint(poly)
	return [rot_pt_around(p, center, deg) for p in poly]

def polygon_from_rect(rect):
	x,y,w,h = rect
	return [(x,y), (x+w, y), (x+w, y+h), (x,y+h)]

def polygon_midpoint(poly):
	return AABB.from_polygon(poly).get_midpoint()

def point_distance(pt1, pt2):
	return math.hypot(*sub_pt(pt1, pt2))

def point_int(pt):
	return list(map(int, pt))
	
class Transform:
	def __init__(self, start_pos, end_pos):
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.rot_angle = self.end_pos[1] - self.start_pos[1]
		
	def transform(self, pos):
		rel_vec = rot_vec_deg(sub_pt(pos, self.start_pos[0]), self.rot_angle)
		return point_int( add_pt( rel_vec, self.end_pos[0] ) )

def vector_length(vec):
	return math.hypot(*vec)

def vector_angle_diff(vec1, vec2):
	# a.b = |a||b|cos(angle)
	# angle = acos( a.b/(|a||b|) )
	denom = math.hypot(*vec1) * math.hypot(*vec2)
	if denom == 0: return 2*math.pi
	val = dot(vec1,vec2) / denom
	val = max(-1,min(1, val))
	return math.acos( val )

def normalize_orient(o):
	o = o % 360
	return o - 360 if o > 180 else o

def vector_orient(vec):
	deg = math.degrees(vector_angle_diff(vec, [1,0]))
	return -deg if vec[1] < 0 else deg
	
def is_point_in_sector(point, sector_point, look_vector, distance, spread_angle_deg):
	spread_angle_deg /= 2
	vec = sub_pt(point, sector_point)
	if vector_length(vec) > distance: return False
	# return abs( vector_angle_diff( look_vector, vec) ) < math.radians(spread_angle_deg)
	ang=vector_angle_diff(look_vector, vec)
	return 0 <= ang <= math.radians(spread_angle_deg)

def is_polygon_in_sector(polygon, *sector):
	for i in polygon:
		# print('test pt:', i, ' | ', *sector)
		if is_point_in_sector(i, *sector): return True
	if is_point_in_sector(polygon_midpoint(polygon), *sector):
		return True
	return False

# Axis Aligned Bounding Box
class AABB:
	def __init__(self, x=0,y=0):
		self.x = [x,x]
		self.y = [y,y]
	
	@staticmethod
	def from_polygon(poly):
		aabb = AABB(*poly[0])
		for i in poly: aabb.put(*i)
		return aabb
	
	def put(self, x,y=None):
		if y == None and len(x) == 2:
			x,y = x
		self.x = [min(self.x[0], x), max(self.x[1], x)]
		self.y = [min(self.y[0], y), max(self.y[1], y)]
	
	def get_midpoint(self):
		return [sum(self.x) / len(self.x), sum(self.y) / len(self.y)]
	
	def get_size(self):
		return [self.x[1] - self.x[0], self.y[1] - self.y[0]]

def nice_hex(s, spaces=4):
	import binascii
	h = binascii.hexlify(s).decode('ascii')
	return ' '.join([h[i:i+spaces] for i in range(0, len(h)-(len(h)%spaces)+spaces, spaces)])
