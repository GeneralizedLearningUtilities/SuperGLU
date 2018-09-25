/** Messaging gateways and service base classes, which form
 a network of gateways for messages to propogate across.
 This module has two main types of classes:
 A. Gateways: These relay messages to their connected services (children)
 and also to other gateways that will also relay the message.
 Gateways exist to abstract away the network and iframe topology.
 Gateways send messages to their parent gateway and can also distribute
 messages downstream to child gateways and services.
 B. Services: Services that receive messages and may (or may not) respond.
 Services exist to process and transmit messages, while doing
 meaningful things to parts of systems that they control.
 Services only send and receive message with their parent gateway.

 As a general rule, every service should be able to act reasonably and
 sensibly, regardless of what messages it receives. In short, no service
 should hard fail. There may be conditions there the system as a whole may
 not be able to function, but all attempts should be made to soft-fail.

 Likewise, all services should be prepared to ignore any messages that it
 does not want to respond to, without any ill effects on the service (e.g.,
 silently ignore) or, alternatively, to send back a message indicating that
 the message was not understood. Typically, silently ignoring is usually best.

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0

 Requires:
 - Zet.js
 - Serializable.js
 - Messaging.js
 **/
const Zet = require('../util/zet'),
    Serialization = require('../util/serialization'),
    Messaging = require('./messaging'),
    version = require('../reference-data').version,
    UUID = require('../util/uuid'),
    Message = require('../core/message');
    //async = require('asyncawait/async');
var namespace = {}
var CATCH_BAD_MESSAGES = false,
    SESSION_ID_KEY = 'sessionId',
    SEND_MSG_SLEEP_TIME = 5000,
    PROPOSAL_ATTEMPT_COUNT = 'noOfAttemptsForProposal',
    FAIL_SOFT_STRATEGY= 'failSoftStrategyForProposedMsg',
    QUIT_IN_TIME= 'quitInTime'  	
    	
