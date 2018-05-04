package edu.usc.ict.superglu;

import edu.usc.ict.superglu.core.*;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import static edu.usc.ict.superglu.core.Message.CONTEXT_CONVERSATION_ID_KEY;
import static edu.usc.ict.superglu.core.Message.CONTEXT_IN_REPLY_TO_KEY;


public class ProposalPatternTest {

    private MessagingGateway gateway;
    private List<BaseMessage> testMessages;
    private SampleSenderService senderService;
    private SampleSenderServiceTwo senderServiceTwo;
    private SampleReceiverService receiverService;
    private SampleReceiverService receiverServiceTwo;

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

    class SampleSenderServiceTwo extends BaseService {
        private Map<String, List<Message>> proposalAcceptReceived = new HashMap<>();       //store all proposals per conversation-id

        public SampleSenderServiceTwo(String id) {
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
    @Test
    public void testProposalPattern_ScenarioTwo() throws Exception {
        setupScenarioTwo();

        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, senderServiceTwo.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_2");
        senderServiceTwo.sendMessage(msg);

        TimeUnit.SECONDS.sleep(2);      //sleeping for 3 seconds

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

    }
}
