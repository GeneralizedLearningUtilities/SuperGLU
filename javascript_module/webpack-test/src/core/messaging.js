/** Message format for recording events and for real-time service communication
 This message format primarily follows the xAPI format (https://github.com/adlnet/xAPI-Spec/blob/master/xAPI.md)
 but is much more relaxed in the requirements for parameters. It also includes elements
 of the FIPA messaging standard, most notably the Speech Act field (performative, http://www.fipa.org/specs/fipa00061/SC00061G.html)

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0
 Version: 1.0.0

 Requires:
 - zet.js
 - serialization.js
 **/
const Serialization = require('../util/serialization')

var namespace = {};
var VERSION = "1.0.0",
    ReferenceData = require('../reference-data'),
    SUPERGLU_VERSION = ReferenceData.version

var ACCEPT_PROPOSAL_ACT, AGREE_ACT, CANCEL_ACT, CALL_FOR_PROPOSAL_ACT,
    CONFIRM_ACT, DISCONFIRM_ACT, FAILURE_ACT, INFORM_ACT, INFORM_IF_ACT,
    INFORM_REF_ACT, NOT_UNDERSTOOD_ACT, PROPAGATE_ACT, PROPOSE_ACT,
    PROXY_ACT, QUERY_IF_ACT, QUERY_REF_ACT, REFUSE_ACT, REJECT_PROPOSAL_ACT,
    REQUEST_ACT, REQUEST_WHEN_ACT, REQUEST_WHENEVER_ACT, SUBSCRIBE_ACT,

    ACTOR_KEY, VERB_KEY, OBJECT_KEY, RESULT_KEY,
    SPEECH_ACT_KEY, TIMESTAMP_KEY, CONTEXT_KEY,
    CONTEXT_CONVERSATION_ID_KEY, CONTEXT_REPLY_WITH_KEY,
    CONTEXT_IN_REPLY_TO_KEY, CONTEXT_REPLY_BY_KEY,
    AUTHORIZATION_KEY, SESSION_ID_KEY,
    CONTEXT_LANGUAGE_KEY, CONTEXT_ONTOLOGY_KEY,
    SUPERGLU_VERSION_KEY, MESSAGE_VERSION_KEY,
    SPEECH_ACT_SET, tokenizeObject, untokenizeObject;

// Core Speech Acts
INFORM_ACT = "Inform";                       // Asserting something
INFORM_REF_ACT = "Inform Ref";               // Assert the name of something
NOT_UNDERSTOOD_ACT = "Not Understood";       // Informing that you didn't understand an act
QUERY_REF_ACT = "Query Ref";                 // Asking the id of an object
REQUEST_ACT = "Request";                     // Requesting action (now)
REQUEST_WHEN_ACT = "Request When";           // Requesting action, conditional on X
REQUEST_WHENEVER_ACT = "Request Whenever";   // Requesting action, whenever X

// Information Speech Acts
CONFIRM_ACT = "Confirm";
DISCONFIRM_ACT = "Disconfirm";
INFORM_IF_ACT = "Inform If";
QUERY_IF_ACT = "Query If";

// Proposal Speech Acts
ACCEPT_PROPOSAL_ACT = "Accept Proposal";
CALL_FOR_PROPOSAL_ACT = "Call for Proposal";
PROPOSE_ACT = "Propose";
REJECT_PROPOSAL_ACT = "Reject Proposal";

// Action Negotiation Status
AGREE_ACT = "Agree";
CANCEL_ACT = "Cancel";
REFUSE_ACT = "Refuse";
FAILURE_ACT = "Failure";

// Relay Actions
PROPAGATE_ACT = "Propagate";
PROXY_ACT = "Proxy";
SUBSCRIBE_ACT = "Subscribe";

SPEECH_ACT_SET = {
    ACCEPT_PROPOSAL_ACT: true, AGREE_ACT: true, CANCEL_ACT: true,
    CALL_FOR_PROPOSAL_ACT: true, CONFIRM_ACT: true, DISCONFIRM_ACT: true,
    FAILURE_ACT: true, INFORM_ACT: true, INFORM_IF_ACT: true,
    INFORM_REF_ACT: true, NOT_UNDERSTOOD_ACT: true, PROPAGATE_ACT: true,
    PROPOSE_ACT: true, PROXY_ACT: true, QUERY_IF_ACT: true,
    QUERY_REF_ACT: true, REFUSE_ACT: true, REJECT_PROPOSAL_ACT: true,
    REQUEST_ACT: true, REQUEST_WHEN_ACT: true, REQUEST_WHENEVER_ACT: true,
    SUBSCRIBE_ACT: true
};

