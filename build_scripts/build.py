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

    def phaser_clone(self, folder):
        return Repo.clone_from('https://github.com/photonstorm/phaser-ce.git', folder, branch='v2.16.0',
                               single_branch=None)

    def phaser_build(self, folder):
        subprocess.call(['npm', 'uninstall', 'fsevents'], cwd=folder)
        subprocess.call(['npm', 'install'], cwd=folder)

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

        subprocess.call([
            'npx',
            'grunt',
            'custom',
            '--exclude=' + ','.join(exclude),
            '--uglify',
            '--sourcemap'
        ], cwd=folder)

    def webpack(self, prod=False):
        if not prod:
            config = os.path.join(self.project_folder, 'webpack.dev.js')
        else:
            config = os.path.join(self.project_folder, 'webpack.prod.js')
        subprocess.call(['npx', 'webpack-cli', '-c', config])

    def html(self):
        for folder in ['progress', 'info']:
            os.mkdir(os.path.join(self.dist_folder, folder))
            shutil.copytree(os.path.join(self.project_folder, folder),
                            os.path.join(self.dist_folder, folder), dirs_exist_ok=True)
        shutil.copy(os.path.join(self.project_folder, 'src', 'index.html'), self.dist_folder)


if __name__ == '__main__':
    build = Build()
    build_prod = sys.argv[1] == 'prod'
    drxtract_folder = os.path.join(build.script_folder, 'drxtract')
    if not os.path.exists(drxtract_folder):
        build.drxtract_clone(drxtract_folder)

    phaser_folder = os.path.join(build.project_folder, 'phaser-ce')
    if not os.path.exists(phaser_folder):
        build.phaser_clone(phaser_folder)
        build.phaser_build(phaser_folder)
        shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.min.js'), build.dist_folder)
        shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.map'), build.dist_folder)

    build.webpack(build_prod)
    build.html()
