"use strict"
const chai = require('chai')
const expect = chai.expect
import {Animal, Cow} from './nn'

describe("Testing subclassing with parent constructor invocation", () => {
    let a = new Animal()
    let c = new Cow()

    it("Animal Instance Test", () => {
        expect(a).is.not.empty
        expect(a instanceof Animal).to.be.true
        expect(a instanceof Cow).to.be.false
        expect(a.toString()).to.equal(4)
        expect(Animal.staticMethod()).to.equal("staticMethod")
        expect(a.is4Legged()).to.be.true
    })

    it("Cow Instance Test", () => {
        expect(c instanceof Animal).to.be.true
        expect(c instanceof Cow).to.be.true
        expect(c.toString()).to.equal("4 white")
        expect(c.getLegs()).to.equal(4)
        expect(Cow.staticMethod()).to.equal("staticMethod")
        expect(c.is4Legged()).to.be.true
    })
})
