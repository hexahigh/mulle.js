'use strict'

import ObjectAnimation from './animation'

/**
 * Weak bridge (map 8)
 * @type {{MapObject}}
 */
const MapObject = {}

MapObject.onCreate = function () {
  const animations = new ObjectAnimation(this, 'CDDATA.CXT')
  animations.load(this.def.FrameList)
  animations.static('normal', this.opt.Direction)

  const splash = animations.add('splash', 'Splash', this.opt.Direction)
  splash.onComplete.add(() => {
    this.visible = false
  }, this)
  console.log(this.opt)
}

MapObject.onEnterInner = function (car) {
  const weight = this.game.mulle.user.Car.getProperty('weight')
  if (weight >= 20) {
    // TODO: Check sound and cutscene
    console.log('Car weight ', weight)
    console.log('Car too heavy, bridge broken')
    this.animations.play('splash')
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

export default MapObject
