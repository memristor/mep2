weight=2

def unload(n):
	p = pressure(n)
	@_do
	def _():
		print(State.pumpe[n].val)
		if State.pumpe[n].val != False and p.val == True:
			# addpts(State.color_vaga_bodovi[State.pumpe[n].val])
			addpts(State.color_elem_bodovi[State.pumpe[n].val])
		State.pumpe[n].val = False

def run():
		if not any([State.pumpe[i].val for i in range(1,10)]):
			return False
			
		
		#-----------------------------------------------------------------------------
		#isporuka plavog
		r.speed(100)
		r.goto(-1250+10+10,250-50-20-50,1)
		x = -1180
		r.goto(x,110,1)  
		r.absrot(-90)
		unload(4)
		pump(4,0)
		sleep(1)
		
		#isporuka zeleni prvi
		r.goto(x,-390,1)
		unload(5) 
		pump(5,0) # zeleni
		
		#isporuka crveni
		r.goto(x,-600,1)  #bilo 600
		unload(6)
		pump(6,0)
		
		# OKRETANJE
		r.goto(x,-620,1) 
		r.turn(-180)
		#crveni drugi put
		r.goto(x,-570,1)
		unload(3) 
		pump(3,0)
		
		#zeleni drugi put i crveni
		r.goto(x,-310,1)
		unload(2)  
		pump(2,0) # crveni drugi
		
		r.goto(x,-250,1)
		unload(1) 
		pump(1,0) # zeleni drugi
		sleep(1)
		
		r.goto(-1300,850,1)
	
		
	
