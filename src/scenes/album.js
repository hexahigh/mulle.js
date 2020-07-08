/* global Phaser */
import MulleState from 'scenes/base'

import MulleSprite from 'objects/sprite'
import MulleBuildCar from 'objects/buildcar'
import MulleButton from 'objects/button'

/**
 * Album UI
 */
class AlbumState extends MulleState {
  /**
   * Create a sprite with director position
   * @param {string} dir Director movie
   * @param {string|int} num Director number or name
   * @returns {Phaser.Sprite}
   */
  positionSprite (dir, num) {
    const image = this.game.mulle.getDirectorImage(dir, num)
    const x = 320 - image.frame.regpoint.x
    const y = 240 - image.frame.regpoint.y
    return new Phaser.Sprite(this.game, x, y, image.key, image.name)
  }

  init (mode) {
    this.mode = mode
  }

  preload () {
    this.DirResource = '06.DXR'
    super.preload()
    this.game.load.pack('album', 'assets/album.json', null, this)
    if (!this.game.mulle.user.savedCars) {
      this.game.mulle.user.savedCars = []
    }
  }

  buildPages () {
    let pageNumSprite
    this.savedCars = this.game.mulle.user.savedCars

    for (let page = 1; page <= 12; page++) {
      if (page in this.savedCars) { // Is a car saved on this page?
        pageNumSprite = this.positionSprite(this.DirResource, page + 60)
      } else {
        pageNumSprite = this.positionSprite(this.DirResource, page + 48)
      }

      if (page === this.selectedPage) {
        if (this.pagenumSpriteSelected) {
          this.pagenumSpriteSelected.destroy()
        }

        this.pagenumSpriteSelected = this.positionSprite(this.DirResource, page + 72)
        this.game.add.existing(this.pagenumSpriteSelected)
        if (this.fetchButton) {
          this.fetchButton.displaySprite.visible = page in this.savedCars
          this.fetchButton.visible = page in this.savedCars
        }
      } else {
        const button = MulleButton.fromRectangle(this.game, pageNumSprite.x, pageNumSprite.y, 40, 40, {
          click: () => {
            this.setPage(page)
          }
        })

        this.game.add.existing(button)
      }

      this.game.add.existing(pageNumSprite)
    }
  }

  /**
   * Select album page
   * @param page
   */
  setPage (page) {
    this.selectedPage = page
    this.game.mulle.playAudio('06e003v0')
    this.showSavedCar(page)
    this.buildPages()
  }

  /**
   * Show a car in the album
   */
  albumCar (parts = null) {
    if (this.albumCarImage) {
      this.albumCarImage.destroy()
    }

    this.albumCarImage = new MulleBuildCar(this.game, 320, 240, parts, true, false)
    this.game.add.existing(this.albumCarImage)
  }

  /**
   * Picture in the left corner ready for pasting
   */
  showPasteFrame () {
    this.imageFrame = new MulleButton(this.game, 67, 401, {
      imageDefault: [this.DirResource, 159],
      click: () => { this.pasteCar() }
    })

    this.game.add.existing(this.imageFrame)

    this.pasting_car = new MulleBuildCar(this.game, 0, 400, null, true, false)
    this.pasting_car.height = this.pasting_car.height / 2
    this.pasting_car.width = this.pasting_car.width / 2
    this.game.add.existing(this.pasting_car)
  }

  /**
   * Paste a car in the album
   */
  pasteCar () {
    this.imageFrame.destroy()
    this.imageFrame.displaySprite.visible = false
    this.pasting_car.destroy()
    this.albumCar()

    this.saveCar(this.selectedPage, this.game.mulle.user.Car.Parts)
  }

  /**
   * Save a car
   * @param {int} page Album page
   * @param {array} parts
   */
  saveCar (page, parts) {
    console.log(`Save car to page ${page}`)
    this.game.mulle.user.savedCars[page] = parts
    this.game.mulle.user.save()
  }

  /**
   * Build the saved car
   * @param {int} page Album page
   */
  buildSavedCar (page) {
    let partId
    const parts = this.game.mulle.user.savedCars[page]
    // Place redundant parts in the junk yard
    for (partId of this.game.mulle.user.Car.Parts) {
      if (!(partId in parts)) {
        if (this.game.mulle.PartsDB[partId].master) { // Un-morph parts
          partId = this.game.mulle.PartsDB[partId].master
        }

        // Place the part in the junk yard
        this.game.mulle.user.addPart('Pile1', partId, null, true)
      }
    }

    this.removeParts(parts) // Remove the parts from wherever they are
    this.game.mulle.user.Car.Parts = parts
    this.close()
  }

  /**
   * Show the saved car in the album
   * @param {int} page Album page
   */
  showSavedCar (page) {
    this.parts = this.game.mulle.user.savedCars[page]
    if (!this.parts && this.albumCarImage) {
      this.albumCarImage.destroy()
    } else {
      this.albumCar(this.parts)
    }
  }

  /**
   * Remove a part from junk piles, shop floor and yard
   * @param {int} partId Part id
   */
  removePart (partId) {
    if (this.game.mulle.PartsDB[partId].master) { // Un-morph parts
      partId = this.game.mulle.PartsDB[partId].master
    }

    for (const pile in this.game.mulle.user.Junk) {
      if (partId in this.game.mulle.user.Junk[pile]) {
        console.log(`Remove part ${partId} from ${pile}`)
        delete this.game.mulle.user.Junk[pile][partId]
      }
    }
  }

  /**
   * Remove multiple parts from junk piles, shop floor and yard
   * @param {array} parts Array with part ids
   */
  removeParts (parts) {
    for (const part of parts) {
      this.removePart(part)
    }
  }

  importCar () {
    console.warn('Not implemented')
  }

  create () {
    this.game.mulle.addAudio('album')
    super.create()

    this.background = new MulleSprite(this.game, 320, 240)
    this.background.setDirectorMember(this.DirResource, 93)
    this.game.add.existing(this.background)

    if (this.mode === 'save') {
      this.game.mulle.playAudio('06e002v0', () => {
        this.game.mulle.playAudio('06d001v0')
      })

      this.showPasteFrame()

      const { key, frame } = this.game.mulle.getDirectorImage(this.DirResource, 101)
      this.name_input = new Phaser.Sprite(this.game, 215, 434, key, frame.name)
      this.game.add.existing(this.name_input)

      this.export_button = new MulleButton(this.game, 487, 413, {
        imageDefault: ['06.DXR', 164],
        click: () => {
          console.warn('Export car not implemented')
        }
      })

      this.game.add.existing(this.export_button)
    } else { // Show picture
      this.game.mulle.playAudio('07d001v0')

      this.fetchButton = new MulleButton(this.game, 76, 400, {
        imageDefault: [this.DirResource, 162],
        click: () => {
          this.buildSavedCar(this.selectedPage)
        }
      })

      this.game.add.existing(this.fetchButton)

      this.importButton = new MulleButton(this.game, 487, 413, {
        imageDefault: ['06.DXR', 161],
        click: () => {
          this.importCar()
        }
      })
      this.game.add.existing(this.importButton)
    }

    this.close_button = new MulleButton(this.game, 554, 414, {
      imageDefault: ['06.DXR', 153],
      click: () => {
        console.log('Close album')
        this.close()
      }
    })

    this.game.add.existing(this.close_button)
    this.setPage(1)
  }

  close () {
    this.game.state.start('garage')
  }

  shutdown (game) {
    this.cutscene = 83
    super.shutdown(game)
  }
}

export default AlbumState
