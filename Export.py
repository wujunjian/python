#!/usr/bin/python
#coding:utf-8

import sys
import os
import re
import shutil
import datetime
import time
import subprocess
import gc
import gzip


dir = sys.argv[1]
pos = int(sys.argv[2])

def run():
    
    fields = {}
    for filepath in walk_tree_files(dir):
        if not filepath.endswith('.gz.done'):
            continue

        f = gzip.open(filepath)
        lines = f.readlines()

        for line in lines:
            field = parse_line(line)
            if field != None:
                fields[field] = 1 

        f.close()

    for field in fields.iterkeys():
        print field
    
def runfile(filename):
    fields = {}
    f = gzip.open(filename)
    lines = f.readlines()

    for line in lines:
        field = parse_line(line)
        if field != None:
            fields[field] = 1

    f.close()

    for field in fields.iterkeys():
        print field

def walk_tree_files(dir):
    if dir and os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for name in files:
                yield os.path.join(root, name)


def parse_line(line):
    parts = line.strip().split('\t')
    part_count = len(parts)
    if part_count < pos+1:
        return None 
    else:
        return parts[pos]

def get_stat_lines(filepath):
    with gzip.open(filepath) as f:
        return f.readlines()
                
def get_set(d, k):
    v = d.get(k)
    if not v:
        v = set()
        d[k] = v
    return v

if __name__ == '__main__':
    if len(sys.argv) < 3:
        import sys
        sys.exit()

    try:
        if os.path.isdir(dir):
            run()
        else:
            runfile(dir)
    except Exception, e:
        import sys
        sys.exit() 
