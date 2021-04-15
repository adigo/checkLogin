# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\chengyi.lee\\PycharmProjects\\checkLogin'],
             binaries=[('./driver/chromedriver.exe', './driver')],
             datas=[('checkLogin.json', '.'), ('checkLogin.ini', '.')],
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
          [],
          name='checkLogin-selenium',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
import shutil
shutil.copyfile('checkLogin.ini', '{0}/checkLogin.ini'.format(DISTPATH))
shutil.copyfile('checkLogin.json', '{0}/checkLogin.json'.format(DISTPATH))