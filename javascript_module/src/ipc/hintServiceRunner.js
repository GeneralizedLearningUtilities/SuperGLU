
const MESSAGING_GATEWAY  = require('../core/messaging-gateway.js')
const MESSAGE  = require('../core/message.js')
const Zet = require('../util/zet')
const Serialization = require('../util/serialization')
const zmq = require('zeromq')
const pullSocket = zmq.socket('pull')
const pushSocket = zmq.socket('push')
const messagingGateway = new MESSAGING_GATEWAY.MessagingGateway();
var ZERO_MQ_SINK = "tcp://localhost:5555";
var ZERO_MQ_SENDER = "tcp://localhost:5556";

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
            console.log("Message received by " + self.getId() + " With Speech Act = " + msg.getSpeechAct() + " and Repond to Proposal : " +self.respondToProposal);
            if (msg.getSpeechAct() == "Propose" && self.respondToProposal == true) {
            		console.log("Message received NOW INSIDE" );
                    var conversationId = msg.getContextValue('conversation-id');
                    self.replyingConversationId = "conversation_accept_proposal_" + self.getId() + "_" + new Date().getTime();
                    self.proposalsAccepted[self.replyingConversationId] = msg;
                    var msg2 = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Accept Proposal', {}, null, 'message1');
                    msg2.setContextValue('originatingServiceId', self.getId());
                    msg2.setContextValue('conversation-id', self.replyingConversationId);
                    msg2.setContextValue('in-reply-to', conversationId);
                    msg2.setContextValue('proposalId', msg.getContextValue('proposalId'));
                    self.sendMessage(msg2);
                } else if (msg.getSpeechAct() == "Confirm Proposal") {
                    self.originalConversationId = msg.getContextValue('in-reply-to');
                    console.log(self.originalConversationId);
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
                } else if (msg.getSpeechAct() == "Proposed Message" && msg.getContextValue("toBeServicedBy") == self.getId() && self.respondToProposedMessage) {
                    var originalConversationId = msg.getContextValue('proposalId');
                    var hinterPresenterId = msg.getContextValue('originatingServiceId');
                    var flag = self.maintainACountForResponse && (self.counterForResponse < 2) ? true : !self.maintainACountForResponse ? true : false;
                    if(flag && self.proposalsConfirmedToServ[hinterPresenterId] != undefined &&  self.proposalsConfirmedToServ[hinterPresenterId].has(originalConversationId)) {
                        var messageId = msg.getId();
                        self.proposedMsgRequests.push(msg.getId());
                        self.auditOfProposedMsgReq[msg.getId()] = originalConversationId;
                        var proposalMessageRespose = self.proposedMsgRequests[0];
                        if(proposalMessageRespose != null) {
                            var msgAck = MESSAGE('Penguin', 'eats', 'fish', 'Fish Eaten', 'Proposed Message Acknowledgement', {}, null, 'message1');
                            msgAck.setContextValue('originatingServiceId', self.getId());
                            msgAck.setContextValue('conversation-id', "conversation_accept_proposal_" + self.getId() + "_" + new Date().getTime());
                            msgAck.setContextValue("proposedMessageId", proposalMessageRespose);
                            msgAck.setContextValue('proposalId', self.auditOfProposedMsgReq[proposalMessageRespose]);
                            msgAck.setContextValue('in-reply-to', messageId);
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
            pushSocket.send(str.toString());
            console.log(str.toString())
        }
    }
})

var hintService1 = new HintService();
hintService1.respondToProposal = true;
hintService1.respondToProposedMessage = true;

var nodes = [];
nodes.push(hintService1);
var gateway = new ServiceGateway("ServiceGateway", nodes, null);
hintService1.addNodes(gateway)
pushSocket.bind(ZERO_MQ_SENDER);
pullSocket.connect(ZERO_MQ_SINK);
pullSocket.on('message', function(msg){
	console.log('work: %s', msg.toString());
	msg = Serialization.untokenizeObject(Serialization.makeNative(msg))
	console.log('work: %s', msg);
	gateway.sendMessage(msg);
});