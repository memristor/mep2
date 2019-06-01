weight=1
a=_State(False, shared=False)
def run():
	r.speed(100)
	# sleep(1)
	# return False
	if not pathfind(1000, -400):
		return False

	enable_task('t2')
	# _label('a')

	# _goto('a')
