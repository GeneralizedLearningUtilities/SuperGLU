// Requires Util\Zet, SKO_Architecture\Messaging, SKO_Architecture\Client_Messaging_Gateway
if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

var BUCKET_KEY, NAME_KEY, DESCRIPTION_KEY, TAGS_KEY, 
    TYPE_KEY, ALLOW_CREATE_KEY, DATA_TYPE_KEY, 
    HAS_ELEMENT_VERB, CONTAINS_VERB, 
    VALUE_VERB, ASSIGNED_URI_VERB, VOID_VERB,
    STORAGE_ADAPTER_MONGODB, STORAGE_ADAPTER_S3,
    SERIALIZABLE_DATA_TYPE;
    
BUCKET_KEY = "bucket";
NAME_KEY = "name";
DESCRIPTION_KEY = "description";
TAGS_KEY = "tags";
TYPE_KEY = "type";
DATA_TYPE_KEY = "dataType";
ALLOW_CREATE_KEY = "allowCreate";

HAS_ELEMENT_VERB = "HasElement";
CONTAINS_VERB = "Contains";
VALUE_VERB = "Value";
ASSIGNED_URI_VERB = "AssignedURI";
VOID_VERB = "Void";

STORAGE_ADAPTER_MONGODB = 0;
STORAGE_ADAPTER_S3 = 1;

SERIALIZABLE_DATA_TYPE = 'Serializable';

