package edu.usc.ict.superglu.core;

import java.util.Arrays;
import java.util.List;

public enum SpeechActEnum {

    INFORM_ACT("Inform"),                       //# Asserting something
    INFORM_REF_ACT("Inform Ref"),               //# Assert the name of something
    NOT_UNDERSTOOD_ACT("Not Understood"),      // # Informing that you didn't understand an act
    QUERY_REF_ACT("Query Ref"),                // # Asking the id/name of an object
    REQUEST_ACT("Request"),                    // # Requesting action (now)
    REQUEST_WHEN_ACT("Request When"),          // # Requesting action, conditional on X
    REQUEST_WHENEVER_ACT("Request Whenever"),   //# Requesting action, whenever X
    PROPOSE_ACT("Propose"),
    ACCEPT_PROPOSAL_ACT("Accept Proposal"),
    CONFIRM_PROPOSAL_ACT("Confirm Proposal"),
    REJECT_PROPOSAL_ACT("Reject Proposal"),
    PROPOSED_MESSAGE("Proposed Message"),
    PROPOSED_MESSAGE_ACKNOWLEDGMENT("Proposed Message Acknowledgement"),
    RESEND_MSG_WITH_ATTEMPT_COUNTS("Resend with Attempt Counts"), //Fail Soft Strategy 1 - Resend messages with attempt count and Fail self if response still not received. 
    RESEND_MSG_WITH_DEPRIORITZATION("Resend with Deprioritized Service"), //Fail Soft Strategy 2 - Resend messages with Deprioritized list of Services that have rejected/refused service before.  
    QUIT_IN_X_TIME("Quit in x Seconds"), //Fail Soft Strategy 3 - Quit the sending of message after waiting for x seconds.
    ALL_TIME_ACCEPT_PROPOSAL_ACK("Accept at all times"), // Policy Type 1 - Accept Proposal Acknowledgement from Servers Full Time.
    X_TIME_ACCEPT_PROPOSAL_ACK("Accept for time X"); // Policy Type 2 - Accept Proposal Acknowledgement from Servers for time X.


    private String value;

    SpeechActEnum(final String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return this.getValue();
    }

    public static SpeechActEnum getEnum(String value) {
        List<SpeechActEnum> list = Arrays.asList(SpeechActEnum.values());
        return list.stream().filter(m -> m.value.equals(value)).findAny().orElse(null);
    }
}
