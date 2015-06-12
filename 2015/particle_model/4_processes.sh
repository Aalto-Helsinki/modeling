#!bin/bash

echo "Spawning 4 processes"
for i in {1..4} ;
do
    ( (python server.py) & )
 done