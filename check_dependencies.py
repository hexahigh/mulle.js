try:
    import json
    import os, sys, struct

    from subprocess import call

    from enum import Enum

    import json

    import wave, aifc, sunau

    import glob

    from PIL import Image, ImageDraw, ImagePalette

    import bitstring

    import tempfile

    import platform
except ImportError as e:
    print(e)
    exit(1)
