# -*- coding: utf-8 -*-
import datetime
from email import policy
import json
from queue import Queue
import time
import traceback
import urllib
import asyncio
from uuid import uuid4

from SuperGLU.Core.BlackWhiteListEntry import BlackWhiteListEntry, GatewayBlackWhiteListConfiguration
from SuperGLU.Core.FIPA.SpeechActs import REQUEST_WHENEVER_ACT, RESEND_MSG_WITH_ATTEMPT_COUNTS, QUIT_IN_X_TIME, RESEND_MSG_WITH_DEPRIORITZATION, ALL_TIME_ACCEPT_PROPOSAL_ACK

from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.Messaging import VHMessage, GIFTMessage
from SuperGLU.Core.ServiceConfiguration import  ServiceConfiguration
from SuperGLU.Util.ErrorHandling import logError, logWarning
from SuperGLU.Util.Serialization import (SuperGlu_Serializable, serializeObject,
                            nativizeObject)
import stomp
from pip._vendor.retrying import Attempt


CATCH_BAD_MESSAGES = False
SESSION_KEY = 'sessionId'
ORIGINATING_SERVICE_ID_KEY = 'originatingServiceId'
USE_BLACK_WHITE_LIST = False

SEND_MSG_SLEEP_TIME = 5000
PROPOSAL_ATTEMPT_COUNT = 'noOfAttemptsForProposal'
FAIL_SOFT_STRATEGY= 'failSoftStrategyForProposedMsg'
QUIT_IN_TIME= 'quitInTime'
PROPOSED_MSG_ATTEMPT_COUNT = 'noOfAttemptsForProposedMsg';

#Modify PolicyType and Look for SuccessCallBack failSoftStrategyForProposedMsg
class Proposals(SuperGlu_Serializable):

    def __init__(self, id=None, proposal=None, proposalProcessed=False, acknowledgementReceived=False, 
                 retryParams={}, policyType=ALL_TIME_ACCEPT_PROPOSAL_ACK, failSoftStrategyForProposedMsg='noOfAttempts',
                  proposedMessage={}, proposedTime=None):
        self.id = id;
        self.proposal = proposal
        self.proposalProcessed = proposalProcessed
        self.acknowledgementReceived = acknowledgementReceived
        self.retryParams = retryParams
        self.policyType = policyType
        self.failSoftStrategyForProposedMsg = failSoftStrategyForProposedMsg
        self.proposedMessage = proposedMessage
        self.proposedTime = proposedTime
        
    def getId(self):
        return self.id
    
    def setproposal(self, id):
        self.id = id
    
    def getProposal(self):
        return self.proposal
    
    def setProposal(self, proposal):
        self.proposal = proposal
        
    def getProposalProcessed(self):
        return self.proposalProcessed
    
    def setProposalProcessed(self, proposalProcessed):
        self.proposalProcessed = proposalProcessed
    
    def getAcknowledgementReceived(self):
        return self.acknowledgementReceived
    
    def setAcknowledgementReceived(self, acknowledgementReceived):
        self.acknowledgementReceived = acknowledgementReceived
    
    def getRetryParams(self):
        return self.retryParams
    
    def setRetryParams(self, retryParams):
        self.retryParams = retryParams

    def getPolicyType(self):
        return self.policyType
    
    def setPolicyType(self, policyType):
        self.policyType = policyType
    
    def getFailSoftStrategyForProposedMsg(self):
        return self.failSoftStrategyForProposedMsg
    
    def setFailSoftStrategyForProposedMsg(self, failSoftStrategyForProposedMsg):
        self.failSoftStrategyForProposedMsg = failSoftStrategyForProposedMsg

    def getProposedMessage(self):
        return self.proposedMessage
    
    def setProposedMessage(self, proposedMessage):
        self.proposedMessage = proposedMessage
        
    def getProposedTime(self):
        return self.proposedTime
    
    def setProposedTime(self, proposedTime):
        self.proposedTime = proposedTime
        

