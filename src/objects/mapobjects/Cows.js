'use strict'

var MapObject = {}

MapObject.onCreate = function () {
  this.animationHelper.add('idle', 'normal', 1, 12, true)

  const parting = this.animationHelper.add('parting', 'Parting', 1, 5)
  parting.onComplete.add(() => {
    this.animations.play('parted')
  })

  this.animationHelper.add('parted', 'Outer', 1, 12, true)

  const gathering = this.animationHelper.add('gathering', 'Gathering')
  gathering.onComplete.add(() => {
    this.animations.play('idle')
  })

  this.animations.play('idle')
}

MapObject.onEnterOuter = function (car) {

}

MapObject.onEnterInner = function (car) {
  var allowed = this.game.mulle.user.Car.getProperty('horntype', 0) >= 1

  var horns = ['05e050v0', '05e049v0', '05e044v0', '05e042v0', '05d013v0']

  if (allowed) {
    this.animations.play('parting')

    if (!this.playedSound) {
      this.game.mulle.playAudio(horns[ this.game.mulle.user.Car.getProperty('horntype', 0) - 1 ])

      this.playedSound = true

      const audio_allowed = this.game.mulle.playAudio('31e001v0')
      audio_allowed.onStop.addOnce(() => {
        this.playedSound = null
      })
    }
  } else {
    if (!this.playedSound) {
      this.playedSound = true

      const audio_error = this.game.mulle.playAudio('31d001v0')
      audio_error.onStop.addOnce(() => {
        this.playedSound = null
      })
    }

    car.speed = 0
    car.stepback(2)
    this.enteredInner = false
  }
}

MapObject.onExitInner = function () {
  this.animations.play('gathering')
}

export default MapObject
