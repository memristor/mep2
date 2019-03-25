def run():
	print('initial pos loaded')
	
	# neki test kretanja
	# r.setpos(-1370, 10, 0) #  r.setpos(490,48)  180 gleda u minus x
	# sleep(1)
	# r.forward(100)
	# r.speed(50)	
	# r.goto(-730,-830,1) #  r.goto(720,48)
	
	#---------------------------------------------
	#ljubicasti akcelerator pokretanje na 200mm
	rrucica(0)
	sleep(2)
	rrucica(1)
	sleep(2)
	r.forward(220)
	sleep(2)
	r.forward(-220)
	rrucica(0)
	#---------------------------------------------
	#ROZI MEHANIZAM PROBA NA 220mm
	# napgold(0)
	# sleep(2)
	# napgold(1)
	# sleep(2)
	# r.forward(-220)
	# sleep(2)
	# napgold(0)
	# r.forward(220)
	# sleep(2)
	# napgold(1)
	
	#---------------------------------------------
	#braon MEHANIZAM golden uzimanje PROBA NA 220mm

	# nazgold(0)
	# sleep(1)
	# r.forward(220)
	# sleep(3)
	# nazgold(1)
	# sleep(6)
	
	# nazgold(0)
	# r.forward(-350)
	# sleep(2)
	# nazgold(1)
	#---------------------------------------------
	
	# TEST FLIPER BUDJ
	# rfliper(0)
	# rfliper(1)
	# sleep(0.5)
	# rfliper(0)
	# sleep(0.5)
	# r.forward(100)
	# rfliper(1)
	# sleep(0.5)
	# rfliper(0)
	# sleep(0.5)
	# rfliper(1)
	# sleep(0.5)
	# r.forward(100)
	# rfliper(0)
	# sleep(0.5)
	# rfliper(1)
	# sleep(0.5)
	# rfliper(0)
	# r.forward(50)
	# sleep(0.5)
	# rfliper(1)
	# sleep(0.5)
	# rfliper(0)
	# r.forward(50)
	# sleep(0.5)
	# rfliper(1)
	# sleep(0.5)
	# rfliper(0)
	# sleep(0.5)
	# rfliper(1)
	#---------------------------------------------
	
