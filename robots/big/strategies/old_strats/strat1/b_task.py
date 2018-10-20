name ='...a_task...'
description='basic task'
weight=4
task_instances = [
	{
		'weight': 5,
		'time': 7
	}
]

def leave():
	pass



def run():
	
	r.goto(705,-35)
	sleep(0.3)

	for i in range(2):
		r.forward(25)
		sleep(0.01)
		r.forward(-25)
		sleep(0.01)
	sleep(0.5)

	##########################
	######## PCELICA #########
	##########################

	r.forward(-200)
	sleep(0.05)
	r.goto(1050,-430)
	r.goto(1150,-430)
	r.goto(1600,-95)
	sleep(0.05)
	r.turn(-180)
	pcelica(1)
	sleep(0.5)
	r.goto(1815,-95,-1)
	sleep(0.5)
	pcelica(0)
	sleep(1)
	r.forward(100)
	r.turn(180)
	r.conf_set('enable_stuck',1)


	##########################
	######## PREKIDAC ########
	##########################
	r.speed(130)
	r.goto(700,-1100,-1)
	r.goto(100,-930, -1)
	r.speed(40)
	r.conf_set('enable_stuck',0)
	r.goto(-100,-930,-1)
	r.setpos(0,-930,-90)
	r.speed(20)
	r.conf_set('enable_stuck',1)
	r.goto(100,-930)
	sleep(0.05)
	prekidac(1)
	sleep(0.5)
	r.goto(24, -930,-1)
	r.goto(100, -930)
	prekidac(0)
	#r.send(b's')
	#r.goto(58,-37,-1)

	###########################
	########SORTIRANJE########
	##########################
	r.goto(1400, -2400)
	r.goto(1755, -2600)
	#r.goto(1744, -2500)
	r.turn(180)
	cev2(0)
	cev(1)
	klapna(1)
	r.goto(1755, -2265, -1)
	r.conf_set('enable_stuck',0)

	for i in range(1):
		r.forward(20)
		sleep(0.05)
		r.forward(-20)
		sleep(0.05)

		r.goto(1755,-2217,-1)
		sleep(2)
		klapna(2)
		sleep(1)
		klapna(1)
		cev2(1)
		sleep(1)
		r.goto(1755,-2265)

		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)

		sleep(0.05)
		r.goto(1755, -2217, -1)
		sleep(2)
		klapna(2)
		sleep(2)

		for i in range(3):
			r.goto(1755,-2265)
			sleep(0.05)

		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)

		r.goto(1755,-2217,-1)
		sleep(0.3)
		klapna(1)
		sleep(0.3)
		r.goto(1755,-2165,-1)
		sleep(0.05)

		for i in range(1):
			r.forward(20)
			sleep(0.05)
			
			r.forward(-20)
			
			sleep(0.05)

		sleep(0.05)
		r.goto(1755,-2217)
		sleep(0.5)
		klapna(2)
		sleep(0.5)

		klapna(1)
		r.conf_set('enable_stuck',1)
		cev(1)
		
	#  import core.Chain
	#  core.Chain.f.close()
