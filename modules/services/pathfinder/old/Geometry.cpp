#include "Geometry.hpp"
#include <algorithm>
#include <cmath>
#include <iostream>
// #include <debug/Debug.hpp>
#include <tuple>

namespace my {

Point::Point(){}
Point::Point(int x, int y) {
	this->x = x;
	this->y = y;
}
bool Point::operator< (const Point& b) const { 
	return x < b.x || (x == b.x && y < b.y); 
}

bool Point::operator==(const Point& b) const {
	return x == b.x && y == b.y;
}

Vec2F Point::Normalized() const {
	float len = vec_length(*this);
	return Vec2F((float)x/len,(float)y/len);
}

void Point::MoveInDirection(float xnorm, float ynorm, int amount) {
	x += xnorm*amount;
	y += ynorm*amount;
}

Vec2 operator-(const Point& p1, const Point& p2) {
	return {p1.x-p2.x, p1.y-p2.y};
}

float vec_length(const Vec2& v) {
	return sqrt(v.x*v.x + v.y*v.y);
}

float Point::Dot(Point p) {
	return x*p.x + y*p.y;
}

// ========= LINE SEGMENT ==============

static double perpDot(const Vec2 &a, const Vec2 &b)
{
	/*
		| b.x b.y |
		| a.x a.y |
		-y, x
	*/
	return (a.y * b.x) + (a.x * (-b.y));
}


LineSegment::LineSegment(){}
LineSegment::LineSegment(const Point& a, const Point& b) {
	this->a = a;
	this->b = b;
	this->vec = b-a;
}


void LineSegment::GetPoints(Point& a, Point &b) const {
	a = this->a;
	b = this->b;
}

const Vec2& LineSegment::GetVector() const {
	return vec;
}

Vec2 LineSegment::GetPerpVector() const {
	return Vec2(-vec.y, vec.x);
}

float LineSegment::GetDistance() const {
	return vec_length(vec);
}

bool LineSegment::ConnectedWith(const LineSegment& seg) const {
	return a == seg.a || a == seg.b || b == seg.a || b == seg.b;
}

/*stage
stage		v1
stage		v2
stage		
stage		v = v1*t
stage		v = v2*t
stage		
stage		v.x = v1x*t1 + p1x = v2x*t2 + p2x
stage		v.y = v1y*t1 + p1y = v2y*t2 + p2y
stage		
stage		t1 = (( v2x*t2 + (p2x - p1x) ) / v1x)
stage		
stage		v1y * ((p2x - p1x) / v1x) + (p1y - p2y) = v2y*t2 - v1y/v1x*v2x*t2
stage		v1y * ((p2x - p1x) / v1x) + (p1y - p2y) = (v2y - v1y/v1x*v2x) * t2
stage		
stage		t2 = (v1y * ((p2x - p1x) / v1x) - (p2y - p1y)) / (v2y - v1y/v1x*v2x)
stage		t2 = (v1y/v1x * pdx - pdy) / (v2y - (v1y/v1x)*v2x)
stage		t2 = (v1_slope * pdx - pdy) / (v2y - v1_slope*v2x)
stage		
stage		point = v2*t2
stage	*/
Point LineSegment::IntersectionPoint(const LineSegment& b) const {
	/*
	const Vec2 &v1 = vec;
	const Vec2 &v2 = b.vec;
	
	int pdx = b.x-a.x;
	int pdy = b.y-a.y;
	double v1_slope = (double)v1.y / (double)v1.x;
	if(v2.y == v1_slope*v2.x) v2.y+=0.1;
	double t2 = (v1_slope * pdx - pdy) / (v2.y - v1_slope*v2.x);
	return Point(v2.x*t2, v2.y*t2);
	*/
}

Point LineSegment::GetClosestPoint(Point pt) {
	Vec2 perp = GetPerpVector();
	float perp_len = vec_length(perp);
	float dist = perp.Dot(a-pt) / perp_len;
	// std::cout << "dist: " << perp.x << ", " << perp.y << " " << dist << "\n";
	pt.MoveInDirection(perp.x / perp_len, perp.y / perp_len, dist);
	return pt;
}

bool LineSegment::IsBetween(Point p) {
	Vec2 v2 = p-a;
	float vlen = vec_length(vec);
	float dist = vec.Dot(v2) / vlen;
	if(dist > 0 && dist < vlen) {
		return true;
	}
	return false;
}

bool LineSegment::Intersects(const LineSegment& seg) const {

	dbg(sdb::Stage stage("Intersects","", true);)
	dbg(stage.Report("clear", 0);)
	dbg(stage.Report("line", seg, 0xFFCEFB);)
	double f = perpDot(this->vec, seg.vec);
	if (f == 0.0) { // lines are parallel
		/*
		float dist1 = GetDistance();
		float dist2 = seg.GetDistance();
		LineSegment* lsa = this;
		LineSegment* lsb = &seg;
		
		if(dist1 < dist2) {
			lsa = &seg;
			lsb = this;
		}
		
		// if intersects then, at least one point of lsb is in lsa
		
		LineSegment(lsa->a, lsb->a)
		
		if(LineSegment(a,seg.a).GetDistance() < dist ||
		   LineSegment(a,
		*/
		dbg(stage.Report("line", *this, 0x00E7F6);)
		return false;
	}

	Point vc = seg.b - this->b;

	double aa = perpDot(this->vec, vc);
	double bb = perpDot(seg.vec, vc);

	if (f <= 0.0)
	{
		if (aa >= 0.0 || bb >= 0.0 || aa <= f || bb <= f) {
			// dbg(stage.Report("line", *this, 0x51F600);)
			dbg(stage.Break();)
			return false;
		}
	}
	else
	{
		if (aa <= 0.0 || bb <= 0.0 || aa >= f || bb >= f) {
			// dbg(stage.Report("line", *this, 0x51F600);)
			dbg(stage.Break();)
			return false;
		}
	}

	if(!ConnectedWith(seg)) {
		dbg(stage.Report("line", *this, 0xF60500);)
		dbg(stage.Break();)
		return true;
	} else {
		return false;
	}
}

// ============ AABB ============
AABB::AABB(){}
void AABB::SetAABB(const Point& a, const Point& b) {
	pa = a;
	pb = b;
	
	/*
		pa	b
		a		c
			d  pb
	*/
	ls_a = LineSegment(a,		Point(a.x, b.y));
	ls_b = LineSegment(a,		Point(b.x, a.y));
	ls_c = LineSegment(Point(b.x, a.y), 		b);
	ls_d = LineSegment(Point(a.x, b.y), 		b);
}

void AABB::GetAABB(Point &a, Point &b) {
	a=pa; 
	b=pb;
}

bool AABB::IsInsideAABB(const Point &p) const {
	return p.x >= pa.x && p.y >= pa.y && p.x <= pb.x && p.y <= pb.y;
}

bool AABB::IsIntersectingAABB(const LineSegment& ls) const {
	Point a,b;
	ls.GetPoints(a,b);
	return IsInsideAABB(a) || ls_a.Intersects(ls) || ls_b.Intersects(ls) || ls_c.Intersects(ls) || ls_d.Intersects(ls);
}


// ========== NODE ==========



Node::~Node() {
	
	for(NodeLink* l : visible_nodes) {
		if(!l->visible) continue;
		Node* target = l->target;
		if(target == this) {
			target = l->source;
		}
		target->visible_nodes.erase(l);
		l->target=0;
		l->source=0;
		l->deleted = true;
		l->unref();
	}
	for(NodeLink* l : obstructed_links) {
		l->target=0;
		l->source=0;
		l->deleted = true;
		l->unref();
	}
	
	glob_ref_count--;
}


int Node::glob_ref_count = 0;


// ========== NODE LINK ===========

int NodeLink::glob_ref_count = 0;
void NodeLink::makeObstructed() {
	if(obstructions_count == 0) {
		// add to obstructed list
		if(target->visible_nodes.count(this) == 1) {
			target->visible_nodes.erase(this);
		}
		target->obstructed_links.push_back(this);
		if(source->visible_nodes.count(this) == 1) {
			source->visible_nodes.erase(this);
		}
		source->obstructed_links.push_back(this);
	}
	obstructions_count++;
	incref();
	// std::cout << "obstructing " << ref_count << ", " << obstructions_count << "\n"; // debug
}

void NodeLink::makeVisible() {
	
	// std::cout << "make visible(" << deleted<< ") " << ref_count << ", " << obstructions_count << "\n"; // debug
	unref();
	if(deleted) {
		std::cout << "makeVisible: DELETED\n";
		exit(-1);
		return;
	}
	
	if(--obstructions_count == 0) {
		
		auto& t = target->obstructed_links;
		auto it_t = std::find(t.begin(), t.end(),this);
		if(it_t != t.end() ) {
			target->visible_nodes.insert(this);
			target->obstructed_links.erase(it_t);
		} else {
			std::cout << "NOT FOUND 1\n";
			exit(-2);
		}
		
		auto& s = source->obstructed_links;
		auto it_s = std::find(s.begin(), s.end(),this);
		if(it_s != s.end()) {
			source->visible_nodes.insert(this);
			source->obstructed_links.erase(it_s);
		} else {
			std::cout << "NOT FOUND 2\n";
			exit(-2);
		}
		
	} else if(obstructions_count < 0) {
		std::cout << "MAKE VISIBLE underflow: " << obstructions_count << "\n";
		exit(-1);
	}
	// std::cout << "after make visible(" << deleted<< ") " << ref_count << ", " << obstructions_count << "\n"; // debug
	
}

bool NodeLink::unref() {
	ref_count--;
	if(ref_count == 0) {
		free_node_link(this);
		return true;
	} else if(ref_count < 0) {
		std::cout << "UNREF FAIL: " << ref_count << "\n";
		exit(-1);
	}
	return false;
}

void NodeLink::incref() {
	ref_count++;
}

void NodeLink::destroy() {
	if(!deleted) {
		deleted = true;
		if(source->visible_nodes.count(this) == 1) {
			source->visible_nodes.erase(this);
			
		} else {
			
			auto &s = source->obstructed_links;
			auto it = std::find(s.begin(), s.end(), this);
			if(it != s.end()) {
				s.erase(it);
			}
			
		}
		
		if(target->visible_nodes.count(this) == 1) {
			target->visible_nodes.erase(this);
			
		} else {
			
			auto &t = target->obstructed_links;
			auto it = std::find(t.begin(), t.end(), this);
			if(it != t.end()) {
				t.erase(it);
			}
			
		}
		unref();
		unref();
	}
}

void NodeLink::MakeSource(Node* n) {
	if(target == n) {
		Node* tmp;
		tmp = source;
		source = target;
		target = tmp;
	}
}

// ========== POLYGON =============


Polygon::Polygon(std::vector<Point> points) {
	if(points.size() <= 1) return;
	// std::cout << "CONSTR POLY " << points.size() << "\n"; // stage
	float alpha_sum = 0;
	float prev_alpha = 0;
	dbg(sdb::Stage stage("\x1b[31mPolygon\x1b[0m");)
	// get AABB
	Point pmin(9999,9999),pmax(0,0);
	for(auto it = points.begin(); it != points.end(); it++) {
		auto &p = *it;
		pmin.x = std::min<int>(pmin.x, p.x);
		pmin.y = std::min<int>(pmin.y, p.y);
		pmax.x = std::max<int>(pmax.x, p.x);
		pmax.y = std::max<int>(pmax.y, p.y);
	}
	SetAABB(pmin, pmax);
	
	// fix polygon winding
	/*
	int i=0;
	if(points.size() > 2) {
		for(auto it = points.begin()+2; it != points.end(); it++) {
			Point &p = *it;
			// sum angles to make polygon winding correction
			Point &prev = *(it-2);
			Point &mid = *(it-1);
			Vec2 vec1 = {mid.x - prev.x, mid.y - prev.y};
			Vec2 vec2 = {p.x - mid.x, p.y - mid.y};
			
			float alpha = atan2( vec2.y, vec2.x ) - atan2( vec1.y, vec1.x );
			if(alpha > M_PI) alpha -= 2*M_PI;
			if(alpha < -M_PI) alpha += 2*M_PI;
			alpha_sum += alpha;
		}
	}
	bool right_winding = false;
	stage.Msg("alpha_sum: ", alpha_sum*180.0f/M_PI);
	if(alpha_sum > M_PI) {
		stage.Msg("right winding");
		right_winding = true;
	} else {
		stage.Msg("left winding");
	}
	
	if(!right_winding) {
		std::reverse(points.begin(), points.end());
	}
	*/
	
	if(points.back() == points.front()) {
		points.erase( points.end()-1 );
	}
	
	
	Node* prev = 0;
	for(Point& p : points) {
		Node* n = alloc_node();
		n->point = p;
		if(prev) {
			n->prev = prev;
			prev->next = n;
		}
		prev = n;
		dbg(stage.Msg("adding point : ", p.x, ", ", p.y);)
		
		nodes.push_back(n);
	}
	nodes.back()->next = nodes.front();
	nodes.front()->prev = nodes.back();
	
}

const std::vector<Node*>& Polygon::GetNodes() const {
	return nodes;
}

bool Polygon::IsPointInsidePolygon(const Point &point) const
{
	if(!IsInsideAABB(point)) return false;

	bool c = false;
	for (unsigned i = 0, j = nodes.size() - 1; i < nodes.size(); j = i++) {
		Point &p1 = nodes[i]->point;
		Point &p2 = nodes[j]->point;
		
		if (p1 == point) {
			return false;
		}

		if ((p1.y >= point.y) != (p2.y >= point.y)) {
			double intersection_x = (point.y - p1.y) * (p2.x - p1.x) / (double)(p2.y - p1.y) + p1.x;
			
			if((intersection_x - point.x) >= 0.0) {
				c = !c;
			}
		}
	}

	return c;
}

Point Polygon::GetClosestExitPoint(Point pt) {
	Point min_pt;
	float min_len=9999;
	for (unsigned i = 0, j = nodes.size() - 1; i < nodes.size(); j = i++) {
		Point &p1 = nodes[i]->point;
		Point &p2 = nodes[j]->point;
		
		// get closest edge
		LineSegment ls(p1,p2);
		Point p3 = ls.GetClosestPoint(pt);
		if(!ls.IsBetween(p3)) {
			continue;
		}
		Vec2F norm = (p3 - pt).Normalized();
		p3.MoveInDirection(norm.x, norm.y, 5);
		float len = vec_length(p3 - pt);
		if (len < min_len) {
			min_pt = p3;
			min_len = len;
		}
	}
	return min_pt;
}


Polygon& Polygon::operator=(const Polygon& p) {
	// std::cout << "COPY op =\n"; // stage
	this->~Polygon();
	new (this) Polygon(p);
	return *this;
}


Polygon& Polygon::operator=(Polygon&& p) {
	// std::cout << "MOVE op =\n"; // stage
	this->~Polygon();
	new (this) Polygon(p);
	return *this;
}



Polygon::Polygon(Polygon&& p) : AABB(std::move(p)) {
	// std::cout << "MOVE CTOR\n"; // stage
	nodes = std::move(p.nodes);
}

Polygon::Polygon(const Polygon &p) : AABB(p) {
	// std::cout << "COPY CTOR " << p.nodes.size() << "\n"; // stage
	nodes.reserve(p.nodes.size());
	Node* prev = 0;
	for(Node* p : p.nodes) {
		Node* n = alloc_node();
		n->point = p->point;
		if(prev) {
			n->prev = prev;
			prev->next = n;
		}
		prev = n;
		nodes.push_back(n);
	}
	nodes.back()->next = nodes.front();
	nodes.front()->prev = nodes.back();
}

Polygon::~Polygon() {
	// std::cout << "DESTROYING " << nodes.size() << " : " << Node::ref_count << "\n"; // stage
	for(NodeLink* l : obstructed_links) {
		if(!l->deleted) {
			l->makeVisible();
		}
	}
	
	for(Node* n : nodes) {
		free_node(n);
	}
}

bool Polygon::IsLineSegmentIntersectingPolygon(const LineSegment ls) const {
	if(!IsIntersectingAABB(ls)) {
		return false;
	}
	
	int p1Node = -1, p2Node = -1;
	Point p1,p2;
	ls.GetPoints(p1,p2);
	dbg(sdb::Stage stage("\x1b[31mpolygon_intersection\x1b[0m", "intersecting: (" + std::to_string(p1.x) + ", " + std::to_string(p1.y) + "), ("  + std::to_string(p2.x) + ", " + std::to_string(p2.y) + ") with polygon");)
	// stage.Report("clear", 0);
	int edgeCount = 0;
	bool bothSameEdge = false;
	for(unsigned int i=0; i < nodes.size(); i++)
	{
		const Point &edgeP1 = nodes[i]->point;
		const Point &edgeP2 = nodes[i+1 >= nodes.size() ? 0 : i+1]->point;
		
		if(p1Node == -1) {
			if(p1 == edgeP1) {
				p1Node = i;
			} else if(p1 == edgeP2) {
				p1Node = i+1 >= nodes.size() ? 0 : i+1;
			}
			if(p1Node != -1) {
				dbg(stage.Msg("p1Node: ", p1Node);)
				edgeCount++;
			}
		}
		if(p2Node == -1) {
			if(p2 == edgeP1) {
				p2Node = i;
			} else if(p2 == edgeP2) {
				p2Node = i+1 >= nodes.size() ? 0 : i+1;
			}
			if(p2Node != -1) {
				dbg(stage.Msg("p2Node: ", p2Node);)
				edgeCount++;
			}
		}

		if(edgeCount == 2) {
			if((p1Node == 0 && p2Node == nodes.size()-1) || (p2Node == 0 && p1Node == nodes.size()-1)) {
				dbg(stage.Msg(" [SAME EDGE] ");)
				break; // return false
			}
			if(p1Node+1 == p2Node || p2Node+1 == p1Node) {
				dbg(stage.Msg(" [SAME EDGE] ");)
				break; // return false
			}
			
			
			// check if goes through polygon
			if(IsPointInsidePolygon(Point((p1.x+p2.x)/2, (p1.y+p2.y)/2))) {
				dbg(stage.Msg("FAIL\n");)
				dbg(stage.Break();)
				return true;
			}
			
		}

		dbg(stage.Msg(" [line segment ", i, "] ");)
		if(LineSegment(edgeP1, edgeP2).Intersects(ls)) {
			dbg(stage.Msg("FAIL\n");)
			dbg(stage.Break();)
			return true;
		} else if(edgeCount != 2) {
			if(p1Node == -1 && IsPointInsidePolygon(p1)) {
				return true;
			} else if(p2Node == -1 && IsPointInsidePolygon(p2)) {
				return true;
			}
		}
	}
	dbg(stage.Msg("SUCCESS\n");)
	dbg(stage.Break();)
	return false;
}


void Polygon::obstructLink(NodeLink* link) {
	obstructed_links.push_back(link);
	link->makeObstructed();
}


void Polygon::ExtendPolygon(int size) {
	/*
	Node* a = nodes.front();
	Node* b = a->next;
	Node* c = b->next;
	Vec2 dir = b->point - a->point;
	float mag = vec_length(dir);
	
	// rotated normalized vector
	float xdir = -dir.y / mag;
	float ydir = dir.x / mag;
	
	a->point.MoveInDirection(xdir, ydir, size);
	b->point.MoveInDirection(xdir, ydir, size);
	
	// int len = nodes.size();
	for(auto it = nodes.begin(); it != nodes.end()-1;) {
		
		
		LineSegment la(a->point, b->point);
		LineSegment lb(b->point, c->point);
		
		Point pt = la.IntersectionPoint(lb);
		
		
		a = b;
		b = c;
		c = c->next;
		it++;
	}
	*/
}

#ifdef USE_FSA
FixedSizeAllocator<Node, FSA_SIZE> node_allocator;
FixedSizeAllocator<NodeLink, FSA_SIZE> node_link_allocator;
#endif

}