ACTOR_KEY = "actor";
VERB_KEY = "verb";
OBJECT_KEY = "object";
RESULT_KEY = "result";
SPEECH_ACT_KEY = "speechAct";
TIMESTAMP_KEY = "timestamp";
CONTEXT_KEY = "context";

CONTEXT_CONVERSATION_ID_KEY = "conversation-id";
CONTEXT_IN_REPLY_TO_KEY = "in-reply-to";
CONTEXT_REPLY_WITH_KEY = "reply-with";
CONTEXT_REPLY_BY_KEY = "reply-by";

AUTHORIZATION_KEY = "authorization";
SESSION_ID_KEY = "session-id";
CONTEXT_LANGUAGE_KEY = 'language';
CONTEXT_ONTOLOGY_KEY = 'ontology';

SUPERGLU_VERSION_KEY = 'SuperGLU-version';
MESSAGE_VERSION_KEY = 'message-version';

tokenizeObject = Serialization.tokenizeObject;
untokenizeObject = Serialization.untokenizeObject;

/** Message format, for passing information between services
 This is serializable, and can be cast into JSON, along with
 any contained objects (including Messages) that are also serializable.
 **/


namespace.version = VERSION;

namespace.SPEECH_ACT_SET = SPEECH_ACT_SET;
namespace.ACCEPT_PROPOSAL_ACT = ACCEPT_PROPOSAL_ACT;
namespace.AGREE_ACT = AGREE_ACT;
namespace.CANCEL_ACT = CANCEL_ACT;
namespace.CALL_FOR_PROPOSAL_ACT = CALL_FOR_PROPOSAL_ACT;
namespace.CONFIRM_ACT = CONFIRM_ACT;
namespace.DISCONFIRM_ACT = DISCONFIRM_ACT;
namespace.FAILURE_ACT = FAILURE_ACT;
namespace.INFORM_ACT = INFORM_ACT;
namespace.INFORM_IF_ACT = INFORM_IF_ACT;
namespace.INFORM_REF_ACT = INFORM_REF_ACT;
namespace.NOT_UNDERSTOOD_ACT = NOT_UNDERSTOOD_ACT;
namespace.PROPAGATE_ACT = PROPAGATE_ACT;
namespace.PROPOSE_ACT = PROPOSE_ACT;
namespace.PROXY_ACT = PROXY_ACT;
namespace.QUERY_IF_ACT = QUERY_IF_ACT;
namespace.QUERY_REF_ACT = QUERY_REF_ACT;
namespace.REFUSE_ACT = REFUSE_ACT;
namespace.REJECT_PROPOSAL_ACT = REJECT_PROPOSAL_ACT;
namespace.REQUEST_ACT = REQUEST_ACT;
namespace.REQUEST_WHEN_ACT = REQUEST_WHEN_ACT;
namespace.REQUEST_WHENEVER_ACT = REQUEST_WHENEVER_ACT;
namespace.SUBSCRIBE_ACT = SUBSCRIBE_ACT;

namespace.ACTOR_KEY = ACTOR_KEY;
namespace.VERB_KEY = VERB_KEY;
namespace.OBJECT_KEY = OBJECT_KEY;
namespace.RESULT_KEY = RESULT_KEY;
namespace.SPEECH_ACT_KEY = SPEECH_ACT_KEY;
namespace.TIMESTAMP_KEY = TIMESTAMP_KEY;
namespace.CONTEXT_KEY = CONTEXT_KEY;

namespace.CONTEXT_CONVERSATION_ID_KEY = CONTEXT_CONVERSATION_ID_KEY;
namespace.CONTEXT_IN_REPLY_TO_KEY = CONTEXT_IN_REPLY_TO_KEY;
namespace.CONTEXT_REPLY_WITH_KEY = CONTEXT_REPLY_WITH_KEY;
namespace.CONTEXT_REPLY_BY_KEY = CONTEXT_REPLY_BY_KEY;

namespace.AUTHORIZATION_KEY = AUTHORIZATION_KEY;
namespace.SESSION_ID_KEY = SESSION_ID_KEY;
namespace.CONTEXT_LANGUAGE_KEY = CONTEXT_LANGUAGE_KEY;
namespace.CONTEXT_ONTOLOGY_KEY = CONTEXT_ONTOLOGY_KEY;

namespace.SUPERGLU_VERSION_KEY = SUPERGLU_VERSION_KEY;
namespace.MESSAGE_VERSION_KEY = MESSAGE_VERSION_KEY;

module.exports = namespace
