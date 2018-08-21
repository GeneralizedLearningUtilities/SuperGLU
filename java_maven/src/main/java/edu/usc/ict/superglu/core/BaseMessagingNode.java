package edu.usc.ict.superglu.core;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Consumer;
import java.util.function.Predicate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;

/**
 * """ Base class for messaging """
 *
 * @author auerbach
 */
public class BaseMessagingNode {

	protected Logger log = LoggerFactory.getLogger(this.getClass().getSimpleName());

	protected String id;
	protected Map<String, Pair<Message, Consumer<Message>>> requests;
	protected Predicate<BaseMessage> conditions;
	protected Map<String, BaseMessagingNode> nodes;
	protected List<ExternalMessagingHandler> handlers;
	protected Map<String, Object> context;

	protected List<BlackWhiteListEntry> blackList;
	protected List<BlackWhiteListEntry> whiteList;

	private static boolean CATCH_BAD_MESSAGES = false;

	public static final String ORIGINATING_SERVICE_ID_KEY = "originatingServiceId";
	public static final String SESSION_KEY = "sessionId";
	
	protected static final boolean USE_BLACK_WHITE_LIST = true;
	
	//Added Attributes for Proposal Pattern
	protected Map<String, Proposal> proposals;
	protected static final long SEND_MSG_SLEEP_TIME = 10;// Create Default and sender service can override this
	protected static final String PROPOSAL_ATTEMPT_COUNT = "noOfAttemptsForProposal";
	protected static final String FAIL_SOFT_STRATEGY= "failSoftStrategyForProposedMsg";
	protected static final String QUIT_IN_TIME= "quitInTime";
	protected static final String PROPOSED_MSG_ATTEMPT_COUNT = "noOfAttemptsForProposedMsg";
	protected Map<String, Integer> prioritizedAcceptedServiceIds;
	protected List<String> demotedAcceptedServiceIds;
	
	public BaseMessagingNode(String anId, Predicate<BaseMessage> conditions, Collection<BaseMessagingNode> nodes,
			List<ExternalMessagingHandler> handlers, List<BlackWhiteListEntry> blackList,
			List<BlackWhiteListEntry> whiteList) {
		this.nodes = new HashMap<>();

		if (anId == null)
			this.id = UUID.randomUUID().toString();
		else
			this.id = anId;

		this.requests = new HashMap<>();

		if (conditions != null)
			this.conditions = conditions;

		this.requests = new HashMap<>();

		this.addNodes(nodes);

		if (handlers != null)
			this.handlers = handlers;
		else
			this.handlers = new ArrayList<>();

		this.context = new HashMap<>();

		if (blackList != null)
			this.blackList = blackList;
		else
			this.blackList = new ArrayList<>();

		if (whiteList != null)
			this.whiteList = whiteList;
		else
			this.whiteList = new ArrayList<>();
		
		this.proposals = new HashMap<>();
		this.prioritizedAcceptedServiceIds = new LinkedHashMap<>();
		this.demotedAcceptedServiceIds = new ArrayList<>();
	}

	protected boolean acceptIncomingMessge(BaseMessage msg) {
		boolean result = true;

		if (USE_BLACK_WHITE_LIST) {
			// black list takes priority of white list.
			for (BlackWhiteListEntry entry : this.whiteList) {
				if (entry.evaluateMessage(msg)) {
					result = true;
					break;
				}
			}

			for (BlackWhiteListEntry entry : this.blackList) {
				if (entry.evaluateMessage(msg)) {
					log.info(this.id + " recieved a blacklisted message: "
							+ SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT)
							+ "| message will be ignored");
					result = false;
					break;
				}
			}
		}

