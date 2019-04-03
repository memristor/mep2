weight= 4
# kupi prvi pak 
def run():
	
	#r.goto(1100,780) # da zaobidje pak ispred red	
	#Mora da zaobidje prvi pak ispred pocetne pozicije
	# 180 je set pos  
	r.forward(-100)
	
	sleep(1)	
	r.turn(-60)
	r.curve_rel(-380, -110)
	r.curve_rel(-300, -100)
	
	r.goto(-850,250,1)
	sleep(1)

	#ide do prvog 
	r.goto(-975,250,1)
	sleep(1)
	r.goto(-975,390,1)
	r.goto(-975,250,-1)
	sleep(1)
	
	r.goto(-850,250)
	r.goto(-850,-550,1)
	r.goto(-1150,-550,1)
	sleep(1)
	
