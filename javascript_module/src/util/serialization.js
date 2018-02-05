const Zet = require('./zet')
const JSONRWFormat = require('./json_rw_format')
const StorageToken = require('./storage_token')
const UUID = require('./uuid')


// GLOBAL is the reference in nodejs implementation to the global scope
// node.js supports Modules specs, so, Zet will go into separate scope
const globalscope = {}
if (typeof module !== "undefined" && module && module.exports) {
    module.exports = globalscope
}

var MAP_STRING = "map",
    LIST_STRING = 'list'

var NAME_KEY = 'name'

// Format Constants
var JSON_FORMAT = 'json',
    XML_FORMAT = 'xml',
    VALID_SERIAL_FORMATS = [JSON_FORMAT, XML_FORMAT]

var JSONRWFormatter = JSONRWFormat(),
    XMLRWFormat = null,
    XMLRWFormatter = null

/** Create a serializable instance from an arbitrary storage token
 @param token: Storage token
 @param context (optional): Mutable context for the loading process. Defaults to null.
 @param onMissingClass (optional): Function to transform/error on token if class missing
 */
var createFromToken = function (token, context, onMissingClass) {
    var classId, AClass
    var id = token.getId()
    var instance = {}
    if ((context != null) && (id in context)) {
        instance = context[id]
    } else {
        //Need to import the right class
        classId = token.getClassId()
        AClass = Zet.getFactoryClass(classId)
        if (typeof AClass !== "undefined") {
            instance = AClass()
            instance.initializeFromToken(token, context)
        } else {
            if (onMissingClass == null) {
                onMissingClass = defaultOnMissing
            }
            instance = onMissingClass(token)
        }
    }
    return instance
}

/** What to do if a class is missing (error or console message) **/
var defaultOnMissing = function (token, errorOnMissing) {
    if (!(errorOnMissing)) {
        console.log("ERROR: Couldn't make class from factory: " + token.getClassId())
        return token
    } else {
        throw new Error("Class Factory failed to import " + token.getClassId())
    }
}

// Convenience Function to Serialize and Un-Serialize Objects
//----------------------------------------------------------
/** A function that will attempt to turn any valid object
 (Serializable, StorageToken, map, list, atomic) into
 its string serialized equivalent.
 @param obj: Any object that can be serialized, i.e., Serializable, StorageToken, TokenRWFormat.VALID_VALUE_TYPES
 @type obj: object
 @param sFormat: Serializable format to pack things as
 @type sFormat: string
 @return: Serialized object
 @rtype: string
 **/
var serializeObject = function serializeObject(obj, sFormat) {
    return makeSerialized(tokenizeObject(obj), sFormat)
}

/** A function that will attempt to turn any valid object
 (Serializable, StorageToken, map, list, atomic) into
 its highest native equivalent (Serializable > StorageToken > list/map > atomic).
 @param obj: Any object that can be serialized, i.e., Serializable, StorageToken, TokenRWFormat.VALID_VALUE_TYPES
 @type obj: object
 @param sFormat: Serializable format to unpack things as
 @type sFormat: string
 @return: Least serialized form of this object
 @rtype: string
 **/
var nativizeObject = function nativizeObject(obj, context, sFormat) {
    if (Serializable.isInstance(obj)) {
        return obj
    } else if (StorageToken.isInstance(obj)) {
        return createFromToken(obj, context)
    } else if (typeof obj === "string" || obj instanceof String) {
        obj = makeNative(obj, sFormat)
        return untokenizeObject(obj)
    } else {
        return obj
    }
}

// Convenience Function to Tokenize and Un-Tokenize Objects
//----------------------------------------------------------

/** Generic function to tokenize an object, recursively **/
var tokenizeObject = function (obj) {
    var i, key, rt
    rt = null
    if (Serializable.isInstance(obj)) {// Serializable
        rt = obj.saveToToken()
    } else if (obj instanceof Array) { // Array
        rt = []
        for (i = 0; i < obj.length; i++) {
            rt[i] = tokenizeObject(obj[i])
        }
    } else if ((obj instanceof Object) &&
        !(obj instanceof Array)) { // Object
        rt = {}
        for (key in obj) {
            rt[tokenizeObject(key)] = tokenizeObject(obj[key])
        }
    } else {
        rt = obj
    }
    return rt
}

/** Generic function to create an object from a token
 @param obj: Object to turn from tokens into object
 @param context (optional): Mutable context for the loading process. Defaults to null.
 */
var untokenizeObject = function (obj, context) {
    var i, key
    var rt = null
    if (StorageToken.isInstance(obj)) {// StorageToken
        rt = createFromToken(obj, context)
    } else if (obj instanceof Array) { // Array
        rt = []
        for (i in obj) {
            rt[i] = untokenizeObject(obj[i], context)
        }
    } else if ((obj instanceof Object) &&
        !(obj instanceof Array)) { // Object
        rt = {}
        for (key in obj) {
            rt[untokenizeObject(key, context)] = untokenizeObject(obj[key], context)
        }
    } else {
        rt = obj
    }
    return rt
}

