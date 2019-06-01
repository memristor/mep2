weight=4

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
		r.goto(1250,250-30,1)
		x = 1180
		r.goto(x,110,1)  
		r.absrot(-90)
		unload(3)
		pump(3,0)
		sleep(1)
		
		#isporuka zeleni prvi
		r.goto(x,-390,1)
		unload(1) 
		pump(1,0) # zeleni
		
		#isporuka crveni
		r.goto(x,-600,1)  #bilo 600
		unload(2)
		pump(2,0)
		
		# OKRETANJE
		r.goto(x,-620,1) 
		r.absrot(90)
		#crveni drugi put
		r.goto(x,-570,1)
		unload(4) 
		pump(4,0)
		
		#zeleni drugi put i crveni
		r.goto(x,-310,1)
		unload(5)  
		pump(5,0) # crveni drugi
		
		r.goto(x,-250,1)
		unload(6) 
		pump(6,0) # zeleni drugi
		sleep(1)
		
		
		
		r.goto(1300,720,1)
		
		return
		#-----------------------------------------------------------------------------
		#isporuka plavog
		r.speed(100)
		#r.goto(1180,110,1)
		x,y = coord('start_plavi')
		r.goto(x+50,y+100,1)
		r.goto(x,y+100,1)
		r.absrot(-90)
		unload(3)
		pump(3,0)
		sleep(0.2)
		
		
		
		#isporuka zeleni prvi
		#r.goto(1180,-390,1)
		x,y = coord('start_zeleni') 		
		r.goto(x,y+50,1) 
		unload(1)
		pump(1,0) # zeleni
		sleep(0.2)
		
		
		#isporuka crveni
		#r.goto(1180,-520,1)  #bilo 600
		x,y = coord('start_crveni')
		r.goto(x,y,1)  #bilo 600
		unload(2)
		pump(2,0)
		sleep(0.2)
		
		
		
		# OKRETANJE
		x,y = coord('start_crveni')
		#r.goto(1180,-620,1) 
		r.goto(x,y-150,1) #OVO MENJAS
		r.absrot(90)
		#crveni drugi put
		#r.goto(1180,-570,1)		
		r.goto(x,y-50,1) 
		unload(4)
		pump(4,0)
		sleep(0.2)
		
		
		#zeleni drugi put i crveni
		#r.goto(1180,-290,1)  
		r.goto(x-100,y+230,1)  
		unload(6)
		pump(6,0) # crveni drugi
		sleep(0.2)
		
		
		
		x,y = coord('start_zeleni')
		
		#r.goto(1180,-270,1) 
		r.goto(x-100,y+120,1) 
		unload(5)
		pump(5,0) # zeleni drugi
		sleep(0.2)
		
		
		# r.goto(1200,800,1) #ZEKIIII  1265
		#dodati spustanje lifta skroz dole
		
