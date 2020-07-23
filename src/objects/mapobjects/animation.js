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
    FrameList = FrameList[1]
    let frame
    let key
    for (const animation of Object.keys(FrameList)) {
      console.log(animation)
      animations[animation] = []
      for (const frameName of FrameList[animation]) {
        [key, frame] = DirectorHelper.getDirectorImage(this.game, this.movie, frameName)
        animations[animation].push(frame.name)
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
   * @param {int} frameRate The speed at which the animation should play. The speed is given in frames per second. - Default: 60
   * @param {boolean} loop Whether or not the animation is looped or just plays once.
   * @returns {Phaser.Animation} The Animation object that was created.
   */
  add (name, frameListName, frameRate = 12, loop = false) {
    if (this.animations[frameListName] === undefined) {
      console.error(`Invalid frameList: ${frameListName}`)
    }
    return this.sprite.animations.add(name, this.animations[frameListName], frameRate, loop)
  }
}

export default ObjectAnimation