		return result;
	}

	/**
	 * handler for receiving messages
	 * 
	 * @param msg
	 *            incoming message
	 * @return true if we should handle the message, false otherwise.
	 */
	public boolean receiveMessage(BaseMessage msg) {
		if (!acceptIncomingMessge(msg))
			return false;

		//log.info(this.id + " received MSG:" + this.messageToString(msg));
		
		if (msg instanceof Message)
			this.triggerRequests((Message) msg);

		for (ExternalMessagingHandler handler : this.handlers)
			handler.handleMessage(msg);

		return true;
	}

	public void sendMessage(BaseMessage msg) {
		//log.debug(this.id + " is sending " + this.messageToString(msg));
		String senderID = (String) msg.getContextValue(ORIGINATING_SERVICE_ID_KEY);
		this.distributeMessage(msg, senderID);
	}
	
	/**
	 * Sends Proposal Request Message With Attempt Count. 
	 * @param msg
	 * @param noOfAttempts
	 */
	public void sendProposal(Message msg, int noOfAttempts) {
		new Thread(new Runnable() {
			public void run() {
				int count = 1;
				String proposalId = msg.getContext().get(Message.PROPOSAL_KEY).toString();
				proposals.get(proposalId).setAcknowledgementReceived(false);
				while (count <= noOfAttempts && !proposals.get(proposalId).isAcknowledgementReceived()) {
					log.info("Send Proposal Request - Attempt " + (count));
					sendMessage(msg);
					count++;
		            try {
						Thread.sleep(SEND_MSG_SLEEP_TIME);        //sleeping to wait for proposal acceptances
						if(!proposals.get(proposalId).isAcknowledgementReceived())
							log.warn("Timeout.");
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
				if(count > noOfAttempts && !proposals.get(proposalId).isProposalProcessed()) {
					log.error("No Respose Received.");	
				}
			}
		}).run();
	}
	
	/**
	 * Decides Proposed Message Strategy and delegates messages accordingly 
	 * to sendProposedMessage(BaseMessage msg, String proposalId).
	 * @param proposalId
	 */
	public void sendProposedMessage(String proposalId) {
		Proposal proposal = this.proposals.get(proposalId);
		if(!proposal.isProposalProcessed()) {
			String failSoftStrategy = proposal.getRetryParams().get(FAIL_SOFT_STRATEGY) != null ? proposal.getRetryParams().get(FAIL_SOFT_STRATEGY).toString() : null;
			if(failSoftStrategy != null) {
				if(SpeechActEnum.getEnum(failSoftStrategy) == SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS) {
					sendProposedMsgWithAttemptCnt(proposal);
				} else if(SpeechActEnum.getEnum(failSoftStrategy) == SpeechActEnum.QUIT_IN_X_TIME) {
					sendProposedMsgWithQuitXTime(proposal);
				} else if(SpeechActEnum.getEnum(failSoftStrategy) == SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION) {
					sendProposedMsgWithPrioritization(proposal);
				}
			} else {
				//No Strategy.
				 for(Iterator<Map.Entry<String, ProposedMessage>> it = proposal.getProposedMessages().entrySet().iterator(); it.hasNext(); ) {
				      Map.Entry<String, ProposedMessage> entry = it.next();
				    	  if(entry.getValue().getNumberOfRetries() < 2) {
				    		  	entry.getValue().setNumberOfRetries(entry.getValue().getNumberOfRetries() + 1);
								log.info("Send Proposed Message - Attempt " + (entry.getValue().getNumberOfRetries()));
								sendProposedMessage(entry.getValue().getMsg(), proposalId);
				    	  }
				    }
				
			}
		}
		
	}
	
	/**
	 * Sends Proposed Message.
	 * @param msg
	 * @param proposalId
	 */
	public void sendProposedMessage(BaseMessage msg, String proposalId) {
		new Thread(new Runnable() {
			public void run() {
				Consumer<Message> proposalMsgSuccessFunction = i -> log.info("Proposal Message Processed");
				makeProposedMessageRequest((Message) msg, proposalMsgSuccessFunction);
				try {
					Thread.sleep(SEND_MSG_SLEEP_TIME); // sleeping for 2 seconds in order to receive all proposal acceptances
					if (proposals.get(proposalId).getProposedMessages().containsKey(msg.getId())) {
						log.info("Seems Proposed Message Hasn't been Processed");
						retryProposal(proposalId);
					}
					else
						log.info("Proposed Message Sent Successfully");
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}).run();
	}
	
	
	/**
	 * Fail Soft Strategy 1 - Send Proposed Message With Attempt Count.
	 * @param proposal
	 */
	private void sendProposedMsgWithAttemptCnt(Proposal proposal) {
		int attemptCount = Integer.parseInt(proposal.getRetryParams().get(PROPOSED_MSG_ATTEMPT_COUNT).toString());			
		for(Iterator<Map.Entry<String, ProposedMessage>> it = proposal.getProposedMessages().entrySet().iterator(); it.hasNext(); ) {
			Map.Entry<String, ProposedMessage> entry = it.next();
		    if(entry.getValue().getNumberOfRetries() < attemptCount) {
		    	entry.getValue().setNumberOfRetries(entry.getValue().getNumberOfRetries() + 1);
				log.info("Send Proposed Message - Attempt " + (entry.getValue().getNumberOfRetries()));
				sendProposedMessage(entry.getValue().getMsg(), proposal.getId());
		    }
		 }
	}
	
	/**
	 * Fail Soft Strategy 2 - Send Proposed Message With Quit in X Time.
	 * @param proposal
	 */
	private void sendProposedMsgWithQuitXTime(Proposal proposal) {
		Long duration = Long.parseLong(proposal.getRetryParams().get(QUIT_IN_TIME).toString());			
		for(Iterator<Map.Entry<String, ProposedMessage>> it = proposal.getProposedMessages().entrySet().iterator(); it.hasNext(); ) {
			Map.Entry<String, ProposedMessage> entry = it.next();
		    if((System.currentTimeMillis() - entry.getValue().getLastTimeSent()) < duration) {
		    	entry.getValue().setNumberOfRetries(entry.getValue().getNumberOfRetries() + 1);
		    	log.info("Send Proposed Message - Attempt " + (entry.getValue().getNumberOfRetries() -1));
				sendProposedMessage(entry.getValue().getMsg(), proposal.getId());
		    } else {
		    	log.info("Cannot Send Message. Attempt to Send Quit After " + (duration) + " seconds.");
		    }
		 }
	}
	
	/**
	 * 
	 * @param proposal
	 */
	private void sendProposedMsgWithPrioritization(Proposal proposal) {
		if(prioritizedAcceptedServiceIds.isEmpty()) 
			log.info("Exhausted All Services");
		else {
			log.info("Attempting to Send Proposed Message After Prioritization");
			for(Iterator<Map.Entry<String, ProposedMessage>> it = proposal.getProposedMessages().entrySet().iterator(); it.hasNext(); ) {
				Map.Entry<String, ProposedMessage> entry = it.next();
				sendProposedMessage(entry.getValue().getMsg(), proposal.getId());
			}
		}
	}
	

	/**
	 * Handle an arriving message from some source. Services other than gateways
	 * should generally not need to change this.
	 *
	 * @param msg:
	 *            The message arriving
	 * @param senderId:
	 *            The id string for the sender of this message.
	 **/
	public void handleMessage(BaseMessage msg, String senderId) {
		this.receiveMessage(msg);
	}

	/**
	 * """ Pass a message down all interested children (except sender) """
	 *
	 * @param msg
	 * @param senderId
	 * @return true if message is distributed, false if not.
	 */
	public void distributeMessage(BaseMessage msg, String senderId) {
		this.distributeMessage_impl(this.nodes, msg, senderId);
	}
	
	
	protected boolean isMessageOnGatewayBlackList(BaseMessagingNode destination, BaseMessage msg)
	{
		return false;
	}
	
	
	protected boolean isMessageOnGatewayWhiteList(BaseMessagingNode destination, BaseMessage msg)
	{
		return true;
	}

	/**
	 * Internal implementation of DistributeMessage ""
	 * " Implement passing a message down all interested children (except sender) "
	 * ""
	 *
	 * @param nodes
	 * @param msg
	 * @param senderId
	 */
	protected void distributeMessage_impl(Map<String, BaseMessagingNode> nodes, BaseMessage msg, String senderId) {
		for (BaseMessagingNode node : nodes.values()) {
			if(!isMessageOnGatewayBlackList(node, msg) && isMessageOnGatewayWhiteList(node, msg))
				if (node.id != senderId && (node.getMessageConditions() == null || node.getMessageConditions().test(msg)))
					node.receiveMessage(msg);
		}
	}

	/**
	 * Transmit the message to another node
	 **/
	protected void transmitMessage(BaseMessagingNode node, BaseMessage msg, String senderId) {
		node.handleMessage(msg, senderId);
	}

	// """ Function to check if this node is interested in this message type """
	public Predicate<BaseMessage> getMessageConditions() {
		return conditions;
	}

	/* handler management */

	public void addHandler(ExternalMessagingHandler handler) {
		this.handlers.add(handler);
	}

	/* Node Management */

	/**
	 * Connect nodes to this node
	 **/
	public void addNodes(Collection<BaseMessagingNode> newNodes) {
		if (newNodes != null) {
			for (BaseMessagingNode node : newNodes) {
				addNode(node);
			}
		}
	}

	public void addNode(BaseMessagingNode node) {
		node.onBindToNode(this);
		this.onBindToNode(node);
	}

	public Collection<BaseMessagingNode> getNodes() {
		return this.nodes.values();
	}

	/**
	 * Register the node and signatures of messages that the node is interested
	 * in
	 **/
	public void onBindToNode(BaseMessagingNode node) {
		if (!this.nodes.containsKey(node.getId())) {
			this.nodes.put(node.getId(), node);
		}
	}

	/**
	 * This removes this node from a connected node (if any)
	 **/
	public void onUnbindToNode(BaseMessagingNode node) {
		if (this.nodes.containsKey(node.getId())) {
			this.nodes.remove(node.getId());
		}
	}

	protected Collection<Pair<Message, Consumer<Message>>> getRequests() {
		return this.requests.values();
	}

	protected void addRequest(Message msg, Consumer<Message> callback) {
		if (callback != null) {
			Message clone = (Message) msg.clone(false);
			Pair<Message, Consumer<Message>> messageAndCallback = new Pair<Message, Consumer<Message>>(clone, callback);

			this.requests.put(msg.getId(), messageAndCallback);
		}
	}

	protected void makeRequest(Message msg, Consumer<Message> callback) {
		this.addRequest(msg, callback);
		this.sendMessage(msg);
	}

	/**
	 * Makes Proposed Message Request
	 * @param msg
	 * @param callback
	 */
	protected void makeProposedMessageRequest(Message msg, Consumer<Message> callback) {
		this.addProposedMessageRequest(msg, callback);
		this.sendMessage(msg);
	}
	
	/**
	 * Adds Proposed Message Request callback function.
	 * @param msg
	 * @param callback
	 */
	protected void addProposedMessageRequest(Message msg, Consumer<Message> callback) {
		if (callback != null) {
			Pair<Message, Consumer<Message>> messageAndCallback = new Pair<Message, Consumer<Message>>(msg, callback);
			this.requests.put(msg.getId(), messageAndCallback);
		}
	}

	protected void triggerRequests(Message msg) {
		String convoId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, null);
		if (convoId != null) {
			if (this.requests.containsKey(convoId)) {
				String key = convoId;
				Pair<Message, Consumer<Message>> value = this.requests.get(key);
				Message oldMsg = value.getFirst();
				Consumer<Message> callback = value.getSecond();
				callback.accept(msg);
				if (!oldMsg.getSpeechAct().equals(SpeechActEnum.REQUEST_WHENEVER_ACT))
					this.requests.remove(key);
			} else if (msg.getSpeechAct().equals(SpeechActEnum.ACCEPT_PROPOSAL_ACT)
					&& this.proposals.containsKey(convoId)) {
				// When the proposal request is accepted, it executes the callback function and
				this.proposals.get(convoId).setProposalProcessed(true);
				Consumer<Message> callback = this.proposals.get(convoId).getSuccessCallbackFn() != null ?
						this.proposals.get(convoId).getSuccessCallbackFn() : null;
				if (callback != null)
					callback.accept(msg);

			}
		}
	}

	protected BaseMessage createRequestReply(BaseMessage msg) {
		String oldId = msg.getId();
		BaseMessage copy = (BaseMessage) msg.clone(true);
		copy.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId);
		return copy;
	}

	// # Pack/Unpack Messages
	public String messageToString(BaseMessage msg) {
		return SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
	}

	public BaseMessage stringToMessage(String msgAsString) {
		BaseMessage result = null;
		if (CATCH_BAD_MESSAGES) {

			try {
				result = (Message) SerializationConvenience.nativeizeObject(msgAsString,
						SerializationFormatEnum.JSON_FORMAT);
			} catch (Exception e) {
				log.error("ERROR: could not process message data received.  Received: " + msgAsString);
				log.error("Exception Caught:" + e.toString());
			}
		} else {
			result = (BaseMessage) SerializationConvenience.nativeizeObject(msgAsString,
					SerializationFormatEnum.JSON_FORMAT);
		}

		return result;
	}

	public List<String> messagesToStringList(List<BaseMessage> msgs) {
		List<String> result = new ArrayList<>();

		for (BaseMessage msg : msgs) {
			result.add(messageToString(msg));
		}

		return result;
	}

	public List<BaseMessage> stringListToMessages(List<String> strMsgs) {
		List<BaseMessage> result = new ArrayList<>();

		for (String strMsg : strMsgs) {
			BaseMessage msg = this.stringToMessage(strMsg);
			result.add(msg);
		}

		return result;
	}
	
	/*
	 * Making Proposal performs 2 Tasks: maintains a list of all proposals that will be sent across and actually sends the message.  
	 * It generates a random Proposal ID, attaches it to the proposal and sends the message across for further distribution.
	 */
	protected void makeProposal(Message msg, Consumer<Message> successCallback, Map<String, Object> retryParams, String policyType) {
		String proposalId = null;
		if(msg.getContext().get(Message.PROPOSAL_KEY) == null) {
			proposalId = UUID.randomUUID().toString();
			msg.getContext().put(Message.PROPOSAL_KEY, proposalId);
		}
		msg.getContext().put(Message.CONTEXT_CONVERSATION_ID_KEY, proposalId);
		Proposal makePropsalPckt = new Proposal(proposalId, msg, false, successCallback, retryParams, policyType, System.currentTimeMillis());
		
		makePropsalPckt.setPolicyType(SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.toString());
		
		//Checking if the retryParams are set. If set, then calls functions accordingly.
		if(retryParams != null) { 
			if(retryParams.containsKey(PROPOSAL_ATTEMPT_COUNT)) {
				int proposalNoOfAttempts = Integer.parseInt(retryParams.get(PROPOSAL_ATTEMPT_COUNT).toString());
				if(retryParams.containsKey(FAIL_SOFT_STRATEGY)) {
					SpeechActEnum failSoftStrategy = SpeechActEnum.getEnum(retryParams.get(FAIL_SOFT_STRATEGY).toString());
					makePropsalPckt.setFailSoftStrategyForProposedMsg(failSoftStrategy.toString());
					if(failSoftStrategy == SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS) {
						makePropsalPckt.getRetryParams().put(PROPOSED_MSG_ATTEMPT_COUNT,Integer.parseInt(retryParams.get(PROPOSED_MSG_ATTEMPT_COUNT).toString()));
					} else if(failSoftStrategy == SpeechActEnum.QUIT_IN_X_TIME) {
						makePropsalPckt.getRetryParams().put(QUIT_IN_TIME, Long.parseLong(retryParams.get(QUIT_IN_TIME).toString()));
					} 
				}
				this.proposals.put(proposalId, makePropsalPckt);
				this.sendProposal(msg, proposalNoOfAttempts);
			} else {
				this.proposals.put(proposalId, makePropsalPckt);
				this.sendMessage(msg);
			}
		} else {
			this.proposals.put(proposalId, makePropsalPckt);
			this.sendMessage(msg);
		}
	}
	
	/*
	 * This Overridden function of Make Proposal is used when proposal exists for which Proposed Message function has failed.
	 */
	protected void retryProposal(String proposalId) {
		Proposal proposal = this.proposals.get(proposalId);
		this.sendProposal(proposal.getProposal(), Integer.parseInt(proposal.getRetryParams().get(PROPOSAL_ATTEMPT_COUNT).toString()));
	}
		
	public String getId() {
		return this.id;
	}

	public Map<String, Object> getContext() {
		return context;
	}

	public void setContext(Map<String, Object> context) {
		this.context = context;
	}

	public void addToContext(String key, Object value) {
		this.context.put(key, value);
	}

	/**
	 * @return the proposals
	 */
	public Map<String, Proposal> getProposals() {
		return proposals;
	}

	/**
	 * @param proposals the proposals to set
	 */
	public void setProposals(Map<String, Proposal> proposals) {
		this.proposals = proposals;
	}

}
