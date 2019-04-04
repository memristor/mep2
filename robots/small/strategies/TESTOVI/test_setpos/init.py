def run():
	r.setpos(0,0,0)
	r.conf_set('enable_stuck', 1)

	r.speed(40)
	@_on('motion:stuck')
	def _():
		_goto('after_stuck', ref='main')

	r.goto(-1000, 0, -1)

	_label('after_stuck')
	r.setpos(x=155/2-1500)


	r.goto(0,0)
