_disabled=True
weight=-1
def run():
	if not pathfind(*State.start):
		return False
