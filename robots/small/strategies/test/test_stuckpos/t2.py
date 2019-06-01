weight=.5
def run():
	sleep(3)
	r.stuckpos(-1, y=500)
	@_do
	def pos():
		print('new pos', _core.get_position())

	sleep(2)
	r.absrot(90)
