'use strict'

var DATA_TYPE_MEDIA, DATA_TYPE_DB

DATA_TYPE_DB = 0
DATA_TYPE_MEDIA = 1

const Messaging_Gateway = require('../../core/messaging-gateway'),
    Messaging = require('../../core/messaging'),
    Message = require('../../core/message'),
    Zet = require('../../util/zet')

// NOTE: When calling this, pass in a when.js deferred.resolve function as a callback
var StorageServiceInterface = Zet.declare({
    CLASS_ID: 'StorageServiceInterface',
    // JS client interface for the storage service
    superclass: Messaging_Gateway.BaseService,
    defineBody: function (self) {
        // Private Properties
        var BUCKET_KEY, NAME_KEY, DESCRIPTION_KEY, TAGS_KEY, TYPE_KEY,
            DATA_TYPE_KEY, ALLOW_CREATE_KEY,
            HAS_ELEMENT_VERB, CONTAINS_VERB,
            VALUE_VERB, ASSIGNED_TAGS, ASSIGNED_URI_VERB, VOID_VERB,
            STORAGE_SERVICE_NAME
        BUCKET_KEY = "bucket"
        NAME_KEY = "name"
        DESCRIPTION_KEY = "description"
        TAGS_KEY = "tags"
        TYPE_KEY = "type"
        DATA_TYPE_KEY = "dataType"
        ALLOW_CREATE_KEY = "allowCreate"

        HAS_ELEMENT_VERB = "HasElement"
        CONTAINS_VERB = "Contains"
        VALUE_VERB = "Value"
        ASSIGNED_TAGS = "AssignedTags"
        ASSIGNED_URI_VERB = "AssignedURI"
        VOID_VERB = "Void"

        STORAGE_SERVICE_NAME = "StorageService"

        // Public Properties
        self.construct = function construct(gateway, defaultBucketName, id) {
            self.inherited(construct, [id, gateway])
            if (typeof defaultBucketName === "undefined") {
                defaultBucketName = null
            }
            self._defaultBucketName = defaultBucketName
        }

        self.hasDataKey = function hasDataKey(callback, key, tags, type, name, bucketName) {
            var context = self.makeMessageContext(bucketName, tags, type, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackHasDataKeyResponse),
                Messaging.REQUEST_ACT, HAS_ELEMENT_VERB, key, null, context)
        }

        self.getDataKeys = function getDataKeys(callback, tags, type, bucketName) {
            var context = self.makeMessageContext(bucketName, tags, type, null, null, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataKeysResponse),
                Messaging.REQUEST_ACT, CONTAINS_VERB, null, null, context)
        }

        self.getDataNames = function getDataNames(callback, tags, type, bucketName) {
            var context = self.makeMessageContext(bucketName, tags, type, null, null, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataNamesResponse),
                Messaging.REQUEST_ACT, CONTAINS_VERB, null, null, context)
        }

        self.getDataIdByName = function getDataIdByName(callback, name, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataKeyResponse),
                Messaging.REQUEST_ACT, Messaging.INFORM_REF_ACT, null, null, context)
        }

        self.getDataName = function getDataName(callback, key, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, null, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataNameResponse),
                Messaging.REQUEST_ACT, Messaging.INFORM_REF_ACT, key, null, context)
        }

        self.renameData = function renameData(callback, key, name, newName, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackRenameDataResponse),
                Messaging.INFORM_REF_ACT, HAS_ELEMENT_VERB, key, newName, context)
        }

        self.getDataValue = function getDataValue(callback, key, name, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataValueResponse),
                Messaging.REQUEST_ACT, VALUE_VERB, key, null, context)
        }

        self.getDataValues = function getDataValues(callback, keys, bucketName) {
            var i = 0,
                data = {},
                count = 0,
                length = keys.length,
                context = self.makeMessageContext(bucketName, null, null, null, null, null, null),
                // Track receipt of each value in a mapping
                onReceiveVal = function (msg, oldMsg) {
                    var key = msg.getObject(),
                        val = msg.getResult()
                    if (val != null) {
                        data[key] = val
                    }
                    count += 1
                    if (count >= length) {
                        callback(data)
                    }
                }
            // Dispatch all the read requests
            for (i = 0; i < keys.length; i++) {
                self.sendRequest(onReceiveVal, Messaging.REQUEST_ACT, VALUE_VERB, keys[i], null, context)
            }
        }

        self.getDataTags = function getDataTags(callback, key, name, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataTagsResponse),
                Messaging.REQUEST_ACT, ASSIGNED_TAGS, key, null, context)
        }

        self.getDataLink = function getDataLink(callback, key, name, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackGetDataLinkResponse),
                Messaging.REQUEST_ACT, ASSIGNED_URI_VERB, key, null, context)
        }

        self.addDataValue = function addDataValue(callback, key, data, tags, type, name, description, dataType, bucketName) {
            this.setDataValue(callback, key, data, tags, type, true, name, description, bucketName, dataType)
        }

        self.setDataValue = function setDataValue(callback, key, data, tags, type, allowCreate, name, description, dataType, bucketName) {
            var context = self.makeMessageContext(bucketName, tags, type, allowCreate, name, description, dataType)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackSetDataValueResponse),
                Messaging.INFORM_ACT, VALUE_VERB, key, data, context)
        }

        self.delDataValue = function delDataValue(callback, key, name, bucketName) {
            var context = self.makeMessageContext(bucketName, null, null, null, name, null, null)
            self.sendRequest(self.makeResponseCallback(callback, self.unpackDelDataValueResponse),
                Messaging.INFORM_ACT, VOID_VERB, key, null, context)
        }

        //  Messaging and Callback Creation
        self.sendRequest = function sendRequest(callback, speechAct, verb, key, result, context) {
            var msg = Message(STORAGE_SERVICE_NAME, verb, key, result, speechAct, context)
            msg.updateTimestamp()
            self._makeRequest(msg, callback)
        }

        // Message Builders
        self.makeMessageContext = function makeMessageContext(bucket, tags, type, allowCreate, name, description, dataType) {
            var context = {}
            if (bucket == null) {
                bucket = self._defaultBucketName
            }
            context = {}
            context[BUCKET_KEY] = bucket
            if (type != null) {
                context[TYPE_KEY] = type
            }
            if (tags != null) {
                context[TAGS_KEY] = tags
            }
            if (allowCreate != null) {
                context[ALLOW_CREATE_KEY] = allowCreate
            }
            if (name != null) {
                context[NAME_KEY] = name
            }
            if (description != null) {
                context[DESCRIPTION_KEY] = description
            }
            if (dataType != null) {
                context[DATA_TYPE_KEY] = dataType
            }
            return context
        }

        self.makeResponseCallback = function makeResponseCallback(callback, unpacker) {
            if (callback == null) {
                return null
            } else {
                return function (msg, oldMsg) {
                    callback(unpacker(msg))
                }
            }
        }

        // Message Result Unpacking
        self.unpackHasDataKeyResponse = function unpackHasDataKeyResponse(msg) {
            return msg.getResult()
        }

        self.unpackGetDataKeyResponse = function unpackGetDataKeyResponse(msg) {
            return msg.getObject()
        }

        self.unpackGetDataKeysResponse = function unpackGetDataKeysResponse(msg) {
            return msg.getResult()
        }

        self.unpackGetDataNamesResponse = function unpackGetDataNamesResponse(msg) {
            return msg.getContextValue(NAME_KEY, [])
        }

        self.unpackGetDataNameResponse = function unpackGetDataNameResponse(msg) {
            return msg.getResult()
        }

        self.unpackRenameDataResponse = function unpackRenameDataResponse(msg) {
            return (msg.getSpeechAct() === Messaging.CONFIRM_ACT)
        }

        self.unpackGetDataValueResponse = function unpackGetDataValueResponse(msg) {
            return msg.getResult()
        }

        self.unpackGetDataTagsResponse = function unpackGetDataTagsResponse(msg) {
            return msg.getResult()
        }

        self.unpackGetDataLinkResponse = function unpackGetDataLinkResponse(msg) {
            return msg.getResult()
        }

        self.unpackAddDataValueResponse = function unpackAddDataValueResponse(msg) {
            return (msg.getSpeechAct() === Messaging.CONFIRM_ACT)
        }

        self.unpackSetDataValueResponse = function unpackSetDataValueResponse(msg) {
            return (msg.getSpeechAct() === Messaging.CONFIRM_ACT)
        }

        self.unpackDelDataValueResponse = function unpackDelDataValueResponse(msg) {
            return (msg.getSpeechAct() === Messaging.CONFIRM_ACT)
        }
    }
})

// namespace.StorageServiceInterface = StorageServiceInterface;
// })(window.Storage_Service_Client = window.Storage_Service_Client || {});
module.exports = StorageServiceInterface