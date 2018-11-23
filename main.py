#!/usr/bin/env python3
from core.Core import Core
import sys
import os
#  sys.dont_write_bytecode = True

def main():
	robot=os.environ['ROBOT']
	core = Core(robot)
	core.load_config()
	core.load_strategy(sys.argv[1])
	core.run()

if __name__ == '__main__':
	main()
