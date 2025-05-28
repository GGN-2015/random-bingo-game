#!/bin/bash

rm -rf ./try.out
g++ -o try.out try.cpp -O3 -flto
