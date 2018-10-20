weight=1
#weight=10#dodatooooooo
def run():

	sleep(0.3)
	r.speed(150)

	y_sort = 833

	#r.goto(1200,1400)
	#return
	###################
	## SORTIRANJE
	#################
	cev(1)
	#pathfind(914,481) #1396,2278,-1
	sleep(0.05)
	if not pathfind(-1140,785):
		return False	
	#r.goto(-1140,785,-1) #1700, 2493,-1
	sleep(0.05)
	r.speed(30)
	r.goto(-1140,960,-1) # 1740,2474
	sleep(0.3)
	r.setpos(y=920)
	r.goto(-1140,y_sort)
	r.speed(90)
	klapna(1)
	r.goto(-950-5-5,y_sort)

	addpts(10)

	for i in range(6):
		r.forward(25)
		sleep(0.05)
		r.forward(-25)
		sleep(0.05)
	sleep(0.5)
	r.goto(-885-20-5,y_sort)
	cev2(1)
	klapna(2)
	sleep(0.5)
	r.goto(-840-20-5-5,y_sort)
	sleep(0.5)
	
	for i in range(6):
		r.forward(25)
		sleep(0.05)
		r.forward(-25)
		sleep(0.05)
	
	return
		
	
#############
#STARO
	
	sleep(0.3)
	r.speed(150)
	
	r.goto(500,50)
	r.goto(100,450)
	r.goto(0,500)
	r.goto(-150,500)
	r.goto(-1000,500)
	r.goto(-790,500,-1)
	
	r.goto(-790, 830)
	r.speed(40)

	r.conf_set('enable_stuck',0)
	r.goto(-600,830,-1)
	r.setpos(x=-610)
	r.goto(-705, 840)
	turbina(25)
	r.goto(-735, 870)
	r.goto(-772, 870)
	
	for i in range(15):
			r.forward(25)
			sleep(0.01)
			r.forward(-25)###bio -25
			sleep(0.01) 
	
	
	
	
	sleep(5)
