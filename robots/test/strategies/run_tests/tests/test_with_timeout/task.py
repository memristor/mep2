import time
cnt = _State(5)
def run():
	# r.conf_set('send_status_interval', 10)
	# r.turn(-1)
	# r.absrot(0)
	# r.forward(400)
	# r.forward(40)
	# r.goto(0,-500)

	# r.setpos(0,0,0)
	@_core.do
	def pr_time(n):
		_print(str(n), time.time())
	# r.move( 200 ,100,0)
	
	with _while(lambda: cnt.val > 0):
		@_do
		def _():
			print( cnt.val )
		
		with _timeout(1.0):
			pr_time('0')
			sleep(1.5)
			pr_time('01')
			# r.move( -600 ,200)
		pr_time('02')
		sleep(5)
		pr_time('1')
		sleep(5)
		pr_time('2')
		sleep(5)
		pr_time('3')
		sleep(5)
		pr_time('4')
		sleep(5)
		cnt.inc(-1)
		# r.move( -600 ,-200)
		
		# r.move( 600 ,-200)
		
		# r.move( 600 ,200)
		
		# r.move( 600 ,200)



