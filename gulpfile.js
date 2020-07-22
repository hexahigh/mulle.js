const gulp = require('gulp')
const child_process = require('child_process')
const exec = require('gulp-exec');
const texturePacker = require('gulp-free-tex-packer')
const git = require('gulp-git')
const rename = require('gulp-rename')
const sass = require('gulp-sass')
const spawn = require('gulp-spawn')
const webpack = require('webpack-stream')

const WebpackDev = require('./webpack.dev.js')
const WebpackProd = require('./webpack.prod.js')

function detectPython () {
  const processPy = child_process.spawnSync('python', ['-V'])
  if (processPy.output[1].toString().search('Python 3') === 0) {
    return 'python'
  }

  const processPy3 = child_process.spawnSync('python3', ['-V'])
  if (processPy3.output[1].toString().search('Python 3') === 0) {
    return 'python3'
  }
}

const python = detectPython()

gulp.task('phaser-clone', function (done) {
  return git.clone('https://github.com/photonstorm/phaser-ce.git', { args: './phaser-ce' }, function (error) {
    if (error) throw error
    git.checkout('v2.16.0', {'cwd': './phaser-ce'})
    done()
  })
})

gulp.task('phaser-install', function (done) {
  child_process.exec('npm uninstall fsevents', {'cwd': './phaser-ce'}, function () {
    child_process.exec('npm install', {'cwd': './phaser-ce'}, function () {
      done()
    })
  })
})

gulp.task('phaser-build', function (done) {
  var exclude = [
    'gamepad',
    // 'rendertexture',
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

  var cmd = [
    'npx',
    'grunt',
    'custom',
    '--exclude=' + exclude.join(','),
    '--uglify',
    '--sourcemap'
  ]

  child_process.exec(cmd.join(' '), {'cwd': './phaser-ce'}, function (err, stdout, stderr) {
    console.log('phaser err: ' + err)
    console.log('phaser stdout: ' + stdout)
    console.log('phaser stderr: ' + stderr)

    gulp.src('./phaser-ce/dist/phaser.min.js').pipe(gulp.dest('dist/'))
    gulp.src('./phaser-ce/dist/phaser.map').pipe(gulp.dest('dist/'))
    done()
  })
})

gulp.task('html', function (done) {
  gulp.src('./progress/**').pipe(gulp.dest('dist/progress/'))
  gulp.src('./info/**').pipe(gulp.dest('dist/info/'))
  gulp.src('./src/index.html').pipe(gulp.dest('dist/'))
  done()
})

gulp.task('css', function () {
  return gulp.src('./src/style.scss').pipe(sass({ /* outputStyle: 'compressed' */ }).on('error', sass.logError)).pipe(gulp.dest('dist/'))
})

gulp.task('copy_data', function (done) {
  gulp.src('./cst_out_new/00.CXT/Standalone/122.bmp', { buffer: false })
    .pipe(
      spawn({
        cmd: 'magick',
        args: ['convert', '-', 'png:-'],
        filename: function (base) {
          return base + '.png'
        }
      })
    )
    .pipe(rename('loading.png')).pipe(gulp.dest('./dist/'))

  gulp.src('./data/*.json').pipe(gulp.dest('dist/data/'))

  gulp.src('./ui/*').pipe(gulp.dest('dist/ui/'))

  gulp.src('./topography/topography*').pipe(gulp.dest('dist/assets/topography/'))

  const cursors = {
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

  for (const [number, name] of Object.entries(cursors)) {
    gulp.src(`./cst_out_new/00.CXT/Standalone/${number}.png`).pipe(rename(name + '.png')).pipe(gulp.dest('dist/ui'))
  }

  /*for (let i=161; i<=191; i++) {
    gulp.src(`./cst_out_new/05.DXR/Internal/${i}.png`).pipe(gulp.dest)
  }*/

  done()
})

gulp.task('pack_topography', function () {
  return gulp.src('topography/30t*.png')
    .pipe(texturePacker({
      textureName: 'topography',
      removeFileExtension: true,
      prependFolderName: false,
      exporter: 'JsonHash',
      width: 2048,
      height: 2048,
      fixedSize: false,
      padding: 1,
      allowRotation: false,
      allowTrim: true,
      detectIdentical: true,
      packer: 'MaxRectsBin',
      packerMethod: 'BottomLeftRule'
    }))
    .pipe(gulp.dest('topography'))
})

gulp.task('build_topography', function () {
  const process = child_process.spawn(python, ['build_scripts/topography.py'])

  process.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`)
  })
  process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`)
  })

  return process
})

gulp.task('assets', function () {
  console.log('do assets dev')
  const process = child_process.spawn(python, ['assets.py', '0'])

  process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`)
  })
  return process
})

gulp.task('optipng', function () {
  const options = {
    continueOnError: false, // default = false, true means don't emit error event
    pipeStdout: false, // default = false, true means stdout is written to file.contents
  };
  const reportOptions = {
    err: true, // default = true, false means don't write err
    stderr: true, // default = true, false means don't write stderr
    stdout: true // default = true, false means don't write stdout
  };

  return gulp.src('./dist/assets/*.png')
    .pipe(exec(file => `optipng -o7 ${file.path}`, options))
    .pipe(exec.reporter(reportOptions));
})

gulp.task('js-dev', function () {
  return gulp.src('src/index.js').pipe(
    webpack(WebpackDev)
  ).pipe(
    gulp.dest('dist/')
  )
})

gulp.task('js-prod', function () {
  return gulp.src('src/index.js').pipe(
    webpack(WebpackProd)
  ).pipe(
    gulp.dest('dist/')
  )
})

gulp.task('rename', function () {
  return child_process.spawn(python, ['build_scripts/rename.py', 'cst_out_new'])
})

/*gulp.task('package', function () {
  gulp.src('./dist').pipe(exec(file=>`tar -czfO ${file.path}`))
  child_process.spawn('tar', ['-czf', '-', process.env.BUILD_LANG, ])
//  tar -czf ~/Mulle_${BUILD_LANG}.tgz -C ${TRAVIS_BUILD_DIR}/dist .
//tar -czf ~/Mulle_cst_${BUILD_LANG}.tgz -C ${TRAVIS_BUILD_DIR}/cst_out_new .

})*/

gulp.task('phaser', gulp.series('phaser-clone', 'phaser-install', 'phaser-build'))
gulp.task('data', gulp.series('build_topography', 'pack_topography', 'copy_data'))
gulp.task('build-dev', gulp.series('phaser', 'js-dev', 'html', 'css'))
gulp.task('build-prod', gulp.series('phaser', 'js-prod', 'html', 'css'))

gulp.task('build-full', gulp.series('phaser', 'js-prod', 'html', 'css', 'assets', 'optipng', 'data'))
gulp.task('build-full-no', gulp.series('rename', 'build-full'))

gulp.task('default', gulp.series('build-dev', 'assets', 'data'))
