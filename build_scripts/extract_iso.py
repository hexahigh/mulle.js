import os
import sys
from ShockwaveExtractor import main
from pycdlib.dr import DirectoryRecord
import pycdlib

dir_path = os.path.dirname(os.path.realpath(__file__))
movies_path = os.path.realpath(os.path.join(dir_path, '..', 'Movies'))
if not os.path.exists(movies_path):
    os.mkdir(movies_path)

# Check that there are enough command-line arguments.
if len(sys.argv) != 2:
    print('Usage: %s [iso image]' % sys.argv[0])
    sys.exit(1)


iso = pycdlib.PyCdlib()
iso.open(sys.argv[1])

for child in iso.list_children(iso_path='/Movies'):
    assert isinstance(child, DirectoryRecord)
    if child is None or child.is_dot() or child.is_dotdot():
        continue

    file = iso.full_path_from_dirrecord(child)
    extracted_file = os.path.join(movies_path, os.path.basename(file).upper())
    iso.get_file_from_iso(extracted_file, iso_path=file)
    os.chdir(os.path.join(dir_path, '..'))
    main(['-e', '-i', extracted_file])
