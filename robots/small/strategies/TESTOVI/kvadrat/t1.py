weight = 10

def run():	

	for i in range(9):
		r.speed(100)
		y=500
		s=0.5
		r.goto(700,0)
		sleep(s)
		r.goto(700,y)
		sleep(s)	
		r.goto(0,y)
		sleep(s)
		r.goto(0,0)
		sleep(s)
		r.absrot(0)
