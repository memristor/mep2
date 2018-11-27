#!/bin/bash
mkdir -p stripped
mkdir -p orig
cp *.cpp orig/

sed -e '/stage/ d' -e '/debug/ d' Pathfinder.cpp > stripped/Pathfinder.cpp
sed -e '/stage/ d' -e '/debug/ d' Geometry.cpp > stripped/Geometry.cpp

cp *.hpp stripped/
