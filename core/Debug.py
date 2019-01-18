######### DBG
tl = -1
from contextlib import contextmanager
@contextmanager
def inc_tab():
	global tl
	tl += 1
	yield
	tl -= 1
def tabs():
	return '\n' + ' ' * (tl * 4)
def dump(obj):
	for attr in dir(obj):
		print("obj.%s = %r" % (attr, getattr(obj, attr)))

names=[]
def dbg(name='', *args):
	if name in names:
		print('['+name+']:', *[str(a) for a in args])
##########
