
weight =1
def run():

	pump(1,1)
	sleep(1)
	p = napredp.picked()
	@_do
	def _():
		if p.val:
			State.pokupio = 1
	pump(1,0)
