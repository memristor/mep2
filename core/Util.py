import math
import time
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def asyn(f):
	def wrapper(*args, **kwargs):
		if 'future' in kwargs:
			# set future to class instance
			args[0].future = kwargs['future']
			if args[0].future:
				args[0].future.time = time.monotonic()
			del kwargs['future']
		f(*args, **kwargs)
	return wrapper

def asyn2(f):
	def wrapper(*args, **kwargs):
		fut = None
		if 'future' in kwargs:
			fut = kwargs['future']
			del kwargs['future']
		f(*args, **kwargs)
		if fut:
			fut.set_result(1)
	return wrapper
	

class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

# vector rotation
from math import sin,cos,radians
#
# sin(a+b) = asin(a)cos(b) + acos(a)sin(b)
# cos(a+b) = acos(a)cos(b) - asin(a)sin(b)
#
# x2 = xcos(b) - ysin(b)
# y2 = ycos(b) + xsin(b)
# 
#  cos  sin
# -sin  cos

	
def rot_vec(vec, rad):
	c = cos(rad)
	s = sin(rad)
	return [vec[0]*c - vec[1]*s, vec[0]*s + vec[1] * c]

def rot_vec_deg(vec, deg):
	return rot_vec(vec, radians(deg))
	
def is_in_rect(pt, rect):
	if pt[0] > rect[0] and\
	   pt[0] < rect[0]+rect[2] and\
	   pt[1] > rect[1] and\
	   pt[1] < rect[1]+rect[3]:
		return True
	else:
		return False
		
#  import numpy as np
from operator import add,sub

def perp( a ) :
    #  b = empty_like(a)
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

def mul_pt_s(p,scalar):
	return [p[0]*scalar, p[1]*scalar]
	
# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def seg_intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    
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
		#  print('w',p1,p2,s)
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
	p=[0,0]
	for i in poly:
		p[0] += i[0]
		p[1] += i[1]
	return [p[0]/len(poly), p[1]/len(poly)]

#  def 

class Transform:
	# pos ([x,y], 20)
	def __init__(self, start_pos, end_pos):
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.rot_angle = self.end_pos[1] - self.start_pos[1]
		
	def transform(self, pos):
		rel_vec = rot_vec_deg(list(map(sub, pos, self.start_pos[0])), self.rot_angle)
		return list(map(int, map(add, rel_vec, self.end_pos[0])))


def point_distance(pt1, pt2):
	return math.hypot(*sub_pt(pt1, pt2))
	
def vector_length(vec):
	return math.hypot(*vec)
	
def vector_angle_diff(vec1, vec2):
	# a.b = |a||b|cos(angle)
	# angle = acos( a.b/(|a||b|) )
	
	denom = math.hypot(*vec1) * math.hypot(*vec2)
	if denom == 0:
		return 360
	return math.acos( dot(vec1,vec2) / denom )
	
def point_int(pt):
	return [int(pt[0]), int(pt[1])]
	
def is_point_in_pie_shape(point, pie_start_pt, pie_look_vec, pie_range, pie_angle_spread_deg):
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
	def put(self, x,y):
		self.x[0] = min(self.x[0], x)
		self.x[1] = max(self.x[1], x)
		self.y[0] = min(self.y[0], y)
		self.y[1] = max(self.y[1], y)
		
	def get_midpoint(self):
		return [(self.x[1] + self.x[0]) / 2, (self.y[1] + self.y[0]) / 2]
		
	def get_size(self):
		return [self.x[1] - self.x[0], self.y[1] - self.y[0]]
import binascii
def nice_hex(s, spaces=4):
	h = binascii.hexlify(s).decode('ascii')
	return ' '.join([h[i:i+spaces] for i in range(0, len(h)-(len(h)%spaces)+spaces, spaces)])
