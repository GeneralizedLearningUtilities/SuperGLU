var TIMEOUT_PERIOD = 25;

buster.testCase("LocalStorageServiceTests", {
    setUp: function (){
        var bucket;
        this.dbType = 0;
        this.mediaType = 1;
        this.dataLink = "www.x-in-y.com";   // Default link for now
        this.bucketName = "ONR";
        this.client = Storage_Service_Client.StorageServiceInterface(null, this.bucketName);
        this.storage = Local_Storage_Service.LocalStorageService("StorageService", null);
        this.storage.addBucket(this.bucketName);
        this.gateway = Client_Messaging_Gateway.MessagingGateway("ProcessGateway", [this.client, this.storage]);
        // Populate some storage values
        bucket = this.storage._getBucket(this.bucketName);
        this.keyExists = "Mad Max";
        this.keyExistsName = this.keyExists + "_NAME";
        this.keyExistsVal = "Mel Gibson";
        this.mediaKeyExists = "IMDB";
        this.tag1 = "Cop";
        this.tag2 = "Movie";
        bucket.setValue(this.keyExists, this.keyExistsVal, this.keyExistsName, "Guy in a leather jacket", [this.tag1, this.tag2], this.dbType);
        bucket.setValue(this.mediaKeyExists, "www.imdb.com", this.mediaKeyExists, "", [this.tag2], this.mediaType);
        bucket.setValue("Pallindrome", "Emordnillap", null, "", null, this.dbType);
        this.keyMissing = "Missing";
        this.keys = [this.keyExists, "IMDB", "Pallindrome"];
        this.tags1 = [this.keyExists];
        this.tags2 = [this.keyExists, "IMDB"];
    },
    "testIsTrue": function () {
        buster.assert(true);
    },
    "testAddData": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.addDataValue(callback, "Big", "Ben");
        setTimeout(function() {
            buster.assert(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testSetData": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.setDataValue(callback, "Big", "Ben");
        setTimeout(function() {
            buster.assert(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetData": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.setDataValue(null, "Big", "Ben");
        this.client.getDataValue(callback, "Big");
        setTimeout(function() {
            buster.assert.equals(result, "Ben");
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetData_Exists": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = this.keyExistsVal;
        this.client.getDataValue(callback, this.keyExists);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetData_Missing": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.getDataValue(callback, this.keyMissing);
        setTimeout(function() {
            buster.assert.equals(result, undefined);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testDelData_Exists": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.delDataValue(callback, this.keyExists);
        setTimeout(function() {
            buster.assert(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testDelData_Missing": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.delDataValue(callback, this.keyMissing);
        setTimeout(function() {
            buster.refute(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testHasDataKey_True": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.hasDataKey(callback, this.keyExists);
        setTimeout(function() {
            buster.assert(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testHasDataKey_False": function (done) {
        var result, callback;
        callback = function (val) {
            result = val;
            };
        this.client.hasDataKey(callback, this.keyMissing);
        setTimeout(function() {
            buster.refute(result);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataKeys": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = this.keys;
        this.client.getDataKeys(callback);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataKeys_Tags1": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = this.tags1;
        this.client.getDataKeys(callback, [this.tag1]);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataKeys_Tags2": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = this.tags2;
        this.client.getDataKeys(callback, [this.tag2]);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataKeys_Tags2_DB": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = [this.keyExists];
        this.client.getDataKeys(callback, [this.tag2], this.dbType);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataKeys_Tags2_Media": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = [this.mediaKeyExists];
        this.client.getDataKeys(callback, [this.tag2], this.mediaType);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataLink": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = this.dataLink;
        this.client.getDataLink(callback, this.mediaKeyExists);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataLink_NonMedia": function (done) {
        var result, callback, expectedResult;
        callback = function (val) {
            result = val;
            };
        expectedResult = null;
        this.client.getDataLink(callback, this.keyExists);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testGetDataName": function (done) {
        var result, callback, expectedResult;
        expectedResult = this.keyExistsName;
        callback = function (val) {
            result = val;
            };
        this.client.getDataName(callback, this.keyExists);
        setTimeout(function() {
            buster.assert.equals(result, expectedResult);
            done();
            }, TIMEOUT_PERIOD);
    },
    "testRename": function (done) {
        var client, key, result, callback, expectedResult;
        key = this.keyExists;
        expectedResult = "SomeNewName";
        callback = function (val) {
            result = val;
            };

        this.client.renameData(callback, key, null, expectedResult);
        client = this.client;
        setTimeout(function() {
            var callback2, newName;
            callback2 = function (val) {
                newName = val;
            };
            buster.assert(result);
            client.getDataName(callback2, key);
            setTimeout(function() {
                buster.assert.equals(newName, expectedResult);
                done();
                }, TIMEOUT_PERIOD*2);
            }, TIMEOUT_PERIOD);
    }
});