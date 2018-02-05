var Zet = require('./zet')
var Serializable = require('./serialization').Serializable

module.exports = Zet.declare({
    superclass: Serializable,
    CLASS_ID: 'NamedSerializable',
    defineBody: function (self) {
        // Constructor Function
        self.NAME_KEY = NAME_KEY

        /** Constructor for named serializable
         *   @param id (optional): GUID for this object.  If none given, a V4 random GUID is used.
         *   @param name: The name for the object
         **/
        self.construct = function construct(id, name) {
            if (name == null) {
                name = null
            }
            self.inherited(construct, [id])
            self._name = name
        }

        /** Get the name for the object **/
        self.getName = function getName() {
            return self._name
        }

        /** Set the name for the object **/
        self.setName = function setName(name) {
            if (name == null) {
                name = null
            } else if (name instanceof String || typeof name === 'string') {
                self._name = name
            } else {
                throw new Error("Set name failed, was not a string.")
            }
        }

        /** Equality operator **/
        self.eq = function eq(other) {
            return (self.inherited(eq, [other]) && (self._name === other._name))
        }

        self.initializeFromToken = function initializeFromToken(token, context) {
            self.inherited(initializeFromToken, [token, context])
            self._name = untokenizeObject(token.getitem(self.NAME_KEY, true, null), context)
        }

        self.saveToToken = function saveToToken() {
            var token = self.inherited(saveToToken)
            if (self._name != null) {
                token.setitem(self.NAME_KEY, tokenizeObject(self._name))
            }
            return token
        }
    }
})