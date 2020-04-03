
@_core.do
def test2():
	sleep(1)
	_return(35)

	
@_core.do
def test1():
	_return(test2())

@_core.do
def test():
	_print('test')
	a=_spawn(test1)
	@_do
	def _():
		print('test1', a.val)
	return a
	
def run():
	a=test()
	@_do
	def _():
		print('ret', a.val)
	
	@_spawn
	def _():
		_return(67)
	
	a=future()
	sleep(1)
	@_do
	def _():
		print(a.val)

