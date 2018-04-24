# -*- mode: python -*-
# -*- coding: utf-8 -*-

"""
This is a PyInstaller spec file.
"""

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.archive.pyz_crypto import PyiBlockCipher

# Constants
DEBUG = os.environ.get("CEFPYTHON_PYINSTALLER_DEBUG", False)

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


a = Analysis(
    ["../main.py"],
    hookspath=["."],  # To find "hook-cefpython3.py"
    cipher=None,
    win_private_assemblies=True,
    win_no_prefer_redirects=True,
)

if not os.environ.get("PYINSTALLER_CEFPYTHON3_HOOK_SUCCEEDED", None):
    raise SystemExit("Error: Pyinstaller hook-cefpython3.py script was "
                     "not executed or it failed")

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=None)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name="ImageShare",
          debug=DEBUG,
          strip=False,
          upx=False,
          console=DEBUG,
          icon="../resources/icon.ico")

COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        name="ImageShare")