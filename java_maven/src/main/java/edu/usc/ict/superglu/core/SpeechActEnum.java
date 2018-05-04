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
    REJECT_PROPOSAL_ACT("Reject Proposal");


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
