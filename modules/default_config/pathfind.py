from modules.services.PathfinderService import *
from modules.processors.InfraProcessor import *
pathfinder = PathfinderService()
pathfinder.export_cmds()
_core.add_module([pathfinder, InfraProcessor()])
#_core.add_module([pathfinder])
