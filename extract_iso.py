import os
import sys

import pycdlib
from pycdlib.dr import DirectoryRecord
from pycdlib.pycdlibexception import PyCdlibInvalidInput

from ShockwaveExtractor import main

dir_path = os.path.dirname(os.path.realpath(__file__))
movies_path = os.path.realpath(os.path.join(dir_path, 'Movies'))
if not os.path.exists(movies_path):
    os.mkdir(movies_path)

# Check that there are enough command-line arguments.
if len(sys.argv) != 2:
    print('Usage: %s [iso image]' % sys.argv[0])
    sys.exit(1)
iso_path = os.path.realpath(sys.argv[1])

if not os.path.exists(iso_path):
    raise FileNotFoundError(iso_path)

iso = pycdlib.PyCdlib()
iso.open(iso_path)

try:
    children = iso.list_children(iso_path='/Movies')
    iso.get_record(iso_path='/Movies')
except PyCdlibInvalidInput:
    children = iso.list_children(iso_path='/MOVIES')
    iso.get_record(iso_path='/MOVIES')

for child in children:
    assert isinstance(child, DirectoryRecord)
    if child is None or child.is_dot() or child.is_dotdot():
        continue

    file = iso.full_path_from_dirrecord(child)
    extracted_file = os.path.join(movies_path, os.path.basename(file).upper())
    iso.get_file_from_iso(extracted_file, iso_path=file)
    main(['-e', '-i', extracted_file])
