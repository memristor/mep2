class Stream:
	def __init__(self, send_func=None):
		self.send = send_func
		self.recv = None
	
