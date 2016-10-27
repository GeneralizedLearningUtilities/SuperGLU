#!/usr/bin/env python

'''
Created on May 19, 2016
@author: skarumbaiah
'''

import random as rand
from datetime import datetime
import csv,os
from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode
from SuperGLU.Util.ErrorHandling import logInfo, tryRaiseError
#from SuperGLU.Services.LoggingService  import LoggingService  
from SuperGLU.Services.RLService.Constants import *
from math import ceil
from SuperGLU.Util.Representation.Classes import Speech

"""
    This module contains the Reinforcement Learning service for 2 functionalities -
    1. RL Coach - There are three flavors to it - random, feature space and full state space
    2. RL AAR - for now its random
    
    Refer google docs for detailed documentation and design -
    https://docs.google.com/document/d/1RfX9zMZEjgFuY31qRXaRPC_b64N0yOLxdXTuean8K2s/edit#
"""

RL_SERVICE_NAME = "RL Service"

#tutoring state for RL coach
tutoring_state = {  SCENARIO_NUMBER : 1,                        #Scenario number (1/2) (default 1)
                    GENDER : 1,                                 #gender of the participant (1(male)/2(female)) (default 1)
                    NUMBER_OF_RESPONSE_PREV : 0,                #Number of responses in previous scenario (clustered in 6 classes) (default 0)
                    NUMBER_OF_CORRECT_PREV : 0,                 #Number of correct responses in previous scenario (clustered in 6 classes) (default 0)
                    NUMBER_OF_MIXED_PREV : 0,                   #Number of mixed responses in previous scenario (clustered in 6 classes) (default 0)
                    NUMBER_OF_INCORRECT_PREV : 0,               #Number of incorrect responses in previous scenario (clustered in 6 classes) (default 0)
                    SCORE_PREV : 0,                             #Score in previous scenario (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_PREV : 0,                 #Average user response time for all responses in previous scenario (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_CORRECT_PREV : 0,         #Average user response time for correct responses in previous scenario (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_MIXED_PREV : 0,           #Average user response time for mixed responses in previous scenario (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_INCORRECT_PREV : 0,       #Average user response time for incorrect responses in previous scenario (clustered in 6 classes) (default 0)
                    SEEN_BEFORE : 0,                            #Has the system question appeared in the previous scenario? (0(no)/1(yes)) (default 0)
                    QUALITY_PREV_IF_SEEN : 0,                   #Quality of response in the previous scenario if the same question has appeared (0(null)/1(Correct)/2(Mixed)/3(Incorrect)) (default 0)
                    QUALITY_ANSWER : 0,                         #correctness of the previous answer 0(null)/1(Correct)/2(Mixed)/3(Incorrect) (default 0)
                    QUALITY_ANSWER_LAST : 0,                    #correctness of the 2nd last answer 0(null)/1(Correct)/2(Mixed)/3(Incorrect) (default 0)
                    QUALITY_ANSWER_LAST_LAST : 0,               #correctness of the 3rd last answer 0(null)/1(Correct)/2(Mixed)/3(Incorrect) (default 0)
                    NUMBER_OF_RESPONSE : 0,                     #Number of responses in current scenario so far (clustered in 6 classes) (default 0)
                    NUMBER_OF_CORRECT : 0,             #Number of correct responses in current scenario so far (clustered in 6 classes) (default 0)
                    NUMBER_OF_MIXED : 0,               #Number of mixed responses in current scenario so far (clustered in 6 classes) (default 0)
                    NUMBER_OF_INCORRECT : 0,           #Number of incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
                    SCORE : 0,                                  #Score in current scenario so far (clustered in 6 classes) (default 0)
                    RESPONSE_TIME : 0,                          #User response time for previous question (clustered in 6 classes) (default 0)
                    RESPONSE_TIME_LAST : 0,                     #User response time for 2nd last question (clustered in 6 classes) (default 0)
                    RESPONSE_TIME_LAST_LAST : 0,                #User response time for 3rd last question (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME : 0,                      #Average user response time for all responses in current scenario so far (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_CORRECT : 0,              #Average user response time for correct responses in current scenario so far (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_MIXED : 0,                #Average user response time for mixed responses in current scenario so far (clustered in 6 classes) (default 0)
                    AVG_RESPONSE_TIME_INCORRECT : 0,             #Average user response time for incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
                    AFTER_USERRESPONSE_STATE : 0,        ##1 after the user has responded (before there’s potential for feedback), and 0 before the new system prompt (before there’s potential for hints)
                    RESP_QUALITY_AFTER_RESPONSE : 0,
                    FINAL_STATE : 0
                  }

