#!/bin/bash

CC=/usr/bin/clang
CXX=/usr/bin/clang++
BASE=/var/www/duck

cd $BASE/compiler2021
git pull

cd $BASE/kobayashi-compiler
git pull
git checkout $1
commit=$(git rev-parse --short HEAD)
folder=$2-$commit
cd build
cmake ..
make -j$(nproc)

# curl https://r.nya.rs:8987/sync
cd $BASE/testcases
result=$BASE/results/$folder
mkdir $result
echo function_test2020
python3 judge.py function_test2020 2> $result/function_test2020.txt > $result/function_test2020.json
echo function_test2021
python3 judge.py function_test2021 2> $result/function_test2021.txt > $result/function_test2021.json
echo h_functional
python3 judge.py h_functional 2> $result/h_functional.txt > $result/h_functional.json
echo performance_test2021
python3 judge.py performance_test2021 2> $result/performance_test2021.txt > $result/performance_test2021.json
# python3 judge.py performance_test2021 clang 2> $BASE/results/clang.txt > $BASE/results/clang.json
# python3 judge.py performance_test2021 gcc 2> $BASE/results/gcc.txt > $BASE/results/gcc.json

cd $BASE/kobayashi-compiler
git rev-parse --short HEAD > $result/commit.txt
redis-cli get fargs > $result/fargs.txt
git checkout master

rm -f $BASE/lock
