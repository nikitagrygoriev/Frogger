import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = 'C:\\Program Files\\Python36\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\Program Files\\Python36\\tcl\\tk8.6'

executables = [cx_Freeze.Executable('Frogger.py')]
includeFiles = ['frog.png', 'Car1.png', 'Car2.png', 'Car3.png', 'Car4.png', 'Car5.png', 'font.TTF', 'font2.TTF',
                'BackGroundUpd1.png', 'lilyPad.png', 'log.png']

cx_Freeze.setup(
    name='Frogger',
    options={'build_exe': {'packages': ['pygame','time'], 'include_files': includeFiles}},
    executables=executables
)