class ProposedMessage(SuperGlu_Serializable):
    def __init__(self, msgId = None, proposedMessage = None, numberOfRetries = 0, lastTimeSent = None):
        self.msgId = msgId
        self.proposedMessage = proposedMessage
        self.numberOfRetries = numberOfRetries
        self.lastTimeSent = lastTimeSent
        
    def getMsgId(self):
        return self.msgId
    
    def setMsgId(self, msgId):
        self.msgId = msgId
        
    def getProposedMessage(self):
        return self.proposedMessage
    
    def setProposedMessage(self, proposedMessage):
        self.proposedMessage = proposedMessage
        
    def getNumberOfRetries(self):
        return self.numberOfRetries
    
    def setNumberOfRetries(self, numberOfRetries):
        self.numberOfRetries = numberOfRetries
        
    def getLastTimeSent(self):
        return self.lastTimeSent
    
    def setLastTimeSent(self, lastTimeSent):
        self.lastTimeSent = lastTimeSent
          
        
        
                
class BaseMessagingNode(SuperGlu_Serializable):
    """ Base class for messaging """

    def __init__(self, anId=None, gateway=None, authenticator=None, nodes=[], blackList=[], whiteList=[]):
        super(BaseMessagingNode, self).__init__(anId)
        self._gateway = gateway
        self._authenticator = authenticator
        if gateway is not None:
            self.bindToGateway(gateway)
        self._requests = {}

        if nodes is None: nodes = []
        self._nodes = {}

        self.addNodes(nodes)

        #don't allow null values for the black and white list
        #not sure if this is necessary but it won't hurt
        if blackList is None:
            blackList = []

        if whiteList is None:
            whiteList = []

        self._blackList = blackList
        self._whiteList = whiteList
        self.proposals = {}
        self.prioritizedAcceptedServiceIds = {}
        self.demotedAcceptedServiceIds = []
        


    # Manage Child Nodes
    def addNodes(self, nodes):
        for node in nodes:
            node.bindToGateway(self)

    def getNodes(self):
        return [service for condition, service in list(self._nodes.values())]

    def register(self, node):
        """ Register the signatures of messages that the node is interested in """
        self._nodes[node.getId()] = (node.getMessageConditions(), node)

    def unregister(self, node):
        """ Take actions to remove the node from the list """
        if node.getId() in self._nodes:
            del self._nodes[node.getId()]

    def acceptIncomingMessage(self, msg):
        result = True

        if USE_BLACK_WHITE_LIST:
            for entry in self._whiteList:
                if entry.evaluateMessage(msg):
                    result = True
                    break

            for entry in self._blackList:
                if entry.evaluateMessage(msg):
                    result = False
                    break
        return result

    def sendMessage(self, msg):
        #print("%s sending %s"%(self.__class__.__name__, msg))
        if self._gateway is not None:
            #print("Actually sent it.")
            self._gateway.dispatchMessage(msg, self.getId())
        
           
        self.distributeMessage(msg, msg.getContextValue(ORIGINATING_SERVICE_ID_KEY))
        #logWarning("Message DISTRIBUTED: %s"%(msg,))

    def receiveMessage(self, msg):
        if not self.acceptIncomingMessage(msg):
            return
        self._triggerRequests(msg)
    
    def distributeMessage(self, msg, senderId=None):
        """ Pass a message down all interested children (except sender) """
        self._distributeMessage(self._nodes, msg, senderId)

    def _distributeMessage(self, nodes, msg, senderId=None):
        """ Implement passing a message down all interested children (except sender) """
        #print('Currently I am ' + str(self.getId()) + '. And I have ' + str(len(nodes)) + ' in my channel')
        for nodeId in nodes:
            condition = nodes[nodeId][0]
            node = nodes[nodeId][1]
            if not self.isMessageOnGatewayBlackList(node, msg) and self.isMessageOnGatewayWhiteList(node, msg):
                if ((nodeId != senderId) and ((condition  is None) or condition(msg))):
                    node.receiveMessage(msg)
        
    def isMessageOnGatewayBlackList(self, destination, msg):
        return False
    
    def isMessageOnGatewayWhiteList(self, destination, msg):
        return True
    
    
    def bindToGateway(self, gateway):
        self.unbindToGateway()
        self._gateway = gateway
        self._gateway.register(self)

    def unbindToGateway(self):
        if self._gateway is not None:
            self._gateway.unregister(self)

    def getMessageConditions(self):
        """ Function to check if this node is interested in this message type """
        return None

    def _getRequests(self):
        return list(self._requests.values())

    def _addRequest(self, msg, callback):
        if callback is not None:
            self._requests[msg.getId()] = (msg.clone(), callback)

    def _makeRequest(self, msg, callback):
        self._addRequest(msg, callback)
        self.sendMessage(msg)

    def _triggerRequests(self, msg):
        convoId = msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, None)
        if convoId is not None and convoId in self._requests:
            key = convoId
            oldMsg = self._requests[key][0]
            callback = self._requests[key][1]
            callback(msg, oldMsg)
            # Remove from the requests, unless asked for a permanent feed
            if oldMsg.getSpeechAct() != REQUEST_WHENEVER_ACT:
                del self._requests[key]

    def _createRequestReply(self, msg):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg

    # Pack/Unpack Messages
    def messageToString(self, msg):
        return serializeObject(msg)

    def stringToMessage(self, msg):
        if (CATCH_BAD_MESSAGES):
            try:
                msg = nativizeObject(msg)
            except:
                logWarning("ERROR: Could not process message data received.  Received:" + str(msg))
                msg = None
        else:
            msg = nativizeObject(msg)
        return msg

    def messagesToStringList(self, msgs):
        return json.dumps([self.messageToString(m) for m in msgs])

    def stringListToMessages(self, strMsgs):
        return [self.stringToMessage(sm) for sm in json.loads(strMsgs)]
    
    
    # Sends Proposal Request Message With Attempt Count.
    @asyncio.coroutine
    def sendProposal(self, msg, noOfAttempts):
        count = 1
        proposalId = msg.getContextValue(Message.PROPOSAL_KEY, None)
        proposal = self.proposals[proposalId]
        while count <= int(noOfAttempts) and proposal.getAcknowledgementReceived() == False :
            print("Send Proposal Request - Attempt " + str(count))
            self.sendMessage(msg)
            count += 1
            asyncio.sleep(SEND_MSG_SLEEP_TIME);
            if self.proposals[proposalId].getAcknowledgementReceived() == False :
                print("Timeout.")
        if count > int(noOfAttempts) and self.proposals[proposalId].getAcknowledgementReceived() == False :
            print("No Respose Received.")
            
    
    
    # Sends Proposed Message.
    @asyncio.coroutine
    def sendNewProposedMessage(self, msg, proposalId) :
        print('Starting to Send Proposed Message')
        self.sendMessage(msg)
        asyncio.sleep(SEND_MSG_SLEEP_TIME)
        if msg.getId() in self.proposals.get(proposalId).getProposedMessage():
            print("Seems Proposed Message Hasn't been Processed");
            self.retryProposal(proposalId)
        else :
            print("Proposed Message Sent Successfully")
            
            
    # Fail Soft Strategy 1 - Send Proposed Message With Attempt Count.
    def sendProposedMsgWithAttemptCnt(self, proposal) :
        print('Fail Soft Strategy : Sending With Attem')
        attemptCount = int(str(proposal.getRetryParams().get(PROPOSED_MSG_ATTEMPT_COUNT)))    
        for key, value in proposal.getProposedMessage().items() :
            if value.getNumberOfRetries() < attemptCount :
                value.setNumberOfRetries(value.getNumberOfRetries() + 1)
                print("Send Proposed Message - Attempt " + str(value.getNumberOfRetries()))
                proposedMessageLoop = asyncio.get_event_loop()
                
                if proposedMessageLoop.is_running() == True :
                    asyncio.ensure_future(self.sendNewProposedMessage(value.getProposedMessage(), proposal.getId()))
                else :
                    proposedMessageLoop.run_until_complete(self.sendNewProposedMessage(value.getProposedMessage(), proposal.getId()))
                
                
    # Decides Proposed Message Strategy and delegates messages accordingly
    # to sendProposedMessage(BaseMessage msg, String proposalId).
    def sendProposedMessage(self, proposalId) :
        print('Sending')
        proposal = self.proposals[proposalId]
        if proposal.getProposalProcessed() == False :
            failSoftStrategy = proposal.getRetryParams()[FAIL_SOFT_STRATEGY] if proposal.getRetryParams()[FAIL_SOFT_STRATEGY] != None else None
            if failSoftStrategy != None :
                if failSoftStrategy == RESEND_MSG_WITH_ATTEMPT_COUNTS :
                    self.sendProposedMsgWithAttemptCnt(proposal)
                elif failSoftStrategy == QUIT_IN_X_TIME :
                    self.sendProposedMsgWithQuitXTime(proposal)
                elif failSoftStrategy == RESEND_MSG_WITH_DEPRIORITZATION : 
                    self.sendProposedMsgWithPrioritization(proposal);
            else : 
                #No Strategy.
                for key, value in proposal.getProposedMessages() :
                    if value.getNumberOfRetries() < 2 :
                        value.setNumberOfRetries(value.getNumberOfRetries() + 1)
                        print('Send Proposed Message - Attempt ' + str(value).getNumberOfRetries())
                        self.sendNewProposedMessage(value.getProposedMessage(), proposalId);
    

       
    
    # Fail Soft Strategy 2 - Send Proposed Message With Quit in X Time.
    def sendProposedMsgWithQuitXTime (self, proposal) :
        duration = str(proposal.getRetryParams().get(QUIT_IN_TIME))            
        for key, value in proposal.getProposedMessages() :
            if time.time() - value.getLastTimeSent() < duration :
                value.setNumberOfRetries(value.getNumberOfRetries() + 1)
                print('Send Proposed Message')
                self.sendProposedMessage(value.getMsg(), proposal.getId())
            else :
                print("Cannot Send Message. Attempt to Send Quit After " + str(duration) + " seconds.")
    
    
    # Fail Soft Strategy 3
    def sendProposedMsgWithPrioritization(self, proposal) :
        if len(self.prioritizedAcceptedServiceIds) < 1 : 
            print("Exhausted All Services")
        else :
            print("Attempting to Send Proposed Message After Prioritization")
            for key, value in proposal.getProposedMessages() :
                self.sendProposedMessage(value.getMsg(), proposal.getId());
                
                
    # Making Proposal performs 2 Tasks: maintains a list of all proposals that will be sent across and actually sends the message. 
    def makeProposal(self, msg, retryParams, policyType) :  
        proposalId = None;
        if msg.getContext().get(Message.PROPOSAL_KEY) is None:
            proposalId = str(uuid4())
            msg.getContext()[Message.PROPOSAL_KEY] = proposalId
        msg.getContext()[Message.CONTEXT_CONVERSATION_ID_KEY] = proposalId
        makePropsalPckt = Proposals(id = proposalId, proposal = msg, proposalProcessed = False, acknowledgementReceived = False, retryParams = retryParams, policyType = policyType, proposedTime = time.time())         
    
        if (retryParams != None and retryParams[PROPOSAL_ATTEMPT_COUNT] != None) : 
            makeProposal = int(str(retryParams[PROPOSAL_ATTEMPT_COUNT]))
            if FAIL_SOFT_STRATEGY in retryParams :
                failSoftStrategy = str(retryParams.get(FAIL_SOFT_STRATEGY))
                makePropsalPckt.setFailSoftStrategyForProposedMsg(failSoftStrategy)
                if failSoftStrategy == RESEND_MSG_WITH_ATTEMPT_COUNTS :
                    makePropsalPckt.getRetryParams()[PROPOSED_MSG_ATTEMPT_COUNT] = int(retryParams[PROPOSED_MSG_ATTEMPT_COUNT])
                elif failSoftStrategy == QUIT_IN_X_TIME :
                    makePropsalPckt.getRetryParams()[QUIT_IN_TIME]  = retryParams[QUIT_IN_TIME]
                self.proposals[proposalId] = makePropsalPckt
                
                
                if asyncio.get_event_loop() == None :
                    loop = asyncio.new_event_loop()
                else :
                    loop = asyncio.get_event_loop()
                if loop.is_running() == True :
                    asyncio.ensure_future(self.sendProposal(msg, retryParams[PROPOSAL_ATTEMPT_COUNT]))
                else :
                    loop.run_until_complete(self.sendProposal(msg, retryParams[PROPOSAL_ATTEMPT_COUNT]))
            
            else :
                self.proposals[proposalId] = makePropsalPckt
                self.sendMessage(msg);
        else :
                self.proposals[proposalId] = makePropsalPckt
                self.sendMessage(msg)
                
    # This Overridden function of Make Proposal is used when proposal exists for which Proposed Message function has failed.
    def retryProposal (self, proposalId) :
        proposal = self.proposals[proposalId]
        self.sendProposal(proposal.getProposal(), int(proposal.getRetryParams()[PROPOSAL_ATTEMPT_COUNT]));
                        
