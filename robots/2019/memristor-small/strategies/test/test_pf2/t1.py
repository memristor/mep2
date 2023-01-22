weight=1
a=_State(False, shared=False)
def run():
	r.speed(40)
	sleep(1)
	s=State.start
	if not pathfind(-s[0], s[1]):
		return False

	_label('a')

	_goto('a')
