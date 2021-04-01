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
drextract_folder = os.path.join(script_dir, 'drxtract')

os.makedirs(extract_folder, exist_ok=True)

# drextract does not work with absolute path on windows
subprocess.run([sys.executable, 'drxtract', 'pc', sys.argv[1], extract_folder], cwd=drextract_folder)