class MessagingGateway(BaseMessagingNode):

    def __init__(self, anId=None, nodes=None, gateway=None, authenticator=None, scope=None, serviceConfiguration=None):
        if scope is None: scope = {}
        if serviceConfiguration is not None:
            super(MessagingGateway, self).__init__(anId, gateway, authenticator, nodes, serviceConfiguration.getBlackList(), serviceConfiguration.getWhiteList)
        else:
            super(MessagingGateway, self).__init__(anId, gateway, authenticator, nodes)

        self._scope = scope

        #TODO: read in from service configuration when it's ready
        self._gatewayBlackList = {}
        self._gatewayWhiteList = {}

    # Receive Messages
    def receiveMessage(self, msg):
        """ When gateway receives a message, it distributes it to child nodes """
        super(MessagingGateway, self).receiveMessage(msg)
        self.distributeMessage(msg, self.getId())

    # Relay Messages
    def dispatchMessage(self, msg, senderId=None):
        """ Send a message from a child node to parent and sibling nodes """
        self.addContextDataToMsg(msg)
        msg.setContextValue(ORIGINATING_SERVICE_ID_KEY, senderId)
        #logWarning("Message DISPATCH")
        #logWarning(msg)
        self.sendMessage(msg)
        #logWarning("Message DISPATCH SENT: %s"%(msg,))
       

    def addContextDataToMsg(self, msg):
        """ Add extra context to the message, if not present """
        for key in self._scope:
            if not msg.hasContextValue(key):
                msg.setContextValue(key, self._scope[key]);


    def isMessageOnDestinationList(self, entries, msg):
        if entries is not None:
            for entry in entries:
                if entry.evaluateMessage(msg):
                    return True

        return False

    def isMessageOnGatewayBlackList(self, destination, msg):
        destinationId = destination.getId()
        entries = self._gatewayBlackList.get(destinationId, [])
        result = self.isMessageOnDestinationList(entries, msg)
        allDestinationEntries = self._gatewayBlackList.get(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, [])
        result = result or self.isMessageOnDestinationList(allDestinationEntries, msg)
        return result

    def isMessageOnGatewayWhiteList(self, destination, msg):
        destinationId = destination.getId()
        entries = self._gatewayWhiteList.get(destinationId, [])
        
        if entries == []:
            return True
        
        result = self.isMessageOnDestinationList(entries, msg)
        allDestinationEntries = self._gatewayWhiteList.get(GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS, [])
        result = result or self.isMessageOnDestinationList(allDestinationEntries, msg)
        return result

    def isMessageOnGatewayExternalWhiteList(self, msg):
        if not USE_BLACK_WHITE_LIST:
            return False
        externalEntries = self._gatewayWhiteList[GatewayBlackWhiteListConfiguration.EXTERNAL_DESTINATIONS]
        result = self.isMessageOnDestinationList(externalEntries, msg)
        allDestinationEntries = self._gatewayWhiteList[GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS]
        result = result or self.isMessageOnDestinationList(allDestinationEntries, msg)
        return result;

    def isMessageOnGatewayExternalBlackList(self, msg):
        if not USE_BLACK_WHITE_LIST:
            return False
        externalEntries = self._gatewayBlackList[GatewayBlackWhiteListConfiguration.EXTERNAL_DESTINATIONS]
        result = self.isMessageOnDestinationList(externalEntries, msg)
        allDestinationEntries = self._gatewayBlackList[GatewayBlackWhiteListConfiguration.ALL_DESTINATIONS]
        result = result or self.isMessageOnDestinationList(allDestinationEntries, msg)
        return result;

    # return the proposals
    def getProposals(self) :
        return self.proposals

    # proposals the proposals to set
    def setProposals(self, proposals) :
        self.proposals = proposals


