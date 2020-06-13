'use strict'

const MapObject = {}

// End of the world/closed road
MapObject.onCreate = function () {
    let direction = this.opt['Direction'];
    this.setDirectorMember(this.def.FrameList[direction][0]);
    console.log(this.def.FrameList);
}

MapObject.onEnterInner = function (car) {
    car.speed = 0;
    car.stepback(2);

}

export default MapObject
