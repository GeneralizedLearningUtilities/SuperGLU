"use strict"
const Zet = require('./zet')
// Zet.profile({
//     scope : exports
// });

var ZetTestClass = Zet.declare({
    // superclass : null,
    defineBody: function (self) {
        // Constructor Function
        self.construct = function construct(id) {
            self.id = id
        }
    }
})
var ZetTestClass2 = Zet.declare({
    superclass : null,
    CLASS_ID: "ZetTestClass2_OVERRIDE",
    defineBody: function (self) {
        // Constructor Function
        self.construct = function construct(id) {
            self.myId = id
        }
    }
})
var ZetTestClass3 = Zet.declare({
    superclass: ZetTestClass2,
    defineBody: function (self) {
    }
})

describe('ZetTests', () => {
    it('testIsInstance', () => {
        let x = ZetTestClass(1)
        let y = ZetTestClass2(2)
        let z = ZetTestClass3(3)
        expect(ZetTestClass.isInstance(x)).to.be.true
        expect(ZetTestClass.isInstance(y)).to.be.false
        expect(ZetTestClass.isInstance(z)).to.be.false
        expect(ZetTestClass.isInstance(1)).to.be.false
        expect(x.isInstance(x)).to.be.true
        expect(x.isInstance(y)).to.be.false
        expect(x.isInstance(1)).to.be.false

        // Check Y (Class 2)
        expect(ZetTestClass2.isInstance(x)).to.be.false
        expect(ZetTestClass2.isInstance(y)).to.be.true
        expect(ZetTestClass2.isInstance(z)).to.be.true
        expect(ZetTestClass2.isInstance(1)).to.be.false
        expect(y.isInstance(x)).to.be.false
        expect(y.isInstance(y)).to.be.true
        expect(y.isInstance(z)).to.be.true
        expect(y.isInstance(1)).to.be.false


        // Check Z (Class 3)
        expect(ZetTestClass3.isInstance(x)).to.be.false
        expect(ZetTestClass3.isInstance(y)).to.be.false
        expect(ZetTestClass3.isInstance(z)).to.be.true
        expect(ZetTestClass3.isInstance(1)).to.be.false
        expect(z.isInstance(x)).to.be.false
        expect(z.isInstance(y)).to.be.false
        expect(z.isInstance(z)).to.be.true
        expect(z.isInstance(1)).to.be.false
    })

    it("testInstanceOf", () => {
        let x = ZetTestClass(1),
            y = ZetTestClass2(2),
            z = ZetTestClass3(3)

        expect(x.instanceOf(ZetTestClass)).to.be.true
        expect(x.instanceOf(ZetTestClass2)).to.be.false
        expect(x.instanceOf(ZetTestClass3)).to.be.false

        expect(y.instanceOf(ZetTestClass)).to.be.false
        expect(y.instanceOf(ZetTestClass2)).to.be.true
        expect(y.instanceOf(ZetTestClass3)).to.be.false

        expect(z.instanceOf(ZetTestClass)).to.be.false
        expect(z.instanceOf(ZetTestClass2)).to.be.true
        expect(z.instanceOf(ZetTestClass3)).to.be.true
    })

    it('testCLASS_ID', () => {
        let x = ZetTestClass(1),
            y = ZetTestClass2(2),
            z = ZetTestClass3(3)

        expect(x.CLASS_ID === null).to.be.true
        expect(ZetTestClass.CLASS_ID === null).to.be.true
        expect(y.CLASS_ID === 'ZetTestClass2_OVERRIDE').to.be.true
        expect(ZetTestClass2.CLASS_ID === 'ZetTestClass2_OVERRIDE').to.be.true
        expect(z.CLASS_ID === null).to.be.true
        expect(ZetTestClass3.CLASS_ID === null).to.be.true
    })
})
