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

	#ide do prvog 
	r.goto(-1035,250,-1)
	#r.diff_drive(-1035,250,90)
	@_spawn
	def _():
		nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(60)
	#_label('a')
	r.goto(-1035,390,-1)
	sleep(2)
	
	#if not
	#_goto('a')
	r.speed(120)
	r.goto(-1035,250,1)
	sleep(1)
	
	

	r.goto(-200,250)
	r.goto(-200,450,-1)
	nazgold(1)
	pump(1,0)
	sleep(1)
	r.goto(-150,250,1)
	#r.goto(-800,-550,1)
	#r.goto(-1150,-550,1)
	#sleep(1)
	
