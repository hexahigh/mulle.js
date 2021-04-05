'use strict'

// noinspection JSValidateTypes
/**
 * Weak bridge (map 8)
 * @type {MulleMapObject}
 */
const MapObject = {}

MapObject.onCreate = function () {
  this.animationHelper.static('normal', this.opt.Direction)
  this.animationHelper.add('splash', 'Splash', this.opt.Direction)
}

MapObject.onEnterInner = function (car) {
  const weight = this.game.mulle.user.Car.getProperty('weight')
  if (weight >= 20) {
    console.log('Car weight ', weight)
    console.log('Car too heavy, bridge broken')

    car.visible = false
    this.animations.play('splash', undefined, undefined, true)
    this.animationHelper.playAudio(0, () => {
      car.visible = true
      this.animationHelper.playAudio(1)
    })

    car.speed = 0
    car.stepback(9)
  } else {
    console.log('Light car')
    const hasMedal = this.game.mulle.user.Car.hasMedal(6)
    if (!hasMedal) {
      this.game.mulle.user.Car.addMedal(6)
    }
  }
}

MapObject.onEnterOuter = function (car) {
  if (!this.alive) {
    car.speed = 0
    car.stepback(9)
  }
}

export default MapObject
