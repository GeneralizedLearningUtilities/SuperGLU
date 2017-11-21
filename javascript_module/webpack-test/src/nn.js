// var SerializableAll = require('./util/serializable-all')
// const Zet = require('./util/zet')

class Animal {
    static staticMethod() {
        return "staticMethod"
    }

    constructor() {
        this.legs = 4
    }

    toString() {
        return this.legs
    }

    is4Legged() {
        return this.legs === 4
    }
}

class Cow extends Animal {
    constructor() {
        super()
        this.color = 'white'
    }

    getLegs() {
        return this.legs
    }

    getColor() {
        return this.color
    }

    toString() {
        return super.toString() + " " + this.color
    }
}

console.log("Loaded nn.js module with 2 classes")


export {Animal, Cow}

