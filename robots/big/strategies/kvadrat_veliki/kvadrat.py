weight=10
def run():
		s=0.5
		sleep(s)
		r.speed (80)
		for i in range(5):
			x = 1000
			y = 600
			z=1
			r.goto(x,0,z)
			sleep(s)
			r.goto(x,y,z)
			sleep(s)
			r.goto(0,y,z)
			sleep(s)
			r.goto(0,0,z)
			r.absrot(0)
