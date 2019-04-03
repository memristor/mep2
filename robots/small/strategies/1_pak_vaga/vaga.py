weight= 3
# kupi prvi pak 
def run():
	if State.pokupio == 0:
		pump(1,0)
		return
	# nosi na vagu
	r.goto(-200,250)
	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,250,1)
	
	
