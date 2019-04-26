import zmq
import time
import sys
import asyncio
from SuperGLU.Core.ServiceConfiguration import ServiceConfiguration
from SuperGLU.Core import MessagingGateway
from SuperGLU.Core.FIPA import SpeechActs
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import ProposedMessage, BaseMessagingNode
from SuperGLU.Util.Serialization import nativizeObject, serializeObject,\
    JSON_FORMAT
from SuperGLU.Util import ErrorHandling 


class HintPresenter(BaseMessagingNode): 
    def __init__(self, msgId):
        super(HintPresenter, self).__init__(msgId, None, None, None, None, None)
        self.acceptedProposalConversationId = ''
        self.acceptedProposalServiceId = ''
        self.failStrategyToTest = None
        self.acceptedServiceIds = []
        self.proposedMsgAudit = {}
        print('Initiating Presenter')
        

    def receiveMessage(self, msg):
        print("============================================================================")
        print('Message received by ' + self.getId())
        if(msg != None) :
            speechAct = msg.getSpeechAct()
            print('SpeechAct : ' + speechAct)
            proposalIdOfMessage =  str(msg.getContextValue(Message.PROPOSAL_KEY))
            if speechAct == SpeechActs.ACCEPT_PROPOSAL_ACT :
                proposal = MessagingGateway.Proposals(self.proposals[proposalIdOfMessage])
                policyType = proposal.getPolicyType()
                if policyType == SpeechActs.ALL_TIME_ACCEPT_PROPOSAL_ACK or (policyType ==  SpeechActs.X_TIME_ACCEPT_PROPOSAL_ACK and (time.time()-proposal.getProposedTime() < int(str(proposal.getRetryParams()['acceptFor'])))) :
                    self.acceptedProposalConversationId = str(msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY))
                    self.acceptedProposalServiceId = str(msg.getContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY))
                    print('******************\nACCEPTED BY : ' + self.acceptedProposalServiceId + '******************\n')
                    msgConfirm = Message('penguin', 'eats', 'fish', 'Confirming Proposal', SpeechActs.CONFIRM_PROPOSAL_ACT, {}, None , 'msg3')
                    #Message('penguin', 'eats', 'fish', ' Proposal', SpeechActs.CONFIRM_PROPOSAL_ACT, {}, None , 'msg3')
                    msgConfirm.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, self.getId())
                    msgConfirm.setContextValue(Message.CONTEXT_IN_REPLY_TO_KEY, self.acceptedProposalConversationId)
                    msgConfirm.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage)
                    msgConfirm.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, 'conversation_confirm_proposal_' + self.getId() + '_' + str(time.time()))
                    self.proposals.get(proposalIdOfMessage).setAcknowledgementReceived(True)
                    #Sends Confirmation Message.
                    self.sendMessage(msgConfirm)
                    self.acceptedServiceIds.append(self.acceptedProposalServiceId)
                    
                    if self.acceptedProposalServiceId in self.prioritizedAcceptedServiceIds != None :
                        triedFor = int(str(self.prioritizedAcceptedServiceIds.get(self.acceptedProposalServiceId)))
                        if (triedFor + 1) > 3 :
                            self.prioritizedAcceptedServiceIds.remove(self.acceptedProposalServiceId)
                            self.demotedAcceptedServiceIds.add(self.acceptedProposalServiceId)
                        else :
                            self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId] = triedFor + 1
                    elif self.acceptedProposalServiceId not in self.demotedAcceptedServiceIds :
                        self.prioritizedAcceptedServiceIds[self.acceptedProposalServiceId]= 1
                    
                    print('Got Connection Established. Preparing Proposed Message.')
                    #Proposal Request has been successfully processed. Below code, sends the Proposed Message.
                    msg4 = Message('penguin', 'eats', 'fish', 'Proposed Message', SpeechActs.PROPOSED_MESSAGE, {}, None , 'msg3')
                    
                    if (msg4.getId() not in self.proposedMsgAudit) or (msg4.getId() in self.proposedMsgAudit and self.proposedMsgAudit[msg4.getId()] == False) :
                        proposal = MessagingGateway.Proposals(self.proposals[proposalIdOfMessage])
                        self.proposedMsgAudit[msg4.getId()]  = False
                        msg4.setSpeechAct(SpeechActs.PROPOSED_MESSAGE)
                        msg4.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, self.getId())
                        msg4.setContextValue(Message.CONTEXT_IN_REPLY_TO_KEY, self.acceptedProposalConversationId)
                        msg4.setContextValue(Message.PROPOSAL_KEY, proposalIdOfMessage)
                        if proposal.getFailSoftStrategyForProposedMsg() == SpeechActs.RESEND_MSG_WITH_DEPRIORITZATION :
                            if len(self.prioritizedAcceptedServiceIds) > 0 :
                                msg4.setContextValue("toBeServicedBy", list(self.prioritizedAcceptedServiceIds.keys())[0])
                            else :
                                msg4.setContextValue("toBeServicedBy", self.acceptedServiceIds.get(0))
                        else :
                            msg4.setContextValue("toBeServicedBy", self.acceptedServiceIds[0])
                        msg4.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_confirm_proposal_" + self.getId() + "_" + str(time.time()))
                        proposedMessage = None
                        if len(proposal.getProposedMessage()) < 1 :
                            proposedMessage = ProposedMessage(msg4.getId(), msg4, 0)
                            proposedMessage.setLastTimeSent(time.time())
                        else :
                            proposedMessage = list(proposal.getProposedMessage().values())[0]
                        
                        self.proposals[proposalIdOfMessage].getProposedMessage()[msg4.getId()] = proposedMessage
                        print('Sending Proposed Message.')
                        self.sendProposedMessage(proposalIdOfMessage)
                else :
                    print('Acceptance Time Over')
            elif speechAct == SpeechActs.PROPOSED_MESSAGE_ACKNOWLEDGMENT :
                proposedMessages = self.proposals[msg.getContextValue(Message.PROPOSAL_KEY)].getProposedMessage()
                if len(proposedMessages) > 0 :
                    self.proposals[msg.getContextValue(Message.PROPOSAL_KEY)].getProposedMessage().pop(msg.getContextValue('proposedMessageId')) 
                    self.proposals[msg.getContextValue(Message.PROPOSAL_KEY)].setProposalProcessed(True)
                    print('Proposed Message Removed.' + str(len(self.proposals[msg.getContextValue(Message.PROPOSAL_KEY)].getProposedMessage())))
                    self.proposedMsgAudit[str(msg.getContextValue("proposedMessageId"))] = True
                
            
            print("============================================================================")
            return True

