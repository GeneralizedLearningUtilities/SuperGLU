package edu.usc.ict.superglu.core;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Proposal Structure
 *
 * @author rthaker
 */

public class Proposal {

	private String id;

	private Message proposal;

	private boolean proposalProcessed;

	private boolean acknowledgementReceived;

	private Consumer<Message> successCallbackFn;

	private Map<String, Object> retryParams;

	private String policyType;

	private Map<String, ProposedMessage> proposedMessages;

	private String failSoftStrategyForProposedMsg;
	
	private Long proposedTime;

	public Proposal(String id) {
		this.id = id;
		proposal = null;
		proposedMessages = new HashMap<>();
		proposalProcessed = false;
		successCallbackFn = null;
		retryParams = null;
		policyType = SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.getValue();
		failSoftStrategyForProposedMsg = null;
		acknowledgementReceived = false;
		proposedTime = null;
	}

	public Proposal(String id, Message proposal, Map<String, ProposedMessage> proposedMsgs, boolean proposalProcessed,
			Consumer<Message> successCallbackFn, Map<String, Object> retryParams, String policyType, Long proposedTime) {
		this.id = id;
		this.proposal = proposal;
		this.proposedMessages = proposedMsgs;
		this.proposalProcessed = proposalProcessed;
		this.successCallbackFn = successCallbackFn;
		this.retryParams = retryParams;
		this.policyType = policyType;
		failSoftStrategyForProposedMsg = null;
		acknowledgementReceived = false;
		this.proposedTime = proposedTime;
	}

	public Proposal(String id, Message proposal, Message proposedMsg, boolean proposalProcessed,
			Consumer<Message> successCallbackFn, Map<String, Object> retryParams, String policyType, Long proposedTime) {
		this.id = id;
		this.proposal = proposal;
		this.proposedMessages = new HashMap<>();
		ProposedMessage msg = new ProposedMessage(proposedMsg.getId(), proposedMsg, 1);
		this.proposedMessages.put(proposedMsg.getId(), msg);
		this.proposalProcessed = proposalProcessed;
		this.successCallbackFn = successCallbackFn;
		this.retryParams = retryParams;
		this.policyType = policyType;
		failSoftStrategyForProposedMsg = null;
		acknowledgementReceived = false;
		this.proposedTime = proposedTime;
	}

	public Proposal(String id, Message proposal, boolean proposalProcessed, Consumer<Message> successCallbackFn,
			Map<String, Object> retryParams, String policyType, Long proposedTime) {
		this.id = id;
		this.proposal = proposal;
		this.proposedMessages = new HashMap<>();
		this.proposalProcessed = proposalProcessed;
		this.successCallbackFn = successCallbackFn;
		this.retryParams = retryParams;
		this.policyType = policyType;
		failSoftStrategyForProposedMsg = null;
		acknowledgementReceived = false;
		this.proposedTime = proposedTime;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public Message getProposal() {
		return proposal;
	}

	public void setProposal(Message proposal) {
		this.proposal = proposal;
	}

	public boolean isProposalProcessed() {
		return proposalProcessed;
	}

	public void setProposalProcessed(boolean proposalProcessed) {
		this.proposalProcessed = proposalProcessed;
	}

	public Consumer<Message> getSuccessCallbackFn() {
		return successCallbackFn;
	}

	public void setSuccessCallbackFn(Consumer<Message> successCallbackFn) {
		this.successCallbackFn = successCallbackFn;
	}

	public Map<String, Object> getRetryParams() {
		return retryParams;
	}

	public void setRetryParams(Map<String, Object> retryParams) {
		this.retryParams = retryParams;
	}

	public String getPolicyType() {
		return policyType;
	}

	public void setPolicyType(String policyType) {
		this.policyType = policyType;
	}

	public Map<String, ProposedMessage> getProposedMsgs() {
		return this.proposedMessages;
	}

	public void setProposedMsgs(Map<String, ProposedMessage> proposedMsgs) {
		this.proposedMessages = proposedMsgs;
	}

	public Map<String, ProposedMessage> getProposedMessages() {
		return proposedMessages;
	}

	public void setProposedMessages(Map<String, ProposedMessage> proposedMessages) {
		this.proposedMessages = proposedMessages;
	}

	public String getFailSoftStrategyForProposedMsg() {
		return failSoftStrategyForProposedMsg;
	}

	public void setFailSoftStrategyForProposedMsg(String failSoftStrategyForProposedMsg) {
		this.failSoftStrategyForProposedMsg = failSoftStrategyForProposedMsg;
	}

	public boolean isAcknowledgementReceived() {
		return acknowledgementReceived;
	}

	public void setAcknowledgementReceived(boolean acknowledgementReceived) {
		this.acknowledgementReceived = acknowledgementReceived;
	}
	
	public Long getProposedTime() {
		return proposedTime;
	}

	public void setProposedTime(Long proposedTime) {
		this.proposedTime = proposedTime;
	}
	
}
