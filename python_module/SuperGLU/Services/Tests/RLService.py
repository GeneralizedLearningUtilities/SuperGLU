import random as rand
import unittest

from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode
from SuperGLU.Core.ServiceConfiguration import ServiceConfiguration
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, INFORM_REF_ACT, REQUEST_ACT
from SuperGLU.Core import MessagingGateway
from SuperGLU.Core.Messaging import Message

RL_SERVICE_NAME = "RL Service"

ACTIONS = ['do_nothing', 'provide_hint', 'provide_feedback']

class RLServiceProvider(BaseService):
    def __init__(self, msgId):
        super().__init__()

    def getRandomNextAction(self):
        nextRandomInt = rand.random()
        if nextRandomInt < 0.3:
            return ACTIONS[0]
        if nextRandomInt < 0.6:
            return ACTIONS[1]
        return ACTIONS[2]

    def receiveMessage(self, msg):
        super(RLServiceProvider, self).receiveMessage(msg)
        print('RECEIVED Payload:', msg.getSpeechAct(), msg.getResult())
        speechAct =  msg.getSpeechAct()
        if speechAct == INFORM_ACT:
            print('INFORM ACT RECEIVED')
            result = {}
            result['action_to_perform'] =  ACTIONS[0]
            msg = Message(actor='Server', verb='vrResponse', obj='Assessment', result=result, speechAct=INFORM_REF_ACT,
                          context={}, timestamp=None, anId='msg1')
            self.sendMessage(msg)
        elif speechAct == REQUEST_ACT:
            requestType = msg.getResult()['request_type']
            print(requestType)
            nextAction = self.getRandomNextAction()
            result = {}
            result['action_to_perform'] = nextAction
            msg = Message(actor='Server', verb='vrResponse', obj='Assessment', result=result, speechAct=INFORM_REF_ACT,
                          context={}, timestamp=None, anId='msg1')
            self.sendMessage(msg)


class RLServiceUtlizer(BaseService):
    serializeMsg = BaseMessagingNode()
    def __init__(self, msgId):
        super().__init__()

    def receiveMessage(self, msg):
        super(RLServiceUtlizer, self).receiveMessage(msg)
        print('RECEIVED ACTION TO PERFORM :', msg.getResult()['action_to_perform'])


class RLService(unittest.TestCase):

    '''
        Sends A Message to Inform
    '''
    def testScenarioOne(self):
        nodes = []
        hintService1 = RLServiceProvider('HintService1')
        hintPresenter = RLServiceUtlizer('HintPresenter')
        nodes.append(hintService1)
        nodes.append(hintPresenter)
        hintService1.respondToProposal = True
        hintService1.respondToProposedMessage = True;

        configuration = ServiceConfiguration('mockConfiguration', None, {}, None, None, None)
        gateway = MessagingGateway.MessagingGateway('Messaging Gateway Node', nodes, None, None, None, configuration)
        gateway.addNodes([hintPresenter, hintService1])
        hintPresenter._gateway = gateway
        hintService1._gateway = gateway
        result = {}
        result['student_level'] = 0
        result['utterance'] =  'All I\'m saying is I want to go to a different unit.'
        msg = Message(actor='Raj', verb='vrExpress', obj='Assessment', result=result, speechAct=INFORM_ACT,
                      context={}, timestamp=None, anId='msg1')
        msg.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId())
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5")
        hintPresenter.sendMessage(msg=msg)
        pass

    '''
        Sends A Message to Request Next Random Option
    '''
    def testScenarioTwo(self):
        nodes = []
        hintService1 = RLServiceProvider('HintService1')
        hintPresenter = RLServiceUtlizer('HintPresenter')
        nodes.append(hintService1)
        nodes.append(hintPresenter)
        hintService1.respondToProposal = True
        hintService1.respondToProposedMessage = True;

        configuration = ServiceConfiguration('mockConfiguration', None, {}, None, None, None)
        gateway = MessagingGateway.MessagingGateway('Messaging Gateway Node', nodes, None, None, None, configuration)
        gateway.addNodes([hintPresenter, hintService1])
        hintPresenter._gateway = gateway
        hintService1._gateway = gateway
        result = {}
        result['student_level'] = 0
        result['utterance'] =  'All I\'m saying is I want to go to a different unit.'
        result['request_type'] = 'RANDOM'
        msg = Message(actor='Raj', verb='vrExpress', obj='Assessment', result=result, speechAct=REQUEST_ACT,
                      context={}, timestamp=None, anId='msg1')
        msg.setContextValue(MessagingGateway.ORIGINATING_SERVICE_ID_KEY, hintPresenter.getId())
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, "conversation_id_5")
        hintPresenter.sendMessage(msg=msg)
        pass

