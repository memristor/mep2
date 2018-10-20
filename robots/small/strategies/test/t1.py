weight=10
def run():
	print('t1')
	def on_message(msg):
		print('got msg:',msg)
		_label('msg')
	_listen('message', on_message)
	
	
	#  _sync('msg')
	#  sleep(10)
	send_msg('heyya')
	set_state('hehe','yay')
	sleep(5)
