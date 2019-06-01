module := Pathfinder

src := Binder.cpp \
	   Geometry.cpp \
	   Pathfinder.cpp \
	   clipper.cpp

############################################

machine := $(shell uname -m)
bin/$(machine)/$(module).so: $(src)
	mkdir -p bin/$(machine)
	g++ $^ -shared -fpic $(shell python3-config --includes) -lboost_python3 -O2 -o $@

clean:
	rm -rf bin