class HintPresenterMessagingGateway(MessagingGateway.MessagingGateway): 
    
    def __init__(self, anId=None, nodes=None, gateway=None, authenticator=None, scope=None, serviceConfiguration=None):
        super(HintPresenterMessagingGateway, self).__init__(anId=None, nodes=None, gateway=None, authenticator=None, scope=None, serviceConfiguration=None)
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
hintPresenter = None
gateway = None

nodes = []
hintPresenter = HintPresenter('HintPresenter')
nodes.append(hintPresenter)
hintPresenter.respondToProposal = True
hintPresenter.respondToProposedMessage = True;
configuration = ServiceConfiguration('mockConfiguration', None, {}, None, None, None)
gateway = HintPresenterMessagingGateway('Messaging Gateway Node', nodes, None, None, None, configuration)
hintPresenter._gateway = gateway
gateway.addNodes([hintPresenter])

@asyncio.coroutine
async def makeAsyncProposal(hintPresenter):
    await hintPresenter.makeProposal(msg=msg, retryParams=retryParams, policyType='ALL')
    
@asyncio.coroutine
def sendGatewayMessage(gateway,messageAsObject):
    gateway.sendMessage(messageAsObject)

@asyncio.coroutine
def startReception():
    while True:
    #  Wait for next request from client
    
        message = socket.recv(zmq.NOBLOCK).decode('utf-8')
        print("Received request: ", message)
        accepting = gateway.acceptIncomingMessage(message)
        messageAsObject = nativizeObject(message)
        sendGatewayMessage(gateway, messageAsObject)
        asyncio.sleep(10)



port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

msg = Message(actor='penguin', verb='eat', obj='fish', result='Result', speechAct=str(SpeechActs.PROPOSE_ACT), context={}, timestamp=None, anId='msg1')
msg.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId())
msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5")
retryParams = {}
retryParams["msgType"] = "PROPOSAL"
retryParams["noOfAttemptsForProposal"] = "3"
retryParams["noOfAttemptsForProposedMsg"] = "3"
retryParams["acceptFor"] = "40000"
retryParams["failSoftStrategyForProposedMsg"] = SpeechActs.RESEND_MSG_WITH_ATTEMPT_COUNTS

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
boo = asyncio.ensure_future(startReception())
baa = asyncio.ensure_future(makeAsyncProposal(hintPresenter)) 
loop.run_forever()
