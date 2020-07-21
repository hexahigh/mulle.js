var gulp = require('gulp')
var webpack = require('webpack-stream')
// var gutil = require('gulp-util')
var exec = require('child_process').exec
var spawn = require('child_process').spawn
var sass = require('gulp-sass')
const git = require('gulp-git');
const install = require("gulp-install");

// var WebpackDevServer = require("webpack-dev-server")

var WebpackDev = require('./webpack.dev.js')

var WebpackProd = require('./webpack.prod.js')

gulp.task('phaser-clone', function (done) {
  git.clone('https://github.com/photonstorm/phaser-ce.git', { 'args': './phaser-ce' }, function (error) {
    if (error) throw error
    done()
  })
})

gulp.task('phaser-install', function (done) {
  gulp.src('./phaser-ce/package.json').pipe(install({npm: '-f' }, function () {
    done()
  }))
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
    '--gruntfile ./phaser-ce/Gruntfile.js',
    '--exclude=' + exclude.join(','),
    '--uglify',
    '--sourcemap'
  ]

  /*
  var shl = spawn('grunt', cmd, { stdio: 'inherit' })

  shl.stdout.on('data', function(data){
    console.log('grunt stdout: ' + data.toString())
  })
  */

  exec(cmd.join(' '), function (err, stdout, stderr) {
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
  gulp.src('./loading.png').pipe(gulp.dest('dist/'))
  gulp.src('./data/*.json').pipe(gulp.dest('dist/data/'))

  gulp.src('./ui/*').pipe(gulp.dest('dist/ui/'))

  gulp.src('./topography/topography*').pipe(gulp.dest('dist/assets/topography/'))
  done()
})

gulp.task('topography', function () {
  return spawn('python', ['build_scripts/topography.py'])
})

gulp.task('assets-dev', function () {
  console.log('do assets dev')
  return spawn('python', ['assets.py', '0'])
})

gulp.task('assets-prod', function () {
  console.log('do assets prod')
  return spawn('python', ['assets.py', '7'])
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

gulp.task('phaser', gulp.series('phaser-clone', 'phaser-install', 'phaser-build'))
gulp.task('data', gulp.series('topography', 'copy_data'))
gulp.task('build-dev', gulp.series( 'phaser', 'js-dev', 'html', 'css' ))
gulp.task('build-dev', gulp.series( 'phaser', 'js-dev', 'html', 'css' ))
gulp.task('build-prod', gulp.series( 'phaser', 'js-prod', 'html', 'css' ))

gulp.task('build-full', gulp.series( 'phaser', 'js-prod', 'html', 'css', 'assets-prod', 'data' ))

gulp.task('default', gulp.series( 'build-dev', 'assets-dev', 'data' ))
