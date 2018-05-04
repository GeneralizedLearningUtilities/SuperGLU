package edu.usc.ict.superglu;

import edu.usc.ict.superglu.core.*;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import static edu.usc.ict.superglu.core.Message.CONTEXT_CONVERSATION_ID_KEY;

public class ProposalPatternTest {

    private MessagingGateway gateway;
    private List<BaseMessage> testMessages;
    private BaseService senderService;
    private BaseService receiverService;

    private String acceptedProposalConversationId;
    private String acceptedProposalServiceId;
    private String proposalReceiptConversationId, proposalReceiptServiceId;

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

                    Message msg3 = (Message) testMessages.get(2);
                    msg3.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg3.setContextValue(CONTEXT_CONVERSATION_ID_KEY, acceptedProposalConversationId);
                    this.sendMessage(msg3);
                }
            }
            System.out.println("============================================================================");
            return true;
        }
    }

    class SampleReceiverService extends BaseService {

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

                    Message msg2 = (Message) testMessages.get(1);
                    msg2.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msg2.setContextValue(CONTEXT_CONVERSATION_ID_KEY, conversationId);
                    this.sendMessage(msg2);
                }
            }
            System.out.println("============================================================================");
            return true;
        }
    }

    @Before
    public void setUp() throws Exception {
        List<BaseMessagingNode> nodes = new ArrayList<>();
        senderService = new SampleSenderService("senderService");
        nodes.add(senderService);
        receiverService = new SampleReceiverService("receiverService");
        nodes.add(receiverService);

        ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null, null);

        gateway = new MessagingGateway("GatewayNode", null, nodes, null, null, config);
        senderService.addNode(gateway);
        receiverService.addNode(gateway);
        this.testMessages = buildMessages();
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


    @Test
    public void testProposalPattern() {     //propose, accept, confirm
        Message msg = (Message) this.testMessages.get(0).clone(false);
        msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, senderService.getId());
        msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_1");
        senderService.sendMessage(msg);
        Assert.assertEquals("conversation_id_1", acceptedProposalConversationId);
        Assert.assertEquals("receiverService", acceptedProposalServiceId);

        Assert.assertEquals("conversation_id_1", proposalReceiptConversationId);
        Assert.assertEquals("senderService", proposalReceiptServiceId);
    }
}
