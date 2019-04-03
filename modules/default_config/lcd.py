from modules.drivers.LCD import LCD

if not State.sim:
	lcd = LCD()

	@_core.listen('state:change')
	def ch_lcd(st, old, new):
		if st.name == 'points':
			lcd.show_pts(new)

	pts=_State(0, _name='points')
	
	@_core.export_cmd
	@_core.do
	def addpts(points):
		print('addpts', points)
		pts.val = pts.val + points
