from core.Core import Core
import sys
import os
#  sys.dont_write_bytecode = True

def main():
	robot=os.environ['ROBOT']
	core = Core(robot)

	core.load_config()
	print('loaded modules:', '\n\t' + '\n\t'.join(['\x1b[33m'+x.name + '\x1b[0m : class ' + type(x).__name__ for x in core.get_modules()]))
	core.load_strategy(sys.argv[1])


	if core.task_manager.has_task('init'):
		core.task_manager.set_task('init')

	core.run()

if __name__ == '__main__':
	main()
