def run():
	State.strat_counter = 0
	
	@_core.listen('strategy:done')
	def next_strategy_pls():
		strategy_list=['run_tests', 'test_if_while', 'test_listener', 'test_scope',
			'test_sync/sync', 'test_sync/sync_simple', 'test_simulator2']
		print('strategy', strategy_list[State.strat_counter], 'is done')
		if State.timer_future:
			State.timer_future.cancel()
		State.strat_counter += 1
		if State.strat_counter < len(strategy_list):
			_core.task_manager.clear_tasks()
			strat_prefix = 'run_tests/tests/'
			_core.task_manager.load_tasks('test', strat_prefix+strategy_list[State.strat_counter])
			_core.start_strategy()
		else:
			print('ALL TESTS PASS')
			_core.quit()
