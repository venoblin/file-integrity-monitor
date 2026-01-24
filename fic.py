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

def check_path(path):
  if not os.path.isdir(path):
    print(f"Error: Directory '{path}' not found.")
    return
  
  files = os.listdir(path)
  modified_files = []
  
  for f in files:
    if not os.path.isdir(f"{path}/{f}"):
      output = subprocess.run(["sha256sum", f"{path}/{f}"], capture_output=True, text=True).stdout
      raw_hash = output[:64]

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

def view_db():
  all_items_res = db.execute("SELECT * FROM files").fetchall()
  print("All Files:")
  for file_name, hash, file_path in all_items_res:
    print(f"{hash} | {file_name}")

def print_banner():
  print(r"""
     ______   _____    _____ 
    |  ____| |_   _|  / ____|
    | |__      | |   | |     
    |  __|     | |   | |     
    | |       _| |_  | |____ 
    |_|      |_____|  \_____|\
    
    :: File Integrity Checker (v1.0) ::   
    [DESCRIPTION]
      A lightweight, zero-dependency File Integrity Checker.
      Watches your filesystem. Detects the silent creeps.
      "Digital fingerprints don't lie."    
    [USAGE]
      python fic.py [target_directory]   
  """)

def run_check():
  if len(sys.argv) >= 2:
    return print('Error: Invalid command, use --help for command information.')
    
  match sys.argv[1]:
    case '--help':
      print_banner()
    case '-d':
      view_db()
    case '-s':
      if len(sys.argv) >= 3:
        check_path(sys.argv[2])
      else:
        print("Error: Path needed.")

if __name__ == '__main__':
  run_check()
    
  connection.close()