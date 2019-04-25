
const MESSAGING_GATEWAY  = require('../core/messaging-gateway.js')
const MESSAGE  = require('../core/message.js')
const Zet = require('../util/zet')
const Serialization = require('../util/serialization')
const zmq = require('zeromq')
const pullSocket = zmq.socket('pull')
const pushSocket = zmq.socket('push')
const messagingGateway = new MESSAGING_GATEWAY.MessagingGateway();
var ZERO_MQ_SINK = "tcp://127.0.0.1:5558";
var ZERO_MQ_SENDER = "tcp://127.0.0.1:5557";
pushSocket.bind(ZERO_MQ_SENDER);


var HintPresenter = Zet.declare({
    // Base class for messaging gateways
    superclass: MESSAGING_GATEWAY.BaseService,
    CLASS_ID: 'HintPresenter',
    defineBody: function (self) {
        // Public Properties
    	
    	self.failStrategyToTest = null;
    	self.acceptedProposalConversationId = '';
    	self.acceptedProposalServiceId = '';

		self.acceptedServiceIds = [];
		self.proposedMsgAudit = {};
    	
		self.receiveMessage = function receiveMessage(msg) {
            console.log("\n*****Entered HINT PRESENTER : " + self.getId() + "*****\n");
            console.log(" GOT: \n" + self.messageToString(msg))
            self.inherited(receiveMessage, [msg])
            var proposalIdOfMessage = msg.getContextValue('proposalId');
            console.log("\n============================================================================");
            if (msg.getSpeechAct() == "Accept Proposal") {
            	
            	var proposal = self.proposals[proposalIdOfMessage];
				if (proposal.getPolicyType() == 'Accept at all times' || (proposal.getPolicyType() == 'Accept for time X' &&
						(new Date().getTime() - proposal.getProposedTime() < proposal.getRetryParams()["acceptFor"]))) {
						self.acceptedProposalConversationId = msg.getContextValue('conversation-id');
						self.acceptedProposalServiceId = msg.getContextValue('originatingServiceId');
						console.info("******************\nACCEPTED BY : " + self.acceptedProposalServiceId + "******************\n");
						var msg3 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Confirm Proposal', {}, null, 'message3');
						msg3.setContextValue('originatingServiceId', self.getId());
						msg3.setContextValue('in-reply-to', self.acceptedProposalConversationId);
						msg3.setContextValue('proposalId', proposalIdOfMessage);
						msg3.setContextValue('conversation-id', "conversation_confirm_proposal_" + self.getId() + "_" + new Date().getTime());
						self.proposals[proposalIdOfMessage].setAcknowledgementReceived(true);
						// Sends Confirmation Message.
						self.sendMessage(msg3);
						self.acceptedServiceIds.push(self.acceptedProposalServiceId);
						
						
						//SLeep a Bit here
						
						if (self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] != null) {
							var triedFor = self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId];
							if ((triedFor + 1) > 3) {
								delete self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId];
								self.demotedAcceptedServiceIds.push(self.acceptedProposalServiceId);
							} else
								self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] = triedFor + 1;
						} else {
							self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] = 1;
						}
	
						// Proposal Request has been successfully processed. Below code, sends the
						// Proposed Message.
						var msg4 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Proposed Message', {}, null, 'message4');
						if (self.proposedMsgAudit[msg4.getId()] == null || (self.proposedMsgAudit[msg4.getId()] != null
										&& !self.proposedMsgAudit[msg4.getId()])) {
							proposal = self.proposals[proposalIdOfMessage];
							self.proposedMsgAudit[msg4.getId()] = false;
							msg4.setContextValue('originatingServiceId', self.getId());
							msg4.setContextValue('in-reply-to', self.acceptedProposalConversationId);
							msg4.setContextValue('proposalId', self.proposalIdOfMessage);
							if (proposal.getFailSoftStrategyForProposedMsg() == 'Resend with Deprioritized Service') {
								if (self.prioritizedAcceptedServiceIds != undefined && self.prioritizedAcceptedServiceIds.length != 0) {
									msg4.setContextValue("toBeServicedBy", self.prioritizedAcceptedServiceIds.values()[0]);
								}
							} else {
								msg4.setContextValue("toBeServicedBy", self.acceptedServiceIds[0]);
							}
	
							msg4.setContextValue("conversation-id", "conversation_confirm_proposal_" + self.getId() + "_" + new Date().getTime());
							var proposedMessage = null;
							
							if (proposal.getProposedMessages().length < 1) {
								console.log('****************DONKEY****************');
								proposedMessage = MESSAGING_GATEWAY.ProposedMessage(msg4.getId(), msg4, 3, new Date().getTime());
								proposedMessage.setLastTimeSent(new Date().getTime());
							} else {
								console.log('****************HOTEY****************');
								var firstKey = null;
								for(key in proposal.getProposedMessages() ){
									firstKey = key;
									break;
								}
								proposedMessage = proposal.getProposedMessages()[firstKey]
							}
							console.log('****************YEEEEEHAWWWWW****************' + proposedMessage);
							self.proposals[proposalIdOfMessage].getProposedMessages()[msg4.getId()] = proposedMessage;
							self.sendProposedMessage(proposalIdOfMessage);
						}
					} else {
						console.log("Acceptance Time Over");
					}
                } else if (msg.getSpeechAct() == "Proposed Message Acknowledgement") {
					// Proposed Message Acknowledgement.
					delete self.proposals[msg.getContextValue('proposalId')].getProposedMessages()[msg.getContextValue("proposedMessageId")]
					if (self.proposals[msg.getContextValue('proposalId')].getProposedMessages().length < 1)
						self.proposals[msg.getContextValue('proposalId')].setProposalProcessed(true);
					console.log("Proposed Message Removed." + self.proposals[msg.getContextValue('proposalId')].getProposedMessages().length);
					self.proposedMsgAudit[msg.getContextValue("proposedMessageId")] = true;
					console.log("Received The Payload From the Hint Service");
                }
            console.log("\n============================================================================");
        }

        self.sendTestString = function sendTestString(aStr) {
            console.log("Test Service is Sending: " + aStr)
            self.sendMessage(Message("TestService", "Sent Test", "To Server", aStr))
        }

        self.sendTestMessage = function sendTestMessage(actor, verb, object, result, speechAct, context, addGatewayContext) {
            var msg
            if (context == null) {
                context = {}
            }
            if (addGatewayContext == null) {
                addGatewayContext = true
            }
            msg = Message(actor, verb, object, result, speechAct, context)
            if ((self._gateway != null) && (addGatewayContext)) {
                msg = self._gateway.addContextDataToMsg(msg)
            }
            self.sendMessage(msg)
        }

        self.sendTestRequest = function sendTestRequest(callback, actor, verb, object, result, speechAct, context, addGatewayContext) {
            var msg
            if (context == null) {
                context = {}
            }
            if (addGatewayContext == null) {
                addGatewayContext = true
            }
            if ((self._gateway != null) && (addGatewayContext)) {
                msg = self._gateway.addContextDataToMsg(msg)
            }
            self._makeRequest(msg, callback)
        }
    }
})

