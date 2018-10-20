#ifndef MY_PATHFINDER_HPP
#define MY_PATHFINDER_HPP

#include <vector>
#include <list>
#include "Geometry.hpp"
#include <map>

namespace my {

typedef std::list<Point> Path;

class Pathfinder {
	private:
		int last_id;
		int unit_size;
		bool has_unprocessed;
		// polygon id, polygon
		std::map<int, Polygon> m_polygons;
		// polygon id, link
		
		std::set<NodeLink*, NodeLinkSetCompare> all_node_links;
		
		unsigned int run_count;
		Polygon* findObstacleInLineOfSight(const LineSegment& ls);
		void findObstaclesExceptPolygon(const LineSegment& ls, Polygon& exclude_polygon, std::vector<Polygon*> &result);
		void processPolygon(Polygon& p);
		void processEndNode(Node* n);
		void processNode(Polygon& poly, Node* n);
		void checkForObstruction(Polygon& p);
		void removeRendundantLinks(Polygon& p);
		void extendPolygonToUnitSize(Polygon& p);
		
	public:
		Pathfinder();
		int AddPolygon(const Polygon& poly);
		void RemovePolygon(int polygon_id);
		Path Search(Point start, Point end);
		void Clear();
		const std::map<int, Polygon>& GetPolygons();
};
}

#endif