var Proposal = Zet.declare('Proposal', {
	CLASS_ID: 'Proposal',
    defineBody: function (self) {
	    // Private Properties
	    // Public Properties
	    /**
		* Create a Proposal
		* @param proposedMessage: The Main Proposed Message.
		* @param numberOfRetries: Number of Tries to be attempted to send the Proposed Message.
		* @param lastTimeSent: Time in Milliseconds when the Proposed Message was Last Attempted to Send.
		*/
	    self.construct = function construct(id, proposal, proposalProcessed, acknowledgementReceived, 
                retryParams, policyType, failSoftStrategyForProposedMsg,
                proposedMessages, proposedTime) {
	    	if (typeof id === "undefined") {
	    		id = UUID.genV4().toString()
	    	}
	    	if (typeof proposal === "undefined") {
	    		proposal = null
	    	}
	    	if (typeof proposalProcessed === "undefined") {
	    		proposalProcessed = false
	    	}
	    	if (typeof acknowledgementReceived === "undefined") {
	    		acknowledgementReceived = false
	    	}
	    	if (typeof retryParams === "undefined") {
	    		retryParams = {}
	    	}
	    	if (typeof policyType === "undefined") {
	    		policyType = ALL_TIME_ACCEPT_PROPOSAL_ACK
	    	}
	    	if (typeof failSoftStrategyForProposedMsg === "undefined") {
	    		failSoftStrategyForProposedMsg = 'noOfAttempts'
	    	}
	    	if (typeof proposedMessages === "undefined") {
	    		proposedMessages = {}
	    	}
	    	if (typeof proposedTime === "undefined") {
	    		proposedTime = new Date().getTime();
	    	}
	    	
	    	self._id = id
	    	self._proposal = proposal
	    	self._proposalProcessed = proposalProcessed
	    	self._acknowledgementReceived = acknowledgementReceived
	    	self._retryParams = retryParams
	    	self._policyType = policyType
	    	self._failSoftStrategyForProposedMsg = failSoftStrategyForProposedMsg
	    	self._proposedMessages = proposedMessages
	    	self._proposedTime = proposedTime
	    }
	    			
		/** Get the Proposal ID * */
	    self.getId = function getId() {
    		return self._id
    	}
	    
	    /** Set the Proposal ID * */
	    self.getId = function getId() {
    		return self._id
    	}
	    
    	/** Set the Proposal Request  * */
    	self.setProposal = function setProposal(proposal) {
    		self._proposal = proposal
    	}

    	/** Get the Proposal Request  * */
    	self.getProposal = function getProposal() {
    		return self._proposal
    	}
    	
    	/** Get the whether the Proposal is Processed or not * */
    	self.getProposalProcessed = function getProposalProcessed() {
    		return self._proposalProcessed
    	}
    	
    	/** Set the whether the Proposal is Processed or not * */
    	self.setProposalProcessed = function setProposalProcessed(proposalProcessed) {
    		self._proposalProcessed = proposalProcessed
    	}

    	/** Get the Whether Acknowledgement for Proposal Request is received or not. * */
    	self.getAcknowledgementReceived = function getAcknowledgementReceived() {
    		return self._acknowledgementReceived
    	}
    	
    	/** Set the Whether Acknowledgement for Proposal Request is received or not. * */
    	self.setAcknowledgementReceived = function setAcknowledgementReceived(acknowledgementReceived) {
    		self._acknowledgementReceived = acknowledgementReceived
    	}
    	
    	/** Get the Retry Parameters for the Proposal  * */
    	self.getRetryParams = function getRetryParams() {
    		return self._retryParams
    	}
    	
    	/** Set the Retry Parameters for the Proposal  * */
    	self.setRetryParams  = function setRetryParams(retryParams) {
    		self._retryParams = retryParams
    	}

    	/** Get the Policy Type for the Proposal Request  * */
    	self.getPolicyType = function getPolicyType() {
    		return self._policyType
    	}
    	
    	/** Set the Policy Type for the Proposal Request  * */
    	self.setPolicyType = function setPolicyType(policyType) {
    		self._policyType = policyType
    	}
    	
    	/** Get the FailSoftStrategyForProposedMsg for the Proposal Request * */
    	self.getFailSoftStrategyForProposedMsg = function getFailSoftStrategyForProposedMsg() {
    		return self._failSoftStrategyForProposedMsg
    	}
    	
    	/** Set the FailSoftStrategyForProposedMsg for the Proposal Request * */
    	self.setFailSoftStrategyForProposedMsg = function setFailSoftStrategyForProposedMsg(failSoftStrategyForProposedMsg) {
    		self._failSoftStrategyForProposedMsg = failSoftStrategyForProposedMsg 
    	}
    	
    	/** Get the Proposed Messages for the Proposal * */
    	self.getProposedMessages = function getProposedMessages() {
    		return self._proposedMessages
    	}
    	
    	/** Set the Proposed Messages for the Proposal * */
    	self.setProposedMessages = function setProposedMessages(proposedMessages) {
    		self._proposedMessages = proposedMessages
    	}
    	
    	/** Get the Proposed Time for the Last Proposal Request Message. * */
    	self.getProposedTime = function getProposedTime() {
    		return self._proposedTime
    	}
    	
    	/** Set the Proposed Time for the Last Proposal Request Message. * */
    	self.setProposedTime = function setProposedTime(proposedTime) {
    		self._proposedTime = proposedTime
    	}
    	
    	/** Save the Proposed Message to a storage token * */
    	self.saveToToken = function saveToToken() {
    		var key, token, newContext, hadKey
    	    token = self.inherited(saveToToken)
    	    if (self._id != null) {
    	    	token.setitem(PROPOSAL_ID, tokenizeObject(self._id))
    	    }
    		if (self._proposal != null) {
    			token.setitem(PROPOSAL, tokenizeObject(self._proposal))
    		}
    	    if (self._proposalProcessed != null) {
    	    	token.setitem(PROPOSAL_PROCESSED, tokenizeObject(self._proposalProcessed))
    	    }
    	    if (self._acknowledgementReceived != null) {
    	    	token.setitem(PROPOSAL_ACK, tokenizeObject(self._acknowledgementReceived))
    	    }
    		if (self._retryParams != null) {
    			token.setitem(RETRY_PARAMS, tokenizeObject(self._retryParams))
    		}
    	    if (self._policyType != null) {
    	    	token.setitem(POLICY_TYPE, tokenizeObject(self._policyType))
    	    }
    	    if (self._failSoftStrategyForProposedMsg != null) {
    	    	token.setitem(FAIL_SOFT_STRATEGY, tokenizeObject(self._failSoftStrategyForProposedMsg))
    	    }
    		if (self._proposedMessages != null) {
    			token.setitem(PROPOSED_MESSAGES, tokenizeObject(self._proposedMessages))
    		}
    	    if (self._proposedTime != null) {
    	    	token.setitem(LAST_TIME_SENT, tokenizeObject(self._proposedTime))
    	    }
    	    return token
    	}

    	/**
		 * Initialize the message from a storage token and some
		 * additional context (e.g., local objects) *
		 */
    	self.initializeFromToken = function initializeFromToken(token, context) {
    		self.inherited(initializeFromToken, [token, context])
    		
    		self._id = untokenizeObject(token.getitem(PROPOSAL_ID, true, null), context)
	    	self._proposal = untokenizeObject(token.getitem(PROPOSAL, true, null), context)
	    	self._proposalProcessed = untokenizeObject(token.getitem(PROPOSAL_PROCESSED, true, null), context)
	    	self._acknowledgementReceived = untokenizeObject(token.getitem(PROPOSAL_ACK, true, null), context)
	    	self._retryParams = untokenizeObject(token.getitem(RETRY_PARAMS, true, null), context)
	    	self._policyType = untokenizeObject(token.getitem(POLICY_TYPE, true, null), context)
	    	self._failSoftStrategyForProposedMsg = untokenizeObject(token.getitem(FAIL_SOFT_STRATEGY, true, null), context)
	    	self._proposedMessages = untokenizeObject(token.getitem(PROPOSED_MESSAGES, true, null), context)
	    	self._proposedTime = untokenizeObject(token.getitem(LAST_TIME_SENT, true, null), context)
    	}
    }
})

    	
var ProposedMessage = Zet.declare({
	CLASS_ID: 'ProposedMessage',
	defineBody: function (self) {
		// Private Properties
		// Public Properties
		/** Create a ProposedMessage
	    	@param proposedMessage: The Main Proposed Message.
	    	@param numberOfRetries: Number of Tries to be attempted to send the Proposed Message.
	    	@param lastTimeSent: Time in Milliseconds when the Proposed Message was Last Attempted to Send.
		**/
		self.construct = function construct( msgId, proposedMessage, numberOfRetries, lastTimeSent) {
			if (typeof msgId === "undefined") {
    	    	msgId = UUID.genV4().toString()
    	    }
    	    if (typeof proposedMessage === "undefined") {
    	    	proposedMessage = null
    	    }
    	    if (typeof numberOfRetries === "undefined") {
    	    	numberOfRetries = 0
    	    }
    	    if (typeof lastTimeSent === "undefined") {
    	    	lastTimeSent = new Date().getTime();
    	    }
    	    self._msgId = msgId
    	    self._proposedMessage = proposedMessage
    	    self._numberOfRetries = numberOfRetries
    	    self._lastTimeSent = lastTimeSent
		}
		
		/** Get the ProposedMessage ID **/
    	self.getMsgId = function getMsgId() {
    		return self._msgId
    	}
    	
    	/** Set the ProposedMessage ID **/
    	self.setMsgId = function setMsgId(msgId) {
    		self._msgId = msgId
    	}
		
		/** Get the ProposedMessage **/
    	self.getProposedMessage = function getProposedMessage() {
    		return self._proposedMessage
    	}
    	
    	/** Set the ProposedMessage **/
    	self.setProposedMessage = function setProposedMessage(proposedMessage) {
    		self._proposedMessage = proposedMessage
    	}

    	/** Get the NumberOfRetries for the Proposed Message **/
    	self.getNumberOfRetries = function getNumberOfRetries() {
    		return self._numberOfRetries
    	}
    	
    	/** Set the Last Time Sent  for the Proposed Message **/
    	self.setLastTimeSent = function setLastTimeSent(lastTimeSent) {
    		self._lastTimeSent = lastTimeSent
    	}

    	/** Get the NumberOfRetries for the Proposed Message **/
    	self.getLastTimeSent = function getLastTimeSent() {
    		return self._lastTimeSent
    	}
    	
    	/** Set the NumberOfRetries for the Proposed Message **/
    	self.setNumberOfRetries = function setNumberOfRetries(numberOfRetries) {
    		self._numberOfRetries = numberOfRetries
    	}

    	/** Save the Proposed Message to a storage token **/
    	self.saveToToken = function saveToToken() {
    		var key, token, newContext, hadKey
    	    token = self.inherited(saveToToken)
    	    if (self._proposedMessage != null) {
    	    	token.setitem(PROPOSED_MESSAGE, tokenizeObject(self._proposedMessage))
    	    }
    		if (self._numberOfRetries != null) {
    			token.setitem(NUMBER_OF_RETRIES, tokenizeObject(self._numberOfRetries))
    		}
    	    if (self._lastTimeSent != null) {
    	    	token.setitem(LAST_TIME_SENT, tokenizeObject(self._lastTimeSent))
    	    }
    	    return token
    	}

    	/** Initialize the message from a storage token and some additional context (e.g., local objects) **/
    	self.initializeFromToken = function initializeFromToken(token, context) {
    		self.inherited(initializeFromToken, [token, context])
    		self._msgId= untokenizeObject(token.getitem(PROPOSED_MESSAGE_ID, true, null), context)
    	    self._proposedMessage = untokenizeObject(token.getitem(PROPOSED_MESSAGE, true, null), context)
    	    self._numberOfRetries = untokenizeObject(token.getitem(NUMBER_OF_RETRIES, true, null), context)
    	    self._lastTimeSent = untokenizeObject(token.getitem(LAST_TIME_SENT, true, null), context)
    	}
    }
})
    	
    	
/** The base class for a messaging node (either a Gateway or a Service) **/
var BaseMessagingNode = Zet.declare({
    CLASS_ID: 'BaseMessagingNode',
    // Base class for messaging gateways
    superclass: Serialization.Serializable,
    defineBody: function (self) {
        // Public Properties

        /** Initialize a messaging node.  Should have a unique ID and (optionally)
         also have one or more gateways connected.
         @param id: A unique ID for the node. If none given, a random UUID will be used.
         @type id: str
         @param gateways: Gateway objects, which this node will register with.
         @type gateways: list of MessagingGateway object
         **/
        self.construct = function construct(id, nodes) {
            self.inherited(construct, [id])
            if (nodes == null) {
                nodes = []
            }
            self._nodes = {}
            self._requests = {}
            self._uuid = UUID.genV4()
            self.addNodes(nodes)
            self.proposals = {}
            self.prioritizedAcceptedServiceIds = {}
            self.demotedAcceptedServiceIds = []
        }

        /** Receive a message. When a message is received, two things should occur:
         1. Any service-specific processing
         2. A check for callbacks that should be triggered by receiving this message
         The callback check is done here, and can be used as inherited behavior.
         **/
        self.receiveMessage = function receiveMessage(msg) {
            // Processing to handle a received message
            //console.log(self._id + " received MSG: "+ self.messageToString(msg));
            self._triggerRequests(msg)
        }

        /** Send a message to connected nodes, which will dispatch it (if any gateways exist). **/
        self.sendMessage = function sendMessage(msg) {
        	//console.log(self._id + " sent MSG: "+ self.messageToString(msg));
            self._distributeMessage(self._nodes, msg)
        }

        /** Handle an arriving message from some source.
         Services other than gateways should generally not need to change this.
         @param msg: The message arriving
         @param senderId: The id string for the sender of this message.
         **/
        self.handleMessage = function handleMessage(msg, senderId) {
            self.receiveMessage(msg)
        }

        /** Sends a message each of 'nodes', except excluded nodes (e.g., original sender) **/
        self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds) {
            var nodeId, node, condition
            if (excludeIds == null) {
                excludeIds = []
            }
            for (nodeId in nodes) {
                condition = nodes[nodeId].condition
                node = nodes[nodeId].node
                if ((excludeIds.indexOf(nodeId) < 0) &&
                    (condition == null || condition(msg))) {
                    self._transmitMessage(node, msg, self.getId())
                }
            }
        }

        /** Transmit the message to another node **/
        self._transmitMessage = function _transmitMessage(node, msg, senderId) {
            node.handleMessage(msg, senderId)
        }

        // Manage Connected Nodes

        /** Get all connected nodes for the gateway **/
        self.getNodes = function getNodes() {
            return Object.keys(self._nodes).map(function (key) {
                return self._nodes[key].node
            })
        }

        /** Connect nodes to this node **/
        self.addNodes = function addNodes(nodes) {
            var i
            if (nodes == null) {
                nodes = []
            }
            for (i = 0; i < nodes.length; i++) {
                nodes[i].onBindToNode(self)
                self.onBindToNode(nodes[i])
            }
        }

        /** Remove the given connected nodes. If nodes=null, remove all. **/
        self.removeNodes = function removeNodes(nodes) {
            var i
            if (nodes == null) {
                nodes = self.getNodes()
            }
            for (i = 0; i < nodes.length; i++) {
                nodes[i].onUnbindToNode(self)
                self.onUnbindToNode(nodes[i])
            }
        }

        /** Register the node and signatures of messages that the node is interested in **/
        self.onBindToNode = function onBindToNode(node) {
            if (!(node.getId() in self._nodes)) {
                self._nodes[node.getId()] = {
                    'node': node,
                    'conditions': node.getMessageConditions()
                }
            }
        }

        /** This removes this node from a connected node (if any) **/
        self.onUnbindToNode = function onUnbindToNode(node) {
            if (node.getId() in self._nodes) {
                delete self._nodes[node.getId()]
            }
        }

        /** Get a list of conditions functions that determine if a gateway should
         relay a message to this node (can be propagated across gateways to filter
         messages from reaching unnecessary parts of the gateway network).
         **/
        self.getMessageConditions = function getMessageConditions() {
            /** Function to check if this node is interested in this message type */
            return function () {
                return true
            }
        }

        /** Get the conditions for sending a message to a node **/
        self.getNodeMessageConditions = function getNodeMessageConditions(nodeId) {
            if (nodeId in self._nodes) {
                return self._nodes[nodeId].conditions
            } else {
                return function () {
                    return true
                }
            }
        }

        /** Update the conditions for sending a message to a node **/
        self.updateNodeMessageConditions = function updateNodeMessageConditions(nodeId, conditions) {
            if (nodeId in self._nodes) {
                self._nodes[nodeId] = [self._nodes[nodeId].node, conditions]
            }
        }

        // Request Management

        /** Internal function to get all pending request messages **/
        self._getRequests = function _getRequests() {
            var key, reqs
            reqs = []
            for (key in self._requests) {
                reqs.push(self._requests[key][0])
            }
            return reqs
        }

        /** Add a request to the queue, to respond to at some point
         @param msg: The message that was sent that needs a reply.
         @param callback: A function to call when the message is received, as f(newMsg, requestMsg)
         @TODO: Add a timeout for requests, with a timeout callback (maxWait, timeoutCallback)
         **/
        self._addRequest = function _addRequest(msg, callback) {
            if (callback != null) {
                self._requests[msg.getId()] = [msg.clone(), callback]
            }
        }

        /** Make a request, which is added to the queue and then sent off to connected services
         @param msg: The message that was sent that needs a reply.
         @param callback: A function to call when the message is received, as f(newMsg, requestMsg)
         **/
        self._makeRequest = function _makeRequest(msg, callback) {
            self._addRequest(msg, callback)
            self.sendMessage(msg)
            //console.log("SENT REQUEST:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
        }

        /** Trigger any requests that are waiting for a given message. A
         request is filled when the conversation ID on the message matches
         the one for the original request. When a request is filled, it is
         removed, unless the speech act was request whenever (e.g., always)
         @param msg: Received message to compare against requests.
         **/
        self._triggerRequests = function _triggerRequests(msg) {
            var key, convoId, oldMsg, callback
            //console.log("Heard REPLY:" + Serialization.makeSerialized(Serialization.tokenizeObject(msg)));
            convoId = msg.getContextValue(Messaging.CONTEXT_CONVERSATION_ID_KEY, null)
            //console.log("CONVO ID: " + convoId);
            //console.log(self._requests);
            if (convoId != null) {
                // @TODO: This is a dict, so can check directly?
                for (key in self._requests) {
                    if (key === convoId) {
                        oldMsg = self._requests[key][0]
                        callback = self._requests[key][1]
                        callback(msg, oldMsg)
                        // Remove from the requests, unless asked for a permanent feed
                        if (oldMsg.getSpeechAct() !== Messaging.REQUEST_WHENEVER_ACT) {
                            delete self._requests[key]
                        }
                    }
                }
            }
        }

        // Pack/Unpack Messages

        /** Convenience function to serialize a message **/
        self.messageToString = function messageToString(msg) {
            return Serialization.makeSerialized(Serialization.tokenizeObject(msg))
        }

        /** Convenience function to turn a serialized JSON message into a message
         If the message is invalid when unpacked, it is ignored.
         **/
        self.stringToMessage = function stringToMessage(msg) {
            if (CATCH_BAD_MESSAGES) {
                try {
                    msg = Serialization.untokenizeObject(Serialization.makeNative(msg))
                } catch (err) {
                    // console.log("ERROR: Could not process message data received.  Received:");
                    // console.log(msg);
                    msg = undefined
                }
            } else {
                msg = Serialization.untokenizeObject(Serialization.makeNative(msg))
            }
            return msg
        }
        
        self.makeProposal = function makeProposal(msg, successCallback, retryParams, policyType) {
    		var proposalId = null;
    		console.log('Context Keys : ' + msg.getContextKeys())
    		if(msg.getContextKeys()['proposalId'] == undefined) {
    			console.log('Setting ID for PROpOSAL KEY')
    			proposalId = UUID.genV4().toString();
    			msg.setContextValue('proposalId', proposalId);
    		}
    		msg.setContextValue('conversation-id', proposalId);
    		var makePropsalPckt = new Proposal(proposalId, msg, false, successCallback, retryParams, policyType, new Date().getTime());
    		makePropsalPckt.setRetryParams(retryParams);
    		makePropsalPckt.setPolicyType('Accept at all times');
    		makePropsalPckt.setAcknowledgementReceived(false);
    		//Checking if the retryParams are set. If set, then calls functions accordingly.
    		if(retryParams != null) {
    			if(retryParams['noOfAttemptsForProposal'] != null	) {
    				var proposalNoOfAttempts = retryParams['noOfAttemptsForProposal'];
    				if(retryParams['failSoftStrategyForProposedMsg'] != null) {
    					var failSoftStrategy = retryParams['failSoftStrategyForProposedMsg'];
    					makePropsalPckt.setFailSoftStrategyForProposedMsg(failSoftStrategy);
    					if(failSoftStrategy == "RESEND_MSG_WITH_ATTEMPT_COUNTS") {
    						makePropsalPckt.getRetryParams()['noOfAttemptsForProposedMsg'] = retryParams['noOfAttemptsForProposedMsg'];
    					} else if(failSoftStrategy == "QUIT_IN_X_TIME") {
    						makePropsalPckt.getRetryParams()['quitInTime'] = retryParams['quitInTime'];
    					} 
    				}
    				self.proposals[proposalId] =  makePropsalPckt;
    				self.sendProposal(msg, proposalNoOfAttempts);
    			} else {
    				self.proposals[proposalId] = makePropsalPckt;
    				self.sendMessage(msg);
    			}
    		} else {
    			self.proposals[proposalId] = makePropsalPckt;
    			self.sendMessage(msg);
    		}
    	}
        
        self.sendProposal = function sendProposal(msg, noOfAttempts) {
        	console.log('Sending Proposal');
            var count = 1
            var proposalId = msg.getContextValue('proposalId', null)
            var proposal = self.proposals[proposalId]
            while(count <= noOfAttempts && proposal.getAcknowledgementReceived() == false) {
           	 	count += 1
            	self.sendMessage(msg);
           	 	
           	 	async => {
           	 		self.sendProposal(msg, noOfAttempts-count);
           	 		//await(5000);
           	 	}
            	if (self.proposals[proposalId].getAcknowledgementReceived() == false) {
                        console.log("Timeout. Trying Again")   
                }
            }
            if(count > noOfAttempts && self.proposals[proposalId].getAcknowledgementReceived() == false) {
            	console.log("No Respose Received.")
            }
        }
        
        self.retryProposal = function retryProposal(proposalId) {
        	var proposal = self.proposals[proposalId];
        	self.sendProposal(proposal.getProposal(), proposal.getRetryParams()['PROPOSAL_ATTEMPT_COUNT']);
        }
        
        self.sendNewProposedMessage = function sendNewProposedMessage(msg, proposalId) {
            console.log('Starting to Send Proposed Message')
            self.sendMessage(msg)
            if(msg.getId() in self.proposals[proposalId].getProposedMessages()) {
                	console.log("Seems Proposed Message Hasn't been Processed");
                	self.proposals[proposalId].setAcknowledgementReceived(false);
                    self.retryProposal(proposalId)
                } else {
                	console.log("Proposed Message Sent Successfully")
                }
        }
        
        // Fail Soft Strategy 1 - Send Proposed Message With Attempt Count.
        self.sendProposedMsgWithAttemptCnt = function sendProposedMsgWithAttemptCnt(proposal) {
            console.log('Fail Soft Strategy : Sending With Attempt Count')
            var attemptCount = proposal.getRetryParams()['noOfAttemptsForProposedMsg']
            for (var key in proposal.getProposedMessages()) {
            	console.log( proposal.getProposedMessages())
            		var proposedMessage = proposal.getProposedMessages()[key];
            		console.log('HOOOLA' + proposedMessage);
            		if(proposedMessage.getNumberOfRetries() < attemptCount) {
            			proposedMessage.setNumberOfRetries(proposedMessage.getNumberOfRetries() + 1)
                        console.log("Send Proposed Message - Attempt " + proposedMessage.getNumberOfRetries())
                        self.sendNewProposedMessage(proposedMessage.getProposedMessage(), proposal.getId())
                    }
            		
            }
        }
        
        // Decides Proposed Message Strategy and delegates messages accordingly
        // to sendProposedMessage(BaseMessage msg, String proposalId).
        self.sendProposedMessage = function sendProposedMessage(proposalId) {
             var proposal = self.proposals[proposalId]
             
             if(!proposal.getProposalProcessed()) {
                var failSoftStrategy = proposal.getRetryParams()['failSoftStrategyForProposedMsg'] != null ? proposal.getRetryParams()['failSoftStrategyForProposedMsg'] : null;
                console.log('BOOOOOOLA ' + failSoftStrategy); 
                if(failSoftStrategy != null) {
                    if(failSoftStrategy == 'RESEND_MSG_WITH_ATTEMPT_COUNTS') {
                    	self.sendProposedMsgWithAttemptCnt(proposal)
                    } else if(failSoftStrategy == 'QUIT_IN_X_TIME') {
                        self.sendProposedMsgWithQuitXTime(proposal)
                    } else if(failSoftStrategy == 'RESEND_MSG_WITH_DEPRIORITZATION') { 
                        self.sendProposedMsgWithPrioritization(proposal)
                    }
                } else { 
                    //No Strategy.
                    for(const [key, value] in proposal.getProposedMessages()) {
                        if(value.getNumberOfRetries() < 2) {
                            value.setNumberOfRetries(value.getNumberOfRetries() + 1)
                            console.log('Send Proposed Message - Attempt ' + value.getNumberOfRetries())
                            self.sendNewProposedMessage(value.getProposedMessage(), proposalId);
                        }
                    }
                }
            }
        }
        
        //Fail Soft Strategy 2 - Send Proposed Message With Quit in X Time.
        self.sendProposedMsgWithQuitXTimedef = function sendProposedMsgWithQuitXTimedef(proposal) {
            duration = proposal.getRetryParams().get(QUIT_IN_TIME)            
            for(const [key, value] in proposal.getProposedMessages()){
                if(time.time() - value.getLastTimeSent() < duration ){
                    value.setNumberOfRetries(value.getNumberOfRetries() + 1)
                    console.log('Send Proposed Message')
                    self.sendProposedMessage(value.getMsg(), proposal.getId())
                } else {
                    console.log("Cannot Send Message. Attempt to Send Quit After " + str(duration) + " seconds.")
                }
            }
        }
        
        
    }
})

