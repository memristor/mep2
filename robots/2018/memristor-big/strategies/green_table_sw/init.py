import core.State as State
def run():
	r.setpos(1260,-800,180)
	#  r.setpos(-1260,-800,180)
	#r.conf_set('enable_stuck', 1)
	#_do(lambda: print('stuck enabled'))
	#combination = ['blue','green','orange']
	#combination = ['blue','orange','black']
	combination = ['black','blue','green']
	#combination = ['black','yellow','orange']
	#combination = ['black','blue','yellow']
	#combination = ['green','yellow','blue']
	#combination = ['orange','blue','yellow']
	#combination = ['orange','black','green']    
	#combination = ['yellow','black','blue']
	#combination = ['yellow','green','black']

	State.combination = combination
	#  r.softstop()
	#  r.speed(50)
	#  r.forward(-1200)
	sleep(4)
	#  sleep(5000)
