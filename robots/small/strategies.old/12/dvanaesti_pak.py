weight= 4
# kupi prvi pak 
def run():
	
	
	# 180 je set pos  
	r.forward(-100)
	
	
	r.turn(-60)
	r.curve_rel(-380, -110)
	r.curve_rel(-300, -100)
	
	r.goto(-850,250,-1)
	sleep(1)

	#ide do drugog 
	r.goto(1035,250,-1)
	@_spawn
	def _():
		#napgold(1)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(60)
	#_label('a')
	r.goto(1035,390,-1)
	sleep(2)
	
	#if not
	#_goto('a')
	r.speed(120)
	r.goto(1035,250,1)
	sleep(1)
	
	r.goto(-800,250,1)
	r.goto(-800,-550,1)
	r.goto(-1225,-550,-1) # da pak ispred polja da ne bi ovaj sa pumpe lupio u njega 
	r.goto(-1100,-550,1) 
	pump(1,0)
	sleep(1)
	
