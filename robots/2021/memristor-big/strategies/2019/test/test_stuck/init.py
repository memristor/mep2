def run():
	r.conf_set('enable_stuck', 1)
	def f():
		_goto(offset=1, ref='main')
	_on('motion:stuck', f, _name='ramp_stuck')
	r.forward(1000)
	r.conf_set('enable_stuck', 0)
	_unlisten(_name='ramp_stuck')
#r.intr()
	r.forward(0)
