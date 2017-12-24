"use strict"
const Zet = require('./zet')
const Serialization = require('./serialization')
const StorageToken = require('./storage_token')
const Serializable = Serialization.Serializable;

let TestClass = Zet.declare({
    superclass: Serialization.Serializable,
    CLASS_ID: 'TestClass',
    defineBody: function (self) {
        self.construct = function construct(value) {
            self.inherited(construct)
            self._value = value
        }
        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._value = token.getitem('value')
        }
        self.saveToToken = function saveToToken() {
            let token = self.inherited(saveToToken)
            token.setitem('value', self._value)
            return token
        }
    }
})

let TestClass2 = Zet.declare({
    superclass: Serialization.Serializable,
    CLASS_ID: 'TestClass2',
    defineBody: function (self) {
        self.construct = function construct(statement) {
            self.inherited(construct)
            self._statement = statement
        }
        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._statement = token.getitem('statement')
        }
        self.saveToToken = function saveToToken() {
            let token = self.inherited(saveToToken)
            token.setitem('statement', self._statement)
            return token
        }
    }
})


var serializableObj = Serialization.Serializable()
var aTestObj = TestClass(10)
var aTestObj2 = TestClass2("AAA")
var aTestObjNull = TestClass(null)
var aTestObjUndef = TestClass(undefined)

var st = serializableObj.saveToToken()
var t1 = aTestObj.saveToToken()
var t2 = aTestObj2.saveToToken()
var rSerializableObj = Serialization.createFromToken(st)
var rTestObj = Serialization.createFromToken(t1)
var rTestObj2 = Serialization.createFromToken(t2)

describe("Test", () => {
    it("Unit tests", () => {
        expect(t1._data.value).to.equal(10)
        expect(t1.getitem('value')).to.equal(10)
        expect(Serialization.makeSerialized(st)).to.not.be.empty
        expect(Serialization.makeSerialized(t1)).to.not.be.empty
        expect(Serialization.makeSerialized(t2)).to.not.be.empty
        expect(Serialization.makeSerialized(aTestObjNull.saveToToken())).to.not.be.empty
        expect(Serialization.makeSerialized(aTestObjUndef.saveToToken())).to.not.be.empty
        expect(StorageToken.isInstance(st)).to.be.true
        expect(StorageToken.isInstance(t1)).to.be.true
        expect(StorageToken.isInstance(t2)).to.be.true
    })
    it("CLASS_ID", () => {
        expect(rSerializableObj.CLASS_ID).to.equal("Serializable")
        expect(rTestObj.CLASS_ID).to.equal("TestClass")
        expect(rTestObj2.CLASS_ID).to.equal("TestClass2")
    })
    it("Object Equals", () => {
        expect(serializableObj.eq(rSerializableObj)).to.be.true
        expect(aTestObj.eq(rTestObj)).to.be.true
        expect(aTestObj2.eq(rTestObj2)).to.be.true
        expect(rTestObj2.eq(rTestObj)).to.be.false
    })
})

describe("Test 2", () => {
    //1. Object -> Token -> Serializable String
    let obj1 = new Serializable();
    let token1 = Serialization.tokenizeObject(obj1);
    token1._data["name"] = "LIDA";
    token1._data["version"] = "1.2.0";
    token1._data["status"] = "test";
    let str1 = Serialization.makeSerialized(token1);

    //2. Serializable String -> Token -> Object
    let token2 = Serialization.makeNative(str1);
    let obj2 = Serialization.untokenizeObject(token2);
    it("Token Equals", () => {
        expect(token1.eq(token2)).to.be.true
    })
    it("Object Equals", () => {
        expect(obj1.eq(obj2)).to.be.true
    })
})