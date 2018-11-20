import time,math

class col:
	yellow='\x1b[33m'
	green='\x1b[32m'
	red='\x1b[31m'
	blue='\x1b[34m'
	white='\x1b[0m'

class Event(list):
	def __call__(self, *args, **kwargs):
		for f in self:
			f(*args, **kwargs)

def _not(func):
	def not_func(*args, **kwargs):
		return not func(*args, **kwargs)
	return not_func

def pick(k,kw,default=None):
	c=default
	if k in kw:
		c=kw[k]
		del kw[k]
	return c
		
# vector rotation
def rot_vec(vec, rad):
	# sin(a+b) = asin(a)cos(b) + acos(a)sin(b)
	# cos(a+b) = acos(a)cos(b) - asin(a)sin(b)
	#
	# x2 = xcos(b) - ysin(b)
	# y2 = ycos(b) + xsin(b)
	# 
	#  cos  sin
	# -sin  cos
	c = math.cos(rad)
	s = math.sin(rad)
	return [vec[0]*c - vec[1]*s, vec[0]*s + vec[1] * c]

def rot_vec_deg(vec, deg):
	return rot_vec(vec, math.radians(deg))

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
	return in_range(px, x, x+w) and in_range(py, y, y+h)
	
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

def polygon_square_around_point(point, rect_size):
	x,y = point
	h=rect_size/2
	return [(x-h,y-h), (x+h,y-h), (x+h,y+h), (x-h,y+h)]

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
	# pos ([x,y], 20)
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
	if denom == 0:
		return 360
	return math.acos( dot(vec1,vec2) / denom )
	
def is_point_in_pie_shape(point, pie_start_pt, pie_look_vec, pie_range, pie_angle_spread_deg):
	pie_angle_spread_deg /= 2
	vec = sub_pt(point, pie_start_pt)
	if vector_length(vec) > pie_range:
		return False
	return abs( vector_angle_diff( pie_look_vec, vec) ) < math.radians(pie_angle_spread_deg)
		
def is_poly_in_pie_shape(poly, pie_start_pt, pie_look_vec, pie_range, pie_angle_spread_deg):
	for i in poly:
		if is_point_in_pie_shape(i, pie_start_pt, pie_look_vec, pie_range, pie_angle_spread_deg):
			return True
	if is_point_in_pie_shape(polygon_midpoint(poly), pie_start_pt, pie_look_vec, pie_range, pie_angle_spread_deg):
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
		for i in poly:
			aabb.put(*i)
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
