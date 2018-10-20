name ='...a_task...'
description='basic task'
weight = 2
task_instances = [
	{
		'weight': 5,
		'time': 7
	}
]

def leave():
	pass



def run():

		
	r.goto(-500,500)
	sleep(2.5)
	r.turn(100)
	r.turn(100)
	r.goto(-800,-300)
	print('should run')
