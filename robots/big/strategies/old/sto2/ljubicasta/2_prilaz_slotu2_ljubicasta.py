weight=5
def run():
	# remove later
	# with _parallel():
		# llift(0)
		# rlift(0)
		# lift(2,'sredina')
		# lift(1,'sredina')
			
	r.goto(-1100,250,1) 
	r.speed(100)
	
	_sync()
	
	#r.goto(795,355)
	r.goto(*coord('slot_2_1'), 1)
	#sleep(1)
	sleep(0.1)
	r.absrot(0)
	
	for i in (1,2,3):
		pump(i,1)
	
	llift(2)
	lift(2,'sredina', 1)
	llift(1)
	sleep(0.1)
	
	p1 = [pressure(i) for i in (1,2,3)]
	
	
	#TODO: Proveriti boje
	@_do
	def _():
		State.pumpe[1].val = 'crveni' if p1[0].val else False
		State.pumpe[2].val = 'zeleni' if p1[1].val else False
		State.pumpe[3].val = 'plavi' if p1[2].val else False
	sleep(0.1)
	r.absrot(0)	
	sleep(0.1)
	r.turn(180)
	sleep(0.1)
	#r.goto(698,355,-1)
	r.goto(*coord('slot_2_2'),-1)
	sleep(0.1)
	
	for i in (4,5,6):
		pump(i,1)
	rlift(2)
	sleep(0.1)
	lift(1,'sredina', 1)
	rlift(1)
	
	p2 = [pressure(i) for i in (4,5,6)]
	
	
	#TO_DO: Proveriti boje
	@_do
	def _():
		State.pumpe[4].val = 'crveni' if p2[0].val else False
		State.pumpe[5].val = 'zeleni' if p2[1].val else False
		State.pumpe[6].val = 'plavi' if p2[2].val else False
	
	
	
	r.goto(-1500+110+60+30+50-50,350,1)#dodao 30
	return
