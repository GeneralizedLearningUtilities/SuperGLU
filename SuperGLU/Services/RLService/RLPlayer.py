#!/usr/bin/env python

'''
Created on May 19, 2016
@author: skarumbaiah
'''

import random as rand
from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Services.LoggingService  import LoggingService  
from SuperGLU.Services.RLService.StateVariable import *
from SuperGLU.Services.RLService.Constants import DIAGNOSE, DOOVER, SKIP, ORDER, DONE, PERFORM_ACTION, GET_NEXT_AGENDA_ITEM,TRANSCRIPT_UPDATE, BEGIN_AAR
import json

"""
    This module contains the Reinforcement Learning service for 2 functionalities -
    1. RL Coach - There are three flavors to it - random, feature space and full state space
    2. RL AAR - for now its random
"""

RL_SERVICE_NAME = "RL Service"
tutoring_state = {TUTOR_STATE_QUALITY_PREV_ANSWER:1, TUTOR_STATE_STUDENT_QUALITY:2}

#AAR item list
AAR_item = {}

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
    
    #Random policy for AAR
    def updateAARItem(self, item):
        r = rand.random()
        if r < 0.33:
            AAR_item[item] = SKIP
        elif r  < 0.66:
            AAR_item[item] = DIAGNOSE
        else:
            AAR_item[item] = DOOVER
            
 
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
    rLService_random = RLRandom()
    csvLog = LoggingService.CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()
                
    def receiveMessage(self, msg):
        super(RLServiceMessaging, self).receiveMessage(msg)
        
        #Log the message (for debugging)
        #strMsg = self.serializeMsg.messageToString(msg)
        #jMsg = json.dumps(strMsg)
        self.csvLog.logMessage(msg)
        
        #find if the message is for AAR item update
        if TRANSCRIPT_UPDATE in msg.getVerb():
            logInfo('{0} received AAR item update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            item = int(msg.getContextValue(ORDER))
            max_key = int(max(AAR_item.keys(), key=int) if AAR_item else 0)
            if max_key == -1 or None:
                max_key = 0
            
            if item > max_key+1:
                diff = item - (max_key+1)
                for i in range(diff):
                    missed_item = max_key+1+i
                    self.rLService_random.updateAARItem(missed_item)
            print(item)
            self.rLService_random.updateAARItem(item)
            print(AAR_item)
        
        #if message is to get the next agenda item in AAR
        elif GET_NEXT_AGENDA_ITEM in msg.getVerb():
            
            #if AAR Item list reply as done
            if not AAR_item:
                print('Empty AAR')
                item = -1
                action = DONE
            else:
                #loops through dictionary
                for item in list(AAR_item.keys()):
                    action = AAR_item[item]
                    #if skip don't reply
                    if action == SKIP:
                        print('item skipped')
                        del AAR_item[item]
                    else:
                        print('item ' + str(item) +' action ' + action)
                        #delete item and break
                        del AAR_item[item]
                        break
            
            #if SKIPs remain, its the end of the item list
            if action == SKIP:
                item = -1
                action = DONE
             
            #send message   
            reply_msg = self._createRequestReply(msg)
            reply_msg.setResult(action)
            reply_msg.setVerb(PERFORM_ACTION)
            reply_msg.setObject(item)
            
            if reply_msg is not None:
                logInfo('{0} is sending reply for AAR agenda item:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply_msg)), 2)
                self.sendMessage(reply_msg)
            
        #start of AAR
        elif BEGIN_AAR in msg.getVerb():
            logInfo('{0} received AAR item final update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            AAR_item['-1'] = 'DONE'            
        
        #consider message for state update
        else:
            logInfo('{0} received state update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
   
            #update state based on the message
            self.rLService_internal.updateState(msg)
            
            #get state from function call
            state = self.rLService_internal.getState()
            print(state[TUTOR_STATE_QUALITY_PREV_ANSWER])
        
    #prepare message to route  
    def routeMessage(self, msg):
        pass