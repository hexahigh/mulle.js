import os
import subprocess
import shutil

from git import Repo


def drxtract_clone(folder):
    repo = Repo.clone_from('https://github.com/System25/drxtract.git', folder)
    repo.git.checkout('be17978bb9dcf220f2c97c1b0f7a19022a95c001')
    return repo


def phaser_clone(folder):
    return Repo.clone_from('https://github.com/photonstorm/phaser-ce.git', folder, branch='v2.16.0',
                           single_branch=None)


def phaser_build(folder):
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


script_folder = os.path.dirname(__file__)
dist_folder = os.path.join(script_folder, '..', 'dist')

drxtract_folder = os.path.join(script_folder, 'drxtract')
if not os.path.exists(drxtract_folder):
    drxtract_clone(drxtract_folder)

phaser_folder = os.path.join(script_folder, '..', 'phaser-ce')
if not os.path.exists(phaser_folder):
    phaser_clone(phaser_folder)
    phaser_build(phaser_folder)
    shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.min.js'), dist_folder)
    shutil.copy(os.path.join(phaser_folder, 'dist', 'phaser.map'), dist_folder)
