#!/usr/bin/env python
# File Integrity Monitor
# By venoblin

import os
import sys
import subprocess
import sqlite3

connection = sqlite3.connect("fic.db")
db = connection.cursor()

db.execute("CREATE TABLE IF NOT EXISTS files(file_name, hash, file_path)")

def check(path):
  if not os.path.isdir(path):
    print(f"Error: Directory '{path}' not found.")
    return
  
  files = os.listdir(path)
  modified_files = []
  
  for f in files:
    if not os.path.isdir(f"{path}/{f}"):
      output = subprocess.run(["md5sum", f], capture_output=True, text=True).stdout
      raw_hash = output[:32]

      hash_res = db.execute("SELECT * FROM files WHERE hash=?", (raw_hash,))

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
        for f in modified_files:
          db.execute("UPDATE files SET hash=? WHERE hash=?", (f["raw_hash"], f["hash"],))
          connection.commit()
          print(f"Baseline set: {f["raw_hash"]} | {f["file_name"]}")

if __name__ == '__main__':
  path_arg = None

  if len(sys.argv) < 2:
    pwd = subprocess.run(["pwd"], capture_output=True, text=True).stdout
    path_arg = pwd
  else:
    path_arg = sys.argv[1]
  
  try:
    check(path_arg)
  except:
    print("Exiting...")
    
  connection.close()