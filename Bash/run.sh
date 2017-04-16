#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
fi

echo Running Fibonnaci using OpenMP and generating Task Spawn Graph
cd ~/git/openmp/runtime
make
cd src
sudo cp libomp.so /usr/local/lib
cd ~/Documents/Git/HelloWorld/HelloWorld/OpenMP_Fib/src/
export LD_LIBRARY_PATH=/usr/local/lib
export KMP_A_DEBUG=20
gcc -fopenmp -g OpenMP_Fib.c -l:libomp.so -l:libpapi.so -o OpenMP_Fib
./OpenMP_Fib $1 2>test.txt
cp test.txt ~/Documents/Git/HelloWorld/HelloWorld/Python/test.txt
cd ~/Documents/Git/HelloWorld/HelloWorld/Python/
python produceAnimation.py
python readLogFile.py
cd ~/Downloads/xdot-0.7
./xdot.py ~/Documents/Git/HelloWorld/HelloWorld/Python/taskSpawn.dot 
