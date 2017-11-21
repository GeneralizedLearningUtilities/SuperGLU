const Zet = require('./zet')
const TokenRWFormat = require('./token_rw_format')
const StorageToken = require('./storage_token')

module.exports = Zet.declare({        //JSONRWFormat
    superclass: TokenRWFormat,
    CLASS_ID: 'JSONRWFormat',
    defineBody: function (self) {

        // Constructor method
        self.construct = function construct() {
        }

        // Public methods

        /** Parse a JSON-formatted string into basic javascript objects
         (e.g., strings, numeric, arrays, objects)
         **/
        self.parse = function parse(String) {//Parse a JSON string into javascript objects
            var decoded = JSON.parse(String)
            return self.makeNative(decoded)
        }

        /** Turn basic javascript objects into a JSON string **/
        self.serialize = function serialize(data) {
            var serializable = self.makeSerializable(data)
            return JSON.stringify(serializable)
        }

        /** Recursively make all objects serializable into JSON,
         turning any lists, dicts, or StorageTokens into canonical forms
         **/
        self.makeSerializable = function makeSerializable(x) {
            var i, key, keys, rt, temp, xType
            xType = typeof(x)
            rt = null
            // Primitive variables
            if ((xType in self.VALID_ATOMIC_VALUE_TYPES) || (x === null)) {
                rt = x
                // Array
            } else if (x instanceof Array) {
                rt = {}
                temp = []
                for (i = 0; i < x.length; i++) {
                    temp[i] = self.makeSerializable(x[i])
                }
                rt[LIST_STRING] = temp
                // Object
            } else if ((x instanceof Object) &&
                !(StorageToken.isInstance(x))) {
                rt = {}
                temp = {}
                for (key in x) {
                    temp[key] = self.makeSerializable(x[key])
                }
                rt[MAP_STRING] = temp
                // StorageToken
            } else if (StorageToken.isInstance(x)) {
                rt = {}
                temp = {}
                keys = x.keys()
                for (i = 0; i < keys.length; i++) {
                    temp[self.makeSerializable(keys[i])] = self.makeSerializable(x.getitem(keys[i]))
                }
                rt[x.getClassId()] = temp
                //Error
            } else {
                throw new TypeError("Tried to serialize unserializable object of type (" + xType + "): " + x)
            }
            return rt
        }

        /** Recursively turn raw javascript objects in a canonical format into
         primitives, arrays, mappings, and StorageTokens.
         **/
        self.makeNative = function makeNative(x) {
            var i, key, rt, temp, xType, dataTypeName
            xType = typeof(x)
            rt = null
            // Primitive variables
            if ((self.VALID_ATOMIC_VALUE_TYPES[xType]) || (x == null)) {
                rt = x
                return rt
            }
            for (dataTypeName in x) {
                break
            }
            // Array
            if (dataTypeName in self.VALID_SEQUENCE_VALUE_TYPES) {
                rt = []
                for (i = 0; i < x[dataTypeName].length; i++) {
                    rt[i] = self.makeNative(x[dataTypeName][i])
                }
                // Object
            } else if (dataTypeName in self.VALID_MAPPING_VALUE_TYPES) {
                rt = {}
                for (key in x[dataTypeName]) {
                    rt[key] = self.makeNative(x[dataTypeName][key])
                }
                // StorageToken (by default)
            } else {
                rt = {}
                rt[MAP_STRING] = x[dataTypeName]
                rt = self.makeNative(rt)
                rt = StorageToken(undefined, undefined, rt)
            }
            return rt
        }
    }
})