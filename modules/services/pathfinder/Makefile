machine = $(shell uname -m)
Pathfinder_$(machine).so: Binder.cpp Geometry.cpp Pathfinder.cpp clipper.cpp
	g++ $^ -shared -fpic $(shell python3-config --includes) -lboost_python3 -o $@
