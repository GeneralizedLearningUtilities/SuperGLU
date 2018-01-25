//TODO: Note that we just ad-hoc the context and user objects instead
//      of using the serialization framework.  This should really be
//      corrected, but ran out of time

// NOTE: When calling this, pass in a when.js deferred.resolve function as a callback

// JS client interface for the user info service
// Note that we "borrow" the various fields for our messages - we use
// verb as the command/request name, speechAct/key as the request fields,
// and val as the response field.  Context will be used as necessary.
//
// NOTE: all context names are treated as context ID's.  If the context
// can't be found for that ID, the search is re-done and the first context
// with the name is used.
//
// NOTE: functions requiring a "user id" need the actual id of the user
// instance (as stored in the context).  You retrieve this with .getId().
// Note that this is different from .getUserId which returns a (generally)
// user-readable string that represents a login. See also the next note...
//
// NOTE: a null user ID implies a request to use the current user.

const Zet = require('../../util/zet'),
    Messaging = require('../../core/messaging'),
    Messaging_Gateway = require('../../core/messaging-gateway')

var UserDataServiceInterface = Zet.declare({
    superclass: Messaging_Gateway.BaseService,
    CLASS_ID: 'UserDataServiceInterface',
    defineBody: function (self) {
        // Private Properties
        var USER_SERVICE_NAME = "UserDataService"

            ,HAS_CONTEXT_VERB = "HasContext"
            ,HAS_USER_VERB = "HasUser"
            ,CONTAINS_VERB = "Contains"
            ,VALUE_VERB = "Value"
            ,VOID_VERB = "Void"

        //Special context keys
            ,CONTEXT_USER_CONTEXT = "UserContext"
            ,CONTEXT_USER_ID = "UserId"
            ,CONTEXT_USER_AUTH_FALLBACK = "UserAuthFallback"
            ,CONTEXT_ERROR = "ErrorMessage"

        // Public Properties
        self.construct = function construct(gateway, id) {
            self.inherited(construct, [id, gateway])
        }

        // Check if a context exists
        self.hasContext = function hasContext(ctxName, callback) {
            var context = self.createMsgContext(ctxName, null)
            callback = self.createCallback(callback)
            self.sendRequest(callback, HAS_CONTEXT_VERB, ctxName, null, Messaging.REQUEST_ACT, context)
        }

        self.makeContext = function makeContext(ctxName, callback) {
            var context = self.createMsgContext(ctxName, null)
            callback = self.createCallback(callback)
            self.sendRequest(callback, HAS_CONTEXT_VERB, ctxName, true, Messaging.INFORM_ACT, context)
        }

        //Callback called with context object, error (if any), and entire msg
        //This is a bit different from other messages: 
        //Dumps a whole context in the form {'name':str, 'users':[], 'prefs':{}}
        self.readContext = function readContext(ctxName, callback) {
            var context = self.createMsgContext(ctxName, null, false)
            callback = self.createCallback(callback)
            self.sendRequest(callback, VALUE_VERB, null, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with list of context keys, error (if any), and entire msg
        self.readContextKeys = function readContextKeys(ctxName, callback) {
            var context = self.createMsgContext(ctxName, null, false)
            callback = self.createCallback(callback)
            self.sendRequest(callback, CONTAINS_VERB, null, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with matching value (or null if missing), error (if any), and entire msg
        self.readContextVal = function readContextVal(ctxName, key, callback) {
            var context = self.createMsgContext(ctxName, null, false)
            callback = self.createCallback(callback)
            self.sendRequest(callback, VALUE_VERB, key, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with boolean indictaing success, error (if any), and entire msg
        self.writeContextVal = function writeContextVal(ctxName, key, val, callback) {
            var context = self.createMsgContext(ctxName, null, false)
            callback = self.createCallback(callback, function (msg) {
                return msg.getResult() === true
            })
            self.sendRequest(callback, VALUE_VERB, key, val, Messaging.INFORM_ACT, context)
        }

        //Callback called with list of user of context keys, error (if any), and entire msg
        self.readContextUserKeys = function readContextUserKeys(ctxName, userId, callback) {
            var context = self.createMsgContext(ctxName, userId, true)
            callback = self.createCallback(callback)
            self.sendRequest(callback, CONTAINS_VERB, null, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with data from a user object, error (if any), and entire msg
        self.readContextUser = function readContextUser(ctxName, userId, callback) {
            var context = self.createMsgContext(ctxName, userId, true)
            callback = self.createCallback(callback)
            self.sendRequest(callback, VALUE_VERB, null, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with matching user value, error (if any),  and entire msg
        self.readContextUserVal = function readContextUserVal(ctxName, userId, key, callback) {
            callback = self.createCallback(callback)
            var context = self.createMsgContext(ctxName, userId, true)
            self.sendRequest(callback, VALUE_VERB, key, null, Messaging.REQUEST_ACT, context)
        }

        //Callback called with boolean indictaing success, error (if any), and entire msg
        self.writeContextUserVal = function writeContextUserVal(ctxName, userId, key, val, callback) {
            callback = self.createCallback(callback, function (msg) {
                return msg.getResult() === true
            })
            var context = self.createMsgContext(ctxName, userId, true)
            self.sendRequest(callback, VALUE_VERB, key, val, Messaging.INFORM_ACT, context)
        }

        self.createMsgContext = function createMsgContext(ctxName, userId, userAuthFallback) {
            var context = {}
            if (userId != ctxName) {
                context[CONTEXT_USER_CONTEXT] = ctxName
            }
            if (userId != null) {
                context[CONTEXT_USER_ID] = userId
            }
            if (userAuthFallback != null) {
                context[CONTEXT_USER_AUTH_FALLBACK] = userAuthFallback
            }
            return context
        }

        self.sendRequest = function sendRequest(callback, verb, key, result, speechAct, context) {
            if (context != null) {
                console.log("CONTEXT!!!!")
                console.log(context)
            }
            if (context == null) context = {}
            var msg = Messaging.Message(USER_SERVICE_NAME, verb, key, result, speechAct, context)
            msg.updateTimestamp()
            self._makeRequest(msg, callback)
        }

        //Helper: our various methods all wrap the user's callback and
        //then call it with the expected value, an error message (if one
        //was found), and the entire message (just in case).  We provide
        //a default implementation (self assumes the message result is
        //the "real" payload.  This extraction can be overridden by a 
        //function that accepts the msg and returns the payload
        self.createCallback = function createCallback(userCallback, extractor) {
            if (typeof userCallback === "undefined" || userCallback === null) {
                return function (msg) {
                }
            }
            if (typeof extractor === "undefined" || extractor === null) {
                extractor = function (msg) {
                    return msg.getResult()
                }
            }
            return function (msg) {
                var val, errMsg
                if (msg == null) {
                    val = null
                    errMsg = "No Message Received"
                } else {
                    val = extractor(msg)
                    errMsg = msg.getContextValue(CONTEXT_ERROR, null)
                }
                userCallback(val, errMsg, msg)
            }
        }
    }
})

module.exports = UserDataServiceInterface
