weight=1
def run():

	sleep(0.3)
	r.speed(150)

	y_sort = 833

	###################
	## SORTIRANJE
	#################
	cev(1)
	sleep(0.05)
	if not pathfind(-1140,785):
		return False
	
	sleep(0.05)
	r.speed(30)
	r.goto(-1140,960,-1)
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
	
	r.goto(-1140,785)
	
	State.loaded.val = True
