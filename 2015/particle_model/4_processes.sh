#!bin/bash

echo "Spawning 4 processes"
for i in {1..4} ;
do
    ( (python3 server.py example_settings) & )
 done