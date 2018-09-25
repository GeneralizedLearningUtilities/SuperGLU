const MESSAGING_GATEWAY  = require('../src/core/messaging-gateway.js')
const MESSAGE  = require('../src/core/message.js')
const Zet = require('../src/util/zet')

messagingGateway = new MESSAGING_GATEWAY.MessagingGateway();

acceptedProposalConversationId = acceptedProposalServiceId = proposalReceiptConversationId = proposalReceiptServiceId = confirmProposalConversationId = confirmProposalServiceId = ''
var HintPresenter = Zet.declare({
    // Base class for messaging gateways
    superclass: MESSAGING_GATEWAY.BaseService,
    CLASS_ID: 'HintPresenter',
    defineBody: function (self) {
    	var failStrategyToTest = null;
    	self.acceptedProposalConversationId = '';
    	self.acceptedProposalServiceId = '';
    	
    	self.acceptedServiceIds = [];
    	self.proposedMsgAudit = {};
    	
        // Public Properties
        self.receiveMessage = function receiveMessage(msg) {
        	console.log("\n*****Entered HINT PRESENTER : " + self.getId() + "*****\n");
        	console.log("HINT PRESENTER" + self.getId() + " GOT: \n" + self.messageToString(msg));
            self.inherited(receiveMessage, [msg]);
            console.log("\n============================================================================");
            console.log("Message received by " + self.getId());
            proposalIdOfMessage = msg.getContextValue('proposalId');
            if (msg.getSpeechAct() == "Accept Proposal") {
            	var proposal = self.proposals[proposalIdOfMessage];
            	if(proposal.getPolicyType() == 'ALL_TIME_ACCEPT_PROPOSAL_ACK' || proposal.getPolicyType() == 'X_Time') {
            		
                    self.acceptedProposalConversationId = msg.getContextValue('in-reply-to');
                    self.acceptedProposalServiceId = msg.getContextValue('originatingServiceId');
                    console.log("******************\nACCEPTED BY : " + self.acceptedProposalServiceId + "******************\n");
                    msg3 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'CONFIRM_PROPOSAL', {}, null, 'message2')
                    msg3.setContextValue('originatingServiceId', self.getId());
                    msg3.setContextValue('CONTEXT_IN_REPLY_TO_KEY', self.acceptedProposalConversationId);
                    msg3.setContextValue('proposalId', proposalIdOfMessage);
                    msg3.setContextValue('in-reply-to', "conversation_confirm_proposal_" + self.getId() + "_" + new Date().getTime());
                    self.proposals[proposalIdOfMessage].setAcknowledgementReceived(true);
                    //Sends Confirmation Message.
                    self.sendMessage(msg3);
                    self.acceptedServiceIds.push(self.acceptedProposalServiceId);
                    if(self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] != undefined) {
                    	triedFor = self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId];	        
                    	if((triedFor + 1) > 3) {
                    		delete self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId];
	                    	self.demotedAcceptedServiceIds.push(self.acceptedProposalServiceId);
	                    } else {
	                    	self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] = triedFor + 1;
	                    }
                    } else {
                    	self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] = 1;
                    }
            
	                //Proposal Request has been successfully processed. Below code, sends the Proposed Message.
                    msg4 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'PROPOSED_MESSAGE', {}, null, 'message2');
	                if(self.proposedMsgAudit[msg4.getId()] == undefined || (self.proposedMsgAudit[msg4.getContextValue('proposedMessageId')] != undefined && !self.proposedMsgAudit[msg4.getContextValue('proposedMessageId')])) {
	                	proposal = self.proposals[proposalIdOfMessage];
	                	self.proposedMsgAudit[msg4.getContextValue('proposedMessageId')] = false;
	                    msg4.setContextValue('originatingServiceId', self.getId());
	                    msg4.setContextValue('CONTEXT_IN_REPLY_TO_KEY', acceptedProposalConversationId);
	                    msg4.setContextValue('proposalId', proposalIdOfMessage);
	                    if (proposal.getFailSoftStrategyForProposedMsg() == 'RESEND_MSG_WITH_DEPRIORITZATION') {
	                    	if(!self.prioritizedAcceptedServiceIds.isEmpty()) {
	                    		msg4.setContextValue("toBeServicedBy", self.prioritizedAcceptedServiceIds[0].getKey());
	                    	}
	                    } else {
	                    	msg4.setContextValue("toBeServicedBy", self.acceptedServiceIds[0]);
	                    }
		                msg4.setContextValue('in-reply-to', "conversation_confirm_proposal_" + self.getId() + "_" + new Date().getTime());
		                var proposedMessage = null;
		                var count = 0
		                for (var key in proposal.getProposedMessages()) {
		                    if (proposal.getProposedMessages().hasOwnProperty(key))           
		                        count++;
		                }
		                if(count < 1) {
		                	proposedMessage = new MESSAGING_GATEWAY.ProposedMessage(msg4.getId(), msg4, 0);
		                	proposedMessage.setLastTimeSent(new Date().getTime());
		                }else {
		                	proposedMessage = proposal.getProposedMessages()[msg4.getId()];
		                }
		                self.proposals[proposalIdOfMessage].getProposedMessages()[msg4.getId()] = proposedMessage;
		                self.sendProposedMessage(proposalIdOfMessage);
	                }
            	} else {
	                	console.log("Acceptance Time Over");
            	}
            } else if (msg.getSpeechAct() == "PROPOSED_MESSAGE_ACKNOWLEDGEMENT") {
            	//Proposed Message Acknowledgement.
            	delete self.proposals[msg.getContextValue('proposalId')].getProposedMessages()[msg.getContextValue("proposedMessageId")];
            	var count = 0;
            	var remainingProposedMsgs = self.proposals[msg.getContextValue('proposalId')].getProposedMessages()
            	for (var i in remainingProposedMsgs) {
            		if (remainingProposedMsgs.hasOwnProperty(i)) count++;
            	}
            	if(count < 1) {
            		self.proposals[msg.getContextValue('proposalId')].setProposalProcessed(true);
            	}
            	console.log("Proposed Message Removed. Proposed Messages Left to Process : " + count);
            	self.proposedMsgAudit[msg.getContextValue("proposedMessageId")] = true;
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
            msg = Message(actor, verb, object, result, speechAct, context)
            if ((self._gateway != null) && (addGatewayContext)) {
                msg = self._gateway.addContextDataToMsg(msg)
            }
            self._makeRequest(msg, callback)
        }
    }
})



