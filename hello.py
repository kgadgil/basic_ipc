#!/usr/bin/python
   
import os
import sys

print ("Hello!")
sys.stdout.flush()
os.close(sys.stdout.fileno())
os.close(sys.stderr.fileno())

data = sys.stdin.read()
with open("data_received_by_child.txt", "w") as fp:
    print >>fp, data