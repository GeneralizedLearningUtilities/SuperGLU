#!/usr/bin/env python

'''
Created on May 19, 2016
@author: skarumbaiah
'''

import random as rand
import csv
from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Services.LoggingService  import LoggingService  
from SuperGLU.Services.RLService.Constants import *

"""
    This module contains the Reinforcement Learning service for 2 functionalities -
    1. RL Coach - There are three flavors to it - random, feature space and full state space
    2. RL AAR - for now its random
    
    Refer google docs for detailed documentation and design -
    https://docs.google.com/document/d/1RfX9zMZEjgFuY31qRXaRPC_b64N0yOLxdXTuean8K2s/edit#
"""

RL_SERVICE_NAME = "RL Service"
tutoring_state = {TUTOR_STATE_QUALITY_PREV_ANSWER:2, TUTOR_STATE_STUDENT_AVG_PERFORMANCE:2}
avg_performace = {1:0,2:0,3:0}  # 1-Correct, 2-Mixed, 3-Incorrect

#AAR item list
AAR_item = {}

#super class for model specific subclasses 
#performs general action in the player like state updates, logging, etc
class RLPlayer():
    
    def __init__(self):
        pass
    
    #update state with every message
    def updateState(self,msg):
        #state update on relevant messages
        
        #update quality of answer based on the superGlu message
        if msg.getObject() == CORRECTNESS:
            if msg.getResult() == CORRECT:
                avg_performace[1] += 1
                tutoring_state[TUTOR_STATE_QUALITY_PREV_ANSWER] = 1
            elif msg.getResult() == MIXED:
                avg_performace[2] += 1
                tutoring_state[TUTOR_STATE_QUALITY_PREV_ANSWER] = 2 
            elif msg.getResult() == INCORRECT:
                avg_performace[3] += 1
                tutoring_state[TUTOR_STATE_QUALITY_PREV_ANSWER] = 3 
            else:
                print("Incorrect Correctness value")
                
            #update average student performance as the category with maximum 
            tutoring_state[TUTOR_STATE_STUDENT_AVG_PERFORMANCE] = max(avg_performace, key=avg_performace.get)
        
        print(tutoring_state)
           
    def informLog(self, msg):
        pass
    
    def getState(self):
        return tutoring_state   #can also be accessed directly as a global variable   


#Random policy
class RLRandom(RLPlayer):
    #Random policy for Coach
    def getTopAction(self):
        r = rand.random()
        if r < 0.25:
            return GIVE_FEEDBACK
        elif r  < 0.5:
            return GIVE_HINT
        elif r < 0.75:
            return GIVE_HINT_FEEDBACK
        else:
            return DO_NOTHING
    
    #Random policy for AAR
    def updateAARItem(self, item):
        r = rand.random()
        if r < 0.33:
            AAR_item[item] = SKIP
        elif r  < 0.66:
            AAR_item[item] = DIAGNOSE
        else:
            AAR_item[item] = DOOVER
            
 
#Trained policy using function approximation 
class RLCoachFeature(RLPlayer):
    
    def __init__(self):
        pass
    
    #def __init__(self, feature, weight):
        #self.features = feature
        #self.weight = weight
    
    #get top action from the trained policy    
    def getTopAction(self):
        #csv file under the current directory containing policy - replace with actual policy file ???
        with open('test_policy.csv', 'r') as f:
            reader = csv.reader(f)
            weights = list(reader)
        weights = [int(i) for i in weights[0]]
        print("Number of weights in the policy"+len(weights))
        
        #dummy features - need logic to calculate these values ???
        features = list(len(weights))
        
        #compute Q value
        Q = [i*j for i,j in zip(weights, features)]
        
        #dummy max Q value - needs translation from max Q to action ???
        return max(Q)
    
    def getActionValue(self,action):
        pass


#handles incoming and outgoing messages     
class RLServiceMessaging(BaseService):
    
    rLService_internal = RLPlayer()         #for internal updates
    rLService_random = RLRandom()           #random policy
    rLService_feature = RLCoachFeature()    #trained policy for RL Coach
    csvLog = LoggingService.CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()
    
    #receive message and take appropriate action by looking at the message attributes like verb         
    def receiveMessage(self, msg):
        super(RLServiceMessaging, self).receiveMessage(msg)
        
        #Log the message (for debugging)
        #strMsg = self.serializeMsg.messageToString(msg)
        #jMsg = json.dumps(strMsg)
        self.csvLog.logMessage(msg)
        
        #AAR
        #if message is for AAR item update
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
            if msg.getResult() == CORRECT:
                AAR_item[item] = SKIP
            else:
                self.rLService_random.updateAARItem(item)
            print(AAR_item)
        
        #AAR    
        #if message informs the start of AAR
        elif BEGIN_AAR in msg.getVerb():
            logInfo('{0} received AAR item final update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            AAR_item['-1'] = DONE
        
        #AAR
        #if message asks for the next agenda item in AAR
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
        
        #if Elite asks for coaching action
        elif REQUEST_COACHING_ACTIONS in msg.getVerb():
            logInfo('{0} received request coaching action message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            action = self.rLService_random.getTopAction()
            
            #send message   
            reply_msg = self._createRequestReply(msg)
            reply_msg.setResult(action)
            reply_msg.setVerb(COACHING_ACTIONS)
            
            if reply_msg is not None:
                logInfo('{0} is sending reply for coaching request:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply_msg)), 2)
                self.sendMessage(reply_msg)  
            
        #consider message for state update  - can also reuse TRANSCRIPT_UPDATE for correctness ???
        else:
            logInfo('{0} received state update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
   
            #update state based on the message
            self.rLService_internal.updateState(msg)
            
            #get state from function call
            state = self.rLService_internal.getState()
            print(state[TUTOR_STATE_QUALITY_PREV_ANSWER])
            