var MessagingGateway = Zet.declare({
    CLASS_ID: 'MessagingGateway',
    // Base class for messaging gateways
    superclass: BaseMessagingNode,
    defineBody: function (self) {
        // Public Properties

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

        // Handle Incoming Messages
        /** Receive a message from a connected node and propogate it. **/
        self.handleMessage = function handleMessage(msg, senderId) {
            self.receiveMessage(msg)
            self._distributeMessage(self._nodes, msg, [senderId])
        }

        // Relay Messages

        /** Distribute the message, after adding some gateway context data. **/
        self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds) {
            msg = self.addContextDataToMsg(msg)
            self.inherited(_distributeMessage, [nodes, msg, excludeIds])
        }

        /** Add the additional context data in the Gateway scope, unless those
         keys already exist in the message's context object.
         **/
        self.addContextDataToMsg = function addContextDataToMsg(msg) {
            var key
            for (key in self._scope) {
                if (!(msg.hasContextValue(key))) {
                    msg.setContextValue(key, self._scope[key])
                }
            }
            return msg
        }
    }
})

/** Messaging Gateway Node Stub for Cross-Domain Page Communication
 A stub gateway that is a placeholder for a PostMessage gateway in another frame.
 This should only be a child or parent of a PostMessageGateway, because other
 nodes will not know to send messages via HTML5 postMessage to the actual frame
 that this stub represents.
 **/
