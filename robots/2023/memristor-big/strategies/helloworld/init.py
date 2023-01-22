import time
def run():
	r.setpos(0,0,0)
	amp = 300
	
	with _while(1):
		r.move( -amp, -amp)

		r.move(  amp, -amp)

		r.move( amp, amp)

		r.move( -amp, amp)
