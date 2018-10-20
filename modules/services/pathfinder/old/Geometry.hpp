#ifndef MY_GEOMETRY_HPP
#define MY_GEOMETRY_HPP

#include <vector>
#include <set>
#include <functional>

#define NODEBUG
#ifndef NODEBUG
	#define dbg(x) x
	#include <debug/Debug.hpp>
#else
	#define dbg(x)
#endif


// #define USE_FSA

#ifdef USE_FSA
#define FSA_SIZE 2000
#include "fsa.hpp"
#define alloc_node(...) node_allocator.alloc(__VA_ARGS__)
#define alloc_node_link(...) node_link_allocator.alloc(__VA_ARGS__)
#define free_node(a) node_allocator.free(a)
#define free_node_link(a) node_link_allocator.free(a)
#else
#define alloc_node(...) new Node(__VA_ARGS__)
#define alloc_node_link(...) new NodeLink(__VA_ARGS__)
#define free_node(a) delete a
#define free_node_link(a) delete a
#endif

namespace my {

struct Point;
typedef Point Vec2;

struct Vec2F {
	Vec2F(float x, float y) {
		this->x = x;
		this->y = y;
	}
	float x;
	float y;
};

struct Point {
	int x, y;
	Point();
	Point(int x, int y);
	bool operator< (const Point& b) const;
	bool operator==(const Point& b) const;
	Vec2F Normalized() const;
	float Dot(Point p);
	void MoveInDirection(float xnorm, float ynorm, int amount);
};



Vec2 operator-(const Point& p1, const Point& p2);
float vec_length(const Vec2& v);

class LineSegment {
	private:
		Point a,b;
		Vec2 vec;
	public:
		void GetPoints(Point& a, Point &b) const;
		const Vec2& GetVector() const;
		Vec2 GetPerpVector() const;
		float GetDistance() const;
		LineSegment();
		LineSegment(const Point& a, const Point& b);
		
		bool IsBetween(Point p);
		Point IntersectionPoint(const LineSegment& b) const;
		bool Intersects(const LineSegment& b) const;
		bool ConnectedWith(const LineSegment& b) const;
		Point GetClosestPoint(Point pt);
};

class AABB {
	private:
		Point pa, pb;
		LineSegment ls_a, ls_b, ls_c, ls_d;
	public:
		AABB();
		AABB(const AABB& a) = default;
		void SetAABB(const Point& a, const Point& b);
		void GetAABB(Point &a, Point &b);
		bool IsInsideAABB(const Point &p) const;
		bool IsIntersectingAABB(const LineSegment& ls) const;
};

struct Node;

struct NodeLink {
	NodeLink() : deleted(false) { obstructions_count = 0; ref_count = 0; glob_ref_count++; }
	NodeLink(Node* s, Node* t, const LineSegment& seg={}, float dist=0) : deleted(false),
		source(s), target(t), distance(dist), cost(0), seg(seg) { visible = true; obstructions_count = 0; ref_count=2; glob_ref_count++; }
	Node* source;
	Node* target;
	
	LineSegment seg;
	
	float distance;
	float cost;
	float cost_with_heuristic;
	
	bool deleted;
	bool visible;
	bool processed;
	
	int obstructions_count;
	int ref_count;
	
	static int glob_ref_count;
	
	void MakeSource(Node* n);
	void makeObstructed();
	void makeVisible();
	void incref();
	bool unref();
	void destroy();
	
	~NodeLink() {
		ref_count--;
	}
};



/*
	NodeLink set doesn't care about order of source and target
*/
struct NodeLinkSetCompare {
	bool operator()(NodeLink* const& a , NodeLink* const& b ) const {
		
		Node* a_target = a->target;
		Node* a_source = a->source;
		Node* b_target = b->target;
		Node* b_source = b->source;
		
		if(a->source > a->target) {
			a_source = a->target;
			a_target = a->source;
		}
		
		if(b->source > b->target) {
			b_source = b->target;
			b_target = b->source;
		}
		
		return (a_source < b_source) || (a_source == b_source && a_target < b_target);
	}
};


struct Node {
	Node() : processed_marker(0) { glob_ref_count++; }
	~Node();
	Point point;
	std::set<NodeLink*, NodeLinkSetCompare> visible_nodes;
	std::vector<NodeLink*> obstructed_links;
	
	Node* parent;
	Node* prev;
	Node* next;
	float cost;
	unsigned int processed_marker;
	
	static int glob_ref_count;
	
};


#ifdef USE_FSA
extern FixedSizeAllocator<Node, FSA_SIZE> node_allocator;
extern FixedSizeAllocator<NodeLink, FSA_SIZE> node_link_allocator;
#endif

class Pathfinder;
class Polygon : public AABB {
	private:
		std::vector<Node*> nodes;
		std::vector<NodeLink*> obstructed_links;
		int id;
		bool processed;
		friend class Pathfinder;
		
		void obstructLink(NodeLink* link);
	public:
		Polygon():id(-1){}
		Polygon(std::vector<Point> points);
		Polygon(const Polygon &p);
		Polygon& operator=(const Polygon&);
		Polygon(Polygon&& p);
		Polygon& operator=(Polygon&&);
		~Polygon();
		const std::vector<Node*>& GetNodes() const;
		
		int GetId() const { return id; }
		
		Point GetClosestExitPoint(Point pt);
		bool IsPointInsidePolygon(const Point &point) const;
		bool IsLineSegmentIntersectingPolygon(const LineSegment ls) const;
		
		void ExtendPolygon(int size);
};


}

#endif
