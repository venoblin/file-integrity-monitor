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
  modified_files = []
  
  for f in files:
    output = subprocess.run(["md5sum", f], capture_output=True, text=True).stdout
    raw_hash = output[:32]

    hash_res = db.execute("SELECT * FROM files WHERE md5=?", (raw_hash,))

    if hash_res.fetchone() is None:
      file_res = db.execute("SELECT * FROM files WHERE file_name=?", (f,)).fetchone()

      if file_res is None:
        print(f"New file found: {raw_hash} | {f}")
        db.execute("INSERT INTO files VALUES (?, ?, ?)", (f, raw_hash, path))
        connection.commit() 
      else:
        file_name, hash, file_path = file_res
        modified_files.append({
          "raw_hash": raw_hash,
          "hash": hash,
          "file_name": f
        })
        
  if len(modified_files) > 0:
    for f in modified_files:
      print(f"File modified: {f["hash"]} -> {f["raw_hash"]} | {f["file_name"]}")
    
    baseline_input = input("Wish to create new baseline? (Y, n) ")
    match baseline_input.lower().replace(" ", ""):
      case "n":
        return
      case "y" | "":
        res = db.execute("UPDATE files SET hash=? where hash=?", (raw_hash, hash))
        print(res.fetchone())

if __name__ == '__main__':
  path_arg = None

  if len(sys.argv) < 2:
    pwd = subprocess.run(["pwd"], capture_output=True, text=True).stdout
    path_arg = pwd
  else:
    path_arg = sys.argv[1]
  
  check(path_arg)

  connection.close()