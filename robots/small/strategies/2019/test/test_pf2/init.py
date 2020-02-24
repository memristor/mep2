def run():
	sleep(4)
	s=-1
	State.start = [s*1188,16]
	_print('setting pos', State.start)
	r.setpos(*State.start,-180 if s > 0 else 0)

