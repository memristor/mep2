from modules.drivers.LCD import LCD
from core.Util import col

points_states = []
points_idx = 1
lcd = None

def init_master():
	global points_idx, lcd
	points_idx = 0
	if not State.sim:
		lcd = LCD()
		lcd.show_pts(0)

@_core.listen('state:change')
def on_points_change(st, old, new):
	if st.name in ('points1','points2'):
		s = sum((i.val for i in points_states))
		print(col.yellow, st.name, old, '->', new, ' total ', s, col.white)
		if points_idx == 0 and not State.sim and not State.is_sim():
			lcd.show_pts(s)
		
@_core.init_task
def on_init_task():
	global points_states
	points1=_State(0, name='points1', shared=1, local=0)
	points2=_State(0, name='points2', shared=1, local=0)
	points_states=[points1, points2]
	@_core.do
	def addpts(points):
		print('addpts', points)
		points_states[points_idx].val += points
	_core.export_cmd('addpts', addpts)
