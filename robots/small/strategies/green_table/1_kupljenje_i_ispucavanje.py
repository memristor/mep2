
weight=20
def run():
	r.speed(80)###PROMJENIO SA 120 
	turbina(0)
	klapna(1)
	cev(0)
	turbina(85) ###########
	sleep(0.5)

	with disabled('collision'):
		r.goto(1316, -195)
		for i in range(8):
			r.forward(25)
			sleep(0.01)
			r.forward(-25)
			sleep(0.01) 

		sleep(0.5)
		r.speed(120)
		r.forward(-100)
		turbina(0)
		r.goto(934, 135)
	
	addpts(50)
