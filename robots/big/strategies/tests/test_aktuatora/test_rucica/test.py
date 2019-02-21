weight = 1


def run():

	_print("************** Otvori rucice")
	@_listen('servo:error')
	def on_servo_err(name):
		print('servo error', name)

	a=lfliper(1)
	@_do
	def _():
		print('servo status',a.val.val)
	rfliper(1)

	sleep(1)
	_print("************** Zatvori rucice")
	lfliper(0)
	rfliper(0)
