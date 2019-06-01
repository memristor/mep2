def run():
	r.conf_set('keep_count', 10000)
	r.speed(50)
	
	# r.curve_rel(500+20,48-6-2+1+3)
	# r.curve_rel(-330+20+20-100-50,34-3-2-2)
	# return
	
	# with r.chain():
	# r.move(200,200)
	# r.move(300,200)
	# r.move(300,-200)
	# r.move(0,0)
	# return
	r.speed(70)
	r.accel(700)
	a=30
	rad=250
	with r.chain():
		# r.end_speed(80)
		# r.forward(300)
		# r.speed(80)
		# r.end_speed(150)
		# r.forward(300)
		# r.speed(150)
		# r.end_speed(60)
		# r.accel(900)
		# r.forward(300)
		# r.speed(60)
		# r.forward(300)
	# r.forward(-300*4)
		r.forward(200)
		r.curve_rel(rad,a)
		r.curve_rel(-rad,a*2)
		
		r.curve_rel(rad,a*2)
		r.curve_rel(-rad,a*2)
	return
	r.speed(200)
	# r.curve_rel(200,50)
	# r.curve_rel(-200,50*2)
	# r.curve_rel(200,50*2)
	# r.curve_rel(-200,50*2)
	# r.curve_rel(200,50)
	# return
	# r.absrot(90)
	r.conf_set('send_status_interval',10)
	r.accel(500)
	# with r.chain(100):
		# a = 400
		# rad = 200
		
		# for i in range(10):
			# r.move(a,a, rad)
			# r.move(a,-a, rad)
			# r.move(-a,-a, rad)
			# r.move(-a,a, rad)
	# return
	r.setpos(-1000,0)
	with r.chain():
		for i in range(5):
			# r.end_speed(100)
			r.speed(200)
			r.end_speed(80)
			r.forward(100)
			
			r.speed(80)
			r.forward(100)
		# for i in range(10):
			# r.forward(30)
	
	with r.chain():
		a = 180
		b = 200
		
		for i in range(2):
			r.curve_rel(b, a)
			r.curve_rel(-b, a)
		
		r.curve_rel(b, a)
		r.curve_rel(b, a)
		
		for i in range(2):
			r.curve_rel(-b, a)
			r.curve_rel(b, a)

	r.goto(500,20)
	with r.chain():
		r.forward(100)
		r.forward(100)
		r.forward(200)
		# r.end_speed(0)
		r.curve_rel(200,360)
		r.end_speed(0)
		r.curve_rel(-200,360)
		r.end_speed()
		r.forward(100)
		r.forward(100)
		r.forward(-100)
		r.forward(-100)
		r.forward(-100)
		r.forward(-100)
