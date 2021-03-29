import os
import sys
import subprocess

"""
Helper script to extract score using drxtract
"""

movie_file = os.path.realpath(sys.argv[1])
movie_name = os.path.basename(movie_file)
movie_dir = os.path.dirname(movie_file)
extract_folder = os.path.join(movie_dir, 'drxtract', movie_name)

script_dir = os.path.realpath(os.path.dirname(__file__))
drextract_script = os.path.join(script_dir, 'drxtract', 'drxtract')

os.makedirs(extract_folder)
script = os.path.join('drxtract', 'drxtract')

subprocess.run([sys.executable, drextract_script, 'pc', sys.argv[1], extract_folder])
