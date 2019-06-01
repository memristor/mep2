weight=1
from core.Util import *
def run():
	ents = _core.entities.get_entities_in_polygon(polygon_square_around_point([680-100,-800], [250,100]))
	print([e.name for e in ents])
	return False
