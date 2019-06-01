
def run():
	@_core.listen('test')
	def _():
		print('a test 2')
	@_core.on('test')
	def _():
		print('a test')

	_emit('test')
	_emit('test')
	_emit('test')
