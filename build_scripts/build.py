import os
import subprocess
import shutil
import sys

from git import Repo


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
            os.mkdir(os.path.join(self.dist_folder, folder))
            shutil.copytree(os.path.join(self.project_folder, folder),
                            os.path.join(self.dist_folder, folder), dirs_exist_ok=True)
        shutil.copy(os.path.join(self.project_folder, 'src', 'index.html'), self.dist_folder)

    def css(self):
        process = subprocess.run(
            ['sass', os.path.join(self.project_folder, 'src', 'style.scss'),
             os.path.join(self.dist_folder, 'style.css')])
        process.check_returncode()


if __name__ == '__main__':
    build = Build()
    build_prod = sys.argv[1] == 'prod'
    build.webpack(build_prod)

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
