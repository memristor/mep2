weight=1
def run():
	x = 0.5
	r.setpos(58,48)
	r.speed(int(100*x))
	turbina(0)
	##
	#  sleep(10)
	
	def listen_msg(msg):
		print('listen2 msg', msg)
		if msg == 'continue':
			_label('continue')
	_listen('message', listen_msg)
	
	#  _sync('continue')
	def cont():
		print('continuing')
	_do(cont)

	##########################
	### ISPALJIVANJE NASIH ###
	##########################
	klapna(1)
	cev(0)
	#  turbina(85)

	#  r.goto(720,48)	
	
	#  sleep(0.3)
	#  for i in range(8):
		#  r.forward(1)
		#  sleep(0.01)
		#  r.forward(-15)
		#  sleep(0.01)
	#  sleep(0.5)

	##########################
	######## PCELICA #########
	##########################
	r.setpos(0,0)
	r.goto(-500, 0, -1)
	r.goto(0,0)
	return
	turbina(0)
	r.speed(int(130 * x))
	sleep(0.05)
	
	r.goto(1050,430)
	r.goto(500,48,-1)
	#  r.goto(1300,630)
	
