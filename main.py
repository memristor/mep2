#!/usr/bin/env python3
import sys,os
from core.Core import Core

def main():
	robot=os.environ['ROBOT']
	core = Core(robot)
	core.load_config()
	if len(sys.argv) > 1:
		core.load_strategy(sys.argv[1])
	core.start_strategy()
	core.run()

if __name__ == '__main__':
	main()
