# -*- coding: utf-8 -*-
# Core Speech Acts
INFORM_ACT = "Inform"                       # Asserting something
INFORM_REF_ACT = "Inform Ref"               # Assert the name of something
NOT_UNDERSTOOD_ACT = "Not Understood"       # Informing that you didn't understand an act
QUERY_REF_ACT = "Query Ref"                 # Asking the id/name of an object
REQUEST_ACT = "Request"                     # Requesting action (now)
REQUEST_WHEN_ACT = "Request When"           # Requesting action, conditional on X
REQUEST_WHENEVER_ACT = "Request Whenever"   # Requesting action, whenever X

# Information Speech Acts
CONFIRM_ACT = "Confirm"
DISCONFIRM_ACT = "Disconfirm"
INFORM_IF_ACT = "Inform If"
QUERY_IF_ACT = "Query If"

# Proposal Speech Acts
ACCEPT_PROPOSAL_ACT = "Accept Proposal"
CALL_FOR_PROPOSAL_ACT = "Call for Proposal"
PROPOSE_ACT = "Propose"
CONFIRM_PROPOSAL_ACT = "Confirm Proposal"
REJECT_PROPOSAL_ACT = "Reject Proposal"
RESEND_MSG_WITH_ATTEMPT_COUNTS = "Resend with Attempt Counts"
QUIT_IN_X_TIME = "Quit in x Seconds"
RESEND_MSG_WITH_DEPRIORITZATION = "Resend with Deprioritized Service"
PROPOSED_MESSAGE = "Proposed Message"
PROPOSED_MESSAGE_ACKNOWLEDGMENT = "Proposed Message Acknowledgement"
CONFIRM_PROPOSAL_ACT = "Confirm Proposal"
ALL_TIME_ACCEPT_PROPOSAL_ACK = "Accept at all times"
X_TIME_ACCEPT_PROPOSAL_ACK = "Accept for time X"

# Action Negotiation Status
AGREE_ACT = "Agree"
CANCEL_ACT = "Cancel"
REFUSE_ACT = "Refuse"
FAILURE_ACT = "Failure"

# Relay Actions
PROPAGATE_ACT = "Propagate"
PROXY_ACT = "Proxy"
SUBSCRIBE_ACT = "Subscribe"

SPEECH_ACT_SET = frozenset([ACCEPT_PROPOSAL_ACT, AGREE_ACT, CANCEL_ACT, CALL_FOR_PROPOSAL_ACT,
                            CONFIRM_ACT, DISCONFIRM_ACT, FAILURE_ACT, INFORM_ACT, INFORM_IF_ACT,
                            INFORM_REF_ACT,  NOT_UNDERSTOOD_ACT, PROPAGATE_ACT, PROPOSE_ACT,
                            PROXY_ACT, QUERY_IF_ACT, QUERY_REF_ACT, REFUSE_ACT, REJECT_PROPOSAL_ACT,
                            RESEND_MSG_WITH_ATTEMPT_COUNTS, QUIT_IN_X_TIME, RESEND_MSG_WITH_DEPRIORITZATION,
                            PROPOSED_MESSAGE, PROPOSED_MESSAGE_ACKNOWLEDGMENT, CONFIRM_PROPOSAL_ACT,
                            ALL_TIME_ACCEPT_PROPOSAL_ACK, X_TIME_ACCEPT_PROPOSAL_ACK,
                            REQUEST_ACT, REQUEST_WHEN_ACT, REQUEST_WHENEVER_ACT, SUBSCRIBE_ACT])
