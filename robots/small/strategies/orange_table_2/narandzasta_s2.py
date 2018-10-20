from core.Core import Core
from core.Util import Transform
weight=1
def run():
	##
	_unlisten('collision')
	core = Core()
	r.conf_set('send_status_interval',100)
	r.setpos(58,-37)
	core.transform = Transform( ([58,-37], 90), ([-1500+50, -1000+50], 0) )
	r.speed(100)
	r.t(0)
	##


	#######################
	# TASK
	#######################

	'''
	cev(1)
	cev2(1)
	r.forward(-450)
	r.t(115)
	sleep(2)
	cev(0)
	sleep(2)
	r.t(0)
	'''
	#exit(0)

	#################
	## INICIJALIZACIJA
	##################


	'''
	klapna(1)
	sleep(0.3)
	klapna(2)
	sleep(0.3)
	klapna(1)
	sleep(0.3)


	cev(0)
	sleep(0.3)
	cev(1)
	sleep(0.3)
	cev(0)
	sleep(0.3)

	cev2(0)
	sleep(0.3)
	cev2(1)
	sleep(0.3)
	cev2(0)
	sleep(0.3)



	prekidac(0)
	sleep(0.3)
	prekidac(1)
	sleep(0.3)
	prekidac(0)
	sleep(0.3)'''
	klapna(1)
	cev(0)
	cev2(0)
	prekidac(0)
	#sleep(10)

	##########################
	### ISPALJIVANJE NASIH ###
	##########################
	r.t(85)
	r.goto(705,-35)
	sleep(0.3)
	for i in range(8):
		r.forward(25)
		sleep(0.01)
		r.forward(-25)
		sleep(0.01)
	sleep(0.5)

	##########################
	######## PCELICA #########
	##########################

	r.forward(-200)
	r.t(0)
	r.speed(110)### za drugi sto na prvom je bilo 130
	sleep(0.05)
	r.goto(1050,-430)
	r.goto(1150,-430)
	r.goto(1600,-85)
	sleep(0.05)
	r.turn(-180)
	pcelica(2)
	sleep(0.5)
	##########m za drugi sto stavljam -60 za prvi bilo -65
	
	r.goto(1815,-65,-1)
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
	_listen('collision')
	r.goto(700,-1100,-1)
	_unlisten('collision')
	r.goto(100,-930, -1)
	r.speed(40)
	r.conf_set('enable_stuck',0)
	r.goto(-100,-930,-1)
	r.setpos(0,-930)
	r.speed(20)
	r.conf_set('enable_stuck',1)
	r.goto(100,-930)
	sleep(0.05)
	prekidac(1)
	sleep(0.5)
	r.goto(24, -930,-1)
	r.goto(100, -930)
	prekidac(0)
	r.speed(130)
	#r.send(b's')
	#r.goto(58,-37,-1)
	#r.goto(1200,-1400)
	#exit(0)

	###########################
	########SORTIRANJE########
	##########################
	r.goto(1400, -2400)
	r.goto(1700, -2600)
	r.turn(180)
	r.conf_set('enable_stuck',0)
	r.speed(60)###promjenio sa 50
	r.goto(1900, -2600)
	sleep(0.3)
	#  core.transform.transform(([58,-37], 0), ([-1500, -800], 90))
	'''
	r.setpos(1840,-2600)
	r.goto(1740, -2600,-1)
	sleep(0.5)
	r.speed(60)
	r.goto(1740, -2900)
	sleep(0.3)
	klapna(1)
	###DODAJEM MU -2820 za drugi sto na prvom bilo -2830
	r.setpos(1740,-2830)#promjenio y sa 2840
	r.speed(100)

	r.goto(1246,-2830,-1)#povecali x 1243, dosao na odlicnu poziciju

	######SORTIRANJE#############

	for i in range(1):
		r.forward(20)
		sleep(0.05)
		r. forward(-30)
		sleep(0.05)
	r.goto(1200,-2820,-1)
	sleep(0.5)
	klapna(2)
	sleep(1)
	cev2(1)
	klapna(1)
	sleep(1)
	r.goto(1246,-2820)
	##########SORTIRANJE###############
	for i in range(3):
		r.goto(1200,-2820,-1)
		sleep(0.1)
		klapna(2)
		r.goto(1155,-2820,-1)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-30)
		sleep(0.1)
		r.goto(1200,-2820)
		sleep(0.1)
		klapna(1)
		r.goto(1246,-2820)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-30)

	cev(1)
	klapna(1)
	'''

	sleep(0.5)
	'''
	r.forward(200)
	r.goto(1000,-3150,-1)##sa 3100
	r.goto(500,-3170,-1)
	exit(0)
	r.goto(500, -3570)#asa 900
	exit(0)
	r.turn(90)
	r.conf_set('enable_stuck',0)
	r.forward(300)
	cev2(0)
	###DODATO
	sleep(2)
	r.forward(-300)
	r.goto(500,-3600)
	r.goto(400,-3500)

	'''
	
