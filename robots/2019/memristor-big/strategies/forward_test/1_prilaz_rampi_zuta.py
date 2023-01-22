weight=15


def run():
	r.speed(120)
	r.forward(1000)
	r.forward(-1000)
	r.forward(1000)
	r.forward(-1000)
	r.speed(50)
	r.curve_rel(100,360)
	r.curve_rel(100,-360)
	r.curve_rel(-100,360)
	r.curve_rel(-100,-360)
	
	
