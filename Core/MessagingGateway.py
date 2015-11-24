# -*- coding: utf-8 -*-
import time
import json
from queue import Queue
from Core.FIPA.SpeechActs import REQUEST_WHENEVER_ACT
from Core.Messaging import Message
from Services.Tables import IncomingMessage
from Util.ErrorHandling import logError, logWarning
from Util.Serialization import (Serializable, serializeObject,
                                nativizeObject)

CATCH_BAD_MESSAGES = False
SESSION_KEY = 'sessionId'

class BaseMessagingNode(Serializable):
    """ Base class for messaging """

    def __init__(self, anId=None, gateway=None, authenticator=None):
        super(BaseMessagingNode, self).__init__(anId)
        self._gateway = gateway
        self._authenticator = authenticator
        if gateway is not None:
            self.bindToGateway(gateway)
        self._requests = {}

    def sendMessage(self, msg):
        if self._gateway is not None:
            self._gateway.dispatchMessage(msg, self.getId())

    def receiveMessage(self, msg):
        self._triggerRequests(msg)

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


class MessagingGateway(BaseMessagingNode):

    def __init__(self, anId=None, nodes=None, gateway=None, authenticator=None, scope=None):
        if scope is None: scope = {}
        super(MessagingGateway, self).__init__(anId, gateway, authenticator)
        if nodes is None: nodes = []
        self._nodes = {}
        self._scope = scope
        self.addNodes(nodes)

    # Receive Messages
    def receiveMessage(self, msg):
        """ When gateway receives a message, it distributes it to child nodes """
        super(MessagingGateway, self).receiveMessage(msg)
        self.distributeMessage(msg, None)
    
    # Relay Messages
    def dispatchMessage(self, msg, senderId=None):
        """ Send a message from a child node to parent and sibling nodes """
        self.addContextDataToMsg(msg)
        self.sendMessage(msg)
        self._distributeMessage(self._nodes, msg, senderId)
    
    def distributeMessage(self, msg, senderId=None):
        """ Pass a message down all interested children (except sender) """
        self._distributeMessage(self._nodes, msg, senderId)

    def _distributeMessage(self, nodes, msg, senderId=None):
        """ Implement passing a message down all interested children (except sender) """
        for nodeId in nodes:
            condition = nodes[nodeId][0]
            node = nodes[nodeId][1]
            if ((nodeId != senderId) and ((condition  is None) or condition(msg))):
                node.receiveMessage(msg)

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

    def addContextDataToMsg(self, msg):
        """ Add extra context to the message, if not present """
        for key in self._scope:
            if not msg.hasContextValue(key):
                msg.setContextValue(key, self._scope[key]);
                    

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
        logWarning("message Received")
        logWarning(msg)
        self.queueAJAXMessage(msg)
        self.distributeMessage(msg)

    # Handling Websocket Communication
    def clearPendingAJAXMessages(self):
        self._messages = Queue()

    def queueAJAXMessage(self, msg):
        #logWarning("QUEUE MSG", msg.saveToSerialized())
        sessionId = msg.getContextValue(SESSION_KEY, None)
        sid = msg.getContextValue("sid", None)
        msg = serializeObject(msg)
        self._messages.put((sid, sessionId, msg))
        print ("message away")

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
                # sessionId in 
                #if sessionId and len(self._socketio.server.rooms(sessionId)) > 0:
                self._socketio.emit(msgKey, {dataKey: msg, sessionKey: sessionId}, namespace=messagesNS, room=sessionId)
               # elif False:
                #    logWarning("ERROR: Could not find room %s (Message was: %s)"%(sessionId, msg))
                

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
        self.sendMessage(Messaging.Message("TestService", "Sent Test", "To Server", aStr))

    def sendTestMessage(self, actor, verb, obj, result, speechAct, context=None):
        if context is None: context = {}
        msg = Message(actor, verb, obj, result, speechAct, context=context)
        that.sendMessage(msg)

    def sendTestMessage(self, callback, actor, verb, obj, result, speechAct, context=None):
        if context is None: context = {}
        msg = Messaging.Message(actor, verb, obj, result, speechAct, context=context)
        that._makeRequest(msg, callback)
