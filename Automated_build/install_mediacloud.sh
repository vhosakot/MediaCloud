#!/bin/bash

cd mercury/bootstrap/
source mercury-env.sh
cd ../..
./part1.py
cd mercury/bootstrap/
source mercury-env.sh
cd ../..
./part2.py