Zet.declare('StorageBucket', {
    // Base class for messaging gateways
    superclass : Serialization.Serializable,
    defineBody : function(self){
        // Public Properties

        self.construct = function construct(name){
            self.inherited(construct);
            if (name == null){ name = "";}
            self._name = name;
            self._tagMaps = {};
            self._nameMap = {};
            self._adaptorMap = {};
            self._data = {};
        };
        
        self.getJSON = function getJSON(){
            var data = {};
            data.name = self._name;
            data.tagMaps = self._tagMaps;
            data.nameMap = self._nameMap;
            data.adaptorMap = self._adaptorMap;
            data.data = self._data;
            return data;
        };
        
        self.setJSON = function setJSON(data){
            self._name = data.name;
            self._tagMaps = data.tagMaps;
            self._nameMap = data.nameMap;
            self._adaptorMap = data.adaptorMap;
            self._data = data.data;
        };
        
        self.getBucketName = function getBucketName(){
            return self._name;
        };
        
        self.setBucketName = function setBucketName(name){
            if (typeof name == 'string' || name instanceof String){
                self._name = name;
            } else {
                throw TypeError("Name must be a string");
            }
        };
        
        self.getObjectTags = function getObjectTags(key, name){
            var tag, tags;
            key = self.resolveRef(key, name);
            tags = [];
            if (self.hasKey(key)) {
                for (tag in self._tagMaps) {
                    if (key in self._tagMaps[tag]) {
                        tags.push(tag);
                    }
                }
            }
            return tags;
        };
        
        self.getMatchingKeys = function getMatchingKeys(tags, storageType){
            var i, k, keys, keyDict;
            keys = [];
            keyDict = {};
            if (tags != null){
                for (i=0; i<tags.length; i++){
                    if (tags[i] in self._tagMaps){
                        for (k in self._tagMaps[tags[i]]){
                            if ((storageType == null) || 
                                (storageType === self._adaptorMap[k])){
                                keyDict[k] = true;
                            }
                        }
                    }
                }
                for (k in keyDict){
                    keys.push(k);
                }
            } else if (storageType != null){
                for (k in self._adaptorMap){
                    if (storageType === self._adaptorMap[k]){
                        keys.push(k);
                    }
                }
            } else {
                for (k in self._adaptorMap){
                    keys.push(k);
                }
            }
            return keys;
        };

        self.hasKey = function hasKey(key){
            return (key in self._adaptorMap);
        };
        
        self.hasName = function hasName(name){
            return (name in self._nameMap);
        };
        
        self.hasRef = function hasRef(key, name){
            return (self.resolveRef(key, name) != null);
        };
        
        self.resolveRef = function resolveRef(key, name){
            var ref = null;
            if (key != null || name != null){
                if ((name == null && self.hasKey(key)) || 
                    (name != null && self.getName(key) === name)){
                    ref = key;
                } else if (key == null && self.hasName(name)){
                    ref = self._nameMap[name];
                }
            }
            return ref;
        };

        self.hasTag = function hasTag(tag){
            return (tag in self._tagMaps);
        };

        self.hasTagKey = function hasTagKey(tag, key, name){
            key = self.resolveRef(key, name);
            if (self.hasTag(tag) && self.hasKey(key)) {
                return key in self._tagMaps[tag];
            }
            return false;
        };

        self.addTagKey = function addTagKey(tag, key, name){
            key = self.resolveRef(key, name);
            if (typeof tag == 'string' || tag instanceof String){
                if (!self.hasTag(tag)){
                    self._tagMaps[tag] = {};
                }
                self._tagMaps[tag][key] = true;
            }
        };
        
        self.changeTags = function changeTags(tags, key, name){
            var tag, oldTags, validTags;
            key = self.resolveRef(key, name);
            validTags = {};
            oldTags = self.getObjectTags(key);
            for (tag in oldTags){
                validTags[tag] = false;
            }
            // Add new tags
            for (tag in tags){
                self.addTagKey(tag, key);
                validTags[tag] = true;
            }
            // Remove ones not in the new set
            for (tag in validTags){
                if (validTags[tag] === false){
                    self.delTagKey(tag, key);
                }
            }
        };

        self.delTagKey = function delTagKey(tag, key, name){
            key = self.resolveRef(key, name);
            if (self.hasTagKey(tag, key)){
                delete self._tagMaps[tag][key];
            }
        };

        self.getStorageAdaptor = function getStorageAdaptor(key, name){
            key = self.resolveRef(key, name);
            if (self.hasKey(key)){
                return self._adaptorMap[key];
            } else {
                return null;
            }
        };

        self._getData = function _getData(key){
            var storageType;
            storageType = self.getStorageAdaptor(key);
            if (storageType != null){
                return self._data[key];
            } else {
                return undefined;
            }
        };
        
        self.getValue = function getValue(key, name){
            var data;
            key = self.resolveRef(key, name);
            data = self._getData(key);
            if (data != null){
                return data.value;
            } else {
                return undefined;
            }
        };
        
        self.getLink = function getLink(key, name){
            key = self.resolveRef(key, name);
            if (self.getStorageAdaptor(key) === STORAGE_ADAPTER_S3){
                return "www.x-in-y.com";
            } else {
                return null;
            }
        };
        
        self.getName = function getName(key){
            var data;
            data = self._getData(key);
            if (data != null){
                return data.name;
            } else {
                return undefined;
            }
        };
        
        self.changeName = function changeName(newName, key, name){
            var data, value;
            key = self.resolveRef(key, name);
            if ((key != null)  && (!self.hasName(newName))){
                name = self.getName(key);
                // Rename the data
                data = self._getData(key);
                if (data != null){
                    // Update the internal data
                    if (data.dataType === SERIALIZABLE_DATA_TYPE){
                        value = data.value;
                        value = Serialization.nativizeObject(value, null, Serialization.JSON_FORMAT);
                        if (Serialization.NamedSerializable.isInstance(value)){
                            value.setName(newName);
                        }
                        value = Serialization.serializeObject(value, Serialization.JSON_FORMAT);
                        data.value = value;
                    }
                    // Update the stored name
                    data.name = newName;
                    // Update the name map
                    if (name != null){
                        delete self._nameMap[name];
                    }
                    if (newName != null){
                        self._nameMap[newName] = key;
                    }
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        };
        
        self.getDescription = function getDescription(key, name){
            var data;
            key = self.resolveRef(key, name);
            data = self._getData(key);
            if (data != null){
                return data.description;
            } else {
                return undefined;
            }
        };
        
        self.getDataType = function getDataType(key, name){
            var data;
            key = self.resolveRef(key, name);
            data = self._getData(key);
            if (data != null){
                return data.dataType;
            } else {
                return undefined;
            }
        };
        
        self.setValue = function setValue(key, value, name, description, tags, storageType, dataType, allowOverwrite, allowCreate){
            var i, hasKey;
            // Early exit if no key given
            if (key == null){ 
                return false;
            }
            // Default Values
            if (allowOverwrite == null) {allowOverwrite = false;} 
            if (allowCreate == null) {allowCreate = true;}
            if (name == null) {name = null;} 
            hasKey = self.hasKey(key);
            if (hasKey && allowOverwrite &&
                ((name == null) || (!(self.hasName(name))) ||
                 (self._nameMap[name] === key))){
                if (name != null){
                    if (self._data[key].name != null){
                        delete self._nameMap[self._data[key].name];
                    }
                    self._data[key].name = name;
                    self._nameMap[name] = key;
                }
                if (value != null){
                    self._data[key].value = value;
                }
                if (dataType != null){
                    self._data[key].dataType = dataType;
                }
                if (description != null){
                    self._data[key].description = description;
                }
                if (storageType != null){
                    self._adaptorMap[key] = storageType;
                }
                if (tags != null){
                    self.changeTags(tags, key);
                }
                return true;
            } else if (((!hasKey) && allowCreate) && (value != null) && 
                        ((name == null) || (!(self.hasName(name))))){
                if (description == null) {description = "";}
                if (dataType == null) {dataType = "";}
                if (tags == null) {tags = [];}
                if (storageType == null) {storageType = STORAGE_ADAPTER_MONGODB;}
                self._data[key] = {'value' : value, 'description' : description, 'dataType' : dataType, 'name' : name};
                if (name != null){
                    self._nameMap[name] = key;
                }
                self._adaptorMap[key] = storageType;
                for (i=0; i<tags.length; i++){
                    self.addTagKey(tags[i], key);
                }
                return true;
            } else {
                return false;
            }
        };
	
        self.delValue = function delValue(key, name){
            key = self.resolveRef(key, name);
            if (key != null){
                name = self.getName(key);
                self.changeTags([], key);
                delete self._data[key];
                delete self._nameMap[name];
                delete self._adaptorMap[key];
                return true;
            } else {
                return false;
            }
        };
    }
});
      
      
Zet.declare('LocalStorageService', {
    // Base class for messaging gateways
    superclass : Client_Messaging_Gateway.BaseService,
    defineBody : function(self){
        // Public Properties

        self.construct = function construct(id, gateway){
            self.inherited(construct, [id, gateway]);
            self._storage = {};
        };
        
        self.saveToLocalStorage = function saveToLocalStorage(keyName){
            var key, localData;
            localData = {};
            for (key in self._storage){
                localData[key] = self._storage[key].getJSON();
            }
            localData = JSON.stringify(localData);
            localStorage.setItem(keyName, localData);
        };
        
        self.loadFromLocalStorage = function loadFromLocalStorage(keyName){
            var key, localData;
            // load from HTML5
            if ((keyName in localStorage) && (localStorage[keyName] !== '{}')){
                localData = localStorage.getItem(keyName);
                localData = JSON.parse(localData);
                self._storage = {};
                for (key in localData){
                    self._storage[key] = StorageBucket(name);
                    self._storage[key].setJSON(localData[key]);
                }
            }
        };
        
        self.hasBucket = function hasBucket(name){
            return (name in self._storage);
        };
        
        self._getBucket = function _getBucket(name){
            return self._storage[name];
        };
        
        self.addBucket = function addBucket(name){
            self._storage[name] = StorageBucket(name);
        };
        
        self.getBucketNames = function getBucketNames(){
            var k, keys;
            keys = [];
            for (k in self._storage){
                keys.push(k);
            }
            return keys;
        };
        
        self.renameBucket = function renameBucket(oldName, newName){
            if (!(oldName in self._storage)){
                throw Error("Bucket named '" + oldName + "' did not exist, could not rename.");
            } else if (newName in self._storage){
                throw Error("New bucket name '" + newName + "' already exists in storage.");
            } else {
                // Should have a try-catch to prevent name mismatch on error
                self._storage[newName] = self._storage[oldName];
                self._storage[newName].rename(newName);
                delete self._storage[oldName];
            }
        };
        
        self.delBucket = function delBucket(name){
            delete self._storage[name];
        };
        
        self.receiveMessage = function receiveMessage(msg){
            var bucket, value, response;
            //console.log("RECEIVE MSG (" + self.getId() + "):" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
            // Message must have a bucket and be for a Storage Service
            console.log(msg);
            if ((msg.getActor() === "StorageService") && 
                (msg.getContextValue(BUCKET_KEY, null) != null) &&
                (msg.getContextValue(BUCKET_KEY) in self._storage)){
                bucket = self._storage[msg.getContextValue(BUCKET_KEY)];
                // Inform: Set some value(s)
                if (msg.getSpeechAct() === Messaging.INFORM_ACT){
                    try {
                        value = self.processStorageInform(bucket, 
                                                          msg.getVerb(), 
                                                          msg.getObject(), 
                                                          msg.getResult(), 
                                                          msg.getContextValue(TAGS_KEY, null), 
                                                          msg.getContextValue(TYPE_KEY, null),
                                                          msg.getContextValue(ALLOW_CREATE_KEY, null),
                                                          msg.getContextValue(NAME_KEY, null),        
                                                          msg.getContextValue(DESCRIPTION_KEY, null),
                                                          msg.getContextValue(DATA_TYPE_KEY, null));
                        if (value === true){
                            response = self.makeConfirmMessage(msg);
                        } else {
                            response = self.makeDisconfirmMessage(msg);
                        }
                    } catch (err){
                        self.sendMessage(self.makeDisconfirmMessage(msg));
                        throw err;
                    }
                    self.sendMessage(response);
                // Request: get some value(s)
                } else if (msg.getSpeechAct() === Messaging.REQUEST_ACT){
                    try {
                        value = self.processStorageRequest(bucket, 
                                                           msg.getVerb(), 
                                                           msg.getObject(), 
                                                           msg.getContextValue(TAGS_KEY, null), 
                                                           msg.getContextValue(TYPE_KEY, null),
                                                           msg.getContextValue(NAME_KEY, null));
                        if ((msg.getVerb() != Messaging.INFORM_REF_ACT) || (value == null)){
                            response = self.makeRequestAnswerMessage(msg, value);
                        } else {
                            response = self.makeReplyToInformRefMessage(msg, value[0], value[1]);
                        }
                    } catch (err){
                        self.sendMessage(self.makeDisconfirmMessage(msg));
                        throw err;
                    }
                    self.sendMessage(response);
                 } else if (msg.getSpeechAct() === Messaging.INFORM_REF_ACT){
                    try {
                        value = self.processStorageRename(bucket, 
                                                          msg.getVerb(), 
                                                          msg.getObject(),
                                                          msg.getResult(),
                                                          msg.getContextValue(NAME_KEY, null));
                        if (value === true){
                            response = self.makeConfirmMessage(msg);
                        } else {
                            response = self.makeDisconfirmMessage(msg);
                        }
                    } catch (err){
                        self.sendMessage(self.makeDisconfirmMessage(msg));
                        throw err;
                    }
                    self.sendMessage(response);
                } else {
                    console.log("COULD NOT PROCESS (" + self.getId() + "):" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
                }
            }
        };
        
        self.processStorageInform = function processStorageInform(bucket, verb, key, value, tags, type, allowCreate, name, description, dataType){
            console.log("RECEIVED Inf: " + verb);
            if (verb === VALUE_VERB){
                if (Serialization.Serializable.isInstance(value)){
                    dataType = SERIALIZABLE_DATA_TYPE;
                    // Serializable ID allowed as a default key
                    if (key == null){
                        key = value.getId();
                    // Key must match id for a Serializable class, or invalid data
                    } else if (key !== value.getId()) {
                        return false;
                    }
                    if (Serialization.NamedSerializable.isInstance(value)){
                        // NamedSerializable name allowed as a default name
                        if (name == null){
                            name = value.getName();
                        // Name must match name for a Serializable class, or invalid data
                        } else if (name != value.getName()){
                            return false;
                        }
                    }
                    // Store the value.  If a Serializable, pack before storing.
                    value = Serialization.serializeObject(value, Serialization.JSON_FORMAT);
                }
                return bucket.setValue(key, value, name, description, tags, type, dataType, true, allowCreate);
            } else if (verb === VOID_VERB){
                return bucket.delValue(key, name);
            }
        };
        
        self.processStorageRequest = function processStorageRequest(bucket, verb, key, tags, type, name){
            var value;
            console.log("RECEIVED Req: " + verb);
            // Access by Key or Name
            if (verb === HAS_ELEMENT_VERB){
                return bucket.hasRef(key, name);
            } else if (verb === CONTAINS_VERB){
                return bucket.getMatchingKeys(tags, type);
            } else if (verb === VALUE_VERB){
                // Get the value.  If a Serializable, unpack before sending.
                value = bucket.getValue(key, name);
                if (bucket.getDataType(key, name) === SERIALIZABLE_DATA_TYPE){
                    value = Serialization.nativizeObject(value, Serialization.JSON_FORMAT);
                }
                return value;
            } else if (verb === ASSIGNED_URI_VERB){
                return bucket.getLink(key, name);
            } else if (verb === Messaging.INFORM_REF_ACT){
                if (key != null){
                    return [key, bucket.getName(key)];
                } else if (name != null){
                    return [bucket.resolveRef(key, name), name];
                } else {
                    return null;
                }
            } else {
                throw new Error("Error, invalid request for storage service.");
            }
        };
        
        self.processStorageRename = function processStorageRename(bucket, verb, key, newName, name){
            if (verb === HAS_ELEMENT_VERB){
                return bucket.changeName(newName, key, name);
            } else {
                return false;
            }
        };
        
        self.makeConfirmMessage = function makeConfirmMessage(msg){
            // Maybe make a copy first?
            var id;
            id = msg.getId();
            msg = msg.clone();
            msg.updateId();
            msg.setSpeechAct(Messaging.CONFIRM_ACT);
            msg.setContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, id);
            return msg;
        };
        
        self.makeDisconfirmMessage = function makeDisconfirmMessage(msg){
            var id;
            id = msg.getId();
            msg = msg.clone();
            msg.updateId();
            msg.setSpeechAct(Messaging.DISCONFIRM_ACT);
            msg.setContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, id);
            return msg;
        };
        
        self.makeRequestAnswerMessage = function makeRequestAnswerMessage(msg, result){
            var id;
            id = msg.getId();
            msg = msg.clone();
            msg.updateId();
            msg.setSpeechAct(Messaging.INFORM_ACT);
            msg.setContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, id);
            msg.setResult(result);
            return msg;
        };
        
        self.makeReplyToInformRefMessage = function makeReplyToInformRefMessage(msg, key, name){
            var id;
            id = msg.getId();
            msg = msg.clone();
            msg.updateId();
            msg.setSpeechAct(Messaging.INFORM_ACT);
            msg.setObject(key);
            msg.setResult(name);
            msg.setContextValue(Messaging.NAME_KEY, name);
            msg.setContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, id);
            return msg;
        };
    }
});

namespace.LocalStorageService = LocalStorageService;
})(window.Local_Storage_Service = window.Local_Storage_Service || {});