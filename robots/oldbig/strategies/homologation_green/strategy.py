weight=1
def run():

	###############################################################
	r.setpos(330,-100)
	x=0.3
	r.speed(int(50*x))
	def hg():
		print('hom green')
	_do(hg)
	# 575 -54
	lift(1)
	#r.goto(330, -150)
	sleep(0.1)
	#r.absrot(0)
	r.speed(int(50*x))
	r.goto(450,-150)
	#r.absrot(0)
	r.speed(int(50*x))
	r.goto(1500,-150)
	r.goto(450,-150, -1)
	r.goto(700,-150)
	send_msg('continue')
	sleep(1)
	rotate(0)
	lift(0)
	pump(0,1)
	sleep(1.5)
	lift(1)
	sleep(1.5)
	rotate(2)
	pump(0,0)
	r.goto(800,-150, -1)