#AAR item list
AAR_item = {}

#Random policy
class RLRandom():
    #Random policy for Coach
    def getTopAction(self):
        r = rand.random()
        if r < 0.5:
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
            
    def updateNonCorrectAARItem(self, item):
        r = rand.random()
        if r  < 0.5:
            AAR_item[item] = DIAGNOSE
        else:
            AAR_item[item] = DOOVER
            
 
#Trained policy using function approximation 
class RLCoachFeature():
    
    def __init__(self):
        pass
      
    #get top action from the trained policy    
    def getTopAction(self):
        #weights.csv file in the same directory as Application.py directory containing policy
        cur = os.getcwd()
        filepath = os.path.join(cur, 'weights.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            weights = list(reader)

        action = {DO_NOTHING:0, HINT:0, FEEDBACK:0, FEEDBACK_HINT:0}
        
        #add weights for the state indicators set in tutoring_state
        for w in weights:
            if w[2] == DONOTHING:
                if tutoring_state[w[0]] == int(w[1]):
                    action[DO_NOTHING] += float(w[3])
            if w[2] == HINT:
                if tutoring_state[w[0]] == int(w[1]):
                    action[HINT] += float(w[3])
            if w[2] == FEEDBACK:
                if tutoring_state[w[0]] == int(w[1]):
                    action[FEEDBACK] += float(w[3])
            if w[2] == FEEDBACK_HINT:
                if tutoring_state[w[0]] == int(w[1]):
                    action[FEEDBACK_HINT] += float(w[3])
                    
        #get best action
        top_action = max(action, key=action.get)
        print(top_action)
        return top_action  

#performs general action in the player like state updates, logging, etc
class RLPlayer(BaseService):
    
    #interval
    interval = {None:0, 0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2, 9:3, 10:3, 11:3, 12:3, 13:4, 14:4, 15:4, 16:4}
    time_interval = {None:0, 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:2, 11:3, 12:3, 13:3, 14:3, 15:3, 16:4, 17:4, 18:4, 19:4, 20:4}
    quality_state = {(0,0):0, (0,1):1, (1,0):2, (1,1):3, (2,0):4, (2,1):5, (3,0):6, (3,1):7} #(quality,state)
    
    num_response = None
    num_correct_response = None
    num_incorrect_response = None
    num_mixed_response = None
    start = None
    end = None
    time_taken = None
    sum_time_taken = None
    sum_time_correct = None
    sum_time_mixed = None
    sum_time_incorrect = None
    questions = []
    
    rLService_random = RLRandom()           #random policy
    rLService_feature = RLCoachFeature()    #trained policy for RL Coach
    
    def __init__(self):
        pass
    
    #update state with every message
    def updateStateRLCoach(self,msg):
        #state update on relevant messages
        
        try:
            #update scenario
            if BEGIN_AAR in msg.getVerb():
                logInfo('{0} received scenario update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                
                #set previous values 
                tutoring_state[SCENARIO_NUMBER] = 2
                tutoring_state[SCORE_PREV] = tutoring_state[SCORE]
                tutoring_state[NUMBER_OF_RESPONSE_PREV] = tutoring_state[NUMBER_OF_RESPONSE]
                tutoring_state[NUMBER_OF_CORRECT_PREV] = tutoring_state[NUMBER_OF_CORRECT]
                tutoring_state[NUMBER_OF_MIXED_PREV] = tutoring_state[NUMBER_OF_MIXED]
                tutoring_state[NUMBER_OF_INCORRECT_PREV] = tutoring_state[NUMBER_OF_INCORRECT]
                tutoring_state[AVG_RESPONSE_TIME_PREV] = tutoring_state[AVG_RESPONSE_TIME]
                tutoring_state[AVG_RESPONSE_TIME_CORRECT_PREV] = tutoring_state[AVG_RESPONSE_TIME_CORRECT]
                tutoring_state[AVG_RESPONSE_TIME_MIXED_PREV] = tutoring_state[AVG_RESPONSE_TIME_MIXED]
                tutoring_state[AVG_RESPONSE_TIME_INCORRECT_PREV] = tutoring_state[AVG_RESPONSE_TIME_INCORRECT]
                
                #reset current values
                tutoring_state[QUALITY_ANSWER_LAST_LAST] = 0
                tutoring_state[QUALITY_ANSWER_LAST] = 0
                tutoring_state[QUALITY_ANSWER] = 0
                tutoring_state[SCORE] = 0
                tutoring_state[SEEN_BEFORE] = 0
                tutoring_state[QUALITY_PREV_IF_SEEN] = 0
                tutoring_state[NUMBER_OF_RESPONSE] = 0
                tutoring_state[NUMBER_OF_CORRECT] = 0
                tutoring_state[NUMBER_OF_INCORRECT] = 0
                tutoring_state[NUMBER_OF_MIXED] = 0
                tutoring_state[RESPONSE_TIME] = 0
                tutoring_state[RESPONSE_TIME_LAST] = 0
                tutoring_state[RESPONSE_TIME_LAST_LAST] = 0
                tutoring_state[AVG_RESPONSE_TIME] = 0
                tutoring_state[AVG_RESPONSE_TIME_CORRECT] = 0
                tutoring_state[AVG_RESPONSE_TIME_INCORRECT] = 0
                tutoring_state[AVG_RESPONSE_TIME_MIXED] = 0
                
                #recent locals for current
                self.num_response = None
                self.num_correct_response = None
                self.num_incorrect_response = None
                self.num_mixed_response = None
                self.start = None
                self.end = None
                self.time_taken = None
                self.time_correct = None
                self.time_mixed = None
                self.time_incorrect = None
            
            #get Gender
            elif REGISTER_USER_INFO in msg.getVerb():
                logInfo('{0} received gender update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                gend = msg.getObject()
                if gend ==  FEMALE:
                    tutoring_state[GENDER] = 2
                elif gend == MALE:
                    tutoring_state[GENDER] = 1
            
            #update response time
            #verb should be GameLog, the object should be PracticeEnvironment and the result should be RandomizedChoices
            if msg.getVerb() == GAME_LOG and msg.getObject() == PRACTICE_ENVIRONMENT and msg.getResult() == RANDOMIZED_CHOICES:
                logInfo('{0} received start timestamp update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                self.start = msg.getTimestamp()
                print("start = ",self.start)
            
            #once the participant answers
            elif TRANSCRIPT_UPDATE in msg.getVerb():
                logInfo('{0} received transcript update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                
                #store unique ID of node
                if tutoring_state[SCENARIO_NUMBER] == 1:
                    logInfo('{0} received question store message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                    node_id = msg.getContextValue(NODE_ID_CONTEXT_KEY)
                    node = [node_id, 0] #quality null - will be updated when checked for correctness
                    self.questions.append(node)
            
                #check if Chen's Utterances stored before
                if tutoring_state[SCENARIO_NUMBER] == 2:
                    logInfo('{0} received if seen before message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                    node_id = msg.getContextValue(NODE_ID_CONTEXT_KEY)
                    for question in self.questions:
                        if question[0] == node_id:
                            tutoring_state[SEEN_BEFORE] = 1
                            tutoring_state[QUALITY_PREV_IF_SEEN] = question[1]
                            break
                        else:
                            tutoring_state[SEEN_BEFORE] = 0
                            tutoring_state[QUALITY_PREV_IF_SEEN] = 0
            
                print(self.start)
                
                #update lasts
                tutoring_state[QUALITY_ANSWER_LAST_LAST] = tutoring_state[QUALITY_ANSWER_LAST]
                tutoring_state[QUALITY_ANSWER_LAST] = tutoring_state[QUALITY_ANSWER]
                tutoring_state[RESPONSE_TIME_LAST_LAST] = tutoring_state[RESPONSE_TIME_LAST]
                tutoring_state[RESPONSE_TIME_LAST] = tutoring_state[RESPONSE_TIME]
                
                #get response time
                self.end = msg.getTimestamp()
                if self.start is not None:
                    frmt = "%Y-%m-%dT%H:%M:%S.%f"
                    self.time_taken = (datetime.strptime(self.end, frmt) - datetime.strptime(self.start, frmt)).seconds
                
                #get counts and averages
                self.num_response = 1 if self.num_response is None else self.num_response + 1
                tutoring_state[NUMBER_OF_RESPONSE] = self.interval.get(int(self.num_response),5) 
                
                self.sum_time_taken = self.time_taken if self.sum_time_taken is None else self.sum_time_taken + self.time_taken
                tutoring_state[RESPONSE_TIME] = self.time_interval.get(ceil(self.time_taken),5)
                tutoring_state[AVG_RESPONSE_TIME] = self.time_interval.get(ceil(self.sum_time_taken/self.num_response),5)
                
                #correctness based responses
                if msg.getResult() == INCORRECT:
                    tutoring_state[QUALITY_ANSWER] = 1
                    
                    self.num_incorrect_response = 1 if self.num_incorrect_response is None else self.num_incorrect_response + 1
                    tutoring_state[NUMBER_OF_INCORRECT] = self.interval.get(int(self.num_incorrect_response),5) 
                    
                    self.sum_time_incorrect = self.time_taken if self.sum_time_incorrect is None else self.sum_time_incorrect + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_INCORRECT] = self.time_interval.get(ceil(self.sum_time_incorrect/self.num_incorrect_response),5)
                    
                    self.questions[-1][1] = 1
                
                elif msg.getResult() == MIXED:
                    tutoring_state[QUALITY_ANSWER] = 2
                    
                    self.num_mixed_response = 1 if self.num_mixed_response is None else self.num_mixed_response + 1
                    tutoring_state[NUMBER_OF_MIXED] = self.interval.get(int(self.num_mixed_response),5)
                    
                    self.sum_time_mixed = self.time_taken if self.sum_time_mixed is None else self.sum_time_mixed + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_MIXED] = self.time_interval.get(ceil(self.sum_time_mixed/self.num_mixed_response),5)
                    
                    self.questions[-1][1] = 2
                    
                elif msg.getResult() == CORRECT:
                    tutoring_state[QUALITY_ANSWER] = 3 
                    
                    self.num_correct_response = 1 if self.num_correct_response is None else self.num_correct_response + 1
                    tutoring_state[NUMBER_OF_CORRECT] = self.interval.get(int(self.num_correct_response),5)
                    
                    self.sum_time_correct = self.time_taken if self.sum_time_correct is None else self.sum_time_correct + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_CORRECT] = self.time_interval.get(ceil(self.sum_time_correct/self.num_correct_response),5)
                    
                    self.questions[-1][1] = 3
                else:
                    print("Incorrect Correctness value")
                
                #get score
                scr = tutoring_state[NUMBER_OF_CORRECT] + (0.5 * tutoring_state[NUMBER_OF_MIXED]) 
                tutoring_state[SCORE] = self.interval.get(ceil(float(scr)),5)
                
                #update quality_state
                tutoring_state[RESP_QUALITY_AFTER_RESPONSE] = quality_state[(tutoring_state[QUALITY_ANSWER], tutoring_state[AFTER_USERRESPONSE_STATE])]
        except:
            logInfo('{0} received RL Coach update message exception: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                       
        print(tutoring_state)
    
    #update AAR item
    def updateStateRLAAR(self,msg):
        
        try:
            #if message is transcript update
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
                    self.rLService_random.updateNonCorrectAARItem(item)
                print(AAR_item)
            #if message informs the start of AAR
            elif BEGIN_AAR in msg.getVerb():
                logInfo('{0} received AAR item final update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                AAR_item['-1'] = DONE
        except:
            logInfo('{0} received RL AAR update message exception: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
    
    def getState(self):
        return tutoring_state   #can also be accessed directly as a global variable       

#handles incoming and outgoing messages     
class RLServiceMessaging(BaseService):
    
    rLService_internal = RLPlayer()         #for internal updates
    rLService_random = RLRandom()           #random policy
    rLService_feature = RLCoachFeature()    #trained policy for RL Coach
    #csvLog = LoggingService.CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()
    
    
    def __init__(self, experimentCondition="Default"):
        super().__init__()
        self.experimentCondition=experimentCondition
    
    
    #receive message and take appropriate action by looking at the message attributes like verb         
    def receiveMessage(self, msg):
        super(RLServiceMessaging, self).receiveMessage(msg)
        
        #Check specific messages for AAR and Coach
        #if message asks for the next agenda item in AAR
        if GET_NEXT_AGENDA_ITEM in msg.getVerb():
            
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
            
            #for random RL
            if self.experimentCondition=="A":
                action = self.rLService_random.getTopAction()
            
            else:
                #for trained policy based RL
                try:
                    action = self.rLService_feature.getTopAction()
                except:
                    action = DO_NOTHING
                
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
            
            #update RL AAR state based on the message
            self.rLService_internal.updateStateRLAAR(msg)
            
            #update RL coach state based on the message
            self.rLService_internal.updateStateRLCoach(msg)
