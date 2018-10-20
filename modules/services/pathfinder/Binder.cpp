#include <boost/python.hpp>
#include <numeric>
#include "Pathfinder.hpp"
#include "clipper.hpp"
using namespace boost::python;
using namespace my;
#include <iostream>
#include <string>

using namespace ClipperLib;

namespace { // Avoid cluttering the global namespace.

  class PathfinderBinder {
	private:
		Pathfinder pf;
	public:
		PathfinderBinder() {}
		int AddPolygon(list& lt, double offset) {
			ClipperLib::Path subj;
			for (int i = 0; i < len(lt); ++i) {
				tuple t = boost::python::extract<tuple>(lt[i]);
				int x = boost::python::extract<int>(t[0]);
				int y = boost::python::extract<int>(t[1]);
				// points.emplace_back(x,y);
				subj << IntPoint(x,y);
			}
			
			Paths solution;
			std::vector<Point> points;
			
			if (offset != 0) {
				ClipperOffset co;
				co.AddPath(subj, jtSquare, etClosedPolygon);
				co.Execute(solution, offset);
			} else {
				solution.push_back(subj);
			}
			
			for(auto pt : solution[0]) {
				points.emplace_back(pt.X, pt.Y);
			}
			
			Polygon poly(points);
			
			return pf.AddPolygon(poly);
		}
		
		void RemovePolygon(int poly_id) {
			pf.RemovePolygon(poly_id);
		}
		
		list GetPolygon(int poly_id) {
			list l;
			auto polygons = pf.GetPolygons();
			const Polygon& poly = polygons[poly_id];
			auto nodes = poly.GetNodes();
			for(auto &node : nodes) {
				auto &pt = node->point;
				// std::cout << "path: " << pt.x << ", " << pt.y << "\n";
				l.append(boost::python::make_tuple(pt.x, pt.y));
			}
			return l;
		}
		
		list Search(tuple start, tuple end) {
			int x1 = extract<int>(start[0]);
			int y1 = extract<int>(start[1]);
			int x2 = extract<int>(end[0]);
			int y2 = extract<int>(end[1]);
			Point pt_start = Point(x1,y1);
			Point pt_end = Point(x2,y2);
			my::Path path = pf.Search(pt_start, pt_end);
			
			
			list l;
			for(auto &pt : path) {
				// std::cout << "path: " << pt.x << ", " << pt.y << "\n";
				l.append(boost::python::make_tuple(pt.x, pt.y));
			}
			return l;
		}
		void Clear() {
			pf.Clear();
		}
  };
  
  
  
  
}

// export to python
BOOST_PYTHON_MODULE(Pathfinder_x86_64)
{
	// int AddPolygon(const Polygon& poly);
	// void RemovePolygon(int polygon_id);
	// Path Search(const Point& start, const Point& end);
	// void Clear();
	// const std::map<int, Polygon>& GetPolygons();
    class_<PathfinderBinder>("Pathfinder")
		.def("AddPolygon", &PathfinderBinder::AddPolygon)
		.def("RemovePolygon", &PathfinderBinder::RemovePolygon)
		.def("GetPolygon", &PathfinderBinder::GetPolygon)
		.def("Search", &PathfinderBinder::Search)
		.def("Clear", &PathfinderBinder::Clear)
		;
}

BOOST_PYTHON_MODULE(Pathfinder_armv7l)
{
	 class_<PathfinderBinder>("Pathfinder")
		.def("AddPolygon", &PathfinderBinder::AddPolygon)
		.def("RemovePolygon", &PathfinderBinder::RemovePolygon)
		.def("GetPolygon", &PathfinderBinder::GetPolygon)
		.def("Search", &PathfinderBinder::Search)
		.def("Clear", &PathfinderBinder::Clear)
		;
	
}

/*
	compile with:
		g++ example.cpp -shared -fpic $(python3-config --includes) -lboost_python3 -o example.so

	in python:
		>> import example
		>> a=example.TextClass()
		>> a.GetVector()
		>> example.greet()
		'hello world'
		>> example.square(6)
		36
	
	docs:
	* 	https://wiki.python.org/moin/boost.python
		https://wiki.python.org/moin/boost.python/SimpleExample
		https://www.boost.org/doc/libs/1_61_0/libs/python/doc/html/tutorial/tutorial/exposing.html
*/
