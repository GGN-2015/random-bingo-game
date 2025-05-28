#!/bin/bash

rm -rf "$PROJECT_PATH/try.out"
g++ -o "$PROJECT_PATH/try.out" "$PROJECT_PATH/try.cpp" -O3 -flto
