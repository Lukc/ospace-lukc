# tweak PYTHONPATH
import sys
sys.path.insert(0, 'lib')
sys.path.insert(0, '../server/lib')

from distutils.core import setup

havePy2Exe = False
try:
    import py2exe
    havePy2Exe = True
except ImportError:
    pass

havePy2App = False
try:
    import py2app
    havePy2App = True
except ImportError:
    pass

import glob
import shutil
import os
import stat

# hack to persuade py2exe to include PyGame libraries
if havePy2Exe:
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
        if "pygame" in pathname.lower():
            return 0
        return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL

# copy server library
if not os.path.exists("libsrvr"):
    shutil.copytree("../server/lib", "libsrvr")
else:
    sys.path.append("libsrvr")


# collect data files
data_files = []
data_files.append(
    (
        ".",
        ["../ChangeLog.txt", "../COPYING", "../README", "../README_CZ"]
    )
)

# resources
for root, dirs, files in os.walk('res'):
    try:
        dirs.remove(".svn")
    except ValueError:
        pass
    if files:
        data_files.append((root, [os.path.join(root, file) for file in files]))

data_files.append(
    (
        "res/techspec",
        [
            "../server/lib/ige/ospace/Rules/techs.spf",
            "../server/lib/ige/ospace/Rules/Tech.spf",
        ]
    )
)

if havePy2Exe:
    data_files.append((".", ["../updater/update.exe"]))

# version
import ige.version

# generate up-to-date rules
import ige.ospace.Rules

# setup
extraArgs = dict()

if havePy2Exe:
    extraArgs = dict(
        windows = [
            {
                "script": "osc.pyw",
                "icon_resources": [(1, "res/icon48.ico")]
            }
        ],
    )
elif havePy2App:
    extraArgs = dict(
        app = ["osc.pyw"],
    )
else:
    extraArgs = dict(
        scripts = ["osc.py"]
    )
        
setup(
    name = 'Outer Space',
    version = '%(major)s.%(minor)s.%(revision)s' % ige.version.version,
    description = 'Client for Outer Space on-line game',
    author = "Ludek Smid",
    author_email = "qark@ospace.net",
    maintainer = 'Ludek Smid',
    maintainer_email = 'qark@ospace.net',
    url = 'http://www.ospace.net/',
    data_files = data_files,
    package_dir = {"osci": "lib/osci", "pygameui": "lib/pygameui", "": "libsrvr"},
    packages = ["osci", "osci.dialog", "pygameui", "igeclient", "ige", "ige.ospace", "ige.ospace.Rules"],
    py_modules = ["log"],
    **extraArgs
)

# cleanup
def onerror(func, path, err):
    if func is os.remove:
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)

shutil.rmtree("libsrvr", onerror = onerror)
