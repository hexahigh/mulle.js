import DirectorHelper from '../objects/DirectorHelper'

class directorAnimation {
  /**
   *
   * @param {array} frames
   * @param {int|string} offset Offset number or frame name
   * @return {[]}
   */
  static offset(frames, offset) {
    const framesOffset = []
    if(typeof(offset)==='string') {
      DirectorHelper.getDirectorImage()
    }

    for(const frame of frames) {
      framesOffset.push(frame + offset)
    }
    return framesOffset
  }

  /**
   * Resolve a list of director frame numbers
   * @param {MulleGame|Phaser.Game} game
   * @param {string} movie
   * @param {array} frames
   * @return {array}
   */
  static resolveDirectorFrames (game, movie, frames) {
    if (!movie) {
      console.error('Movie not set')
      return []
    }

    const DirectorFrames = []
    const DirectorFramesObjects = []
    let key, frame
    for (const frameName of frames) {
      if (frameName === 'Dummy')
        continue
      [key, frame] = DirectorHelper.getDirectorImage(game, movie, frameName)
      DirectorFrames.push(frame.name)
      DirectorFramesObjects.push(frame)
    }

    return [key, DirectorFrames, DirectorFramesObjects]
  }

  /**
   * Offset and resolve frames from a director animation
   * @param {MulleGame|Phaser.Game} game
   * @param {string} movie Move file name
   * @param {int} firstFrame First frame number
   * @param {array} frames Frames relative to first frame
   * @return {array} Resolved frames
   */
  static createAnimation(game, movie, firstFrame, frames)
  {
    const offset_frames = directorAnimation.offset(frames, firstFrame - 1)
    return this.resolveDirectorFrames(game, movie, offset_frames)
  }
}

export default directorAnimation