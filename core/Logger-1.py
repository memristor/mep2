import time
class Logger:
	def __init__(self):
		import datetime
		d = datetime.datetime.now()
		fname = d.strftime('logs/%d-%m-%Y-%H-%M-%S.log')
		self.f = open(fname, 'a')
		self.ofs = time.time()
	
	def print(self, *args, **kwargs):
		self.log(*args)
		
	def reset(self):
		self.ofs = time.time()
		
		
	def log_print(self):
		import builtins
		builtins.print2 = print
		builtins.print = self.print
	
	def log(self, *msg, _type='terminal'):
		t = time.time() - self.ofs
		self.f.write(('<%s time="%.4f" >' % (_type,t)) +' '.join([str(m) for m in msg])+'</'+_type+'>\n')
		print2(*msg)
	
	def close(self):
		self.f.close()
