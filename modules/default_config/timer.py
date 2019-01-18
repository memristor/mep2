import asyncio
async def timer_task():
	time = 0
	while time < 100:
		await asyncio.sleep(1)
		time+=1
		print('time', time)
		if not _core.task_manager.current_task:
			print('no more tasks')
	print('round has ended')
	_core.fullstop()

@_core.do
def start_timer():
	asyncio.ensure_future(timer_task())
