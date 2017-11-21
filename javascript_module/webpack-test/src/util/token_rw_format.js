var Zet = require('./zet')

/** Utility function to merge two mappings
 @param targetObj: Object to have key-value pairs added
 @param sourceObj: Object to take keys from
 @return: Modified version of the targetObj
 **/
var updateObjProps = function (targetObj, sourceObj) {
    var key
    for (key in sourceObj) {
        targetObj[key] = sourceObj[key]
    }
    return targetObj
}

module.exports = Zet.declare({        //TokenRWFormat
    superclass: null,
    CLASS_ID: 'TokenRWFormat',
    defineBody: function (self) {
        // Public Class Properties

        // Valid Types in Storage Token
        self.VALID_KEY_TYPES = {'string': true}
        self.VALID_ATOMIC_VALUE_TYPES = {'number': true, 'string': true, 'boolean': true, 'undefined': true}
        self.VALID_SEQUENCE_VALUE_TYPES = {'list': true, 'tuple': true}
        self.VALID_MAPPING_VALUE_TYPES = {'map': true}
        self.VALID_VALUE_TYPES = {}

        // Setup for Class Properties
        self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_ATOMIC_VALUE_TYPES)
        self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_SEQUENCE_VALUE_TYPES)
        self.VALID_VALUE_TYPES = updateObjProps(self.VALID_VALUE_TYPES, self.VALID_MAPPING_VALUE_TYPES)
        self.VALID_VALUE_TYPES.StorageToken = true

        // Constructor method
        self.construct = function construct() {
        }

        // Public methods
        self.parse = function parse(string) {
            // Parse a string into javascript objects
            throw new Error("NotImplementedError")
        }

        self.serialize = function serialize(data) {
            // Serialize javascript objects into a string form
            throw new Error("NotImplementedError")
        }
    }
})