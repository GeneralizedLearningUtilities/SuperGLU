/** SuperGLU (Generalized Learning Utilities) Standard API
 This manages all versioning within the core libraries.

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0
 **/
const Zet = require('./util/zet'),
    Serialization = require('./util/serialization'),
    Message = require('./core/message'),
    Messaging = require('./core/messaging'),
    Messaging_Gateway = require('./core/messaging-gateway'),
    ReferenceData = require('./reference-data')

window.ReferenceData = ReferenceData
var namespace = window.SuperGLU = window.SuperGLU || {}
namespace.version = "0.1.9"

// Core API Modules
namespace.Zet = window.Zet = Zet
namespace.Serialization = Serialization
namespace.Messaging = Messaging
namespace.Messaging.Message = Message
namespace.Messaging_Gateway = Messaging_Gateway
namespace.VERBS = {}
namespace.CONTEXT_KEYS = {}
namespace.ReferenceData = ReferenceData

module.exports = namespace