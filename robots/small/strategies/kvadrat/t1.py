weight = 10

def run():	
	for i in range(5):
		r.speed(50)
		y=500
		s=0.5
		r.goto(1000,0)
		sleep(s)
		r.goto(1000,y)
		sleep(s)	
		r.goto(0,y)
		sleep(s)
		r.goto(0,0)
		sleep(s)
		r.absrot(0)