var PostMessageGatewayStub = Zet.declare({
    CLASS_ID: 'PostMessageGatewayStub',
    superclass: BaseMessagingNode,
    defineBody: function (self) {
        // Private Properties
        var ANY_ORIGIN = '*'

        // Public Properties

        /** Initialize a PostMessageGatewayStub
         @param id: Unique id for the gateway
         @param gateway: The parent gateway for this stub
         @param origin: The base URL expected for messages from this frame.
         @param element: The HTML element (e.g., frame/iframe) that the stub represents. By default parent window.
         **/
        self.construct = function construct(id, gateway, origin, element) {
            var nodes = null
            if (gateway != null) {
                nodes = [gateway]
            }
            self.inherited(construct, [id, nodes])
            if (origin == null) {
                origin = ANY_ORIGIN
            }
            if (element == null) {
                element = parent
            }
            if (element === window) {
                element = null
            }
            self._origin = origin
            self._element = element
            self._queue = []
        }

        /** Get the origin, which is the frame location that is expected **/
        self.getOrigin = function getOrigin() {
            return self._origin
        }

        /** Get the HTML element where messages would be sent **/
        self.getElement = function getElement() {
            return self._element
        }

        self.getQueue = function getQueue() {
            return self._queue
        }
    }
})


/** Messaging Gateway for Cross-Domain Page Communication
 Note: This should not directly take other PostMessageGateways as nodes.
 PostMessageGatewayStub objects must be used instead. Only use ONE
 PostMessageGateway per frame.
 **/
