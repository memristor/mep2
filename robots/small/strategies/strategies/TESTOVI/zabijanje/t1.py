weight=1
def zabijanje(setpos=[0,0], vec=[0,0]):

	r.conf_set('enable_stuck', 1)
	@_on('motion:stuck')
	def on_stuck():
		#_next_cmd()
		_goto('a', ref='main')

	pos=_core.get_position()
	r.goto(pos[0] + vec[0]*1000, pos[1] + vec[1]* 1000)
	
	_label('a')
	r.setpos(setpos[0] if setpos[0] != 0 else None, setpos[1] if setpos[1] != 0 else None)

def run():

	r.conf_set('enable_stuck', 1)
	@_on('motion:stuck')
	def on_stuck():
		#_next_cmd()
		_goto('a', ref='main')

	r.goto(1000, 0)
	
	_label('a')
	r.setpos(x=400)

