weight=1
def run():
	r.stuckpos(1, y=100)
	@_do
	def pos():
		print('new pos', _core.get_position())
