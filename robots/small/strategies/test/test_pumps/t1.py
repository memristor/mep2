weight=1
a = _State('hh', 'naziv')
def run():
	@_spawn(_name='haha')
	def _():
		#with _while(1):
		_label('a')
		_goto('a')
		_label('b')
		p1=nazadp.picked()
		p2=napredp.picked()
		sleep(0.1)
		@_do
		def _():
			# print('drzi ', hex(p1.val), hex(p2.val))
			print('drzi ', p1.val, p2.val)
		_goto('b')

	for i in range(1,3):
		sleep(4)
		_goto('b', ref='haha')
		pump(i,1)
		sleep(5)
		pump(i,0)
		sleep(5)
	
