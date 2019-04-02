order=1
a = _State()
def run():
	
	#################### _sync deco + _sync(ref=) + _sync([' ', ' '])
	
	_print('test1')
	@_spawn(_name='work1')
	def _():
		_print('\tdoing1')
		sleep(1)
		_print('\tmiddle1')
		a.val = 'middle'
		sleep(1)
		_print('\tdone1')
	
	@_spawn(_name='work2')
	def _():
		_print('\twork2 doing')
		sleep(0.1)
		_sync('lol',ref='work1')
		_print('\twork2 pause work')
		sleep(3)
		@_do
		def _():
			if a.val == 'middle':
				print('fail')
				exit(0)
		sleep(1)
		_label('lol')
		_print('\twork2 done')
		_return(ref='work1')

	_print('\tmain should wait for work')
	_sync(['work1','work2'])
	
	################# _sync([' ', ' '])
	a.val = None
	
	_print('test2')
	def _():
		_print('\tdoing1')
		sleep(1)
		_print('\tmiddle1')
		a.val = 'middle'
		sleep(1)
		_print('\tdone1')
	work1 = _spawn(_, _name='work1')
	
	def _():
		_print('\twork2 doing')
		sleep(0.1)
		_sync('lol1',ref='work1')
		_print('\twork2 pause work')
		sleep(3)
		@_do
		def _():
			if a.val == 'middle':
				print('\tfail')
				exit(0)
		sleep(1)
		_label('lol1')
		_print('\twork2 done')
		_return(ref='work1')
	work2 = _spawn(_, _name='work2')
	
	_print('main should wait for work')
	_sync(['work1','work2'])
	
	############## _sync([ , ])
	a.val = None
	
	_print('test3')
	def _():
		_print('\tdoing1')
		sleep(1)
		_print('\tmiddle1')
		a.val = 'middle'
		sleep(1)
		_print('\tdone1')
	work1 = _spawn(_, _name='work1')
	
	def _():
		_print('\twork2 doing')
		sleep(0.1)
		_sync('lol3',ref='work1')
		_print('\twork2 pause work')
		sleep(3)
		@_do
		def _():
			if a.val == 'middle':
				print('fail')
				exit(0)
		sleep(1)
		_label('lol3')
		_print('\twork2 done')
		_return(ref='work1')
	work2 = _spawn(_, _name='work2')
	
	_print('main should wait for work')
	_sync([work1, work2])

