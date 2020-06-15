import os
import sys
from glob import glob
from ShockwaveExtractor import main

gameDir = sys.argv[1]
if not os.path.exists(gameDir):
    raise FileNotFoundError('Game directory %s not found' % gameDir)
gameDir = os.path.realpath(gameDir)
gameDir = os.path.join(gameDir, 'MOVIES')

files = glob('%s%s*.CXT' % (gameDir, os.path.sep)) + glob('%s%s*.DXR' % (gameDir, os.path.sep))
if not files:
    raise FileNotFoundError('No files found')

for file in files:
    main(['-e', '-i', file])
