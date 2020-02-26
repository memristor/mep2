weight=1
def run():
	@_spawn
	def _():
		rfliper(2)
	lfliper(2)
	
	@_spawn	
	def _():
		sleep(40)
		_goto('done', ref='main')

	with _while(1):
		col1 = levi.color()
		col2 = desni.color()
		@_do
		def _():
			print( col1.val, col2.val )

		sleep(0.1)

	_label('done')
	_print('warning zatvaranje flipera :)')
	sleep(10)
	@_spawn
	def _():
		rfliper(0)
	lfliper(0)
