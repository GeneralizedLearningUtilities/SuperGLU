package edu.usc.ict.superglu.ipc;

import static edu.usc.ict.superglu.core.Message.CONTEXT_CONVERSATION_ID_KEY;
import static edu.usc.ict.superglu.core.Message.CONTEXT_IN_REPLY_TO_KEY;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author rthaker
 *
 */

import  org.zeromq.ZMQ;

import com.google.common.base.Predicate;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.ExternalMessagingHandler;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.core.SpeechActEnum;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;


public class HintServiceIPCRunner {
	
	final String ZERO_MQ_SENDER = "tcp://localhost:5558";
	final String ZERO_MQ_SINK = "tcp://localhost:5557";
	
	protected Logger logger = LoggerFactory.getLogger(this.getClass().getSimpleName());

	private List<BaseMessage> testMessages;

	private static HintService hintService;

	private MessagingGateway gateway;

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
                		logger.info("My Service name is : "+ this.id + "I am Not Answering Right Now. ");
                	}
                	counterForResponse++;
                }
            } 
            logger.info("============================================================================");
            return true;
		}
	}
	class ServiceGateway extends MessagingGateway {
		
		private ZMQ.Socket requester;
		
		public ServiceGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
                Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, ServiceConfiguration config) {
			super(anId, scope, nodes, conditions, handlers, config);		
			ZMQ.Context context = ZMQ.context(1);
	        //  Socket to talk to server
			requester = context.socket(ZMQ.PUSH);
			requester.bind(ZERO_MQ_SENDER);
					
		}

		@Override
		public void distributeMessage(BaseMessage msg, String senderId) {
			// TODO Auto-generated method stub
			super.distributeMessage(msg, senderId);
			if (((Message) msg).getSpeechAct() != SpeechActEnum.PROPOSE_ACT) {
				try {
					String json = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
				    System.out.println("launch and connect client.");
					requester.send(json);
				} catch (Exception e) {
					System.out.println("Something Wrong");
				}
			}
		}
	}

	public void run() {
		ZMQ.Context context = ZMQ.context(1);
		ZMQ.Socket receiver = context.socket(ZMQ.PULL);
		receiver.connect(ZERO_MQ_SINK);
		List<BaseMessagingNode> nodes = new ArrayList<>();
		hintService = new HintService("HintService");
		hintService.respondToProposal = true;
		hintService.respondToProposedMessage = true;
		nodes.add(hintService);
		ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null,
				null);
		gateway = new ServiceGateway("GatewayNode", null, nodes, null, null, config);
		testMessages = buildMessages();
		startReception(receiver);
	}
	
	private void startReception(ZMQ.Socket receiver) {
		ExecutorService receiverService = Executors.newSingleThreadExecutor();
		receiverService.submit(() -> {
			while (!Thread.currentThread().isInterrupted()) {
				String receptionString = null;
				if((receptionString = new String(receiver.recv(0)).trim()) != null) {
					System.out.println(receptionString);
					System.out.println("CONVERTInG MESSAGE");
					SuperGlu_Serializable message =  SerializationConvenience.nativeizeObject(receptionString, SerializationFormatEnum.JSON_FORMAT);
					BaseMessage msgRcd = (BaseMessage) message;
					System.out.println("CONVERTED MESSAGE!!! BINGO!!");
					new Thread(new Runnable() {
					    public void run() {
					    	gateway.sendMessage(msgRcd);
					    }
					}).start();
					System.out.print(receptionString + '.');
				}
			}
		});
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
	
	public static void main(String[] args) {
		HintServiceIPCRunner server = new HintServiceIPCRunner();
		server.run();
	}
}