var PostMessageGateway = Zet.declare({
    superclass: MessagingGateway,
    CLASS_ID: 'PostMessageGateway',
    defineBody: function (self) {
        // Private Properties
        var ANY_ORIGIN = '*'

        // Public Properties

        /** Initialize a PostMessageGateway
         @param id: The unique ID for this gateway.
         @param nodes: Child nodes for the gateway
         @param origin: The origin URL for the current window
         @param scope: Additional context parameters to add to messages sent by children.
         **/
        self.construct = function construct(id, nodes, origin, scope) {
            if (origin == null) {
                origin = ANY_ORIGIN
            }
            self._origin = origin
            // Get these ready before adding nodes in base constructor
            self._postNodes = {}
            self._validOrigins = {}
            self._anyOriginValid = true
            self._registrationInterval = 0
            self._registry = {}
            // Construct
            self.inherited(construct, [id, nodes, scope])
            self.validatePostingHierarchy()
            if (window) {
                self.bindToWindow(window)
            }
            if (nodes && nodes.length) {
                nodes.forEach(function (t) {
                    if (PostMessageGatewayStub.isInstance(t) && t.getElement() === window.parent) {
                        self.startRegistration(t)
                        t._isActive = false        //stub is inactive unless registered
                    }
                })
            }
        }

        self.startRegistration = function (node) {
            var senderId = self.getId()
            var msg = Message(senderId, 'REGISTER', null, true)
            var interval = setInterval(function () {
                self._transmitPostMessage(node, msg, senderId)
            }, 2000)
            self._registrationInterval = interval
        }

        self.stopRegistration = function () {
            clearInterval(self._registrationInterval)
        }

        /** Get the origin for this window **/
        self.getOrigin = function getOrigin() {
            return self._origin
        }

        /** Get a stub that is the equivalent to this gateway **/
        self.getStub = function getStub() {
            return PostMessageGatewayStub(self._id, self._gateway, self._origin)
        }

        /** Validates that no additional PostMessageGateway nodes are connected
         and in the same frame. Valid neighbors can have no PostMessageGateway nodes,
         and only the parent OR the children can be of the PostMessageGatewayStub class
         **/
        self.validatePostingHierarchy = function validatePostingHierarchy() {
            var key
            for (key in self._nodes) {
                if (PostMessageGateway.isInstance(self._nodes[key])) {
                    throw TypeError("Error: Cannot directly connect PostMessageGateways")
                }
            }
            // @TODO: Check for cycles in the posting hierarchy
        }

        /** Register the node and signatures of messages that the node is interested in **/
        self.onBindToNode = function onBindToNode(node) {
            self.inherited(onBindToNode, [node])
            self._onAttachNode(node)
        }

        /** This removes this node from a connected node (if any) **/
        self.onUnbindToNode = function onUnbindToNode(node) {
            self._onDetachNode(node)
            self.inherited(onUnbindToNode, [node])
        }

        /** When attaching nodes, adds any origins of PostMessageGatewayStubs
         to an allowed list of valid origins for HTML5 postMessages.
         @param node: A child node to attach.
         @type node: BaseMessagingNode
         **/
        self._onAttachNode = function _onAttachNode(node) {
            // @TODO: Should check if already attached and raise error
            if (PostMessageGatewayStub.isInstance(node) &&
                (!(node.getId() in self._postNodes))) {
                if (self._validOrigins[node.getOrigin()] == null) {
                    self._validOrigins[node.getOrigin()] = 1
                } else {
                    self._validOrigins[node.getOrigin()] += 1
                }
                if (node.getOrigin() === ANY_ORIGIN) {
                    self._anyOriginValid = true
                }
                self._postNodes[node.getId()] = node
            }
        }

        /** When detaching nodes, clears any origins of PostMessageGatewayStubs
         from an allowed list of valid origins for HTML5 postMessages.
         @param node: A child node to attach.
         @type node: BaseMessagingNode
         **/
        self._onDetachNode = function _onDetachNode(node) {
            if (PostMessageGatewayStub.isInstance(node) &&
                (node.getId() in self._postNodes)) {
                self._validOrigins[node.getOrigin()] += -1
                if (self._validOrigins[node.getOrigin()] === 0) {
                    delete self._validOrigins[node.getOrigin()]
                    if (!(ANY_ORIGIN in self._validOrigins)) {
                        self._anyOriginValid = false
                    }
                }
                delete self._postNodes[node.getId()]
            }
        }

        /** Bind the HTML5 event listener for HTML5 postMessage **/
        self.bindToWindow = function bindToWindow(aWindow) {
            var eventMethod, eventer, messageEvent
            eventMethod = aWindow.addEventListener ? "addEventListener" : "attachEvent"
            eventer = aWindow[eventMethod]
            messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message"
            eventer(messageEvent, function (event) {
                self._receivePostMessage(event)
            })
        }

        // Messaging

        /** Send a message to parent. Send as normal, but send using sendPostMessage
         if sending to a PostMessage stub.
         **/
        /** Transmit the message to another node **/
        self._transmitMessage = function _transmitMessage(node, msg, senderId) {
            if (PostMessageGatewayStub.isInstance(node)) {
                if (node._isActive) {
                    self._processPostMessageQueue(node)
                    self._transmitPostMessage(node, msg, senderId)
                } else {
                    node.getQueue().push({
                        msg: msg,
                        senderId: senderId
                    })
                }
            } else {
                node.handleMessage(msg, senderId)
            }
        }

        self._processPostMessageQueue = function (stub) {
            stub.getQueue().forEach(function (o) {
                self._transmitPostMessage(stub, o.msg, o.senderId)
            })
            stub.getQueue().splice(0, stub.getQueue().length)
        }

        // HTML5 PostMessage Commands
        self._transmitPostMessage = function _transmitPostMessage(node, msg, senderId) {
            if (node._stubId) {
                msg.setObject(msg.getObject() == null ? {} : msg.getObject())
                msg.getObject()["stubId"] = node._stubId
            }

            var postMsg, element
            postMsg = JSON.stringify({
                'SuperGLU': true,
                'msgType': 'SuperGLU',
                'version': version,
                'senderId': senderId,
                'targetId': node.getId(),
                'msg': self.messageToString(msg)
            })
            element = node.getElement()
            if (element != null) {
                // console.log(JSON.parse(postMsg).senderId + " POSTED UP " + self.messageToString(msg));
                element.postMessage(postMsg, node.getOrigin())
            }
        }

        self._receivePostMessage = function _receivePostMessage(event) {
            var senderId, message, targetId
            //console.log(self._id + " RECEIVED POST " + JSON.parse(event.data));
            if (self.isValidOrigin(event.origin)) {
                try {
                    message = JSON.parse(event.data)
                } catch (err) {
                    // console.log("Post Message Gateway did not understand: " + event.data);
                    return
                }
                senderId = message.senderId
                targetId = message.targetId
                message = self.stringToMessage(message.msg)
                // console.log(message);
                if (Message.isInstance(message) &
                    (targetId === self.getId()) &&
                    message.getVerb() === 'REGISTER'
                ) {
                    var obj = message.getObject() || {}
                    var node = null
                    var verb = 'REGISTERED'
                    var stubId = UUID.genV4().toString()
                    if (obj.stubId) {
                        stubId = obj.stubId
                        node = self._registry[stubId]
                    } else {
                        node = PostMessageGatewayStub(senderId, null, null, event.source)
                        self._registry[stubId] = node
                        self.addNodes([node])
                    }
                    var msg = Message(self.getId(), verb, {stubId: stubId}, true)
                    self._transmitPostMessage(node, msg, self.getId())
                } else if (Message.isInstance(message) &
                    (targetId === self.getId()) &&
                    message.getVerb() === 'REGISTERED'
                ) {
                    var nodes = self.getNodes()
                    nodes.forEach(function (node) {
                        if (PostMessageGatewayStub.isInstance(node) && node.getElement() === window.parent) {
                            self.stopRegistration()
                            node._isActive = true        //stub is inactive unless registered
                            self._stubId = message.getObject().stubId
                            self._processPostMessageQueue(node)
                        }
                    })
                }
                else if (Message.isInstance(message) &
                    (targetId === self.getId()) &&
                    (senderId in self._postNodes)) {
                    if (PostMessageGatewayStub.isInstance(self._postNodes[senderId])) {
                        self._postNodes[senderId]._isActive = true
                    }
                    self.handleMessage(message, senderId)
                }
            }
        }

        self.isValidOrigin = function isValidOrigin(url) {
            if (self._anyOriginValid) {
                return true
            } else {
                return url in self._validOrigins
            }
        }
    }
})


