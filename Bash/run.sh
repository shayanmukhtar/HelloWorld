#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
fi

echo Running Fibonnaci using OpenMP and generating Task Spawn Graph
cd ~/Documents/Git/HelloWorld/HelloWorld/OpenMP_Fib/src/
export KMP_A_DEBUG=20
./OpenMP_Fib $1 2>test.txt
cp test.txt ~/Documents/Git/HelloWorld/HelloWorld/Python/test.txt
cd ~/Documents/Git/HelloWorld/HelloWorld/Python/
python readLogFile.py
cd ~/Downloads/xdot-0.7
./xdot.py ~/Documents/Git/HelloWorld/HelloWorld/Python/taskSpawn.dot 