// Convenience functions to serialize and unserialize tokens and raw data
//---------------------------------------------
/** Generic function to turn a tokenized object into serialized form
 @param obj: Tokenized object
 @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
 */
var makeSerialized = function makeSerialized(obj, sFormat) {
    if (sFormat === undefined) { // Default format is JSON_FORMAT
        sFormat = JSON_FORMAT
    }
    if (sFormat == JSON_FORMAT) {
        return JSONRWFormatter.serialize(obj)
    } else if (sFormat == XML_FORMAT) {
        return XMLRWFormatter.serialize(obj)
    } else {
        throw new TypeError("No serialization format of type: " + sFormat)
    }
}

/** Generic function to turn a serialized string into a tokenized object
 *   @param String: Serialized object, as a string
 *   @param sFormat (optional): Serialization format.  Defaults to JSON_FORMAT
 */
var makeNative = function makeNative(String, sFormat) {
    if (sFormat === undefined) { // Default format is JSON_FORMAT
        sFormat = JSON_FORMAT
    }
    if (sFormat == JSON_FORMAT) {
        return JSONRWFormatter.parse(String)
    } else if (sFormat == XML_FORMAT) {
        // Not currently implemented
        return XMLRWFormatter.parse(String)
    } else {
        throw new TypeError("No unserialization format of type: " + sFormat)
    }
}

// Expose Variables Publicly
// var namespace = {}
globalscope.JSON_FORMAT = JSON_FORMAT
globalscope.XML_FORMAT = XML_FORMAT
globalscope.VALID_SERIAL_FORMATS = VALID_SERIAL_FORMATS

// Expose Functions Publicly
globalscope.createFromToken = createFromToken
globalscope.serializeObject = serializeObject
globalscope.nativizeObject = nativizeObject
globalscope.makeSerialized = makeSerialized
globalscope.makeNative = makeNative
globalscope.tokenizeObject = tokenizeObject
globalscope.untokenizeObject = untokenizeObject

// Expose Classes Publicly
// namespace.Serializable = Serializable;
// namespace.NamedSerializable = NamedSerializable
// namespace.StorageToken = StorageToken
// namespace.TokenRWFormat = TokenRWFormat
// namespace.JSONRWFormat = JSONRWFormat
//namespace.XMLRWFormat = XMLRWFormat;

// Expose Instances Publicly
globalscope.JSONRWFormatter = JSONRWFormatter
//namespace.XMLRWFormatter = XMLRWFormatter;

// SuperGLU.Serialization = namespace;
// })(window.Serialization = window.Serialization || {});
// globalscope.Serialization = namespace

var Serializable = Zet.declare({
    superclass: null,
    CLASS_ID: 'Serializable',
    defineBody: function (self) {
        // Constructor Function

        /** Constructor for serializable
         *   @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
         **/
        self.construct = function construct(id) {
            if (id == null) {
                self._id = UUID.genV4().toString()
            } else {
                self._id = id
            }
        }

        // Public Functions
        /** Equality operator **/
        self.eq = function eq(other) {
            return ((self.getClassId() == other.getClassId()) && (self.getId() == other.getId()))
        }

        /** Not-equal operator **/
        self.ne = function ne(other) {
            return !(self.eq(other))
        }

        /** Get the ID for the serializable. Ideally unique. **/
        self.getId = function getId() {
            return self._id
        }

        /** Update the id, either by setting a new one or generating a new random UUID
         @param id: The new id for the serializable.  If null/undefined, generates new random UUID
         **/
        self.updateId = function updateId(id) {
            if (id === undefined) {
                self._id = UUID.genV4().toString()
            } else {
                self._id = id
            }
        }

        /** Get the class name for this serializable **/
        self.getClassId = function getClassId() {
            return self.className || self.CLASS_ID      //patch to get serialization.test.js to work
        }

        /** Initialize serializable from token.
         @param token: The token form of the object.
         @param context (optional): Mutable context for the loading process. Defaults to null.
         */
        self.initializeFromToken = function initializeFromToken(token, context) {
            self._id = token.getId()
        }

        /** Create and return a token form of the object that is valid to serialize **/
        self.saveToToken = function saveToToken() {
            var token = StorageToken(self.getId(), self.getClassId())
            return token
        }

        /** Create a serialized version of this object **/
        self.saveToSerialized = function saveToSerialized() {
            return makeSerialized(self.saveToToken())
        }

        /** Create a clone of the object
         @param newId: Unless false or 0, give the new clone a different UUID
         @return: A new serializable object of the right class type.
         **/
        self.clone = function clone(newId) {
            if (newId == null) {
                newId = true
            }
            var s = makeSerialized(self.saveToToken())
            s = untokenizeObject(makeNative(s))
            if (newId) {
                s.updateId()
            }
            return s
        }
    }
})

globalscope.Serializable = Serializable