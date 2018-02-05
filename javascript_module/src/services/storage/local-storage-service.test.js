'use strict'
const StorageServiceInterface = require('./storage-service-client')
    , LocalStorageService = require('./local-storage-service')
    , Messaging_Gateway = require('../../core/messaging-gateway')

var bucket
var TIMEOUT_PERIOD = 25
var dbType = 0
var mediaType = 1
var dataLink = "www.x-in-y.com"   // Default link for now
var bucketName = "ONR"
var client = StorageServiceInterface(null, bucketName)
var storage = LocalStorageService("StorageService", null)
var keyExists = "Mad Max"
var keyExistsName = keyExists + "_NAME"
var keyExistsVal = "Mel Gibson"
var mediaKeyExists = "IMDB"
var tag1 = "Cop"
var tag2 = "Movie"
var keyMissing = "Missing"
var keys = [keyExists, "IMDB", "Pallindrome"]
var tags1 = [keyExists]
var tags2 = [keyExists, "IMDB"]
Messaging_Gateway.MessagingGateway("ProcessGateway", [client, storage])

describe("Local Storage Unit Tests", function () {
    beforeEach(function () {
        storage.addBucket(bucketName)
        bucket = storage._getBucket(bucketName)
        bucket.setValue(keyExists, keyExistsVal, keyExistsName, "Guy in a leather jacket", [tag1, tag2], dbType)
        bucket.setValue(mediaKeyExists, "www.imdb.com", mediaKeyExists, "", [tag2], mediaType)
        bucket.setValue("Pallindrome", "Emordnillap", null, "", null, dbType)
    })

    afterEach(function () {
        storage.delBucket(bucketName)
    })

    it("Add Data", function (done) {
        this.timeout(TIMEOUT_PERIOD * 2)
        var result, callback
        callback = function (val) {
            result = val
        }
        client.addDataValue(callback, "Big", "Ben")
        setTimeout(function () {
            expect(result).to.be.ok        //truthy value
            done()
        }, TIMEOUT_PERIOD)
    })
    it("Test Set Data", function (done) {
        var result, callback
        callback = function (val) {
            result = val
        }
        client.setDataValue(callback, "Big", "Ben")
        setTimeout(function () {
            expect(result).to.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it("Test Get Data", function (done) {

        var result, callback
        callback = function (val) {
            result = val
        }
        client.setDataValue(null, "Big", "Ben")
        client.getDataValue(callback, "Big")
        setTimeout(function () {
            expect(result === "Ben").to.be.true
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testGetData_Exists", function (done) {

        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = keyExistsVal
        client.getDataValue(callback, keyExists)
        setTimeout(function () {
            expect(result === expectedResult).to.be.true
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testGetData_Missing", function (done) {

        var result, callback
        callback = function (val) {
            result = val
        }
        client.getDataValue(callback, keyMissing)
        setTimeout(function () {
            expect(result).to.not.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testDelData_Exists", function (done) {

        var result, callback
        callback = function (val) {
            result = val
        }
        client.delDataValue(callback, keyExists)
        setTimeout(function () {
            expect(result).to.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testDelData_Missing", function (done) {

        var result, callback
        callback = function (val) {
            result = val
        }
        client.delDataValue(callback, keyMissing)
        setTimeout(function () {
            expect(result).to.not.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testHasDataKey_True", function (done) {

        var result, callback
        callback = function (val) {
            result = val
        }
        client.hasDataKey(callback, keyExists)
        setTimeout(function () {
            expect(result).to.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testHasDataKey_False", function (done) {
        var result, callback
        callback = function (val) {
            result = val
        }
        client.hasDataKey(callback, keyMissing)
        setTimeout(function () {
            expect(result).to.not.be.ok
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataKeys', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = keys
        client.getDataKeys(callback)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataKeys_Tags1', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = tags1
        client.getDataKeys(callback, [tag1])
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it("testGetDataKeys_Tags2", function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = tags2
        client.getDataKeys(callback, [tag2])
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataKeys_Tags2_DB', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = [keyExists]
        client.getDataKeys(callback, [tag2], dbType)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataKeys_Tags2_Media', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = [mediaKeyExists]
        client.getDataKeys(callback, [tag2], mediaType)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataLink', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = dataLink
        client.getDataLink(callback, mediaKeyExists)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataLink_NonMedia', function (done) {
        var result, callback, expectedResult
        callback = function (val) {
            result = val
        }
        expectedResult = null
        client.getDataLink(callback, keyExists)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testGetDataName', function (done) {
        var result, callback, expectedResult
        expectedResult = keyExistsName
        callback = function (val) {
            result = val
        }
        client.getDataName(callback, keyExists)
        setTimeout(function () {
            expect(result).to.eql(expectedResult)
            done()
        }, TIMEOUT_PERIOD)
    })
    it('testRename', function (done) {
        var key, result, callback, expectedResult
        key = keyExists
        expectedResult = "SomeNewName"
        callback = function (val) {
            result = val
        }
        client.renameData(callback, key, null, expectedResult)
        setTimeout(function () {
            var callback2, newName
            callback2 = function (val) {
                newName = val
            }
            expect(result).to.be.ok
            client.getDataName(callback2, key)
            setTimeout(function () {
                expect(newName).to.eql(expectedResult)
                done()
            }, TIMEOUT_PERIOD * 2)
        }, TIMEOUT_PERIOD)
    })
})