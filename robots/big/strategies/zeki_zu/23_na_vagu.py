#weight=12
def run():
		r.goto(-80,410,1)# isporuka na vagu
		r.absrot(0)
		lift(2,'accel')  #skuplja goldenium
		llift(2)
		
		pump(3,0)
		pump(2,0)
		r.forward(-100)
		return