######### DBG
tl = 0
def tabs():
	return '\n' + ' ' * (tl * 4)
def dump(obj):
	for attr in dir(obj):
		print("obj.%s = %r" % (attr, getattr(obj, attr)))

names=[]
# names += ['run_cycle']
#  names += ['task_example']
#  names += ['cycle']
# names += ['run_command']
# names += ['active']
#  names += ['new']

def dbg(name='', *args):
	if name in names:
		print('['+name+']:', *[str(a) for a in args])
##########
