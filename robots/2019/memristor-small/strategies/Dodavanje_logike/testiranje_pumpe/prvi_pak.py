weight= 4
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(60)
i	#r.forward(200)
	
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
				print('Uhvatio----------------------------------')# skontao da je uhvatio!!!!
				_goto('Done', ref='test')
		_goto('a')
		_label('Done')
	r.speed(30)
	
	sleep(2)
	addpts(10)
	_print("pak----------------------------")
	p1=nazadp.picked()
	@_core.do
	def f(p):
		_print(p.val)
	f(p1)
	#r.forward(-200)
	pump(1, 0)
