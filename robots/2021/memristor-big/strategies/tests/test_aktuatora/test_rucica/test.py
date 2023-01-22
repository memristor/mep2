weight = 1


def run():

	_print("************** Otvori rucice")
	@_listen('servo:error')
	def on_servo_err(name):
		print('servo error', name)

	a=lfliper(1)
	
	# jedan nacin provere
	@_do
	def provera_uspeha_servoa():
		if a.val:
			print('servo ok')
		else:
			print('servo fail')
			
	
	# drugi nacin provere
	@_on('servo:error')
	def check_servo(name):
		if name == 'rfliper':
			print('servo rfliper error')
	rfliper(1)
	

	sleep(1)
	_print("************** Zatvori rucice")
	lfliper(0)
	rfliper(0)