class ActiveMQTopicMessagingGateway(MessagingGateway):


    TOPIC_LABEL = "/topic/"

    #This property defines to which system the activeMQ message belongs.
    MESSAGE_SYSTEM_NAME = "SYSTEM_NAME";

    #this is the identifier for SUPERGLU messages
    SUPERGLU = "SUPERGLU_MSG";
    VHMSG = "VHMSG_MSG"; #Identifier for virtual human messages
    GIFT = "GIFT_MSG"; #Identifer for GIFT messages

    MESSAGE_TYPE = "MESSAGE_TYPE"



    def __init__(self, anId=None, nodes=None, gateway=None, authenticator=None, scope=None, server = "localhost", port = "61613", AMQscope = "*"):
        super(ActiveMQTopicMessagingGateway, self).__init__(anId, nodes, gateway, authenticator, scope)
        self.m_port   = port
        self.m_AMQscope  = AMQscope
        self.m_server = server

        self.openConnection()


    #returns boolean
    def openConnection(self):
        if self.m_isOpen:
            return True
        while not self.m_isOpen:
            try:
                if self.m_server is None or self.m_server is '':
                    self.m_server = "localhost"
                if self.m_AMQscope is None or self.m_AMQscope is '':
                    self.m_AMQscope = "*"
                if self.m_port is None or self.m_port is '':
                    self.m_port = "61613"

                self.m_connection = stomp.Connection10([(self.m_server, int(self.m_port))])
                self.m_connection.set_listener('stomp_listener', self)
                self.m_connection.start()
                self.m_connection.connect()
                self.m_connection.subscribe(self.TOPIC_LABEL + self.m_scope)

                self.m_isOpen = True

                return True
            except Exception:
                print("Connection timed Out, waiting for ActiveMQ")


    def on_message(self, headers, msg):
        msg = urllib.parse.unquote(msg)
        msg = msg.replace("+", " ")

        #Only handle superglu messages like this.  for the moment we will ignore other message types until the ontology broker is ready
        if self.MESSAGE_SYSTEM_NAME in headers:
            if headers[self.MESSAGE_SYSTEM_NAME] == self.SUPERGLU:

                try:
                    msg = nativizeObject(msg)
                    if isinstance(msg, Message):
                        if self._gateway is not None:
                            self._gateway.dispatchMessage(msg, self.getId())
                        self.distributeMessage(msg)
                except Exception as err:
                    print("ActiveMQ message was unable to be parsed")
                    logError(err, stack=traceback.format_exc())
    

    def sendMessage(self, msg):

        if self.isMessageOnGatewayExternalBlackList(msg):
            return

        if self.isMessageOnGatewayExternalWhiteList(msg):

            MessagingGateway.sendMessage(self, msg)
            if self.m_connection is None:
                return False
            if isinstance(msg, Message):
                msgAsString = serializeObject(msg)
                headers = {self.MESSAGE_SYSTEM_NAME : self.SUPERGLU, self.MESSAGE_TYPE : "SUPERGLU_MSG"}
                self.m_connection.send(destination=self.TOPIC_LABEL + self.m_scope, body=msgAsString, headers=headers, content_type="text/plain")
            elif isinstance(msg, VHMessage):
                msgAsString = msg.getFirstWord() + " " + msg.getBody()
                headers = {"ELVISH_SCOPE": "DEFAULT_SCOPE", "MESSAGE_PREFIX" : msg.getFirstWord(), "VHMSG_VERSION" : "1.0.0.0", "VHMSG" : "VHMSG" }
                self.m_connection.send(destination=self.TOPIC_LABEL + self.m_scope, body=msgAsString, headers=headers, content_type="text/plain")
            elif isinstance(msg, GIFTMessage):
                msgAsString = serializeObject(msg.getPayload())
                headers = {self.MESSAGE_TYPE : "GIFT_MSG", "Encoding" : 0}
                self.m_connection.send(destination=self.TOPIC_LABEL + self.m_scope, body=msgAsString, headers=headers, content_type="text/plain")

        return True


    #receiving messages is handled by the on_message function, so we don't need to override the receiveMessage function