var HintService = Zet.declare({
    // Base class for messaging gateways
    superclass: MESSAGING_GATEWAY.BaseService,
    CLASS_ID: 'HintService',
    defineBody: function (self) {
        // Public Properties
    	 self.proposalsAccepted = {};     //replying conversation-id, propose msg
    	 self.proposalsConfirmReceived = [];     //replying conversation-id, propose msg
		 
    	 self.proposalsConfirmedToServ = {};
    	 self.proposedMsgRequests = [];
    	 self.auditOfProposedMsgReq = {};
    	 self.respondToProposedMessage = true;
    	 self.respondToProposal = false;
    	 self.maintainACountForResponse = false;
    	 self.counterForResponse = 0;
		 
		 
        self.receiveMessage = function receiveMessage(msg) {
        	console.log("\n*****Entered HINT SERVICE : " + self.getId() + "*****\n");
            console.log(" GOT: \n" + self.messageToString(msg))
            self.inherited(receiveMessage, [msg])
            console.log("\n============================================================================");
            console.log("Message received by " + self.getId());
            if (msg.getSpeechAct() == "PROPOSE" && self.respondToProposal == true) {
                	var conversationId = msg.getContextValue('in-reply-to');
                	self.replyingConversationId = "conversation_accept_proposal_" + self.getId() + "_" + new Date().getTime();
                	self.proposalsAccepted[self.replyingConversationId] = msg;
                    var msg2 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Accept Proposal', {}, null, 'message1');
                    msg2.setContextValue('originatingServiceId', self.getId());
                    msg2.setContextValue('in-reply-to', self.replyingConversationId);
                    msg2.setContextValue('proposalId', msg.getContextValue('proposalId'));
                    msg2.setContextValue('CONTEXT_IN_REPLY_TO_KEY', self.conversationId);
                    self.sendMessage(msg2);
                } else if (msg.getSpeechAct() == "CONFIRM_PROPOSAL") {
                	self.originalConversationId = msg.getContextValue('CONTEXT_IN_REPLY_TO_KEY');
	                if (self.proposalsAccepted[self.originalConversationId] != null) {        //confirm proposals only for which self service accepted
	                	console.log('I have got a Confirmation Proposal Message.');
	                	self.proposalsConfirmReceived.push(msg);
	                    var hintPresenter = msg.getContextValue('originatingServiceId');
	                    var proposalId = msg.getContextValue('proposalId');
	                    if(self.proposalsConfirmedToServ[hintPresenter] == undefined) {
	                    	self.proposalsConfirmedToServ[hintPresenter] = new Set([proposalId]);
	                    } else {
	                    	self.proposalsConfirmedToServ[hintPresenter].add(proposalId);
	                    }
	                } else {
	                	console.log('This Confirmation Proposal Message is not for me.');
	                } 
                } else if (msg.getSpeechAct() == "PROPOSED_MESSAGE" && msg.getContextValue("toBeServicedBy") == self.getId() && self.respondToProposedMessage) {
                	var originalConversationId = msg.getContextValue('proposalId');
                	var hinterPresenterId = msg.getContextValue('originatingServiceId');
                	var flag = self.maintainACountForResponse && (self.counterForResponse < 2) ? true : !self.maintainACountForResponse ? true : false;
                	if(flag && self.proposalsConfirmedToServ[hinterPresenterId] != undefined &&  self.proposalsConfirmedToServ[hinterPresenterId].has(originalConversationId)) {
                    	var messageId = msg.getId();
                    	self.proposedMsgRequests.push(msg.getId());
                    	self.auditOfProposedMsgReq[msg.getId()] = originalConversationId;
                    	var proposalMessageRespose = self.proposedMsgRequests[0];
                		if(proposalMessageRespose != null) {
                			var msgAck = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'PROPOSED_MESSAGE_ACKNOWLEDGEMENT', {}, null, 'message1');
        	            	msgAck.setContextValue('originatingServiceId', self.getId());
        	                msgAck.setContextValue('conversation-id', "conversation_accept_proposal_" + self.getId() + "_" + new Date().getTime());
        	                msgAck.setContextValue("proposedMessageId", proposalMessageRespose);
        	                msgAck.setContextValue('proposalId', self.auditOfProposedMsgReq[proposalMessageRespose]);
        	                msgAck.setContextValue('CONTEXT_IN_REPLY_TO_MESSAGE', messageId);
        	                this.sendMessage(msgAck);
                    	}
                	} else {
                		console.log("My Service name is : "+ self.getId() + "I am Not Answering Right Now.  OR This Message isn't for me!");
                	}
                	self.counterForResponse++;
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

/*
test('Happy Path! Client Sends Proposal to Service 1 & 2 and Proposed Message to Service 1.', () => {
	
	var hintService1 = new HintService();
	var hintService2 = new HintService();
	var hintPresenter = new HintPresenter();
	hintService1.respondToProposal = true;
	hintService1.respondToProposedMessage = true;
	hintService2.respondToProposal = true;
	hintService2.respondToProposedMessage = true;
	
	msg = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'PROPOSE', {}, null, 'message1')
	
	msg.setContextValue('originatingServiceId', hintPresenter.getId());
    msg.setContextValue('in-reply-to', "conversation_id_5");
    var retryParams = {};
    retryParams["msgType"] = "PROPOSAL";
    retryParams["noOfAttemptsForProposal"] = "3";
    retryParams["noOfAttemptsForProposedMsg"] = "3";
    retryParams["acceptFor"] = "4000";
    retryParams["failSoftStrategyForProposedMsg"] = "RESEND_MSG_WITH_ATTEMPT_COUNTS";    
    
    var nodes = [];
	nodes.push(hintService1);
    nodes.push(hintPresenter);
    nodes.push(hintService2);
    var gateway = new MESSAGING_GATEWAY.MessagingGateway("GatewayNode", nodes, null);
    hintPresenter.addNodes(gateway);
    hintService1.addNodes(gateway);
    hintService2.addNodes(gateway);
    
    hintPresenter.makeProposal(msg, null, retryParams, "X_TIME_ACCEPT_PROPOSAL_ACK");
    console.log('\n\n\n\n\n\n')
	
});


test('Client Sends Proposal to Service 1 & 2. Both Services Reject. Client Tries 3 Times and Faces a Timeout.', () => {
	
	var hintService1 = new HintService();
	var hintService2 = new HintService();
	var hintPresenter = new HintPresenter();
	hintService1.respondToProposal = false;
	hintService1.respondToProposedMessage = false;
	hintService2.respondToProposal = false;
	hintService2.respondToProposedMessage = false;
	
	msg = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'PROPOSE', {}, null, 'message1')
	
	msg.setContextValue('originatingServiceId', hintPresenter.getId());
    msg.setContextValue('in-reply-to', "conversation_id_5");
    var retryParams = {};
    retryParams["msgType"] = "PROPOSAL";
    retryParams["noOfAttemptsForProposal"] = "3";
    retryParams["noOfAttemptsForProposedMsg"] = "3";
    retryParams["acceptFor"] = "4000";
    retryParams["failSoftStrategyForProposedMsg"] = "RESEND_MSG_WITH_ATTEMPT_COUNTS";    
    
    var nodes = [];
	nodes.push(hintService1);
    nodes.push(hintPresenter);
    nodes.push(hintService2);
    var gateway = new MESSAGING_GATEWAY.MessagingGateway("GatewayNode", nodes, null);
    hintPresenter.addNodes(gateway);
    hintService1.addNodes(gateway);
    hintService2.addNodes(gateway);
    
    hintPresenter.makeProposal(msg, null, retryParams, "X_TIME_ACCEPT_PROPOSAL_ACK");
    console.log('\n\n\n\n\n\n')
});
*/

test('Client Sends Proposal to Service 1 & 2. Services Accept, But create Issue during sending Proposed Messages. Client Tries 3 times sending Proposal and ProposedMessage.', () => {
	
	var hintService1 = new HintService();
	var hintPresenter = new HintPresenter();
	var hintService2 = new HintService();
	hintService1.respondToProposal = true;
	hintService1.respondToProposedMessage = false;

	hintService2.respondToProposal = true;
	hintService2.respondToProposedMessage = false;
	
	msg = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'PROPOSE', {}, null, 'message1')
	
	msg.setContextValue('originatingServiceId', hintPresenter.getId());
    msg.setContextValue('in-reply-to', "conversation_id_5");
    var retryParams = {};
    retryParams["msgType"] = "PROPOSAL";
    retryParams["noOfAttemptsForProposal"] = "3";
    retryParams["noOfAttemptsForProposedMsg"] = "3";
    retryParams["acceptFor"] = "4000";
    retryParams["failSoftStrategyForProposedMsg"] = "RESEND_MSG_WITH_ATTEMPT_COUNTS";    
    
    var nodes = [];
	nodes.push(hintService1);
	nodes.push(hintService2);
    nodes.push(hintPresenter);
    var gateway = new MESSAGING_GATEWAY.MessagingGateway("GatewayNode", nodes, null);
    hintPresenter.addNodes(gateway);
    hintService1.addNodes(gateway);
    hintService2.addNodes(gateway);
    
    hintPresenter.makeProposal(msg, null, retryParams, "X_TIME_ACCEPT_PROPOSAL_ACK");
    console.log('\n\n\n\n\n\n')
});

