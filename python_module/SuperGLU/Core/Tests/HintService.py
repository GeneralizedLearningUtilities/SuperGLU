import zmq
import time
import sys
import datetime 
import json
from SuperGLU.Core.ServiceConfiguration import ServiceConfiguration
from SuperGLU.Core import MessagingGateway
from SuperGLU.Core.FIPA import SpeechActs
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import ProposedMessage, BaseMessagingNode
from SuperGLU.Util.Serialization import nativizeObject, serializeObject,\
    JSON_FORMAT
from SuperGLU.Util import ErrorHandling 

class HintService(MessagingGateway.BaseMessagingNode) :
    
        def __init__(self, msgId):
            super(HintService, self).__init__(msgId, None, None, None, None, None)
            self.proposalsAccepted = {}
            self.proposalsConfirmReceived= []
            self.proposalsConfirmedToServ = {}
            self.proposedMsgRequests = []
            self.auditOfProposedMsgReq = {}
            self.respondToProposedMessage = False
            self.respondToProposal = False
            print('Initiating Service')
            self.maintainACountForResponse = False
            self.counterForResponse = 0
            
            
        def receiveMessage(self, msg) : 
            
            print("============================================================================")
            print('Message received by ' + self.getId())
            if(msg != None) :
                speechAct = msg.getSpeechAct()
                print('SpeechAct : ' + speechAct)
                proposalIdOfMessage =  str(msg.getContextValue(Message.PROPOSAL_KEY))
                
                if (msg.getSpeechAct() == SpeechActs.PROPOSE_ACT and self.respondToProposal == True) :
                    conversationId = str(msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY))
                    replyingConversationId = "conversation_accept_proposal_" + self.getId() + "_" + str(time.time())
                    self.proposalsAccepted[replyingConversationId] = msg
                    msg2 = Message('penguin', 'eats', 'fish', 'Accepting Proposal', SpeechActs.ACCEPT_PROPOSAL_ACT, {}, None , 'msg2')
                    msg2.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, self.getId());
                    msg2.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, replyingConversationId);
                    msg2.setContextValue(Message.PROPOSAL_KEY, str(msg.getContextValue(Message.PROPOSAL_KEY)))
                    msg2.setContextValue(Message.CONTEXT_IN_REPLY_TO_KEY, conversationId)
                    now = datetime.datetime.now()
                    now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
                    msg2.setContextValue('timestamp' , str(now))
                    self.sendMessage(msg2)
                elif (msg.getSpeechAct() == SpeechActs.CONFIRM_PROPOSAL_ACT) :
                    originalConversationId = str(msg.getContextValue(Message.CONTEXT_IN_REPLY_TO_KEY))
                    if originalConversationId in self.proposalsAccepted :    #//confirm proposals only for which this service accepted
                        self.proposalsConfirmReceived.append(msg)
                        hintPresenter = msg.getContext()[MessagingGateway.ORIGINATING_SERVICE_ID_KEY]
                        proposalId = msg.getContext()[Message.PROPOSAL_KEY]
                        if hintPresenter not in self.proposalsConfirmedToServ :
                            self.proposalsConfirmedToServ[hintPresenter] = [proposalId]
                        else :
                            proposalsAccepted = self.proposalsConfirmedToServ[hintPresenter]
                            proposalsAccepted.append(proposalId);
                            self.proposalsConfirmedToServ[hintPresenter] = proposalsAccepted
                            
                elif (msg.getSpeechAct() == SpeechActs.PROPOSED_MESSAGE and msg.getContextValue("toBeServicedBy") == self.getId() and self.respondToProposedMessage == True) :
                    originalConversationId = msg.getContextValue(Message.PROPOSAL_KEY)
                    hinterPresenterId = msg.getContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY)
                    flag = True if self.maintainACountForResponse and (self.counterForResponse < 2)  else (True if self.maintainACountForResponse == False else False)
                    if flag == True and hinterPresenterId in self.proposalsConfirmedToServ and originalConversationId in self.proposalsConfirmedToServ[hinterPresenterId] :
                        #self.proposedMsgRequests.append(msg.getId());
                        self.auditOfProposedMsgReq[msg.getId()] = originalConversationId
                        msgAck = Message('penguin', 'eats', 'fish', 'Acknowledging Proposal', SpeechActs.PROPOSED_MESSAGE_ACKNOWLEDGMENT, {}, None , 'msg2')
                        msgAck.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, self.getId())
                        msgAck.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_accept_proposal_" + self.getId() + "_" + str(time.time()))
                        msgAck.setContextValue("proposedMessageId", msg._id);
                        msgAck.setContextValue("result", "PROPOSED MESSAGE SUCCESSFULLY ACKNOWLEDGED.");
                        msgAck.setContextValue(Message.PROPOSAL_KEY, msg.getContextValue(Message.PROPOSAL_KEY));
                        msgAck.setContextValue(Message.CONTEXT_IN_REPLY_TO_KEY, msg._id);
                        now = datetime.datetime.now()
                        now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
                        msgAck.setContextValue('timestamp' , str(now))
                        self.sendMessage(msgAck);
                    else : 
                        print("My Service name is : "+ self.getId() + "I am Not Answering Right Now. ")
                    self.counterForResponse += self.counterForResponse
            print("============================================================================")
            return True

class HintServiceMessagingGateway(MessagingGateway.MessagingGateway): 
    
    def __init__(self, anId=None, nodes=None, gateway=None, authenticator=None, scope=None, serviceConfiguration=None):
        super(HintServiceMessagingGateway, self).__init__(anId=None, nodes=None, gateway=None, authenticator=None, scope=None, serviceConfiguration=None)
        print('Initiating Gateway')
        


    def dispatchMessage(self, msg, senderId=None):
        """ Send a message from a child node to parent and sibling nodes """
        self.addContextDataToMsg(msg)
        msg.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, senderId)
        ErrorHandling.logWarning("Message DISPATCH")
        ErrorHandling.logWarning(msg)
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://127.0.0.1:5557")
        zmq_socket.send_string(serializeObject(msg, JSON_FORMAT))
        
        ErrorHandling.logWarning("Message DISPATCH SENT: %s"%(msg,))
       
        

testMessages = []
hintService1 = None
gateway = None

nodes = []
hintService1 = HintService('HintService')
nodes.append(hintService1)
hintService1.respondToProposal = True
hintService1.respondToProposedMessage = True;
configuration = ServiceConfiguration('mockConfiguration', None, {}, None, None, None)
gateway = HintServiceMessagingGateway('Messaging Gateway Node', nodes, None, None, None, configuration)
hintService1._gateway = gateway
gateway.addNodes([hintService1])

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://127.0.0.1:5558")
port = 5558

while True:
    #  Wait for next request from client
    message = socket.recv().decode('utf-8')
    print("Received request: ", message)
    accepting = gateway.acceptIncomingMessage(message)
    messageAsObject = nativizeObject(message)
    gateway.sendMessage(messageAsObject)
    time.sleep (1)  