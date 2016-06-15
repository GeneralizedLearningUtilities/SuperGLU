#!/usr/bin/env python

'''

Created on May 19, 2016
@author: skarumbaiah

'''

from datetime import datetime
from uuid import uuid4
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Services.RLService.StateVariable import *
from SuperGLU.Services import LoggingService  
from SuperGLU.Services.LoggingService.LoggingService import CSVLoggingService
import json

"""
    This module contains the Reinforcement Learning service.
    There are three flavors to it - random, feature space and full state space
"""

RL_SERVICE_NAME = "RL Service"
tutoring_state = {TUTOR_STATE_QUALITY_PREV_ANSWER:1, TUTOR_STATE_STUDENT_QUALITY:2}

#super class for model specific subclasses
class RLPlayer():
    
    def __init__(self):
        pass
    
    #update state with every message
    def updateState(self,msg):
        #example state update code - update quality of answer based on the superGlu message
        if msg.getObject() == "Correctness":
            if msg.getResult() == "mixed":
                tutoring_state[TUTOR_STATE_QUALITY_PREV_ANSWER] = 2
        
    
    def informLog(self, msg):
        pass
    
    def getState(self):
        return tutoring_state   #can also be accessed directly as a global variable   
    
    def getTopAction(self):
        pass
    
    def getActionValue(self,action):
        pass

#Random policy
class RLRandom(RLPlayer):
    def getTopAction(self):
        pass
    
    def getActionValue(self,action):
        return 0.5
 
#Function approximation - features to derive policy
class RLFeature(RLPlayer):
    def __init__(self, feature, weight):
        self.features = feature
        self.weight = weight
        
    def getTopAction(self):
        pass
    
    def getActionValue(self,action):
        pass
        
#Full state space - Q values to derive policy
class RLQValues(RLPlayer):
    def __init__(self, state, action):
        self.state = state
        self.action = action
        
    def getTopAction(self):
        pass
    
    def getActionValue(self,action):
        pass
    
         
class RLServiceMessaging(BaseService):
    
    rLService_internal = RLPlayer()
    #csvLog = CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()
                
    def receiveMessage(self, msg):
        super(RLServiceMessaging, self).receiveMessage(msg)
        
        #Log the message (for debugging)
        #strMsg = self.serializeMsg.messageToString(msg)
        #jMsg = json.dumps(strMsg)
        #self.csvLog.logMessage(msg)
        
        if "HEARTBEAT_VERB" not in msg.getVerb():
            logInfo('{0} received message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
   
            #update state based on the message
            self.rLService_internal.updateState(msg)
            
            #get state from function call
            state = self.rLService_internal.getState()
            print(state[TUTOR_STATE_QUALITY_PREV_ANSWER])
        """
        if msg is not None:
            reply = self.routeMessage(msg)
            pass
        
        if reply is not None:
            logInfo('{0} is sending reply:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply)), 2)
            self.sendMessage(reply)
        """
        
    
    def routeMessage(self, msg):

        #depending on the content of the message react differently
        logInfo('Entering RLServiceMessaging.routeMessage', 5)
        
        result = None
        #Only considering inform
        if msg.getSpeechAct() == INFORM_ACT:
            self.rLService_internal.informLog(msg)
            logInfo('{0} finished processing {1}'.format(RL_SERVICE_NAME, INFORM_ACT), 2)
            
        elif msg.getSpeechAct() == REQUEST_ACT:
            logInfo('{0} is processing a {1} message'.format(RL_SERVICE_NAME, REQUEST_ACT), 4)
            '''
            newRLService = self.rLService_internal.createNewRLService(msg.getObject())
            result = self._createRequestReply(msg)
            result.setActor(RL_SERVICE_NAME)
            result.setSpeechAct(INFORM_ACT)
            result.setObject(msg.getObject())
            if newRLService is not None:
                result.setResult(newRLService.toSerializable())
            else:
                result.setResult(None)
            logInfo('{0} finished processing {1}'.format(RL_SERVICE_NAME, REQUEST_ACT), 4)
        
        return result     
        '''       
    
