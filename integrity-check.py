#!/usr/bin/env python
# File Integrity Monitor
# By venoblin

import os
import sys
import subprocess

def check(path):
  files = os.listdir(path)
  
  for f in files:
    hash = subprocess.run(["md5sum", f], capture_output=True).stdout.splitlines()
    print(hash)

if __name__ == '__main__':
  path_arg = sys.argv[1]
  
  check(path_arg)