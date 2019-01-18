import Pathfinder_armv7l
p=Pathfinder_armv7l.Pathfinder()
p.AddPolygon([(621, -489), (679, -489), (679, -431), (621, -431)], 58)
print(p.Search((1316,-425), (10,-500)))

