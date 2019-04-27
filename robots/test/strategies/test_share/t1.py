weight=1
a=_State('a', name='var1', shared=True)
def run():
	@_do
	def _():
		print(a.val)
	sleep(10)
	a.val = 5
	@_do
	def _():
		print(a.val)
	sleep(10)
	a.val = 8
	@_do
	def _():
		print(a.val)
