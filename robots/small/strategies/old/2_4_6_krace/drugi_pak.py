weight= 10
# kupi drugi pak 
def run():
	# 90 je setpos
	r.speed(80)
	

	r.curve_rel(-200, -180)
	r.speed(120)

	
	
	r.goto(-830,190,-1)
	r.goto(-935,300,-1)
	
	r.absrot(-90)
	
		
	
	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)
	
	r.speed(30)
	sleep(0.5)
	r.goto(-935,438,-1)

	@_spawn(_name='test')
	def _():
		_label('a')
		p1=nazadp.picked()
		sleep(0.1)
		@_do
		def _():
			if p1.val:
				print('Uhvatio')# skontao da je uhvatio!!!!
				_goto('Done', ref='test')
		_goto('a')
		_label('Done')
		
	r.speed(120)
	r.goto(-935,350,1)
	
	'''@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''


	
