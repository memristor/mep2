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
#pump(0, 1)
	for j in range(1000):
		sleep(0.1)
		f()
		
#pump(0, 0)

