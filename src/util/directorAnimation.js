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
    const DirectorFrames = []
    let key, frame
    for (const frameName of frames) {
      if (frameName === 'Dummy')
        continue
      [key, frame] = DirectorHelper.getDirectorImage(game, movie, frameName)
      DirectorFrames.push(frame.name)
    }

    return [key, DirectorFrames]
  }

}

export default directorAnimation