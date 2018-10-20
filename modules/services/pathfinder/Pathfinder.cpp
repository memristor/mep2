
#include "Pathfinder.hpp"

#include <iostream>
#include <algorithm>
#include <cmath>
#include <queue>
#include <memory>
// #include <debug/Debug.hpp>

namespace my {

Pathfinder::Pathfinder() {
	run_count = 0;
	last_id = 0;
	this->unit_size = 1;
	has_unprocessed = false;
}

int Pathfinder::AddPolygon(const Polygon& poly) {
	auto it = m_polygons.insert(std::make_pair(last_id, poly));
	Polygon &p = it.first->second;
	p.id = last_id;
	p.processed = false;
	// processPolygon(p);
	has_unprocessed = true;
	return last_id++;
}

void Pathfinder::RemovePolygon(int polygon_id) {
	auto it = m_polygons.find(polygon_id);
	if(it != m_polygons.end()) {
		if(it->second.processed) {
			for(auto n : it->second.GetNodes()) {
				for(auto l : n->visible_nodes) {
					all_node_links.erase(l);
				}
				for(auto l : n->obstructed_links) {
					all_node_links.erase(l);
				}
			}
		}
		m_polygons.erase(it);
	}
}

Polygon* Pathfinder::findObstacleInLineOfSight(const LineSegment& ls) {
	
	for(auto& pair : m_polygons) {
		Polygon& p = pair.second;
		if(p.IsLineSegmentIntersectingPolygon(ls)) {
			return &p;
		}
	}
	return 0;
}

void Pathfinder::findObstaclesExceptPolygon(const LineSegment& ls, Polygon& exclude_polygon, std::vector<Polygon*> &result) {
	
	for(auto& pair : m_polygons) {
		Polygon& p = pair.second;
		if(p.id == exclude_polygon.id) continue;
		if(p.IsLineSegmentIntersectingPolygon(ls)) {
			result.push_back(&p);
		}
	}
}


void Pathfinder::checkForObstruction(Polygon& poly) {
	for(NodeLink* l : all_node_links) {
		if(l->deleted) {
			continue;
		}
		if(poly.IsLineSegmentIntersectingPolygon(l->seg)) {
			// std::cout << "obstructing " << "\n"; // debug
			poly.obstructLink(l);
		}
	}
}

void Pathfinder::Clear() {
	all_node_links.clear();
	m_polygons.clear();
}

const std::map<int, Polygon>& Pathfinder::GetPolygons() {
	return m_polygons;
}

void Pathfinder::processEndNode(Node* n) {
	for(auto& pair : m_polygons) {
		Polygon& a = pair.second;
		for(Node* an : a.GetNodes()) {
			LineSegment ls = LineSegment(n->point, an->point);
			NodeLink* l = alloc_node_link(n,an,ls,ls.GetDistance());
			l->processed = false;
			l->visible = false;
			n->visible_nodes.insert(l);
		}
	}
}

void Pathfinder::processNode(Polygon& poly, Node* n) {
	int i=0;
	NodeLink nl;
	nl.source = n;
	std::vector<Polygon*> obstacles;
	obstacles.reserve(10);
	for(auto& pair : m_polygons) {
		Polygon& a = pair.second;
		for(Node* an : a.GetNodes()) {
			if(an == n) continue;
			
			LineSegment ls = LineSegment(n->point, an->point);
			
			// if blocked by own polygon, then don't do anything
			if(poly.IsLineSegmentIntersectingPolygon(ls)) continue;
			
			obstacles.clear();
			findObstaclesExceptPolygon(ls, poly, obstacles);
			
			nl.target = an;
			
			
			if(!obstacles.empty()) {
				if(poly.id != -1 && all_node_links.count(&nl) == 0) {
					NodeLink* node_link = alloc_node_link(n, an, ls, ls.GetDistance());
					node_link->processed = true;
					auto it = std::find_if(obstacles.begin(), obstacles.end(), [&](Polygon* p) { return p->id == a.id; });
					if(it == obstacles.end()) {
						all_node_links.insert(node_link);
						for(Polygon* obs : obstacles) {
							// std::cout << "obstructing
							obs->obstructLink(node_link);
						}
					}
				}
			} else {
				// no obstacle, nodes see each other: make node link
				NodeLink* node_link = alloc_node_link(n, an, ls, ls.GetDistance());
				node_link->processed = true;
				auto r1 = an->visible_nodes.insert(node_link);
				if(r1.second) {
					auto r2 = n->visible_nodes.insert(node_link);
					if(poly.id != -1) {
						all_node_links.insert(node_link);
					}
				} else {
					// fail insert (already present)
					// std::cout << "fail insert\n";
					node_link->unref();
					node_link->unref();
				}
			}
		}
	}
}

void Pathfinder::processPolygon(Polygon& p) {
	p.processed=true;
	for(Node* n : p.GetNodes()) {
		processNode(p, n);
	}
	// removeRendundantLinks(p);
	checkForObstruction(p);
}

void Pathfinder::removeRendundantLinks(Polygon& p) {
	for(Node* n : p.GetNodes()) {
		NodeLink tmp_link(n, 0);
		for(auto it = n->visible_nodes.begin(); it != n->visible_nodes.end(); it++) {
			NodeLink* l = *it;
			
			// target get real target from node n
			Node* target = l->target;
			if(target == n) target = l->source;
			
			tmp_link.target = target;
			
			// tmp_link is (n, target)
			
			// does sibling node sees target node
			bool sees = false;
			// if(n->prev) {
			tmp_link.source = n->prev;
			if(n->prev->visible_nodes.count(&tmp_link) == 0) {
				sees = true;
			} else {
				tmp_link.source = n->next;
				if(n->next->visible_nodes.count(&tmp_link) == 0) {
					sees = true;
				}
			}
			// }
			
			// 
			tmp_link.target = n;
			
			tmp_link.source = target->prev;
			if(sees && target->prev->visible_nodes.count(&tmp_link) == 0) continue;
			
			tmp_link.source = target->next;
			if(sees && target->next->visible_nodes.count(&tmp_link) == 0) continue;
			
			
			l->destroy();
			l->deleted = true;
			// all_node_links.erase(l);
		}
		
	}
}

struct NodeLinkCostCompare {
	bool operator() (const NodeLink* a, const NodeLink* b) {
		return a->cost_with_heuristic > b->cost_with_heuristic; // smaller value gets bigger priority
	}
};


dbg(std::string node_get_coord(Node* n) { /*stage*/ return std::to_string(n->point.x) + ", " + std::to_string(n->point.y); })
Path Pathfinder::Search(Point start, Point end) {
	
	// lazy process added controls
	if(has_unprocessed) {
		for(auto& p : m_polygons) {
			if(!p.second.processed) {
				processPolygon(p.second);
			}
		}
		has_unprocessed = false;
	}
	
	std::priority_queue<NodeLink*, std::vector<NodeLink*>, NodeLinkCostCompare> open_list;
	Path path;

	
	auto pf = std::find_if(m_polygons.begin(), m_polygons.end(), [&](std::pair<const int, my::Polygon>& p) {return p.second.IsPointInsidePolygon(start);});
	
	if(pf != m_polygons.end()) {
		std::cout << "start pt in poly\n";
		Point exit_pt = pf->second.GetClosestExitPoint(start);
		dbg(sdb::Stage stage("\x1b[33mExitPoint\x1b[0m");)
		dbg(stage.Report("point", exit_pt, 0xff5763F2));
		start = exit_pt;
	}
	
	std::unique_ptr<Node> startNode = std::make_unique<Node>();
	startNode->point = start;
	std::unique_ptr<Node> endNode = std::make_unique<Node>();
	endNode->point = end;
	
	dbg(sdb::Stage stage("\x1b[33mPathfinder\x1b[0m");)
	if(findObstacleInLineOfSight(LineSegment(start, end)) == 0) {
		path.push_back(start);
		path.push_back(end);
		dbg(stage.Msg("found LOS start, end\n");)
		return path;
	}
	
	if(std::any_of(m_polygons.begin(), m_polygons.end(), [&](std::pair<const int, my::Polygon>& p) {return p.second.IsPointInsidePolygon(end);})) {
		return path;
	}
	
	
	Polygon tmp;
	dbg(stage.Msg("processing start node");)
	dbg(stage.Break();)
	processEndNode(startNode.get()); 
	dbg(stage.Msg("processing end node");)
	dbg(stage.Break();)
	processNode(tmp, endNode.get());
	
	run_count++;
	
	startNode->processed_marker = run_count;
	startNode->parent = 0;
	for(NodeLink* l : startNode->visible_nodes) {
		l->cost = l->distance;
		l->cost_with_heuristic = l->cost + vec_length((endNode->point)-(l->target->point));
					
		open_list.push(l);
		dbg(stage.Msg("pushing ", node_get_coord(l->target));)
	}
	
	dbg(stage.Msg("pushing passed");)
	dbg(stage.Break();)
	
	int num = 0;
	while(!open_list.empty()) {
		NodeLink* bestLink = open_list.top();
		open_list.pop();
		
		if(!bestLink->processed) {
			bestLink->processed = true;
			if(findObstacleInLineOfSight(bestLink->seg)) {
				continue;
			} else {
				
			}
		}
		
		dbg(stage.Msg("\x1b[32mpop-ing\x1b[0m NodeLink ", node_get_coord(bestLink->target), " cost: ", bestLink->cost, " num: ", num);)
		num++;
		
		// if goal found
		if(bestLink->target == endNode.get()) {
			dbg(stage.Msg("goal found!!!");)
			dbg(stage.Break();)
			path.push_front(end);
			Node* n = bestLink->source;
			while(n) {
				dbg(stage.Msg("path: " + node_get_coord(n));)
				path.push_front(n->point);
				n=n->parent;
			}
			dbg(std::cout << "num: " << num << "\n";)
			return path;
		}
		
		dbg(stage.Report("line", LineSegment(bestLink->source->point, bestLink->target->point), 0x7D28BE);)
		dbg(stage.Break();)
		
		Node *n = bestLink->target;
		if(n->processed_marker == run_count) {
			dbg(stage.Msg("target is \x1b[32malready\x1b[0m processed");)
			if(bestLink->cost < n->cost) {
				dbg(stage.Msg("\x1b[31mfound better path\x1b[0m");)
				n->cost = bestLink->cost;
				n->parent = bestLink->source;
			}
		} else {
			dbg(stage.Msg("target is not processed");)
			
			n->parent = bestLink->source;
			n->cost = bestLink->cost;
			for(NodeLink* l : n->visible_nodes) {
				
				if(l->source->processed_marker != run_count) {
					l->MakeSource(n);
					l->cost = n->cost + l->distance;
					l->cost_with_heuristic = l->cost + vec_length((endNode->point)-(l->target->point));
				}
				
				if(l->target->processed_marker != run_count && l->target != n) {
					dbg(stage.Msg("PUSHING ", node_get_coord(l->target), " COST ", l->cost);)
					open_list.push(l);
				}
			}
			n->processed_marker = run_count;
		}
	}
	return path;
}

}
