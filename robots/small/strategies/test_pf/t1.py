weight=1
a=_State(False, shared=False)
def run():
	r.speed(40)
	sleep(1)
	if not pathfind(1300, -400):
		return False

	_label('a')

	_goto('a')