var HTTPMessagingGateway = Zet.declare({
    // Base class for messaging gateways
    // This uses socket.io.js and uuid.js
    superclass: MessagingGateway,
    CLASS_ID: 'HTTPMessagingGateway',
    defineBody: function (self) {
        // Public Properties
        // Events: connecting, connect, disconnect, connect_failed, error,
        //         message, anything, reconnecting, reconnect, reconnect_failed
        // Listed At: github.com/LearnBoost/socket.io/wiki/Exposed-events
        var MESSAGING_NAMESPACE = '/messaging',
            TRANSPORT_SET = ['websocket',
                'flashsocket',
                'htmlfile',
                'xhr-polling',
                'jsonp-polling']
        // Set Socket.IO Allowed Transports


        self.construct = function construct(id, nodes, url, sessionId, scope) {
            self.inherited(construct, [id, nodes, scope])      // Classifier not used here, as messages are exact responses.
            if (url == null) {
                url = null
            }
            if (sessionId == null) {
                sessionId = UUID.genV4().toString()
            }
            self._url = url
            self._socket = io.connect(self._url + MESSAGING_NAMESPACE)
            self._isConnected = false
            self._sessionId = sessionId
            self._socket.on('message', self.receiveWebsocketMessage)
        }

        self.bindToConnectEvent = function bindToConnectEvent(funct) {
            self._socket.on('connect', funct)
        }

        self.bindToCloseEvent = function bindToCloseEvent(funct) {
            self._socket.on('disconnect', funct)
        }

        self.addSessionData = function addSessionData(msg) {
            msg.setContextValue(SESSION_ID_KEY, self._sessionId)
            return msg
        }

        /** Distribute the message, after adding some gateway context data. **/
        self._distributeMessage = function _distributeMessage(nodes, msg, excludeIds, noSocket) {
            msg = self.addContextDataToMsg(msg)
            if (noSocket !== true && self._url != null) {
                msg = self.addSessionData(msg)
                self.sendWebsocketMessage(msg)
            }
            self.inherited(_distributeMessage, [nodes, msg, excludeIds])
        }

        self.sendWebsocketMessage = function sendWebsocketMessage(msg) {
            msg = self.messageToString(msg)
            self._socket.emit('message', {data: msg, sessionId: self._sessionId})
        }

        self.receiveWebsocketMessage = function receiveWebsocketMessage(msg) {
            var sessionId
            sessionId = msg.sessionId
            msg = msg.data
            msg = self.stringToMessage(msg)
            // console.log("GOT THIS:" + sessionId);
            // console.log("Real Sess: " + self._sessionId);
            if (Message.isInstance(msg) &&
                (sessionId == null || sessionId == self._sessionId)) {
                self._distributeMessage(self._nodes, msg, [], true)
            }
        }
    }
})


