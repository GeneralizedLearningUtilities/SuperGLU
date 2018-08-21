package edu.usc.ict.superglu;

import static edu.usc.ict.superglu.core.Message.CONTEXT_CONVERSATION_ID_KEY;
import static edu.usc.ict.superglu.core.Message.CONTEXT_IN_REPLY_TO_KEY;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.function.Consumer;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.HTTPRequestVerbEnum;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.core.Proposal;
import edu.usc.ict.superglu.core.ProposedMessage;
import edu.usc.ict.superglu.core.RESTMessage;
import edu.usc.ict.superglu.core.SpeechActEnum;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.services.RESTMessenger;

public class ProposalUseCasesTest {
	
	protected Logger logger = LoggerFactory.getLogger(this.getClass().getSimpleName());
	
	private List<BaseMessage> testMessages;
	
	public RESTMessenger messenger;
	
	private HintService hintService1;
	private HintService hintService2;
	
	private HintPresenter hintPresenter;
	
	private MessagingGateway gateway;
	
	@Before
    public void setUp() {
		List<BaseMessagingNode> nodes = new ArrayList<>();
		messenger = new RESTMessenger("messenger");
		hintService1 = new HintService("hintService1");
		hintService2 = new HintService("hintService2");
		hintPresenter = new HintPresenter("hintPresenter");
		nodes.add(hintService1);
        nodes.add(hintService2);
        nodes.add(hintPresenter);
        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);
        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        hintPresenter.addNode(gateway);
        messenger.addNode(gateway);
        messenger.addNode(hintService1);
        messenger.addNode(hintService2);
		testMessages = buildMessages();  
    }

	private List<BaseMessage> buildMessages() {
		List<BaseMessage> result = new ArrayList<>();
	    Message msg1 = new Message("penguin", "eats", "fish", "Sending Proposal", SpeechActEnum.PROPOSE_ACT, null, new HashMap<>(), "msg1");
	    result.add(msg1);
	    Message msg2 = new Message("penguin", "eats", "fish", "Accepting Proposal", SpeechActEnum.ACCEPT_PROPOSAL_ACT, null, new HashMap<>(), "msg2");
	    result.add(msg2);
	    Message msg3 = new Message("penguin", "eats", "fish", "Confirming Proposal", SpeechActEnum.CONFIRM_PROPOSAL_ACT, null, new HashMap<>(), "msg3");
	    result.add(msg3);
	    return result;
	}
	
	class HintPresenter extends BaseService {
    	SpeechActEnum failStrategyToTest = null;
    	String acceptedProposalConversationId, acceptedProposalServiceId;
    	
    	List<String> acceptedServiceIds = new ArrayList<>();
    	Map<String, Boolean> proposedMsgAudit = new HashMap<>();
    	
    	
        public HintPresenter(String id) {
            super(id, null);
            acceptedProposalConversationId = "";
            acceptedProposalServiceId = "";
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
            super.receiveMessage(msg);
            logger.info("============================================================================");
            logger.info("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
            	logger.info("SpeechAct : " + ((Message) msg).getSpeechAct());
                String proposalIdOfMessage =  (String) msg.getContextValue(Message.PROPOSAL_KEY);
                if (((Message) msg).getSpeechAct() == SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
                	Proposal proposal = this.proposals.get(proposalIdOfMessage);
                	if(SpeechActEnum.getEnum(proposal.getPolicyType()) == SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK ||
                			(SpeechActEnum.getEnum(proposal.getPolicyType()) == SpeechActEnum.X_TIME_ACCEPT_PROPOSAL_ACK &&
                			(System.currentTimeMillis() - proposal.getProposedTime()) < Long.parseLong(proposal.getRetryParams().get("acceptFor").toString()))) {
                    acceptedProposalConversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                    acceptedProposalServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);
                    logger.info("******************\nACCEPTED BY : " + acceptedProposalServiceId + "******************\n");
                    Message msg3 = (Message) testMessages.get(2).clone(false);
                    msg3.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg3.setContextValue(CONTEXT_IN_REPLY_TO_KEY, acceptedProposalConversationId);
                    msg3.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage);
                    msg3.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + this.getId() + "_" + System.currentTimeMillis());
                    this.proposals.get(proposalIdOfMessage).setAcknowledgementReceived(true);
                    //Sends Confirmation Message.
                    this.sendMessage(msg3);
                    acceptedServiceIds.add(acceptedProposalServiceId);
                    
                    if(this.prioritizedAcceptedServiceIds.containsKey(acceptedProposalServiceId)) {
                    	int triedFor = this.prioritizedAcceptedServiceIds.get(acceptedProposalServiceId);
                    	if((triedFor + 1) > 3) {
                    		this.prioritizedAcceptedServiceIds.remove(acceptedProposalServiceId);
                    		this.demotedAcceptedServiceIds.add(acceptedProposalServiceId);
                    	}
                    	else
                    		this.prioritizedAcceptedServiceIds.put(acceptedProposalServiceId, triedFor + 1);
                    } else if(!this.demotedAcceptedServiceIds.contains(acceptedProposalServiceId)){
                    	this.prioritizedAcceptedServiceIds.put(acceptedProposalServiceId, 1);
                    }
                    
                    //Proposal Request has been successfully processed. Below code, sends the Proposed Message.
                    Message msg4 = (Message) testMessages.get(2).clone(false);
                    if(!this.proposedMsgAudit.containsKey(msg4.getId()) || (this.proposedMsgAudit.containsKey(msg4.getId()) && !this.proposedMsgAudit.get(msg4.getId()))){
                    	proposal = this.proposals.get(proposalIdOfMessage);
                    	this.proposedMsgAudit.put(msg4.getId(), false);
                    	msg4.setSpeechAct(SpeechActEnum.PROPOSED_MESSAGE);
                        msg4.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                        msg4.setContextValue(CONTEXT_IN_REPLY_TO_KEY, acceptedProposalConversationId);
                        msg4.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage);
                        
                        
                        if (SpeechActEnum.getEnum(proposal.getFailSoftStrategyForProposedMsg()) == SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION) {
                        	if(!this.prioritizedAcceptedServiceIds.isEmpty()) 
                        		msg4.setContextValue("toBeServicedBy", this.prioritizedAcceptedServiceIds.entrySet().iterator().next().getKey());
                        } else
                        	msg4.setContextValue("toBeServicedBy", acceptedServiceIds.get(0));
                        
                        
                        msg4.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + this.getId() + "_" + System.currentTimeMillis());
                        ProposedMessage proposedMessage = null;
                        
                       	if(proposal.getProposedMessages().size() < 1) {
                        	proposedMessage = new ProposedMessage(msg4.getId(), msg4, 0);
                       		proposedMessage.setLastTimeSent(System.currentTimeMillis());
                       	}else
                       		proposedMessage = proposal.getProposedMessages().entrySet().iterator().next().getValue();
                        
                        this.proposals.get(proposalIdOfMessage).getProposedMessages().put(msg4.getId(), proposedMessage);
                        this.sendProposedMessage(proposalIdOfMessage);
                    }
                } else {
                	logger.info("Acceptance Time Over");
                }
                }else if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT) {
                	//Proposed Message Acknowledgement.
                	this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().remove(msg.getContextValue("proposedMessageId"));
                	if(this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size() < 1)
                		this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).setProposalProcessed(true);
                	logger.info("Proposed Message Removed." + this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size());
                	this.proposedMsgAudit.put(msg.getContextValue("proposedMessageId").toString(), true);
                	logger.info("Received The Following Payload From the Hint Service : " + msg.getContextValue(Message.RESULT_KEY));
                }
            }
            logger.info("============================================================================");
            return true;
        }
    
		
	}
	
	class HintService extends BaseService {	
        private Map<String, Message> proposalsAccepted = new HashMap<>();     //replying conversation-id, propose msg
        private List<Message> proposalsConfirmReceived = new ArrayList<>();     //replying conversation-id, propose msg
        
        private Map<String, Set<String>> proposalsConfirmedToServ = new HashMap<>();
        private Queue<String>  proposedMsgRequests = new LinkedList<>();
        private Map<String, String> auditOfProposedMsgReq = new HashMap<>();
        private boolean respondToProposedMessage = false;
        private boolean respondToProposal = false;
        private boolean maintainACountForResponse = false;
        private int counterForResponse = 0;
        
        public HintService(String id) {
            super(id, null);
        }

        
		@Override
		public boolean receiveMessage(BaseMessage msg) {
			super.receiveMessage(msg);
			logger.info("============================================================================");
			logger.info("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
            	logger.info("SpeechAct : " + ((Message) msg).getSpeechAct());
                if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSE_ACT && respondToProposal) {
                    String conversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                    String replyingConversationId = "conversation_accept_proposal_" + this.getId() + "_" + System.currentTimeMillis();
                    proposalsAccepted.put(replyingConversationId, (Message) msg);
                    Message msg2 = (Message) testMessages.get(1).clone(false);
                    msg2.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg2.setContextValue(CONTEXT_CONVERSATION_ID_KEY, replyingConversationId);
                    msg2.setContextValue(Message.PROPOSAL_KEY, (String) msg.getContextValue(Message.PROPOSAL_KEY));
                    msg2.setContextValue(CONTEXT_IN_REPLY_TO_KEY, conversationId);
                    this.sendMessage(msg2);
                } else if (((Message) msg).getSpeechAct() == SpeechActEnum.CONFIRM_PROPOSAL_ACT) {
                    String originalConversationId = (String) msg.getContextValue(Message.CONTEXT_IN_REPLY_TO_KEY);
                    if (proposalsAccepted.get(originalConversationId) != null) {        //confirm proposals only for which this service accepted
                        proposalsConfirmReceived.add((Message) msg);
                        String hintPresenter = msg.getContext().get(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY).toString();
                        String proposalId = msg.getContext().get(Message.PROPOSAL_KEY).toString();
                        if(!proposalsConfirmedToServ.containsKey(hintPresenter)) {
                        	proposalsConfirmedToServ.put(hintPresenter, new HashSet<>(Arrays.asList(proposalId)));
                        } else {
                        	Set<String> proposalsAccepted = proposalsConfirmedToServ.get(hintPresenter);
                        	proposalsAccepted.add(proposalId);
                        	proposalsConfirmedToServ.put(hintPresenter, proposalsAccepted);
                        }
                    }
                } else if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSED_MESSAGE && (msg.getContextValue("toBeServicedBy").toString().equals(this.getId())) && respondToProposedMessage) {
                	String originalConversationId = (String) msg.getContextValue(Message.PROPOSAL_KEY);
                	String hinterPresenterId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);
                	boolean flag = maintainACountForResponse && (counterForResponse < 2) ? true : !maintainACountForResponse ? true : false;
                	if(flag && proposalsConfirmedToServ.containsKey(hinterPresenterId) && proposalsConfirmedToServ.get(hinterPresenterId).contains(originalConversationId)) {
                		proposedMsgRequests.add(msg.getId());
                		auditOfProposedMsgReq.put(msg.getId(), originalConversationId);
                		RESTMessage restMessage = new RESTMessage(HTTPRequestVerbEnum.GET, "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys", null, new HashMap<>());
                		messenger.handleMessage(restMessage, "hinterPresenterId");
                	} else {
                		logger.info("My Service name is : "+ this.id + "I am Not Answering Right Now. ");
                	}
                	counterForResponse++;
                }
            } else if (msg instanceof RESTMessage){
            	String MessageId = msg.getId();
            	String proposalMessageRespose = proposedMsgRequests.poll();
            	if(proposalMessageRespose != null) {
	            	Message msgAck = (Message) testMessages.get(1).clone(false);
	                msgAck.setSpeechAct(SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT);
	                msgAck.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
	                msgAck.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_accept_proposal_" + this.getId() + "_" + System.currentTimeMillis());
	                msgAck.setContextValue("proposedMessageId", proposalMessageRespose);
	                msgAck.setContextValue(Message.PROPOSAL_KEY, auditOfProposedMsgReq.get(proposalMessageRespose));
	                msgAck.setContextValue(Message.CONTEXT_IN_REPLY_TO_MESSAGE, MessageId);
	                msgAck.setContextValue(Message.RESULT_KEY, ((RESTMessage) msg).getPayload());
	                this.sendMessage(msgAck);
            	}
            }
            logger.info("============================================================================");
            return true;
		}
	}

	public void setupForScenarioOne() {
		hintService1.respondToProposal = true;
		hintService2.respondToProposal = true;
		hintService1.respondToProposedMessage = true;
		hintService2.respondToProposedMessage = true;
	}
	
	/**
	 * Happy Path.
	 * @throws Exception
	 */
	@Test
	public void testProposalPattern_ScenarioOne() throws Exception {
		setupForScenarioOne();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("acceptFor", "4000");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.X_TIME_ACCEPT_PROPOSAL_ACK.getValue());
        Assert.assertTrue(hintPresenter.proposedMsgAudit.entrySet().stream().anyMatch(entry -> entry.getValue()));
	}
	
	public void setupForScenarioTwo() {
		hintService1.respondToProposal = false;
		hintService2.respondToProposal = false;
	}
	
	/**
	 * Proposal with Attempt Count
	 * @throws Exception
	 */
	@Test
	public void testProposalPattern_ScenarioTwo() throws Exception {
		setupForScenarioTwo();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.getValue());
        Assert.assertTrue(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
	}

	public void setupForScenarioThreeFour() {
		hintService1.respondToProposal = true;
		hintService2.respondToProposal = true;
		hintService1.respondToProposedMessage = false;
		hintService2.respondToProposedMessage = false;
	}
	
	/**
	 * Proposal Accepted but Failed Proposed Message.
	 * Fail Soft Strategy: Proposed Message with Attempt Count. 
	 * @throws Exception
	 */
	@Test
	public void testProposalPattern_ScenarioThree() throws Exception {
		setupForScenarioThreeFour();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.getValue());
        Assert.assertTrue(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertTrue(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
	}
	
	/**
	 * Proposal Accepted but Failed Proposed Message.
	 * Fail Soft Strategy: Quit In X Time. 
	 * @throws Exception
	 */
	@Test
	public void testProposalPattern_ScenarioFour() throws Exception {
		setupForScenarioThreeFour();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("quitInTime", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.QUIT_IN_X_TIME.toString());
        hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.getValue());
        Assert.assertTrue(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertTrue(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
	}
	
	
	public void setupForScenarioFive() {
		hintService1.respondToProposal = true;
		hintService2.respondToProposal = true;
		hintService1.respondToProposedMessage = true;
		hintService2.respondToProposedMessage = true;
		hintService1.maintainACountForResponse = true;
	}
	
	/**
	 * Proposal Accepted but Failed Proposed Message.
	 * Fail Soft Strategy: Proposed Message with Prioritization of Services. 
	 * @throws Exception
	 */
	@Test
	public void testProposalPattern_ScenarioFive() throws Exception {
		setupForScenarioFive();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION.toString());
        hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK.getValue());
        Assert.assertFalse(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertFalse(hintPresenter.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
	}
	
}