weight=1
def run():
	_print('test parallel')
	
	@_core.do
	def test(i):
		sleep(i)
		_print('done',i)
	
	with _parallel():
		test(2)
		test(5)
	
	sleep(10)
	_print('done')
