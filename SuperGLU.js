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
namespace.version = "0.6.0";

// Core API Modules
if (namespace.Zet == null){ namespace.Zet = Zet; }
if (namespace.Serialization == null){ namespace.Serialization = Serialization; }
if (namespace.Messaging == null){ namespace.Messaging = Messaging; }
if (namespace.Messaging_Gateway == null){ namespace.Messaging_Gateway = Messaging_Gateway; }

})(window.SuperGLU = window.SuperGLU || {});