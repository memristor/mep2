#!/usr/bin/env python3
import sys,os
from core.Core import Core

def main():
	robot=os.environ['ROBOT']
	core = Core(robot)
	strat=''
	for p in sys.argv[1:]:
		if p.find('=') != -1:
			s=p.split('=')
			setattr(State, s[0], eval(s[1]))
		else:
			strat = p
	core.load_config()
	if strat: core.load_strategy(strat)
	core.start_strategy()
	core.run()

if __name__ == '__main__':
	main()
