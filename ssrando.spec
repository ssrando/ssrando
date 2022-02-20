# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import re
import glob
def build_datas_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      dest_dirname = os.path.dirname(filename)
      if dest_dirname == "":
        dest_dirname = "."
      
      data_entry = (filename, dest_dirname)
      datas.append(data_entry)
      print(data_entry)
  
  return datas

with open('version.txt') as f:
  VERSION = f.read().strip()

if os.path.isdir(".git"):
  version_suffix = "_NOGIT"
  
  git_commit_head_file = os.path.join(".git", "HEAD")
  if os.path.isfile(git_commit_head_file):
    with open(git_commit_head_file, "r") as f:
      head_file_contents = f.read().strip()
    if head_file_contents.startswith("ref: "):
      # Normal head, HEAD file has a reference to a branch which contains the commit hash
      relative_path_to_hash_file = head_file_contents[len("ref: "):]
      path_to_hash_file = os.path.join(".git", relative_path_to_hash_file)
      if os.path.isfile(path_to_hash_file):
        with open(path_to_hash_file, "r") as f:
          hash_file_contents = f.read()
        version_suffix = "_" + hash_file_contents[:7]
    elif re.search(r"^[0-9a-f]{40}$", head_file_contents):
      # Detached head, commit hash directly in the HEAD file
      version_suffix = "_" + head_file_contents[:7]
  VERSION += version_suffix
else:
  raise Exception('can only build distribution if running from git!')

# save it so it can be included in the binary
with open('version-with-git.txt','w') as f:
  f.write(VERSION)

a = Analysis(['randoscript.py'],
             pathex=[],
             binaries=[],
             datas=build_datas_recursive([
             	'version-with-git.txt',
             	'names.txt',
             	'*.yaml',
             	'assets/*',
              'asm/*.txt',
              'asm/patch_diffs/*.txt'
             ]),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ssrando',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          runtime_tmpdir=None, )
