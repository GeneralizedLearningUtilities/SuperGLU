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
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.core.Proposal;
import edu.usc.ict.superglu.core.ProposedMessage;
import edu.usc.ict.superglu.core.SpeechActEnum;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;


public class ProposalPatternTest {

    private MessagingGateway gateway;
    private List<BaseMessage> testMessages;
    private SampleSenderService senderService;
    private SampleSenderServiceTwo senderServiceTwo;
    private SampleReceiverService receiverService;
    private SampleReceiverService receiverServiceTwo;
    private ProposalSenderService proposalSenderService;
    
    private String acceptedProposalConversationId;
    private String acceptedProposalServiceId;
    private String proposalReceiptConversationId, proposalReceiptServiceId;
    private String confirmProposalConversationId, confirmProposalServiceId;

    class SampleSenderService extends BaseService {

        public SampleSenderService(String id) {
            super(id, null);
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
            super.receiveMessage(msg);
            System.out.println("============================================================================");
            System.out.println("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
                System.out.println("SpeechAct : " + ((Message) msg).getSpeechAct());
                if (((Message) msg).getSpeechAct() == SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
                    acceptedProposalConversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                    acceptedProposalServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);

                    Message msg3 = (Message) testMessages.get(2).clone(false);
                    msg3.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg3.setContextValue(CONTEXT_IN_REPLY_TO_KEY, acceptedProposalConversationId);
                    msg3.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + this.getId() + "_" + System.currentTimeMillis());
                    this.sendMessage(msg3);
                }
            }
            System.out.println("============================================================================");
            return true;
        }
    }
    

    class SampleSenderServiceTwo extends BaseService  {
    	 private Map<String, List<Message>> proposalAcceptReceived = new HashMap<>();       //store all proposals per conversation-id

        public SampleSenderServiceTwo(String id) {
            super(id, null);
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
        	System.out.println("MESSAGE RECEIVED");
            super.receiveMessage(msg);
            System.out.println("============================================================================");
            System.out.println("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
                System.out.println("SpeechAct : " + ((Message) msg).getSpeechAct());
                if (((Message) msg).getSpeechAct() == SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
                    String conversationId = (String) msg.getContextValue(Message.CONTEXT_IN_REPLY_TO_KEY);
                    List<Message> lst = proposalAcceptReceived.get(conversationId);
                    if (lst == null) {
                        lst = new ArrayList<>();
                        proposalAcceptReceived.put(conversationId, lst);
                    }
                    lst.add((Message) msg);
                }
            }
            System.out.println("============================================================================");
            return true;
        }
        
   
        
        
    }
    
    class SampleReceiverService extends BaseService {
        private Map<String, Message> proposalsAccepted = new HashMap<>();     //replying conversation-id, propose msg
        private List<Message> proposalsConfirmReceived = new ArrayList<>();     //replying conversation-id, propose msg

        public SampleReceiverService(String id) {
            super(id, null);
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
            super.receiveMessage(msg);
            System.out.println("============================================================================");
            System.out.println("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
                System.out.println("SpeechAct : " + ((Message) msg).getSpeechAct());
                if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSE_ACT) {
                    String conversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                    proposalReceiptConversationId = conversationId;
                    proposalReceiptServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);

                    String replyingConversationId = "conversation_accept_proposal_" + this.getId() + "_" + System.currentTimeMillis();
                    proposalsAccepted.put(replyingConversationId, (Message) msg);

                    Message msg2 = (Message) testMessages.get(1).clone(false);
                    msg2.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg2.setContextValue(CONTEXT_CONVERSATION_ID_KEY, replyingConversationId);
                    msg2.setContextValue(CONTEXT_IN_REPLY_TO_KEY, conversationId);
                    this.sendMessage(msg2);
                } else if (((Message) msg).getSpeechAct() == SpeechActEnum.CONFIRM_PROPOSAL_ACT) {
                    String originalConversationId = (String) msg.getContextValue(Message.CONTEXT_IN_REPLY_TO_KEY);
                    if (proposalsAccepted.get(originalConversationId) != null) {        //confirm proposals only for which this service accepted
                        confirmProposalConversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                        confirmProposalServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);
                        proposalsConfirmReceived.add((Message) msg);
                    }
                }
            }
            System.out.println("============================================================================");
            return true;
        }
    }

    @Before
    public void setUp() {
        acceptedProposalConversationId = acceptedProposalServiceId = null;
        proposalReceiptConversationId = proposalReceiptServiceId = null;
        confirmProposalConversationId = confirmProposalServiceId = null;
        this.testMessages = buildMessages();
    }

    public void setupScenarioOne() throws Exception {
        List<BaseMessagingNode> nodes = new ArrayList<>();
        senderService = new SampleSenderService("senderService");
        nodes.add(senderService);
        receiverService = new SampleReceiverService("receiverService");
        nodes.add(receiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        senderService.addNode(gateway);
        receiverService.addNode(gateway);
    }

    public void setupScenarioTwo() throws Exception {
        List<BaseMessagingNode> nodes = new ArrayList<>();
        senderServiceTwo = new SampleSenderServiceTwo("senderServiceTwo");
        nodes.add(senderServiceTwo);
        receiverService = new SampleReceiverService("receiverService");
        nodes.add(receiverService);
        receiverServiceTwo = new SampleReceiverService("receiverServiceTwo");
        nodes.add(receiverServiceTwo);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        senderServiceTwo.addNode(gateway);
        receiverService.addNode(gateway);
        receiverServiceTwo.addNode(gateway);
    }
    
    private List<BaseMessage> buildMessages() {
        List<BaseMessage> result = new ArrayList<>();
        Message msg1 = new Message("penguin", "eats", "fish", "Sending Proposal", SpeechActEnum.PROPOSE_ACT, null, new HashMap<>(), "msg1");
        result.add(msg1);
        Message msg2 = new Message("penguin", "eats", "fish", "Accepting Proposal", SpeechActEnum.ACCEPT_PROPOSAL_ACT, null, new HashMap<>(), "msg2");
        result.add(msg2);
        Message msg3 = new Message("penguin", "eats", "fish", "Confirming Proposal", SpeechActEnum.CONFIRM_PROPOSAL_ACT, null, new HashMap<>(), "msg3");
        result.add(msg3);
        Message msg4 = new Message("penguin", "proposal", "fish", "Sending Proposal", SpeechActEnum.PROPOSE_ACT, null, new HashMap<>(), "msg4");
        result.add(msg4);
        return result;
    }


    /**
     * Scenario - A service sends a proposal, receiver replies accept & then the sender confirms the acceptance.
     */
    @Test
    public void testProposalPattern_ScenarioOne() throws Exception {     //propose, accept, confirm
        setupScenarioOne();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, senderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_1");
        senderService.sendMessage(msg);

        Assert.assertTrue(acceptedProposalConversationId.contains("conversation_accept_proposal_receiverService_"));
        Assert.assertEquals("receiverService", acceptedProposalServiceId);

        Assert.assertEquals("conversation_id_1", proposalReceiptConversationId);
        Assert.assertEquals("senderService", proposalReceiptServiceId);

        Assert.assertTrue(confirmProposalConversationId.contains("conversation_confirm_proposal_senderService"));
        Assert.assertEquals("senderService", confirmProposalServiceId);
    }

    /**
     * Scenario - A service sends a proposal, receives 2 accepts and then confirms one of them.
     *
     * @throws Exception
     */
   /* @Test
    public void testProposalPattern_ScenarioTwo() throws Exception {
        setupScenarioTwo();

        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, senderServiceTwo.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_2");
        senderServiceTwo.sendMessage(msg);

        TimeUnit.SECONDS.sleep(2);      //sleeping for 2 seconds in order to receive all proposal acceptances

        Assert.assertEquals(1, receiverService.proposalsAccepted.size());
        Assert.assertEquals(1, receiverServiceTwo.proposalsAccepted.size());
        Assert.assertEquals(2, senderServiceTwo.proposalAcceptReceived.get("conversation_id_2").size());       //2 proposals for given conversation_id were accepted

        //Confirm the second proposal
        Message msgAcceptPropose = senderServiceTwo.proposalAcceptReceived.get("conversation_id_2").get(1);
        Message msg3 = (Message) testMessages.get(2).clone(false);      //confirm proposal message
        msg3.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, senderServiceTwo.getId());
        msg3.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal");
        msg3.setContextValue(CONTEXT_IN_REPLY_TO_KEY, msgAcceptPropose.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY));
        senderServiceTwo.sendMessage(msg3);

        if (((String) msgAcceptPropose.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY)).contains("receiverServiceTwo")) {
            Assert.assertEquals(1, receiverServiceTwo.proposalsConfirmReceived.size());
            Assert.assertEquals(0, receiverService.proposalsConfirmReceived.size());
        } else {
            Assert.assertEquals(0, receiverServiceTwo.proposalsConfirmReceived.size());
            Assert.assertEquals(1, receiverService.proposalsConfirmReceived.size());
        }

        Assert.assertEquals(1, receiverServiceTwo.proposalsConfirmReceived.size() + receiverService.proposalsConfirmReceived.size());       //One of them is confirm//        Assert.assertEquals("conversation_id_2", proposalReceiptConversationId);
        Assert.assertEquals("conversation_confirm_proposal", confirmProposalConversationId);
        Assert.assertEquals("senderServiceTwo", confirmProposalServiceId);

    }*/
    
    /**
     * Scenario - A service sends a proposal, receives Acceptance. Sends Message to Test Fail Soft Strategy 1.
     *
     * @throws Exception
     */
    
    class ProposalSenderService extends BaseService {
    	SpeechActEnum failStrategyToTest = null;
    	boolean successdesired = false;
    	
    	List<String> acceptedServiceIds = new ArrayList<>();
    	Map<String, Boolean> proposedMsgAudit = new HashMap<>();
  
        public ProposalSenderService(String id) {
            super(id, null);
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
            super.receiveMessage(msg);
            System.out.println("============================================================================");
            System.out.println("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
            	System.out.println("SpeechAct : " + ((Message) msg).getSpeechAct());
                String proposalIdOfMessage =  (String) msg.getContextValue(Message.PROPOSAL_KEY);
                if (((Message) msg).getSpeechAct() == SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
                    acceptedProposalConversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
                    acceptedProposalServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);
                    System.out.println("******************\nACCEPTED BY : " + acceptedProposalServiceId + "******************\n");
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
                    	Proposal proposal = this.proposals.get(proposalIdOfMessage);
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
                    
                }else if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT) {
                	//Proposed Message Acknowledgement.
                	this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().remove(msg.getContextValue("proposedMessageId"));
                	if(this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size() < 1)
                		this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).setProposalProcessed(true);
                	System.out.println("Proposed Message Removed." + this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size());
                	this.proposedMsgAudit.put(msg.getContextValue("proposedMessageId").toString(), true);
                	System.out.println("Received The Following Payload From the Hint Service : " + msg.getContextValue(Message.RESULT_KEY));
                }
            }
            System.out.println("============================================================================");
            return true;
        }
    }
    
    class ProposalReceiverService extends BaseService {
		private Map<String, Message> proposalsAccepted = new HashMap<>();     //replying conversation-id, propose msg
        private List<Message> proposalsConfirmReceived = new ArrayList<>();     //replying conversation-id, propose msg
        
        private Map<String, Set<String>> proposalsConfirmedToServ = new HashMap<>();
        private Queue<String>  proposedMsgRequests = new LinkedList<>();
        private Map<String, String> auditOfProposedMsgReq = new HashMap<>();
        private boolean respondToProposedMessage = false;
        private boolean respondToProposal = false;
        private boolean maintainACountForResponse = false;
        private int counterForResponse = 0;
        
        public ProposalReceiverService(String id) {
            super(id, null);
        }

        @Override
        public boolean receiveMessage(BaseMessage msg) {
			super.receiveMessage(msg);
			System.out.println("============================================================================");
			System.out.println("Message received by " + this.getId() + " : " + this.getClass().getName());
            if (msg instanceof Message) {
            	System.out.println("SpeechAct : " + ((Message) msg).getSpeechAct());
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
                    	String MessageId = msg.getId();
                    	proposedMsgRequests.add(msg.getId());
                    	auditOfProposedMsgReq.put(msg.getId(), originalConversationId);
                    	String proposalMessageRespose = proposedMsgRequests.poll();
                		if(proposalMessageRespose != null) {
        	            	Message msgAck = (Message) testMessages.get(1).clone(false);
        	                msgAck.setSpeechAct(SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT);
        	                msgAck.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
        	                msgAck.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_accept_proposal_" + this.getId() + "_" + System.currentTimeMillis());
        	                msgAck.setContextValue("proposedMessageId", proposalMessageRespose);
        	                msgAck.setContextValue(Message.PROPOSAL_KEY, auditOfProposedMsgReq.get(proposalMessageRespose));
        	                msgAck.setContextValue(Message.CONTEXT_IN_REPLY_TO_MESSAGE, MessageId);

        	                this.sendMessage(msgAck);
                    	}
                	} else {
                		System.out.println("My Service name is : "+ this.id + "I am Not Answering Right Now. ");
                	}
                	counterForResponse++;
                }
            }
            System.out.println("============================================================================");
            return true;
		}
    }
    
    public void setupScenarioProposal() {
    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = true;
        nodes.add(proposalSenderService);
        ProposalReceiverService proposalReceiverService = new ProposalReceiverService("receiverService");
        nodes.add(proposalReceiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        proposalSenderService.addNode(gateway);
        proposalReceiverService.addNode(gateway);
    }
    
    public void setupScenarioProposal_ProposalFailure() {
    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = false;
        nodes.add(proposalSenderService);
        proposalSenderService.failStrategyToTest = SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS;
    }
    
    public void setupScenarioProposal_ProposedMsg_Failure() {
    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = true;
        nodes.add(proposalSenderService);
        ProposalReceiverService proposalReceiverService = new ProposalReceiverService("receiverService");
        nodes.add(proposalReceiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        proposalSenderService.addNode(gateway);
        proposalReceiverService.addNode(gateway);
        proposalSenderService.failStrategyToTest = SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS;
        proposalSenderService.successdesired = false;
        

        proposalReceiverService.respondToProposal = true;
        proposalReceiverService.respondToProposedMessage = false;
    }
    
    
    public void setupScenarioProposal_AttemptStrategy_Success() {
    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = true;
        nodes.add(proposalSenderService);
        ProposalReceiverService proposalReceiverService = new ProposalReceiverService("receiverService");
        nodes.add(proposalReceiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        proposalSenderService.addNode(gateway);
        proposalSenderService.addNode(gateway);
        proposalSenderService.failStrategyToTest = SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS;

        proposalReceiverService.respondToProposal = true;
        proposalReceiverService.respondToProposedMessage = true;
    }
    
    @Test
    public void testProposalPattern_happyPathProposal() throws Exception {
    	setupScenarioProposal_AttemptStrategy_Success();
        Message msg = (Message) this.testMessages.get(3).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, proposalSenderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        proposalSenderService.makeProposal(msg, successCallback, retryParams, "ALL");
        Assert.assertTrue(proposalSenderService.proposedMsgAudit.entrySet().stream().anyMatch(entry -> entry.getValue()));
        
        
    }
    
    @Test
    public void testProposalPattern_ProposalFailure() throws Exception {
    	setupScenarioProposal_ProposalFailure();
        Message msg = (Message) this.testMessages.get(3).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, proposalSenderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        proposalSenderService.makeProposal(msg, successCallback, retryParams, "ALL");
        Assert.assertTrue(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        
    }
    
    //Strategy1
    @Test
    public void testProposalPattern_ProposedMsg_Failure() throws Exception {
    	setupScenarioProposal_ProposedMsg_Failure();
        Message msg = (Message) this.testMessages.get(3).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, proposalSenderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());
        proposalSenderService.makeProposal(msg, successCallback, retryParams, "ALL");
        Assert.assertTrue(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertTrue(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
    }
    
    public void setupScenarioProposal_QuitInTimeStrategy_Success() {
    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = true;
        nodes.add(proposalSenderService);
        ProposalReceiverService proposalReceiverService = new ProposalReceiverService("receiverService");
        nodes.add(proposalReceiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        proposalSenderService.addNode(gateway);
        proposalSenderService.addNode(gateway);
        proposalSenderService.failStrategyToTest = SpeechActEnum.QUIT_IN_X_TIME;

        proposalReceiverService.respondToProposal = true;
        proposalReceiverService.respondToProposedMessage = false;
    }
    
    //Strategy 2
    @Test
    public void testProposalPattern_ScenarioFour_Success() throws Exception {
    	setupScenarioProposal_QuitInTimeStrategy_Success();
        Message msg = (Message) this.testMessages.get(3).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, proposalSenderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("quitInTime", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.QUIT_IN_X_TIME.toString());
        proposalSenderService.makeProposal(msg, successCallback, retryParams, "ALL");
        Assert.assertTrue(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertTrue(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
    }
    
    public void setupForScenarioFive() {

    	List<BaseMessagingNode> nodes = new ArrayList<>();
    	proposalSenderService = new ProposalSenderService("BASE");
    	proposalSenderService.successdesired = true;
        nodes.add(proposalSenderService);
        ProposalReceiverService proposalReceiverService = new ProposalReceiverService("receiverService");
        nodes.add(proposalReceiverService);
        
        ProposalReceiverService proposalReceiverService1 = new ProposalReceiverService("receiverService1");
        nodes.add(proposalReceiverService1);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        proposalSenderService.addNode(gateway);
        proposalSenderService.addNode(gateway);
        proposalSenderService.failStrategyToTest = SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION;
    
        proposalReceiverService.respondToProposal = true;
        proposalReceiverService1.respondToProposal = true;
		proposalReceiverService.respondToProposedMessage = true;
		proposalReceiverService1.respondToProposedMessage = true;
		proposalReceiverService.maintainACountForResponse = true;
	}

    @Test
    public void testProposalPattern_ScenarioFive() throws Exception {
		setupForScenarioFive();
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, proposalSenderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5");
        Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
        Map<String, Object> retryParams = new HashMap<>();
        retryParams.put("msgType", "PROPOSAL");
        retryParams.put("noOfAttemptsForProposal", "3");
        retryParams.put("noOfAttemptsForProposedMsg", "3");
        retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION.toString());
        proposalSenderService.makeProposal(msg, successCallback, retryParams, "ALL");
        Assert.assertFalse(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> !entry.getValue().isProposalProcessed()));
        Assert.assertFalse(proposalSenderService.getProposals().entrySet().stream().anyMatch(entry -> entry.getValue().getProposedMsgs().size() > 0));
    	
    }
 
}
