#!/usr/bin/env python
# File Integrity Monitor
# By venoblin

import os
import sys
import subprocess
import sqlite3

connection = sqlite3.connect("fim.db")
db = connection.cursor()

db.execute("CREATE TABLE IF NOT EXISTS files(file_name, md5, file_path)")

def check(path):
  if not os.path.isdir(path):
    print(f"Error: Directory '{path}' not found.")
    return
  
  files = os.listdir(path)

  
  for f in files:
    output = subprocess.run(["md5sum", f], capture_output=True, text=True).stdout
    hash = output[:32]

    res = db.execute("SELECT * FROM files WHERE md5=?", (hash,))

    if res.fetchone() is None:
      print(f"New file found: {f}")
      db.execute("INSERT INTO files VALUES (?, ?, ?)", (f, hash, path))
      connection.commit() 

if __name__ == '__main__':
  path_arg = None

  if len(sys.argv) < 2:
    pwd = subprocess.run(["pwd"], capture_output=True, text=True).stdout
    path_arg = pwd
  else:
    path_arg = sys.argv[1]
  
  check(path_arg)

  connection.close()