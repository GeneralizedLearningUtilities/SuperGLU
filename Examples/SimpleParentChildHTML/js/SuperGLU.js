/** SuperGLU (Generalized Learning Utilities) Standard API
    This manages all versioning within the core libraries.
    
    Package: SuperGLU (Generalized Learning Utilities)
    Author: Benjamin Nye
    License: APL 2.0
    
    Requires:
        - Util\uuid.js 
        - Util\zet.js 
        - Util\serializable.js
        - Core\messaging.js
        - Core\messaging-gateways.js
**/

if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

// Requirements
namespace.UUID = UUID;
namespace.Zet = Zet;
namespace.Serializable = Serializable;
namespace.Messaging = Messaging;
namespace.Messaging_Gateway = Messaging_Gateway;

// Version Numbering
namespace.version = "0.6.0";
namespace.Messaging.version = "1.0.0";

})(window.SuperGLU = window.SuperGLU || {});