class HTTPMessagingGateway(MessagingGateway):
    MESSAGES_KEY = 'message'
    DATA_KEY = 'data'
    MESSAGES_NAMESPACE = '/messaging'

    def __init__(self, anId=None, socketio=None, socketioModule=None,
                 nodes=None, gateway=None, authenticator=None, scope=None):
        super(HTTPMessagingGateway, self).__init__(anId, nodes, gateway, authenticator, scope)
        self._socketio = socketio
        self._socketioModule = socketioModule
        self._messages = Queue()

    def sendMessage(self, msg):
        super(HTTPMessagingGateway, self).sendMessage(msg)
        self.queueAJAXMessage(msg)

    def receiveMessage(self, msg):
        """ Get message from a child and process/distribute it """
        super(HTTPMessagingGateway, self).receiveMessage(msg)
        logWarning("Message Received")
        self.queueAJAXMessage(msg)
        logWarning("Message Distributing %s"%msg.getId())
        self.distributeMessage(msg)
        logWarning("Message Distributed %s"%msg.getId())

    # Handling Websocket Communication
    def clearPendingAJAXMessages(self):
        self._messages = Queue()

    def queueAJAXMessage(self, msg):
        #logWarning("QUEUE MSG", msg.saveToSerialized())

        if self.isMessageOnGatewayExternalBlackList(msg):
            return

        if self.isMessageOnGatewayExternalWhiteList(msg):
            try:
                sessionId = msg.getContextValue(SESSION_KEY, None)
                sid = msg.getContextValue("sid", None)
                msg = serializeObject(msg)
                self._messages.put((sid, sessionId, msg))
                print ("AJAX message queued")
            except Exception as err:
                print("AJAX message failed to queue")
                logError(err, stack=traceback.format_exc())

    def dequeueAJAXMessage(self):
        return self._messages.get()

    def onReceiveAJAXMessage(self, msg, sid):
        """ Take message from client and send parent gateway and any child serices """
        if self.DATA_KEY in msg:
            sessionId = msg.get(SESSION_KEY, None)
            #if sessionId is not None and len(self._socketioModule.rooms()) == 0:
            self._socketio.server.enter_room(sid, sessionId, self.MESSAGES_NAMESPACE)
            # Wrap in a try/except
            msg = self.stringToMessage(msg[self.DATA_KEY])
            msg.setContextValue("sid", sid)
            if isinstance(msg, Message):
                if self._gateway is not None:
                    self._gateway.dispatchMessage(msg, self.getId())
                self.distributeMessage(msg)
        else:
            logWarning("GATEWAY DID NOT UNDERSTAND: ", msg)

    def processQueuedMessages(self, wait=0.001):
        socketio = self._socketio
        msgKey = self.MESSAGES_KEY
        dataKey = self.DATA_KEY
        sessionKey = SESSION_KEY
        messagesNS = self.MESSAGES_NAMESPACE
        while True:
            time.sleep(wait)        
            if not self._messages.empty():
                sid, sessionId, msg = self.dequeueAJAXMessage()
                #if sessionId and len(self._socketio.server.rooms(sessionId)) > 0:
                if sessionId:
                    self._socketio.emit(msgKey, {dataKey: msg, sessionKey: sessionId}, namespace=messagesNS, room=sessionId)
                else:
                    logWarning("Could not find room %s (Message was: %s)"%(sessionId, msg))


