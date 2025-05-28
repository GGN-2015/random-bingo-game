#!/bin/bash

rm -rf "$PROJECT_PATH/data.txt"
rm -rf "$PROJECT_PATH/try.out"
g++ -o "$PROJECT_PATH/try.out" "$PROJECT_PATH/try.cpp" -O3 -flto

"$PROJECT_PATH/try.out" << EOF
    2 0 0 3 3
    0 3 0 0 3
    0 0 3 0 0
    3 0 0 3 0
    3 3 0 0 2
EOF