var ServiceGateway = Zet.declare({
    CLASS_ID: 'ServiceGateway',
    // Base class for messaging gateways
    superclass: MESSAGING_GATEWAY.MessagingGateway,
    defineBody: function (self) {
    	
        /** Initialize a Messaging Gateway.
         @param id: Unique ID for the gateway
         @param nodes: Connected nodes for this gateway
         @param scope: Extra context data to add to messages sent to this gateway, if those keys missing
         **/
        self.construct = function construct(id, nodes, scope) {
            // Should check for cycles at some point
            if (scope == null) {
                scope = {}
            }
            self.inherited(construct, [id, nodes])
            self._scope = scope
        }

        /** Distribute the message, after adding some gateway context data. **/
        self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds) {
            self.inherited(_distributeMessage, [nodes, msg, excludeIds])
            var str = Serialization.makeSerialized(Serialization.tokenizeObject(msg))
            if(msg.getSpeechAct() != 'Accept Proposal' && msg.getSpeechAct() != 'Proposed Message Acknowledgement') {
            	pushSocket.send(str);
            	console.log(str.toString())
            }
        }
    }
})


pullSocket.connect(ZERO_MQ_SINK);
pullSocket.on('message', function(msg){
	console.log('work: %s', msg.toString());
	msg = Serialization.untokenizeObject(Serialization.makeNative(msg))
	console.log('work: %s', msg);
	gateway.sendMessage(msg);
});


var hintPresenter = new HintPresenter();
var nodes = [];
nodes.push(hintPresenter);
var gateway = new ServiceGateway("ServiceGateway", nodes, null);
hintPresenter.addNodes(gateway)
var msg =  MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Propose', {}, null, 'message1');
msg.setContextValue('originatingServiceId', hintPresenter.getId());
msg.setContextValue('conversation-id', "conversation_id_1");
var retryParams = {}
retryParams["msgType"] = "PROPOSAL";
retryParams["noOfAttemptsForProposal"] ="3";
retryParams["noOfAttemptsForProposedMsg"] = "3";
retryParams["acceptFor"] = "4000";
retryParams["failSoftStrategyForProposedMsg"] = 'RESEND_MSG_WITH_ATTEMPT_COUNTS';
hintPresenter.makeProposal(msg, null, retryParams, 'Accept at all times');
