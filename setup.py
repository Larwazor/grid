import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = 'E:\\ptest\\tcl8.6'
os.environ['TK_LIBRARY'] = 'E:\\ptest\\tk8.6'

executables = [cx_Freeze.Executable("game.py", base="Win32GUI")]

cx_Freeze.setup(
    name="Grid Game",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["images/wizard.png", "maps.json"],
                           "excludes": ["tkinter", "numpy", "test", "unittest"]}},
    executables=executables

)
