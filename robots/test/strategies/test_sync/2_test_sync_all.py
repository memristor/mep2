order=2
a=_State(1)
def run():
	@_spawn
	def _():
		sleep(2)
		a.val = 5
	@_spawn
	def _():
		sleep(2)
		a.val = 5
		
	_sync()
	
	@_do
	def _():
		if a.val == 5:
			print('fail')
			exit(0)
	
