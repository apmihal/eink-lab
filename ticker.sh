#!/usr/bin/env

nohup python -u ticker.py > ticker.log &

tail -f ticker.log
