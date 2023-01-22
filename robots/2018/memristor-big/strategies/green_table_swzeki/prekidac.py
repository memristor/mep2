import core.State as State
weight=20
#zelena
def run():

	with disabled('collision'):
		r.speed(150)
		r.goto(640, -750) #  r.goto(700, -50)
		#r.speed(40)	#ne treba	
		r.goto(360, -750) # r.goto(700, -450)		
		r.absrot(-90)
		r.speed(30)
		rotate(2)
		lift_sw()
		
		#_on('stuck', _next_cmd)
		#r.conf_set('enable_stuck',0)
		# dodati za stuck

		r.forward(70) #udarac na 80
		#UDARI PREKIDAC podesiti isklj stuck
		
		r.speed(150)
		r.forward(-160)
		r.goto(200,-460,-1)
		r.absrot(0)

	########################


	
	  
	

	
