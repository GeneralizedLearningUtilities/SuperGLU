#!/usr/bin/env python

'''Python 3 script: RLPlayer.py was created on May 19, 2016 by
@author: skarumbaiah
Documentation here: https://docs.google.com/document/d/1RfX9zMZEjgFuY31qRXaRPC_b64N0yOLxdXTuean8K2s/edit#

Contains class RLServiceMessaging which deals with SuperGLU messages coming from the Engage
system which are:

1. state updates
2. requests for next coaching action. Based on experimental condition, either pick randomly or use RL policy
    to decide.
3. requests for next AAR action. Never include correct response in AAR. Otherwise pick randomly between DOOVER and DIAGNOSE.

Version 1.x: August/September 2017 updates by Mark Core

Consolidated everything into a single class. Moved reading of weights into constructor.
Prints warning if unknown action seen in weights.

KNOWN ISSUES: 
  1. Although this is a class, it has many global variables so if you created multiple instances
      of the class then bad things would happen.
  2. AAR decisions made before end of game and all context known.

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

# BEGIN initialization of global, module variables
# These global variables are initialized the first time an import command references this module

RL_SERVICE_NAME = "RL Service"

#tutoring state for RL coach
tutoring_state = {  SCENARIO_NUMBER : 1,                  #Scenario number (1/2) (default 1)
                    GENDER : RMALE,                       #gender of the participant (RMALE | RFEMALE) 
                  }

def init_global_scenario_context():
    # QUALITY FEATURES: RNULL | RINCORRECT | RMIXED | RCORRECT

    # correctness of 3rd to last answer
    tutoring_state[QUALITY_ANSWER_LAST_LAST] = RNULL
    # correctness of 2nd to last answer
    tutoring_state[QUALITY_ANSWER_LAST] = RNULL
    # correctness of previous answer
    tutoring_state[QUALITY_ANSWER] = RNULL
    #correctness of response in the previous scenario if the same question has appeared 
    tutoring_state[QUALITY_PREV_IF_SEEN] = RNULL
    #Has the system question appeared in the previous scenario? (0(no)/1(yes)) (default 0)
    tutoring_state[SEEN_BEFORE] = 0

    #Score in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[SCORE] = 0

    #Number of responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_RESPONSE] = 0
    #Number of correct responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_CORRECT] = 0
    #Number of mixed responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_MIXED] = 0
    #Number of incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_INCORRECT] = 0

    #User response time for previous question (clustered in 6 classes) (default 0)
    tutoring_state[RESPONSE_TIME] = 0
    #User response time for 2nd to last question (clustered in 6 classes) (default 0)
    tutoring_state[RESPONSE_TIME_LAST] = 0
    #User response time for 3rd to last question (clustered in 6 classes) (default 0)
    tutoring_state[RESPONSE_TIME_LAST_LAST] = 0

    #Average user response time for all responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME] = 0
    #Average user response time for correct responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_CORRECT] = 0
    #Average user response time for mixed responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_MIXED] = 0
    #Average user response time for incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_INCORRECT] = 0

# copies value of context from previous scenario
# to initialize these entries, first initialize scenario context then use this function
# to copy those default values.
def init_prev_scenario_context():
    #Score in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[SCORE_PREV] = tutoring_state[SCORE]
    #Number of responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_RESPONSE_PREV] = tutoring_state[NUMBER_OF_RESPONSE]
    #Number of correct responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_CORRECT_PREV] = tutoring_state[NUMBER_OF_CORRECT]
    #Number of mixed responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_MIXED_PREV] = tutoring_state[NUMBER_OF_MIXED]
    #Number of incorrect responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[NUMBER_OF_INCORRECT_PREV] = tutoring_state[NUMBER_OF_INCORRECT]
    #Average user response time for all responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_PREV] = tutoring_state[AVG_RESPONSE_TIME]
    #Average user response time for correct responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_CORRECT_PREV] = tutoring_state[AVG_RESPONSE_TIME_CORRECT]
    #Average user response time for mixed responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_MIXED_PREV] = tutoring_state[AVG_RESPONSE_TIME_MIXED]
    #Average user response time for incorrect responses in previous scenario (clustered in 6 classes) (default 0)
    tutoring_state[AVG_RESPONSE_TIME_INCORRECT_PREV] = tutoring_state[AVG_RESPONSE_TIME_INCORRECT]

init_global_scenario_context()
init_prev_scenario_context()

#AAR item list
AAR_item = {}


# END initialization of global, module variables

#handles incoming and outgoing messages     
class RLServiceMessaging(BaseService):

    #csvLog = LoggingService.CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()

    # initialize or reset object variables for local context
    def init_local_context(self):
        #recent locals for current
        self.num_response = None
        self.num_correct_response = None
        self.num_incorrect_response = None
        self.num_mixed_response = None
        self.start = None
        self.end = None
        self.time_taken = None

    def __init__(self, experimentCondition="Default"):
        super().__init__()

        self.init_local_context()

        # initialize rest of object variables
        self.experimentCondition=experimentCondition
        self.sum_time_taken = None
        self.sum_time_correct = None
        self.sum_time_mixed = None
        self.sum_time_incorrect = None
        self.questions = []
        #interval
        self.interval = {None:0, 0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2, 9:3, 10:3, 11:3, 12:3, 13:4, 14:4, 15:4, 16:4}
        self.time_interval = {None:0, 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:2, 11:3, 12:3, 13:3, 14:3, 15:3, 16:4, 17:4, 18:4, 19:4, 20:4}
        self.quality_state = {(0,0):0, (0,1):1, (1,0):2, (1,1):3, (2,0):4, (2,1):5, (3,0):6, (3,1):7} #(quality,state)

        #weights.csv policy file needs to be in the same directory as the Python process
        cur = os.getcwd()
        filepath = os.path.join(cur, 'weights.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            self.weights = list(reader)

    #Random policy for Coach
    def getRandomCoachAction(self):
        r = rand.random()
        if r < 0.5:
            return GIVE_HINT_FEEDBACK
        else:
            return DO_NOTHING

    #get top action from the trained policy for the coach   
    def getTopCoachAction(self):

        action = {DO_NOTHING:0, HINT:0, FEEDBACK:0, FEEDBACK_HINT:0}
        
        #add weights for the state indicators set in tutoring_state
        for w in self.weights:
            if w[2] == DONOTHING:
                if tutoring_state[w[0]] == int(w[1]):
                    action[DO_NOTHING] += float(w[3])
            elif w[2] == HINT:
                if tutoring_state[w[0]] == int(w[1]):
                    action[HINT] += float(w[3])
            elif w[2] == FEEDBACK:
                if tutoring_state[w[0]] == int(w[1]):
                    action[FEEDBACK] += float(w[3])
            elif w[2] == FEEDBACK_HINT:
                if tutoring_state[w[0]] == int(w[1]):
                    action[FEEDBACK_HINT] += float(w[3])
            else:
                print("warning: unrecognized action in weights: " + w[2])
                    
        #get best action
        top_action = max(action, key=action.get)
        print("RL picked this coach action: " + top_action)
        return top_action 

    # ************** UPDATE STATE METHODS ******************************

    #update state with every message
    def updateStateRLCoach(self,msg):
        #state update on relevant messages
        
        try:
            #update scenario
            if BEGIN_AAR in msg.getVerb():
                logInfo('{0} received scenario update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                
                #set previous values 
                tutoring_state[SCENARIO_NUMBER] = 2
                init_prev_scenario_context()
                
                #reset current values
                init_global_scenario_context()

                # reset local variables
                self.init_local_context()
            
            #get Gender
            elif REGISTER_USER_INFO in msg.getVerb():
                logInfo('{0} received gender update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                gend = msg.getObject()
                if gend ==  FEMALE:
                    tutoring_state[GENDER] = RFEMALE
                elif gend == MALE:
                    tutoring_state[GENDER] = RMALE
            
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
                else:
                    print("WARNING: decision end seen, but not beginning")
                
                #get counts and averages
                self.num_response = 1 if self.num_response is None else self.num_response + 1
                tutoring_state[NUMBER_OF_RESPONSE] = self.interval.get(int(self.num_response),5) 
                
                self.sum_time_taken = self.time_taken if self.sum_time_taken is None else self.sum_time_taken + self.time_taken
                tutoring_state[RESPONSE_TIME] = self.time_interval.get(ceil(self.time_taken),5)
                tutoring_state[AVG_RESPONSE_TIME] = self.time_interval.get(ceil(self.sum_time_taken/self.num_response),5)
                
                #correctness based responses
                if msg.getResult() == INCORRECT:
                    tutoring_state[QUALITY_ANSWER] = RINCORRECT
                    
                    self.num_incorrect_response = 1 if self.num_incorrect_response is None else self.num_incorrect_response + 1
                    tutoring_state[NUMBER_OF_INCORRECT] = self.interval.get(int(self.num_incorrect_response),5) 
                    
                    self.sum_time_incorrect = self.time_taken if self.sum_time_incorrect is None else self.sum_time_incorrect + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_INCORRECT] = self.time_interval.get(ceil(self.sum_time_incorrect/self.num_incorrect_response),5)
                    
                    self.questions[-1][1] = RINCORRECT
                
                elif msg.getResult() == MIXED:
                    tutoring_state[QUALITY_ANSWER] = RMIXED
                    
                    self.num_mixed_response = 1 if self.num_mixed_response is None else self.num_mixed_response + 1
                    tutoring_state[NUMBER_OF_MIXED] = self.interval.get(int(self.num_mixed_response),5)
                    
                    self.sum_time_mixed = self.time_taken if self.sum_time_mixed is None else self.sum_time_mixed + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_MIXED] = self.time_interval.get(ceil(self.sum_time_mixed/self.num_mixed_response),5)
                    
                    self.questions[-1][1] = RMIXED
                    
                elif msg.getResult() == CORRECT:
                    tutoring_state[QUALITY_ANSWER] = RCORRECT 
                    
                    self.num_correct_response = 1 if self.num_correct_response is None else self.num_correct_response + 1
                    tutoring_state[NUMBER_OF_CORRECT] = self.interval.get(int(self.num_correct_response),5)
                    
                    self.sum_time_correct = self.time_taken if self.sum_time_correct is None else self.sum_time_correct + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_CORRECT] = self.time_interval.get(ceil(self.sum_time_correct/self.num_correct_response),5)
                    
                    self.questions[-1][1] = RCORRECT
                else:
                    print("Incorrect Correctness value")
                
                #get score
                scr = tutoring_state[NUMBER_OF_CORRECT] + (0.5 * tutoring_state[NUMBER_OF_MIXED]) 
                tutoring_state[SCORE] = self.interval.get(ceil(float(scr)),5)
                
        except:
            logInfo('{0} received RL Coach update message exception: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                       
        print(tutoring_state)
    
    # randomly pick an AAR action for this decision
    def updateAARItem(self, item):
        r = rand.random()
        if r < 0.33:
            AAR_item[item] = SKIP
        elif r  < 0.66:
            AAR_item[item] = DIAGNOSE
        else:
            AAR_item[item] = DOOVER
            
    # randomly pick either DIAGNOSE or DOOVER for this decision
    def updateNonCorrectAARItem(self, item):
        r = rand.random()
        if r  < 0.5:
            AAR_item[item] = DIAGNOSE
        else:
            AAR_item[item] = DOOVER

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
                        self.updateAARItem(missed_item)
                print(item)
                
                if msg.getResult() == CORRECT:
                    AAR_item[item] = SKIP
                else:
                    self.updateNonCorrectAARItem(item)
                print(AAR_item)
            #if message informs the start of AAR
            elif BEGIN_AAR in msg.getVerb():
                logInfo('{0} received AAR item final update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                AAR_item['-1'] = DONE
        except:
            logInfo('{0} received RL AAR update message exception: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
    
    def getState(self):
        return tutoring_state   #can also be accessed directly as a global variable       

    
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
                action = self.getRandomCoachAction()
            
            else:
                #for trained policy based RL
                try:
                    action = self.getTopCoachAction()
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
            self.updateStateRLAAR(msg)
            
            #update RL coach state based on the message
            self.updateStateRLCoach(msg)
