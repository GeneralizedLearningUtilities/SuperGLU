var Zet = require('./zet')
/** Class StorageToken
 An object that stores data in a form that can be serialized
 **/

module.exports = Zet.declare({
    superclass: null,
    CLASS_ID: 'StorageToken',
    defineBody: function (self) {
        // -- Class fields
        self.ID_KEY = 'id'
        self.CLASS_ID_KEY = 'classId'

        /** Constructor for storage token
         @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
         @param classId: The name of the class, as known by the class factory
         @param data: Object of key-value pairs to store for this token
         **/
        self.construct = function construct(id, classId, data) {
            /** Create a storage token, which can be directly serialized into a string
             @param id (optional): A GUID for the storage token.  If none given, uses a V4 random GUID.
             @param classId (optional): Id for the class that this StorageToken should create.  Defaults to null.
             @param data (optional): Starting data for the token.  Either a map {} for an array of map pairs [[key, val]].
             */
            var i
            self._data = {}
            if (data !== undefined) {
                //we are assuming that the data will either already
                //be in a dictionary form ({key: value, key2: value2, ...})
                //or is in a sequence form ([[key, value], [key2, value2], ...])
                if (data instanceof Array) { //[[key, value], [key2, value2], ...]
                    for (i in data) {
                        if ((data[i] instanceof Array) && (data[i].length == 2)) {
                            self._data[data[i][0]] = data[i][1]
                        } else {
                            throw new TypeError("Input array doesn't follow the format of [[key, value], [key2, value2], ...]")
                        }
                    }
                } else {// {key: value, key2: value2, ...}
                    self._data = data
                }
            } else {
                self._data = {}
            }
            if (id !== undefined) {
                self.setId(id)
            } else if ((self.getId() === undefined)) {
                self.setId(UUID.genV4().toString())
            }
            if (classId !== undefined) {
                self.setClassId(classId)
            }
        }

        // -- Instance methods

        /** Get the ID for the storage token **/
        self.getId = function getId() {
            return self._data[self.ID_KEY]
        }

        /** Set the ID for the storage token **/
        self.setId = function setId(value) {
            self._data[self.ID_KEY] = value
        }

        /** Get the class name for the storage token **/
        self.getClassId = function getClassId() {
            return self._data[self.CLASS_ID_KEY]
        }

        /** Set the class name for the storage token **/
        self.setClassId = function setClassId(value) {
            self._data[self.CLASS_ID_KEY] = value
        }

        // Convenience Accessor for Named Serializables

        /** Get the name for the storage token (might be null) **/
        self.getName = function getName() {
            if (NAME_KEY in self._data) {
                return self._data[NAME_KEY]
            } else {
                return null
            }
        }

        /** Set a name for the storage token **/
        self.setName = function setName(value) {
            self._data[NAME_KEY] = value
        }

        // -- ##Generic Accessors

        /** Get the number of data values in the storage token **/
        self.len = function len() {
            return self._data.length
        }

        /** Check if a given key is contained in the storage token **/
        self.contains = function contains(key) {
            return key in self._data
        }

        /** Get an item from the data dictionary
         @param key: Key for the item
         @param hasDefault (optional): If True, give a default value.  Else, raise an error if key not found.
         @param defaults (optional): The optional value for this item.
         */
        self.getitem = function getitem(key, hasDefault, defaults) {

            if (!(key in self._data) && (hasDefault)) {
                return defaults
            } else {
                return self._data[key]
            }
        }

        /** Set an item in the data dictionary **/
        self.setitem = function setitem(key, value) {
            self._data[key] = value
        }

        /** Delete an item in the data dictionary **/
        self.delitem = function delitem(key) {
            delete self._data[key]
        }

        /** Return an iterator over the data keys **/
        self.__iterator__ = function __iterator__() {
            var keys = Object.keys(self._data).sort()
            var keys_pos = 0
            return {
                next: function () {
                    if (keys_pos >= keys.length) {
                        throw StopIteration
                    }
                    return keys[keys_pos++]
                }
            }
        }

        /** Return the data keys **/
        self.keys = function keys() {
            var k, aKeys
            aKeys = []
            for (k in self._data) {
                aKeys.push(k)
            }
            return aKeys
        }

        // -- ##Comparison
        /** Equality operator **/
        self.eq = function eq(other) {
            return (typeof(self) == typeof(other)) && (self._data == other._data)
        }

        /** Not equal operator **/
        self.ne = function ne(other) {
            return !(self.eq(other))
        }

        // -- ##Validation
        /** Check if a key would be a valid data key **/
        self.isValidKey = function isValidKey(key) {
            return typeof(key) in self.VALID_KEY_TYPES
        }

        /** Check if a value would be a valid data value **/
        self.isValidValue = function isValidValue(value) {
            return typeof(value) in self.VALID_VALUE_TYPES
        }

        /** Check that the ID, Class Name, and any Name are valid types **/
        self.isValid = function isValid() {
            var idKey
            var classIdKey

            //Check that ID is valid
            if ((self._data[self.ID_KEY] == null) ||
                ((typeof(self._data[self.ID_KEY]) !== 'string') &&
                    (typeof(self._data[self.ID_KEY]) !== 'number'))) {
                return false
            }
            //Check that class name is valid
            if ((self._data[self.CLASS_ID_KEY] == null) ||
                (typeof(self._data[self.CLASS_ID_KEY]) !== 'string')) {
                return false
            }
            // Check that the name (if it exists) is valid
            if ((self._data[NAME_KEY] != null) &&
                (typeof(self._data[NAME_KEY]) !== 'string')) {
                return false
            }
            return true
        }
    }
})