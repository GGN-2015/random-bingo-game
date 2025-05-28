#!/bin/bash
echo $PROJECT_PATH

pushd "$PROJECT_PATH/games"
rm -rf */*.aux
rm -rf */*.log
rm -rf */*.out
rm -rf */*.tex
rm -rf *.aux
rm -rf *.log
rm -rf *.out
rm -rf *.tex
popd

pushd "$PROJECT_PATH"
rm -rf *.aux
rm -rf *.log
rm -rf *.synctex.gz
popd
