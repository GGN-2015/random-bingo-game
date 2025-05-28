#!/bin/bash

rm -rf ./data.txt
rm -rf ./try.out
g++ -o try.out try.cpp -O3 -flto

./try.out << EOF
    2 0 0 3 3
    0 3 0 0 3
    0 0 3 0 0
    3 0 0 3 0
    3 3 0 0 2
EOF