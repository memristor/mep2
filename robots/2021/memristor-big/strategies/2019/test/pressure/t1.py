weight=1
def run():

	@_core.do
	def f():
		a=[]
		for i in range(9):
			a.append( pressure(i) )
		@_do
		def _():
			print('holding ',  [b.val for b in a])
	
	@_core.do
	def t(i):
		p=pressure(i)

		@_do
		def _():
			print('pumpa', i, p.val)
	with _parallel():
		lift(1, 'sredina')
		lift(2, 'sredina')
		llift(1)
		rlift(1)
	_sync()
	for i in (8,9,7,3,2,1,4,6,5):
		_print('pumpa ', i)
		pump(i,1)
		for j in range(15):
			sleep(0.1)
			t(i)
		pump(i,0)
		
