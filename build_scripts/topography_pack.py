import os
from glob import glob

from PyTexturePacker import Packer

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
topo_path = os.path.realpath(os.path.join(dir_path, "topography"))

packer = Packer.create( max_width=2048, max_height=2048, bg_color=0xffffffff, trim_mode=1, enable_rotated=False )

atlasData = {}
for file in glob('%s%s*.png'  % (topo_path, os.path.sep)):
    print(file)
    p = {
        'path': file,
        'width': 316,
        'height': 198,
        'data': {
            'pivotX': 0.5,
            'pivotY': 0.5,
        }
    }
    basename = os.path.basename(file)
    atlasData[basename] = p
