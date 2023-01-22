weight= 4
# kupi prvi pak 
def run():
	# 90 je setpos
	r.speed(120)
	

	r.curve_rel(-200, -180)
	

	
	
	r.goto(-830,190,-1)
	r.goto(-1035,300,-1)
	
	r.absrot(-90)
	
		
	
	@_spawn
	def _():
		nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)

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
	r.speed(30)
	sleep(0.5)
	r.goto(-1035,438,-1)

	r.speed(120)
	r.goto(-1035,350,1)
	
	'''@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
	

	
