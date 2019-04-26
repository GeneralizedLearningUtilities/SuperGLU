package edu.usc.ict.superglu.ipc;

import static edu.usc.ict.superglu.core.Message.CONTEXT_CONVERSATION_ID_KEY;
import static edu.usc.ict.superglu.core.Message.CONTEXT_IN_REPLY_TO_KEY;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.zeromq.ZMQ;

import com.google.common.base.Predicate;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.ExternalMessagingHandler;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.core.Proposal;
import edu.usc.ict.superglu.core.ProposedMessage;
import edu.usc.ict.superglu.core.SpeechActEnum;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;


public class HintPresenterIPCRunner {

	final String ZERO_MQ_SENDER_Python = "tcp://localhost:5558";
	final String ZERO_MQ_SINK_Python = "tcp://localhost:5557";
	final String ZERO_MQ_SINK_JavaScript = "tcp://localhost:5556";
	final String ZERO_MQ_SENDER_JavaScript = "tcp://localhost:5555";
	
	protected Logger logger = LoggerFactory.getLogger(this.getClass().getSimpleName());

	private List<BaseMessage> testMessages;

	private static HintPresenterService hintPresenter;

	private MessagingGateway gateway;

	class HintPresenterService extends BaseService {
		SpeechActEnum failStrategyToTest = null;
		String acceptedProposalConversationId, acceptedProposalServiceId;

		List<String> acceptedServiceIds = new ArrayList<>();
		Map<String, Boolean> proposedMsgAudit = new HashMap<>();

		public HintPresenterService(String id) {
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
				String proposalIdOfMessage = (String) msg.getContextValue(Message.PROPOSAL_KEY);
				if (((Message) msg).getSpeechAct() == SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
					Proposal proposal = this.proposals.get(proposalIdOfMessage);
					if (SpeechActEnum.getEnum(proposal.getPolicyType()) == SpeechActEnum.ALL_TIME_ACCEPT_PROPOSAL_ACK || (SpeechActEnum.getEnum(proposal.getPolicyType()) == SpeechActEnum.X_TIME_ACCEPT_PROPOSAL_ACK && (System.currentTimeMillis() - proposal.getProposedTime()) < Long.parseLong(proposal.getRetryParams().get("acceptFor").toString()))) {
						acceptedProposalConversationId = (String) msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY);
						acceptedProposalServiceId = (String) msg.getContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY);
						logger.info("******************\nACCEPTED BY : " + acceptedProposalServiceId + "******************\n");
						Message msg3 = (Message) testMessages.get(2).clone(false);
						msg3.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
						msg3.setContextValue(CONTEXT_IN_REPLY_TO_KEY, acceptedProposalConversationId);
						msg3.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage);
						msg3.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + this.getId() + "_" + System.currentTimeMillis());
						this.proposals.get(proposalIdOfMessage).setAcknowledgementReceived(true);
						// Sends Confirmation Message.
						this.sendMessage(msg3);
						acceptedServiceIds.add(acceptedProposalServiceId);
						
						try {
							Thread.sleep(5000L);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}

						if (this.prioritizedAcceptedServiceIds.containsKey(acceptedProposalServiceId)) {
							int triedFor = this.prioritizedAcceptedServiceIds.get(acceptedProposalServiceId);
							if ((triedFor + 1) > 3) {
								this.prioritizedAcceptedServiceIds.remove(acceptedProposalServiceId);
								this.demotedAcceptedServiceIds.add(acceptedProposalServiceId);
							} else
								this.prioritizedAcceptedServiceIds.put(acceptedProposalServiceId, triedFor + 1);
						} else if (!this.demotedAcceptedServiceIds.contains(acceptedProposalServiceId)) {
							this.prioritizedAcceptedServiceIds.put(acceptedProposalServiceId, 1);
						}

						// Proposal Request has been successfully processed. Below code, sends the
						// Proposed Message.
						Message msg4 = (Message) testMessages.get(2).clone(false);
						if (!this.proposedMsgAudit.containsKey(msg4.getId())
								|| (this.proposedMsgAudit.containsKey(msg4.getId())
										&& !this.proposedMsgAudit.get(msg4.getId()))) {
							proposal = this.proposals.get(proposalIdOfMessage);
							this.proposedMsgAudit.put(msg4.getId(), false);
							msg4.setSpeechAct(SpeechActEnum.PROPOSED_MESSAGE);
							msg4.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
							msg4.setContextValue(CONTEXT_IN_REPLY_TO_KEY, acceptedProposalConversationId);
							msg4.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage);

							if (SpeechActEnum.getEnum(proposal.getFailSoftStrategyForProposedMsg()) == SpeechActEnum.RESEND_MSG_WITH_DEPRIORITZATION) {
								if (!this.prioritizedAcceptedServiceIds.isEmpty())
									msg4.setContextValue("toBeServicedBy", this.prioritizedAcceptedServiceIds.entrySet().iterator().next().getKey());
							} else
								msg4.setContextValue("toBeServicedBy", acceptedServiceIds.get(0));

