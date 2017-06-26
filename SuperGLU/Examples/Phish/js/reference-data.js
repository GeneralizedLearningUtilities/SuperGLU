/** Data about this reference implementation **/
if (typeof window === "undefined") {
    var window = this;
}

(function(namespace, undefined) {

// Version Numbering
namespace.REFERENCE_IMPLEMENTATION_VERSION_KEY = "reference-implementation-version";
namespace.USER_AGENT_KEY = "UserAgent";
namespace.version = "1.0.1";

})(window.ReferenceData = window.ReferenceData || {});