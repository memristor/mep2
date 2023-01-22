def run():
	r.conf_set('send_status_interval', 10)
	State.startpos = (1195, -610)
	r.setpos(1500-175-138,-1000+310+80,-90)
	
	#napgold(0)
	#nazgold(1)
	#rrucica(0)
	#lrucica(0)
	r.speed(50)