							msg4.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + this.getId() + "_" + System.currentTimeMillis());
							ProposedMessage proposedMessage = null;

							if (proposal.getProposedMessages().size() < 1) {
								proposedMessage = new ProposedMessage(msg4.getId(), msg4, 0);
								proposedMessage.setLastTimeSent(System.currentTimeMillis());
							} else
								proposedMessage = proposal.getProposedMessages().entrySet().iterator().next()
										.getValue();

							this.proposals.get(proposalIdOfMessage).getProposedMessages().put(msg4.getId(), proposedMessage);
							this.sendProposedMessage(proposalIdOfMessage);
						}
					} else {
						logger.info("Acceptance Time Over");
					}
				} else if (((Message) msg).getSpeechAct() == SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT) {
					// Proposed Message Acknowledgement.
					this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().remove(msg.getContextValue("proposedMessageId"));
					if (this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size() < 1)
						this.proposals.get(msg.getContextValue(Message.PROPOSAL_KEY)).setProposalProcessed(true);
					logger.info("Proposed Message Removed." + this.proposals
							.get(msg.getContextValue(Message.PROPOSAL_KEY)).getProposedMessages().size());
					this.proposedMsgAudit.put(msg.getContextValue("proposedMessageId").toString(), true);
					logger.info("Received The Following Payload From the Hint Service : "
							+ msg.getContextValue(Message.RESULT_KEY));
				}
			}
			logger.info("============================================================================");
			return true;
		}

	}
	
	class PresenterGateway extends MessagingGateway {

		private ZMQ.Socket requesterPython;
		private ZMQ.Socket requesterJavaScript;
		
		public PresenterGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
                Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers, ServiceConfiguration config) {
			super(anId, scope, nodes, conditions, handlers, config);		
			ZMQ.Context context = ZMQ.context(1);
	        //  Socket to talk to server
			requesterPython = context.socket(ZMQ.PUSH);
			requesterJavaScript = context.socket(ZMQ.PUSH);
			
			requesterPython.bind(ZERO_MQ_SENDER_Python);
			requesterJavaScript.bind(ZERO_MQ_SENDER_JavaScript);
		}

		@Override
		public void distributeMessage(BaseMessage msg, String senderId) {
			// TODO Auto-generated method stub
			super.distributeMessage(msg, senderId);
			try {
				SpeechActEnum speechAct = ((Message) msg).getSpeechAct();
				if(speechAct != SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT &&  speechAct != SpeechActEnum.ACCEPT_PROPOSAL_ACT) {
					String json = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
			        System.out.println("launch and connect client.");
			        new Thread(new Runnable() {
						
						@Override
						public void run() {
							requesterJavaScript.send(json);
							
						}
					}).start();
			        new Thread(new Runnable() {
						
						@Override
						public void run() {
							requesterPython.send(json);
							
						}
					}).start();
				}
			} catch (Exception e) {
				e.printStackTrace();
				System.out.println("Something Wrong");
			}
		}
	}


	public void run() {
		List<BaseMessagingNode> nodes = new ArrayList<>();
		hintPresenter = new HintPresenterService("hintPresenter");
		nodes.add(hintPresenter);
		ServiceConfiguration config = new ServiceConfiguration("mockConfiguration", null, new HashMap<>(), null, null,
				null);
		gateway = new PresenterGateway("GatewayNode", null, nodes, null, null, config);
		gateway.addNode(hintPresenter);
		hintPresenter.addNode(gateway);
		testMessages = buildMessages();

		Message msg = (Message) this.testMessages.get(0).clone(false);
		msg.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId());
		msg.setContextValue(CONTEXT_CONVERSATION_ID_KEY, "conversation_id_1");
		Consumer<Message> successCallback = i -> System.out.println("SUCCESSFUL PROPOSAL");
		Map<String, Object> retryParams = new HashMap<>();
		retryParams.put("msgType", "PROPOSAL");
		retryParams.put("noOfAttemptsForProposal", "3");
		retryParams.put("noOfAttemptsForProposedMsg", "3");
		retryParams.put("acceptFor", "4000");
		retryParams.put("failSoftStrategyForProposedMsg", SpeechActEnum.RESEND_MSG_WITH_ATTEMPT_COUNTS.toString());

		startReception();
		
		
		ExecutorService makeProposal = Executors.newSingleThreadExecutor();
		makeProposal.submit(() -> {
			hintPresenter.makeProposal(msg, successCallback, retryParams, SpeechActEnum.X_TIME_ACCEPT_PROPOSAL_ACK.getValue());
		});
		
		
	}
	

	private void startReception() {
		ZMQ.Context pythonContext = ZMQ.context(1);
		ZMQ.Context javaScriptContext = ZMQ.context(1);
		ZMQ.Socket receiverPython = pythonContext.socket(ZMQ.PULL);
		receiverPython.connect(ZERO_MQ_SINK_Python);
		ZMQ.Socket receiverJavascript = javaScriptContext.socket(ZMQ.PULL);
		receiverJavascript.connect(ZERO_MQ_SINK_JavaScript);
		ExecutorService receiverService = Executors.newSingleThreadExecutor();
		receiverService.submit(() -> {
			while (!Thread.currentThread().isInterrupted()) {
				String receptionString = null;
				if((receptionString = new String(receiverPython.recv(0)).trim()) != null || (receptionString = new String(receiverJavascript.recv(0)).trim()) != null) {
					System.out.println(receptionString);
					System.out.println("CONVERTInG MESSAGE");
					SuperGlu_Serializable message =  SerializationConvenience.nativeizeObject(receptionString, SerializationFormatEnum.JSON_FORMAT);
					BaseMessage msgRcd = (BaseMessage) message;
					//msgRcd.toString();
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
		HintPresenterIPCRunner server = new HintPresenterIPCRunner();
		server.run();
	}
}
