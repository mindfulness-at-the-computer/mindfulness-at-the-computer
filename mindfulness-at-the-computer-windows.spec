# -*- mode: python -*-

block_cipher = None

####################################
# PLEASE NOTE: The path for the Qt binaries have been hard-coded
####################################

import os
cwd_str = os.getcwd()
# 'C:\\TordPython\\mindfulness-at-the-computer-master'

a = Analysis(['mindfulness-at-the-computer.py'],
             pathex=[cwd_str],
             binaries=[],
             datas=[('.\\README.md', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
             
# Adding the user_files and icons directories
user_files_dir_str = "user_files"
a.datas += Tree('.\\' + user_files_dir_str, prefix=user_files_dir_str, excludes=['*.db'])
# -documentation: https://pythonhosted.org/PyInstaller/advanced-topics.html#the-tree-class
icons_dir_str = "icons"
a.datas += Tree('.\\' + icons_dir_str, prefix=icons_dir_str)

win_icon_path_str = '.\\' + icons_dir_str + '\\icon.ico'

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mindfulness-at-the-computer',
          icon=win_icon_path_str,
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mindfulness-at-the-computer')
