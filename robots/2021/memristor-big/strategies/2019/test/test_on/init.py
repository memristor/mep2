def run():
	def haha():
		print('test')
	_on('hehe', haha, _name='tst')
	_unlisten(_name='tst')
	_emit('hehe')
	


