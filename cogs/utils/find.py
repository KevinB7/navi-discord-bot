#!/usr/bin/env python3

import zipfile
import tempfile
import random
import os

def search(directory, pattern, single=True):
  pattern = set(filter(None, pattern))
  matches = []

  for root, directories, filenames in os.walk(directory):
    for filename in filenames:
      filename = os.path.join(root,filename)
      filename = os.path.realpath(filename)
      if match(filename, pattern):
        matches.append(filename)

  if single:
    return random.choice(matches)
  return matches

def match(filename, pattern):
  pattern.add('-.git')
  for i in pattern:
    if i[0] == '-':
      if i[1:].lower() in filename.lower():
        return False
    elif i not in filename.lower():
      return False
  return True

def extract(filename):
  files = []
  tmp_file = tempfile.mkdtemp()
  with zipfile.ZipFile(filename, 'r') as zip_ref:
    for i in zip_ref.namelist():
      ext = '.' + i.rpartition('.')[2].lower()
      if ext in ['.png', '.jpg', '.gif']:
        zip_ref.extract(i, tmp_file)
        files.append(os.path.join(tmp_file, i))
  return files
