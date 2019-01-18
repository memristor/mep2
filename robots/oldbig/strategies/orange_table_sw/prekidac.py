import core.State as State
weight=20
#NARANDZASTA
def run():
	
	
	with disabled('collision'):
		r.speed(150)
		r.goto(-640, -750) #  r.goto(700, -50)
		
		r.speed(40)
		r.goto(-360, -750) # r.goto(700, -450)		
		r.absrot(-90)
		r.speed(100)#sa 80
		rotate(2)
		lift_sw()

		r.speed(30)
		r.forward(80) #udarac na 80
		#UDARI PREKIDAC podesiti isklj stuck
		#u zelenoj ima kako se to radi 
		#blaske mora to da resi inace ovde izgubi poziciju	
		addpts(25)
		r.speed(150)
		r.forward(-160)
		r.goto(-200,-460,-1)
		r.absrot(180)
		

	########################


	
	  
	

	
