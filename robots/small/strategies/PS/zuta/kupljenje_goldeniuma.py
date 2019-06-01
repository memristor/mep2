aktivirao = _State(0)
weight = 8
def run():
	
	r.speed(80)
	print('trying task gold')
	if not State.goldenium_activated.val:
		return False
		
	x,y=coord('goldenium')
	#r.goto(*coord('goldenium'))
	if not pathfind(x-16,y+8, -1):
		return False
	r.absrot(-90)

	napgold(2)
	sleep(0.3)
	pump(2,1)
	# Implementirati stak umesto ovoga
	
	
	
	r.speed(60)
	r.forward(101)
	sleep(0.3)
	r.speed(140)
	napgold(0)
	r.forward(-91)
	sleep(0.2)
	sleep(1)
	p = napredp.picked()
	@_do
	def _():
		if not p.val:
			addpts(-20)
		if not p.val and State.must_stuck.val != 1:
			State.must_stuck.val = 1
			print('must reactivate')
			State.goldenium_activated.val = 0
			_task_suspend('aktiviranje_akceleratora')
			
	
	State.goldenium_picked.val = 1
	r.speed(120)
	