class BaseService(BaseMessagingNode):
    pass

class TestService(BaseService):

    def receiveMessage(self, msg):
        logWarning("TEST SERVICE GOT: \n", self.messageToString(msg))

        default = "{{missing}}"

        authKey = msg.getContextValue(Message.AUTHENTICATION_KEY, default)
        logWarning(" ===> authN:[%s], authZ:[%s], ShouldBeBlank:[%s] <=== " % (
            authKey,
            msg.getContextValue(Message.AUTHORIZATION_KEY, default),
            msg.getContextValue('BE-BLANK', default),
        ))

        if authKey:
            try:
                from AWS_Core_Services.Authentication.UserData import UserData
                user = UserData.read(authKey)
                if user:
                    logWarning("USER IN MESSAGE: %s" % str(user))
                else:
                    logWarning("USER IN MESSAGE: {{{NONE}}}")
            except:
                pass


        super(TestService, self).receiveMessage(msg)

    def sendTestString(self, aStr):
        logWarning("Test Service is Sending: ", aStr)
        self.sendMessage(Message("TestService", "Sent Test", "To Server", aStr))

    def sendTestMessage(self, actor, verb, obj, result, speechAct, context=None):
        if context is None: context = {}
        msg = Message(actor, verb, obj, result, speechAct, context=context)
        that.sendMessage(msg)

    def sendTestMessage2(self, callback, actor, verb, obj, result, speechAct, context=None):
        if context is None: context = {}
        msg = Message(actor, verb, obj, result, speechAct, context=context)
        that._makeRequest(msg, callback)
