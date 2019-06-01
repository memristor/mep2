weight=1
a=_State(2)
from core.Util import col
def run():
	@_do
	def _():
		sleep(0.2)
		_print('hehe1')
	@_do
	def _():
		sleep(0.2)
		_print('hehe1')
	
	_print(col.yellow,'pick best',col.white)
	with _pick_best():
		sleep(4)
		
		@_do
		def _():
			sleep(3)
			_print('hehe')
		
		@_do
		def _():
			_print('1 sec hehe')
			sleep(1)
			
		@_do
		def _():
			_print('2 sec hehe')
			sleep(2)
			
	sleep(1)
	_print('ow lol')
