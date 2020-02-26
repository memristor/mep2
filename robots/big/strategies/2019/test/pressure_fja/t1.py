weight=1
def run():
	
	llift(2)
	rlift(2)
	@_core.do
	def check_pts(idx):
		p = pressure(idx)
		@_do
		def _():
			if p.val == 1:
				addpts(6)
				print('dodati poeni!!!!!')
				
	'''#test p1
	pump(1,1)
	sleep(3)
	check_pts(1)
	pump(1,0)
	sleep(1)
	
	#test p2
	pump(2,1)
	sleep(3)
	check_pts(2)
	pump(2,0)
	sleep(1)
	
	#test p3
	pump(3,1)
	sleep(3)
	check_pts(3)
	pump(3,0)
	sleep(3)
	
	#test p4
	pump(4,1)
	sleep(3)
	check_pts(4)
	pump(4,0)
	sleep(1)
	
	#test p5
	pump(5,1)
	sleep(3)
	check_pts(5)
	pump(5,0)
	sleep(1)'''
	
	#test p6
	pump(6,1)
	sleep(3)
	check_pts(6)
	pump(6,0)
	sleep(1)
	
	#test p7
	pump(7,1)
	sleep(3)
	check_pts(7)
	pump(7,0)
	sleep(1)
	
	#test p8
	pump(8,1)
	sleep(3)
	check_pts(8)
	pump(8,0)
	sleep(1)
	
	#test p9
	pump(9,1)
	sleep(3)
	check_pts(9)
	pump(9,0)
	sleep(1)
	
