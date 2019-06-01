import asyncio
end_time = 100
State.timer_future = None

async def timer_task():
	State.time = 0
	while State.time < end_time:
		await asyncio.sleep(1)
		State.time+=1
		print('time', State.time)
		if not _core.task_manager.current_task:
			print('no more tasks')
	print('round has ended')
	_core.fullstop()

@_core.do
def start_timer():
	if not State.timer_future:
		State.timer_future = asyncio.ensure_future(timer_task())
		_core.logger.reset()
start = start_timer
