'''
Created on Jul 23, 2018

@author: rthaker
'''
import unittest
import time
from SuperGLU.Core.ServiceConfiguration import ServiceConfiguration
from SuperGLU.Core import MessagingGateway
from SuperGLU.Core.FIPA import SpeechActs
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import ProposedMessage, BaseMessagingNode
from multimethod import overload

    
class HintPresenter(MessagingGateway.BaseMessagingNode): 
    
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
                        self.proposedMsgRequests.append(msg.getId());
                        self.auditOfProposedMsgReq[msg.getId()] = originalConversationId
                        msgAck = Message('penguin', 'eats', 'fish', 'Accepting Proposal', SpeechActs.PROPOSED_MESSAGE_ACKNOWLEDGMENT, {}, None , 'msg2')
                        msgAck.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, self.getId())
                        msgAck.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_accept_proposal_" + self.getId() + "_" + str(time.time()))
                        msgAck.setContextValue("proposedMessageId", msg._id);
                        msgAck.setContextValue(Message.PROPOSAL_KEY, msg.getContextValue(Message.PROPOSAL_KEY));
                        msgAck.setContextValue(Message.CONTEXT_IN_REPLY_TO_KEY, msg._id);
                        self.sendMessage(msgAck);
                        #REST MESSENGER IMPLEMENTATION#
                        
                        #RESTMessage restMessage = new RESTMessage(HTTPRequestVerbEnum.GET, "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys", null, new HashMap<>());
                        #messenger.handleMessage(restMessage, "hinterPresenterId");
                    else : 
                        print("My Service name is : "+ self.getId() + "I am Not Answering Right Now. ")
                    self.counterForResponse += self.counterForResponse
            '''elif (msg instanceof RESTMessage){
                String MessageId = msg.getId();
                String proposalMessageRespose = proposedMsgRequests.poll();
                if(proposalMessageRespose != null) {
                    Message msgAck = (Message) testMessages.get(1).clone(false);
                    msgAck.setSpeechAct(SpeechActEnum.PROPOSED_MESSAGE_ACKNOWLEDGMENT);
                    msgAck.setContextValue(BaseMessagingNode.ORIGINATING_SERVICE_ID_KEY, this.getId());
                    msgAck.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_accept_proposal_" + this.getId() + "_" + System.currentTimeMillis());
                    msgAck.setContextValue("proposedMessageId", proposalMessageRespose);
                    msgAck.setContextValue(Message.PROPOSAL_KEY, auditOfProposedMsgReq.get(proposalMessageRespose));
                    msgAck.setContextValue(Message.CONTEXT_IN_REPLY_TO_MESSAGE, MessageId);
                    msgAck.setContextValue(Message.RESULT_KEY, ((RESTMessage) msg).getPayload());
                    this.sendMessage(msgAck);
                }
            }'''
            print("============================================================================")
            return True
    
                    
'''
    
    def buildMessages(self):
        self.result = []
        msg1 = Message('penguin', 'eats', 'fish', 'Sending Proposal', SpeechActs.PROPOSE_ACT, {}, None , 'msg1 ')
        msg2 = Message('penguin', 'eats', 'fish', 'Accepting Proposal', SpeechActs.ACCEPT_PROPOSAL_ACT, {}, None , 'msg2')
        msg3 = Message('penguin', 'eats', 'fish', 'Confirming Proposal', SpeechActs.CONFIRM_PROPOSAL_ACT, {}, None , 'msg3')
        self.result.append(msg1)
        self.result.append(msg2)
        self.result.append(msg3)

    
    
    
    
    '''

class Test(unittest.TestCase): 
    
    def test__init__(self):
        self.testMessages = []
        self.hintPresenter = None
        self.hintService1 = None
        #self.hintService2 = None
        self.gateway = None
        
    def testName(self):
        nodes = []
        hintService1 = HintService('HintService')
        #self.hintService2 = HintService('Hint Service 2')
        hintPresenter = HintPresenter('HintPresenter')
        nodes.append(hintService1)
        #self.nodes.append(self.hintService2)
        nodes.append(hintPresenter)
       
        hintService1.respondToProposal = True
        #self.hintService2.respondToProposal = True;
        hintService1.respondToProposedMessage = True;
        #self.hintService2.respondToProposedMessage = True;
        
        
        configuration = ServiceConfiguration('mockConfiguration', None, {}, None, None, None)
        gateway = MessagingGateway.MessagingGateway('Messaging Gateway Node', nodes, None, None, None, configuration)
        #('Messaging Gateway Node', None, None, nodes, None, configuration)
        hintPresenter._gateway = gateway
        hintService1._gateway = gateway
        hintService1.addNodes([hintPresenter])
        hintPresenter.addNodes([hintService1])
        
    
        
        msg = Message(actor='penguin', verb='eat', obj='fish', result='Result', speechAct=str(SpeechActs.PROPOSE_ACT), context={}, timestamp=None, anId='msg1')
        #Message('penguin', 'eats', 'fish', 'Sending Proposal', str(SpeechActs.PROPOSE_ACT), {}, None , 'msg1 ')
        msg.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId())
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5")
        retryParams = {}
        retryParams["msgType"] = "PROPOSAL"
        retryParams["noOfAttemptsForProposal"] = "3"
        retryParams["noOfAttemptsForProposedMsg"] = "3"
        retryParams["acceptFor"] = "4000"
        retryParams["failSoftStrategyForProposedMsg"] = SpeechActs.RESEND_MSG_WITH_ATTEMPT_COUNTS
        hintPresenter.makeProposal(msg=msg, retryParams=retryParams, policyType='ALL')
        pass

