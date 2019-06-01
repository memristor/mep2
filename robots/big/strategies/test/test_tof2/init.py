b = _State(0)
import time
def run():
	
	_print('tof test')

	_goto('start')	
	for i in range(8):
		# sleep(0.1)
		_print('shuttin', i)
		tof.start(i)
		tof.stop(i)
	# sleep(5)
	# with _while(lambda: b.val < 10):
	
	# z = tof.measure(7)
	# @_do
	# def _():
		# r.forward(150 + 20 - z.val)
	# return

	_L('start')
	r.speed(20)
	a=State()
	@_do
	def pre():
		a.angle = 30
		a.e=[]
		a.cnt=0
		a.c=None

	@_spawn
	def w():
		a.r = _ref()
		with _while(1):
			m = tof.measure(7)
			@_do
			def add_val():
				a.e.append((_core.get_orientation(), m.val))

				'''
				c = min(a.e, key=lambda a: a[1])
				if a.c == c: a.cnt+=1
				a.c = c
				if a.cnt > 15:
					_print('prefound')
					_sync(1, ref='main')
					r.stop()
					r.absrot(c[0])
					_goto('done', ref='main')
				'''
	sleep(0.3)

	@_do
	def _():
		r.turn(-a.angle)
		r.turn(+a.angle*2)

	@_do
	def post():
		_print('postfound')
		_return(ref=a.r)

		print(a.e)
		m = min(a.e, key=lambda a: a[1])
		print('best',m)
#r.turn((-a.angle+m[0]))
		r.absrot(m[0])

	_L('done')
	tof.stop()
	
		# b.inc()

	# 0 - nista
	# 1 - desna, prednja strana
	# 2 - nista
	# 3 - prednja desna strana
	# 4 - prednja leva strana
	# 5 - nista - bi trebalo da bude desna zadnja
	# 6 - leva,zadnja strana
	# 7 - zadnji
