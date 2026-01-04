#!/usr/bin/env python
# File Integrity Monitor
# By venoblin

import os
import sys
import subprocess
import sqlite3

connection = sqlite3.connect("fim.db")
db = connection.cursor()

try: 
  db.execute("SELECT * FROM files")
except:
  db.execute("CREATE TABLE files(file_name, md5, file_path)")


def check(path):
  files = os.listdir(path)
  
  for f in files:
    hash = subprocess.run(["md5sum", f], capture_output=True).stdout.splitlines()
    db.execute(f"SELECT md5 FROM files WHERE md5={hash}")
    db.fetchone()

if __name__ == '__main__':
  path_arg = sys.argv[1]
  
  check(path_arg)

  db.close()