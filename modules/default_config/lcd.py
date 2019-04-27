from modules.drivers.LCD import LCD

if not State.sim:
	lcd = LCD()

	@_core.listen('state:change')
	def ch_lcd(st, old, new):
		print('state:change', st.name,old,new)
		if st.name == 'points':
			lcd.show_pts(new)

	lcd.show_pts(0)

@_core.init_task
def tinit():
	print('tinit')
	pts=_State(0, name='points', shared=True, local=False)

	@_core.do
	def addpts(points):
		print('addpts', points)
		pts.val = pts.val + points
	_core.export_cmd('addpts', addpts)
