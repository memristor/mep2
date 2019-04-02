weight=1
a=_State('a', name='var1', shared=True)
def run():
	sleep(10)
	a.val = 5
	sleep(10)
	a.val = 8
	
