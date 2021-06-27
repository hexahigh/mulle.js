import os
import shutil
import subprocess
import sys

import pycdlib
import requests
from git import Repo
import ShockwaveExtractor


class Build:
    def __init__(self):
        self.script_folder = os.path.dirname(__file__)
        self.project_folder = os.path.realpath(os.path.join(self.script_folder, '..'))
        self.dist_folder = os.path.join(self.project_folder, 'dist')

    def drxtract_clone(self, folder):
        repo = Repo.clone_from('https://github.com/System25/drxtract.git', folder)
        repo.git.checkout('be17978bb9dcf220f2c97c1b0f7a19022a95c001')
        return repo

    def phaser(self, folder):
        if not os.path.exists(phaser_folder):
            Repo.clone_from('https://github.com/photonstorm/phaser-ce.git', folder, branch='v2.16.0',
                            single_branch=None)

        subprocess.run(['npm', 'uninstall', 'fsevents'], cwd=folder).check_returncode()
        subprocess.run(['npm', 'install'], cwd=folder).check_returncode()

        exclude = ['gamepad',
                   'bitmaptext',
                   'retrofont',
                   'rope',
                   'tilesprite',
                   'flexgrid',
                   'ninja',
                   'p2',
                   'tilemaps',
                   'particles',
                   'weapon',
                   'creature',
                   'video'
                   ]

        subprocess.run([
            'npx',
            'grunt',
            'custom',
            '--exclude=' + ','.join(exclude),
            '--uglify',
            '--sourcemap'
        ], cwd=folder).check_returncode()

        shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.min.js'), self.dist_folder)
        shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.map'), self.dist_folder)

    def webpack(self, prod=False):
        if not prod:
            config = os.path.join(self.project_folder, 'webpack.dev.js')
        else:
            config = os.path.join(self.project_folder, 'webpack.prod.js')
        process = subprocess.run(['npx', 'webpack-cli', '-c', config])
        process.check_returncode()

    def html(self):
        for folder in ['progress', 'info']:
            destination = os.path.join(self.dist_folder, folder)
            print(destination)
            os.mkdir(destination)
            shutil.copytree(os.path.join(self.project_folder, folder), destination, dirs_exist_ok=True)
        shutil.copy(os.path.join(self.project_folder, 'src', 'index.html'), self.dist_folder)

    def css(self):
        process = subprocess.run(
            ['sass', os.path.join(self.project_folder, 'src', 'style.scss'),
             os.path.join(self.dist_folder, 'style.css')])
        process.check_returncode()

    def download_game(self, language='se', show_progress=True):
        if language == 'no':
            url = 'https://archive.org/download/bygg-biler-med-mulle-mekk/Bygg%20biler%20med%20Mulle%20Mekk.iso'
        elif language == 'se':
            url = 'https://archive.org/download/byggbilarmedmullemeck/byggbilarmedmullemeck.iso'
        elif language == 'da':
            url = 'https://archive.org/download/byg-bil-med-mulle-meck/Byg-bil-med-Mulle-Meck.iso'
        else:
            raise AttributeError('Invalid language')
        iso_folder = os.path.join(self.script_folder, 'iso')
        if not os.path.exists(iso_folder):
            os.mkdir(iso_folder)

        local_file = os.path.join(iso_folder, 'mullebil_%s.iso' % language)
        if os.path.exists(local_file):
            return local_file

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_file, 'wb') as fp:
                print('Download to', local_file)
                for chunk in r.iter_content(chunk_size=8192):
                    if show_progress:
                        print(fp.tell(), end='\r')
                    fp.write(chunk)
        return local_file

    def extract_iso(self, language, extract_content=True):
        iso_path = self.download_game(language, False)

        iso = pycdlib.PyCdlib()
        iso.open(iso_path)
        movies_path = os.path.join(self.project_folder, 'Movies')
        if not os.path.exists(movies_path):
            os.mkdir(movies_path)

        try:
            children = iso.list_children(iso_path='/Movies')
            iso.get_record(iso_path='/Movies')
        except pycdlib.pycdlib.pycdlibexception.PyCdlibInvalidInput:
            children = iso.list_children(iso_path='/MOVIES')
            iso.get_record(iso_path='/MOVIES')

        for child in children:
            assert isinstance(child, pycdlib.pycdlib.dr.DirectoryRecord)
            if child is None or child.is_dot() or child.is_dotdot():
                continue

            file = iso.full_path_from_dirrecord(child)
            extracted_file = os.path.join(movies_path, os.path.basename(file).upper())
            iso.get_file_from_iso(extracted_file, iso_path=file)
            if extract_content:
                ShockwaveExtractor.main(['-e', '-i', extracted_file])
        return movies_path


if __name__ == '__main__':
    build = Build()

    if 'webpack-dev' in sys.argv:
        build.webpack()
    elif 'webpack-prod' in sys.argv:
        build.webpack(True)

    if 'scores' in sys.argv:
        drxtract_folder = os.path.join(build.script_folder, 'drxtract')
        if not os.path.exists(drxtract_folder):
            build.drxtract_clone(drxtract_folder)

    if 'phaser' in sys.argv:
        phaser_folder = os.path.join(build.project_folder, 'phaser-ce')
        build.phaser(phaser_folder)

    if 'html_css' in sys.argv:
        build.html()
        build.css()

    if 'download-no' in sys.argv:
        build.extract_iso('no')
    elif 'download-se' in sys.argv:
        build.extract_iso('se')
    elif 'download-da' in sys.argv:
        build.extract_iso('da')