var BaseService = Zet.declare({
    // Base class for messaging gateways
    superclass: BaseMessagingNode,
    CLASS_ID: 'BaseService',
    defineBody: function (self) {
        // Public Properties

        self.construct = function construct(id, gateway) {
            var nodes = null
            if (gateway != null) {
                nodes = [gateway]
            }
            self.inherited(construct, [id, nodes])
        }

        /** Connect nodes to this node.
         Only one node (a gateway) should be connected to a service.
         **/
        self.addNodes = function addNodes(nodes) {
            //if (nodes.length + self.getNodes().length <= 1) {
                self.inherited(addNodes, [nodes])
            //} else {
            //    console.log("Error: Attempted to add more than one node to a service. Service must only take a single gateway node. Service was: " + self.getId())
            //}
        }

        /** Bind nodes to this node.
         Only one node (a gateway) should be connected to a service.
         **/
        self.onBindToNode = function onBindToNode(node) {
            if (self.getNodes().length === 0) {
                self.inherited(onBindToNode, [node])
            } else {
                console.log("Error: Attempted to bind more than one node to a service. Service must only take a single gateway node.")
            }
        }
    }
})

var TestService = Zet.declare({
    // Base class for messaging gateways
    superclass: BaseService,
    CLASS_ID: 'TestService',
    defineBody: function (self) {
        // Public Properties
        self.receiveMessage = function receiveMessage(msg) {
            console.log("TEST SERVICE " + self.getId() + " GOT: \n" + self.messageToString(msg))
            self.inherited(receiveMessage, [msg])
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

namespace.SESSION_ID_KEY = SESSION_ID_KEY
namespace.BaseService = BaseService
namespace.MessagingGateway = MessagingGateway
namespace.PostMessageGatewayStub = PostMessageGatewayStub
namespace.PostMessageGateway = PostMessageGateway
namespace.HTTPMessagingGateway = HTTPMessagingGateway
namespace.TestService = TestService
namespace.Proposal = Proposal
namespace.ProposedMessage = ProposedMessage

module.exports = namespace
