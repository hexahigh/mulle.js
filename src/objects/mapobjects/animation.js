import DirectorHelper from '../DirectorHelper'

class ObjectAnimation {
  /**
   *
   * @param {Phaser.Sprite} sprite
   * @param {string} movie Director movie
   */
  constructor (sprite, movie) {
    this.sprite = sprite
    this.game = sprite.game
    this.movie = movie
  }

  /**
   * Load animations from a FrameList
   * @param {object} FrameList
   * @returns {(*|{})[]}
   */
  load (FrameList) {
    const animations = {}
    let frame
    let key

    if (FrameList[1] === undefined) {
      const FrameListTemp = {}
      FrameListTemp[1] = FrameList
      FrameList = FrameListTemp
    }

    console.log(FrameList)
    console.log(Object.keys(FrameList))

    for (const direction of Object.keys(FrameList)) {
      console.log('Direction', direction)
      animations[direction] = {}
      for (const animation of Object.keys(FrameList[direction])) {
        console.log(animation)
        animations[direction][animation] = []
        for (const frameName of FrameList[direction][animation]) {
          if (frameName === 'Dummy') { continue }
          [key, frame] = DirectorHelper.getDirectorImage(this.game, this.movie, frameName)
          animations[direction][animation].push(frame.name)
        }
      }
    }
    this.sprite.loadTexture(key)
    this.animations = animations
    return animations
  }

  /**
   * Adds a new animation under the given key. Optionally set the frames, frame rate and loop. Animations added in this way are played back with the play function.
   * @param {string} name The unique (within this Sprite) name for the animation, i.e. "run", "fire", "walk".
   * @param {string} frameListName The name of the frame list to use
   * @param {int} direction Direction of the object
   * @param {int} frameRate The speed at which the animation should play. The speed is given in frames per second. - Default: 60
   * @param {boolean} loop Whether or not the animation is looped or just plays once.
   * @param {boolean} reverse Play animation in reverse to return to initial position
   * @returns {Phaser.Animation} The Animation object that was created.
   */
  add (name, frameListName, direction = 1, frameRate = 12, loop = false, reverse = false) {
    if (this.animations[direction][frameListName] === undefined) {
      console.error(`Invalid frameList: ${frameListName}`)
    }
    let frames
    if (reverse) {
      const framesForward = this.animations[direction][frameListName]
      const framesReverse = [...this.animations[direction][frameListName]].reverse()
      frames = framesReverse.concat(framesForward)
    } else {
      frames = this.animations[direction][frameListName]
    }

    console.log('Frames', frames)
    return this.sprite.animations.add(name, frames, frameRate, loop)
  }

  static (frameListName, direction = 1) {
    this.sprite.loadTexture(this.sprite.key, this.animations[direction][frameListName][0])
  }
}

export default ObjectAnimation
