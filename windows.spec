# -*- mode: python -*-

from kivy.deps import sdl2, glew
import os

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tracta',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='rsc\\ship8.ico')
coll = COLLECT(exe, Tree(os.getcwd()),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='tracta')
