import os
import shutil
import subprocess
import sys
import zipfile

import pycdlib
import requests
import sass
from git import Repo
import glob

import ShockwaveExtractor
from PyTexturePacker import Packer
from topography import build_topography


def download_file(url, local_file, show_progress=True):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_file, 'wb') as fp:
            print('Download to', local_file)
            for chunk in r.iter_content(chunk_size=8192):
                if show_progress:
                    print(fp.tell(), end='\r')
                fp.write(chunk)


class Build:
    def __init__(self, language='sv'):
        self.language = language
        self.script_folder = os.path.dirname(__file__)
        self.project_folder = os.path.realpath(os.path.join(self.script_folder, '..'))
        self.dist_folder = os.path.join(self.project_folder, 'dist')
        self.movie_folder = os.path.join(self.project_folder, 'Movies')
        self.extract_folder = os.path.join(self.project_folder, 'cst_out_new')

    def scores(self):
        drxtract_folder = os.path.join(self.script_folder, 'drxtract')
        if not os.path.exists(drxtract_folder):
            repo = Repo.clone_from('https://github.com/System25/drxtract.git', drxtract_folder)
            repo.git.checkout('be17978bb9dcf220f2c97c1b0f7a19022a95c001')

        files = glob.glob('%s/8*' % self.movie_folder)
        for movie_file in files:
            movie_name = os.path.basename(movie_file)
            movie_dir = os.path.dirname(movie_file)
            extract_folder = os.path.join(movie_dir, 'drxtract', movie_name)
            os.makedirs(extract_folder, exist_ok=True)
            subprocess.run([sys.executable, 'drxtract', 'pc', movie_file, extract_folder],
                           cwd=drxtract_folder, capture_output=True).check_returncode()
            score_script = os.path.join(self.script_folder, 'score', 'score.py')
            subprocess.run([sys.executable, score_script, os.path.join(extract_folder, 'score.json')],
                           capture_output=True).check_returncode()

            score_script2 = os.path.join(self.script_folder, 'score', 'build_score_manual.py')
            score_file = os.path.join(self.movie_folder, 'drxtract', '82.DXR', 'score_tracks_82.DXR.json')
            subprocess.run([sys.executable, score_script2, score_file, '4', 'JustDoIt'])
            subprocess.run([sys.executable, score_script2, score_file, '5', 'JustDoIt'])

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
            if not os.path.exists(destination):
                os.mkdir(destination)
            shutil.copytree(os.path.join(self.project_folder, folder), destination, dirs_exist_ok=True)
        shutil.copy(os.path.join(self.project_folder, 'src', 'index.html'), self.dist_folder)

    def css(self):
        sass.compile(dirname=(os.path.join(self.project_folder, 'src'), self.dist_folder))

    def rename(self):
        rename_script = os.path.join(self.script_folder, 'rename.py')
        subprocess.run([sys.executable, rename_script, self.extract_folder]).check_returncode()

    def download_game(self, show_progress=True):
        if self.language == 'no':
            url = 'https://archive.org/download/bygg-biler-med-mulle-mekk/Bygg%20biler%20med%20Mulle%20Mekk.iso'
        elif self.language == 'sv':
            url = 'https://archive.org/download/byggbilarmedmullemeck/byggbilarmedmullemeck.iso'
        elif self.language == 'da':
            url = 'https://archive.org/download/byg-bil-med-mulle-meck/Byg-bil-med-Mulle-Meck.iso'
        elif self.language == 'nl':
            url = 'https://archive.org/download/1.mielmonteurbouwtautosiso/1.Miel%20Monteur%20Bouwt%20Auto%27s%20ISO.iso'
        else:
            raise AttributeError('Invalid language')
        iso_folder = os.path.join(self.script_folder, 'iso')
        if not os.path.exists(iso_folder):
            os.mkdir(iso_folder)

        local_file = os.path.join(iso_folder, 'mullebil_%s.iso' % self.language)
        if os.path.exists(local_file):
            return local_file

        download_file(url, local_file, show_progress)
        return local_file

    def download_plugin(self):
        url = 'https://web.archive.org/web/20011006153539if_/http://www.levende.no:80/mulle/plugin.exe'
        local_file = os.path.join(self.script_folder, 'iso', 'plugin.exe')
        extract_dir = os.path.join(self.script_folder, 'Plugin')
        if not os.path.exists(local_file):
            download_file(url, local_file, False)
        with zipfile.ZipFile(local_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        ShockwaveExtractor.main(['-e', '-i', os.path.join(extract_dir, '66.dxr')])
        ShockwaveExtractor.main(['-e', '-i', os.path.join(extract_dir, 'Plugin.cst')])

    def extract_iso(self, extract_content=True):
        iso_path = self.download_game(False)

        iso = pycdlib.PyCdlib()
        iso.open(iso_path)

        if not os.path.exists(self.movie_folder):
            os.mkdir(self.movie_folder)

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
            extracted_file = os.path.join(self.movie_folder, os.path.basename(file).upper())
            iso.get_file_from_iso(extracted_file, iso_path=file)
            if extract_content:
                ShockwaveExtractor.main(['-e', '-i', extracted_file])
        if self.language != 'sv':
            self.rename()

    def copy_images(self):
        plugin_parts = [22, 25, 29, 33, 36, 39, 43]
        for part in plugin_parts:
            part_file = os.path.join(self.extract_folder, 'PLUGIN.CST', 'Standalone', '%s.bmp' % part)
            output_file = os.path.join(self.dist_folder, 'info', 'img', '%s.png' % part)
            subprocess.run(['magick', 'convert', part_file, output_file]).check_returncode()

        cursors = {
            109: 'default',
            110: 'grab',
            111: 'left',
            112: 'point',
            113: 'back',
            114: 'right',
            115: 'drag_left',
            116: 'drag_right',
            117: 'drag_forward'
        }

        ui_folder = os.path.join(self.dist_folder, 'ui')
        if not os.path.exists(ui_folder):
            os.makedirs(ui_folder, exist_ok=True)

        for number, name in cursors.items():
            part_file = os.path.join(self.extract_folder, '00.CXT', 'Standalone', '%d.bmp' % number)
            output_file = os.path.join(ui_folder, '%s.png' % name)
            subprocess.run(['magick', 'convert', part_file, output_file]).check_returncode()

        loading_file = os.path.join(self.extract_folder, '00.CXT', 'Standalone', '122.bmp')
        output_file = os.path.join(self.dist_folder, 'loading.png')
        subprocess.run(['magick', 'convert', loading_file, output_file]).check_returncode()

    def topography(self):
        subprocess.run([sys.executable, os.path.join(self.script_folder, 'topography.py')])
        source = os.path.join(self.extract_folder, 'CDDATA.CXT', 'Standalone')
        topography_dir = os.path.join(self.dist_folder, 'assets', 'topography')
        if not os.path.exists(topography_dir):
            os.makedirs(topography_dir, exist_ok=True)

        build_topography(source, topography_dir)

        try:
            subprocess.run(['node', os.path.join(self.script_folder, 'topography.js'), topography_dir],
                           capture_output=True).check_returncode()
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode('utf-8'))
            raise e


if __name__ == '__main__':
    if len(sys.argv) > 1 and len(sys.argv[1]) == 2:
        build = Build(sys.argv[1])
    else:
        build = Build()

    if 'build-prod' in sys.argv:
        sys.argv = ['webpack-prod', 'phaser', 'download', 'scores', 'html_css']

    if 'webpack-dev' in sys.argv:
        build.webpack()
    elif 'webpack-prod' in sys.argv:
        build.webpack(True)

    if 'scores' in sys.argv:
        build.scores()

    if 'phaser' in sys.argv:
        phaser_folder = os.path.join(build.project_folder, 'phaser-ce')
        build.phaser(phaser_folder)

    if 'html_css' in sys.argv:
        build.html()
        build.copy_images()
        build.css()

    if 'download' in sys.argv:
        build.extract_iso()
        build.download_plugin()

    if 'topography' in sys.argv:
        build.topography()
