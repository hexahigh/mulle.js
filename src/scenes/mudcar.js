import MulleState from './base'
import DirectorHelper from '../objects/DirectorHelper'
import directorAnimation from '../util/directorAnimation'
import movingAnimation from '../util/movingAnimation'
import partUtil from '../util/partUtil'
import blinkThing from '../util/blinkThing'
import MulleActor from '../objects/actor'

class MudCarState extends MulleState {
  preload () {
    super.preload()

    this.game.load.pack('mudcar', 'assets/mudcar.json', null, this)
    this.dirResource = '82.DXR'
    this.game.load.json('JustDoIt_car', 'data/score/82.DXR_JustDoIt_4.json')
    this.game.load.json('JustDoIt_rope', 'data/score/82.DXR_JustDoIt_5.json')
  }

  /**
   * Animation "titt", driver talks on the phone
   */
  driverAnimation() {
    const driverHead = DirectorHelper.sprite(this.game, 412, 216, this.dirResource, 26, true)
    this.car_layer.add(driverHead)

    let suckFrames = [1,1,1,1,1,2,3,3,3,3,3,3,3,2]
    suckFrames = directorAnimation.offset(suckFrames, 25)
    const [, suckFrameSprites] = directorAnimation.resolveDirectorFrames(this.game, this.dirResource, suckFrames)
    const suckAnimation = driverHead.animations.add('suck', suckFrameSprites, 12, true)
    // suckAnimation.onComplete.add(this.checkStrength, this)
    driverHead.animations.play('suck')

    //Help! i'm stuck in the mud
    this.game.mulle.playAudio('82d009v0', () => {
      driverHead.destroy()
      this.checkStrength()
    })
  }

  /**
   * Check car strength and start the correct animation
   */
  checkStrength() {
    const strength = this.game.mulle.user.Car.getProperty('strength')
    console.log('Car strength is', strength)
    if (strength < 1) { // TODO: Check number
      this.weakCar()
    } else {
      this.strongCar()
    }
  }

  addPart () {
    const part = new partUtil(this.game)
    this.partId = part.getPart()
    this.partSprite = part.showPart(this.partId, 412, 326)
    this.background_layer.add(this.partSprite)
  }

  /**
   * Mulle discovers the part
   */
  findPart () {
    /*this.game.mulle.playAudio('82d006v0', () => {

    }*/
    const mulle = new MulleActor(this.game, -59, 166, 'mulleDefault')
    mulle.talkAnimation = 'talkRegular'
    mulle.silenceAnimation = 'idle'
    this.game.add.existing(mulle)
    this.game.mulle.actors.mulle = mulle

    this.game.mulle.actors.mulle.talk('82d006v0', () => {
      new blinkThing(this.game, this.partSprite, this.exit, this)
    })
  }

  strongCar () {
    this.addPart()
    this.game.mulle.playAudio('82e002v0', () => { this.findPart() })

    let strongFrames = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5]
    strongFrames = directorAnimation.offset(strongFrames, 33)
    const [, strongFrameSprites] = directorAnimation.resolveDirectorFrames(this.game, this.dirResource, strongFrames)
    const strongAnimation = this.rope.animations.add('strong', strongFrameSprites, 12)
    strongAnimation.onComplete.add(this.pullCar, this)
    this.rope.animations.play('strong', 12)
  }

  pullCar () {
    this.stuckCar.destroy()
    this.rope.destroy()

    const JustDoIt = this.game.cache.getJSON('JustDoIt_car')
    const JustDoItAnimation = new movingAnimation(this.game, this.dirResource, JustDoIt)
    this.game.add.existing(JustDoItAnimation.sprite)
    JustDoItAnimation.play()

    const JustDoItRope = this.game.cache.getJSON('JustDoIt_rope')
    const JustDoItRopeAnimation = new movingAnimation(this.game, this.dirResource, JustDoItRope, 12, 320, -43)
    this.game.add.existing(JustDoItRopeAnimation.sprite)
    JustDoItRopeAnimation.play()
    // TODO: Medal
  }

  weakCar () {
    let weakFrames = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 4, 4, 3, 3, 2, 2, 4, 4, 5, 5, 5, 5, 5]
    weakFrames = directorAnimation.offset(weakFrames, 33)
    const [key, weakFrameSprites] = directorAnimation.resolveDirectorFrames(this.game, this.dirResource, weakFrames)
    const weakAnimation = this.rope.animations.add('weak', weakFrameSprites, 12)

    console.log('Engine too weak')
    this.rope.animations.play('weak', 12, true)
    this.game.mulle.playAudio('82e001v0', () => {
      console.log('Audio finished, stop animation')
      this.rope.animations.stop('weak', true)
      this.game.mulle.playAudio('82d003v0', () => {
        this.game.state.start('world')
      })
    })

  }

  create () {
    super.create()
    this.game.mulle.addAudio('mudcar')
    this.car = null

    this.background_layer = this.game.add.group()
    this.car_layer = this.game.add.group()

    const background = DirectorHelper.sprite(this.game, 0, 0, this.dirResource, 1)
    this.background_layer.add(background)

    this.stuckCar = DirectorHelper.sprite(this.game, 389, 279, this.dirResource, 43, true)
    this.car_layer.add(this.stuckCar)

    this.rope = DirectorHelper.sprite(this.game, 3, 291, this.dirResource, 34, false)
    this.car_layer.add(this.rope)

    this.driverAnimation()
  }

  exit() {
    this.game.state.start('world')
  }
}

export default MudCarState