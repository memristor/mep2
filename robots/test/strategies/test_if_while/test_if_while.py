weight=1
from core.Util import col
a=_State(2)
def run():
	################################################
	
	_print(col.yellow,'test case1 (_if(cond, true_func, false_func)',col.white)
	
	_print('\tval a:', a.val)
	def is_true():
		_print('\t\ttrue (bad)')
		bad()
	def is_false():
		_print('\t\tfalse (good)')
	_print('\ta.val == 0?')
	_if(lambda: a.val == 0, is_true, is_false)
	def is_true():
		_print('\t\ttrue (good)')
	def is_false():
		_print('\t\tfalse (bad)')
		bad()
	_print('\ta.val != 0')
	_if(lambda: a.val != 0, is_true, is_false)
	
	################################################
	_print(col.yellow,'test case2 (_if, _elif, _end_if)',col.white)
	
	a.val = 2
	_do(lambda: print('\tval a:', a.val) )
	_print('\ta.val == 0?')
	_if(lambda: a.val == 0)
	
	_print('\t\tis true (good)')
	_elif(lambda: a.val == 3)
	
	_print('\t\tval is:', a.val, '(bad)')
	
	bad()
	
	_else()
	
	_print('\t\tis else (good)')
	_end_if()
	
	################################################
	
	_print(col.yellow,'test case3 (with _if , with _elif, with _else)',col.white)
	
	_do(lambda: print('\tval a:', a.val) )
	_print('\ta.val == 0 or a.val == 3 or else?' )
	with _if(lambda: a.val == 0):
		_print('\tis true')
		_do(exit,-1)
	with _elif(lambda: a.val == 3):
		_print('\tval is:', a.val)
		_do(exit,-1)
	with _else():
		_print('\tis else (good)')
	
	_print(col.yellow,'test case4',col.white)
	a.val = 2
	with _if(lambda: a.val == 2):
		_print('\tis 2 (good)')
	with _elif(lambda: a.val == 3):
		_print('\tval is:', a.val, '(fail)')
		bad()
	with _else():
		_print('\tis none')
		bad()

	################################################
	
	_print(col.yellow,'test case4 (while)',col.white)
	with _while(lambda: a.val != 5):
		a.inc()
		@_do
		def _():
			print('\tval:',a.val)
