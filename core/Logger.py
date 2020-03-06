import time,json,os
class Logger:
	def __init__(self):
		import datetime
		d = datetime.datetime.now()
		# fname = d.strftime('logs/%d-%m-%Y-%H-%M-%S.log')
		if not os.path.exists('logs'):
			os.mkdir('logs')
		try:
			with open('logs/cnt.txt', 'r') as f:
				cnt = int(f.read())
		except:
			cnt = 0
			
		fname = 'logs/' + str(cnt+1) + '.log'
		self.f = open(fname, 'w')
		self.ofs = time.time()
		self.f.write('[')
		_core.on('kill', self.close)
		with open('logs/cnt.txt', 'w') as f:
			f.write(str(cnt+1))
	
	def print(self, *args, **kwargs):
		self.log(*args)
		
	def log_print(self):
		import builtins
		builtins.print2 = print
		builtins.print = self.print
	
	def reset(self):
		self.ofs = time.time()
		
	def replace_colors(self, msg):
		from core.Util import col
		return msg.replace(col.yellow, '^y').replace(col.green, '^g').replace(col.red, '^r').replace(col.white, '^w')
		
	def log(self, *msg, _type='terminal'):
		if self.f.closed: return
		t = time.time() - self.ofs
		# self.f.write(('<%s time="%.4f" >' % (_type,t)) +' '.join([str(m) for m in msg])+'</'+_type+'>\n')
		logmsg = self.replace_colors(' '.join([str(m) for m in msg])) if len(msg) > 1 else msg[0]
		
		if type(logmsg) == bytes:
			logmsg = str(logmsg)

		j = { 'type':_type, 'time':t, 'content': logmsg }
		
		try:
			#self.f.write(('{ "type":"%s", "time":%.4f, "content":' % (_type,t)) +m + ' },\n')
			self.f.write(json.dumps(j) + ',\n')
			# self.f.write('sending' + str(j)+'\n')
		except:
			pass
		if _type == 'terminal':
			print2(*msg)
		_core.introspection.send_log(j)
	
	def close(self):
		self.f.write('{ "type":"end" }]')
		self.f.close()
