weight= 4
# kupi prvi pak 
def run():

	
	r.goto(-200,0,-1)
	
	@_spawn
	def _():
		#nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	sleep(2)
	

	
	r.goto(-400,0,-1)
	
	@_spawn(_name='test')
	def _():
		_label('a')
		p1=nazadp.picked()
		sleep(0.1)
		@_do
		def _():
			if p1.val:
				print("UHVATIO###########")
				_goto('Done', ref='test')
		_goto('a')
		_label('Done')
		_print('#################### vrednost ', State.pokupio)

	
	addpts(10)
	pump(1,0)