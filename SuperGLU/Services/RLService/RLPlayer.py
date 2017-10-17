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
Creates a log file, RLPlayerDiagnostics.txt for specific debug messages and error messages from this script.
Prints error message if unknown action or feature seen in weights.

KNOWN ISSUES: 
  1. Although this is a class, it has many global variables so if you created multiple instances
      of the class then bad things would happen.

'''

import sys
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
tutoring_state = {  SCENARIO_NUMBER : 1,                  # Scenario number (1/2) (default 1)
                    GENDER : RMALE,                       # gender of the participant (RMALE | RFEMALE) 
                    AFTER_USERRESPONSE_STATE: 0,          # always 0.
                    FINAL_STATE: 0,                       # always 0.
                    RESP_QUALITY_AFTER_RESPONSE : 0       # quality_state(quality of answer,AFTER_USERRESPONSE_STATE)
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

    #difficulty class of current decision. 0 means don't know, or not applicable.
    tutoring_state[QUESTION_DIFFICULTY] = 0

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
        self.decision_index = 0
        self.AAR_item_offset = -1
        self.next_AAR_item = -1
        self.next_AAR_action = DEFER
        self.dynamic_state = []
        self.decision_id = "UNKNOWN"

    def writeDiagnostic(self,msg_str):
        cur = os.getcwd()
        
        # open RL log file "RLPlayerDiagnostics.txt" in the same directory as the Python process
        # append msg_str (don't add any newline)
        filepath = os.path.join(cur, "RLPlayerDiagnostics.txt")
        try:
            with open(filepath, 'a') as logfile:
                logfile.write(msg_str)                
        except:
            print("ERROR: CANNOT OPEN DIAGNOSTICS LOG FILE. DIAGNOSTICS ENTRY NOT SAVED.")


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

        self.writeDiagnostic("new session. experimentCondition = " + self.experimentCondition + "\n")

        cur = os.getcwd()

        #weights.csv policy file needs to be in the same directory as the Python process
        filepath = os.path.join(cur, 'weights.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            self.weights = list(reader)

        #weights-AAR.csv policy file needs to be in the same directory as the Python process
        filepath = os.path.join(cur, 'weights-AAR.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            self.weights_AAR = list(reader)

        self.difficulty_dict = {}
        #difficulty.csv file needs to be in the same directory as the Python process
        filepath = os.path.join(cur, 'difficulty.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.difficulty_dict[row[0]] = row[1]


    #Random policy for Coach
    def getRandomCoachAction(self):
        r = rand.random()
        if r < 0.5:
            return GIVE_HINT_FEEDBACK
        else:
            return DO_NOTHING

    # ELITE Coaching policy
    def getELITEcoachAction(self):
        hint = False
        feedback = False

        if (tutoring_state[QUALITY_ANSWER] == RINCORRECT): 
            hint = True
            feedback = True
        elif (tutoring_state[QUALITY_ANSWER] == RMIXED):
            hint= True
            performance = self.num_correct_response / self.num_response
            if (performance < 0.6):
                feedback = True

        if (hint and feedback):
            return GIVE_HINT_FEEDBACK
        elif (hint):
            return GIVE_HINT
        elif (feedback):
            return GIVE_FEEDBACK
        else:
            return DO_NOTHING


    #get top action from the trained policy for the coach   
    def getTopCoachAction(self):

        action = {DO_NOTHING:0, GIVE_HINT:0, GIVE_FEEDBACK:0, GIVE_HINT_FEEDBACK:0}
        logstr = ""

        #add weights for the state indicators set in tutoring_state
        for w in self.weights:
            if (w[0] in tutoring_state):
                if w[2] == RDONOTHING:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[DO_NOTHING] += float(w[3])
                elif w[2] == RHINT:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[GIVE_HINT] += float(w[3])
                elif w[2] == RFEEDBACK:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[GIVE_FEEDBACK] += float(w[3])
                elif w[2] == RHINT_FEEDBACK:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[GIVE_HINT_FEEDBACK] += float(w[3])
                else:
                    logstr = logstr + "ERROR: unrecognized action in weights: " + w[2] + "\n"
            else:
                logstr = logstr + "ERROR: unrecognized feature in weights: " + w[0] + "\n"

        #get best action
        top_action = max(action, key=action.get)
        #logstr = logstr + "RL picked this coach action: " + top_action + "\n"
        self.writeDiagnostic(logstr)
        return top_action 

    #get top action from the trained policy for the AAR   
    def getTopAAR_Action(self):

        action = {DIAGNOSE:0, DOOVER:0}
        logstr = ""

        #add weights for the state indicators set in tutoring_state
        for w in self.weights_AAR:
            if (w[0] in tutoring_state):
                if w[2] == RDIAGNOSE:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[DIAGNOSE] += float(w[3])
                elif w[2] == RDOOVER:
                    if tutoring_state[w[0]] == int(w[1]):
                        action[DOOVER] += float(w[3])
                else:
                    logstr = logstr + "ERROR: unrecognized action in AAR weights: " + w[2] + "\n"
            else:
                logstr = logstr + "ERROR: unrecognized feature in AAR weights: " + w[0] + "\n"

        #get best action
        top_action = max(action, key=action.get)

        self.writeDiagnostic(logstr)
        return top_action 

    def getRandomAAR_Action(self):
        r = rand.random()
        if r  < 0.5:
            return DIAGNOSE
        else:
            return DOOVER

    # ************** UPDATE STATE METHODS ******************************

    def end_scenario(self):
        #set previous values 
        tutoring_state[SCENARIO_NUMBER] = tutoring_state[SCENARIO_NUMBER] + 1
        if (tutoring_state[SCENARIO_NUMBER] == 3):
            self.questions = []
            tutoring_state[SEEN_BEFORE] = 0
            tutoring_state[QUALITY_PREV_IF_SEEN] = RNULL
        init_prev_scenario_context()
                
        #reset current values
        init_global_scenario_context()
        
        # reset local variables
        self.init_local_context()

    def calculate_next_AAR_info(self,item):
        for i in range(item,self.decision_index):
            # if correct, do nothing (i.e., skip over the item)
            if (self.dynamic_state[i][QUALITY_ANSWER] != RCORRECT):
                self.next_AAR_item = i
                self.next_AAR_action = self.getRandomAAR_Action()
                break
        else:
            self.next_AAR_item = -1
            self.next_AAR_action = DONE

    #update state with every message
    def updateStateRLCoach(self,msg):
        #state update on relevant messages
        logstr = ""
        try:
            #update scenario
            if BEGIN_AAR in msg.getVerb():
                #logInfo('{0} received scenario update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                logstr = logstr + "updateStateRLCoach: BEGIN_AAR msg.\n"

                self.calculate_next_AAR_info(0)
            
            elif msg.getVerb() == VR_EXPRESS:
                result = msg.getResult()
                self.decision_id = result.ref
                if (self.decision_id in self.difficulty_dict):
                    tutoring_state[QUESTION_DIFFICULTY] = self.difficulty_dict[self.decision_id]
                    logstr = logstr + "decision id is: " + self.decision_id + " question_difficulty is " + self.difficulty_dict[self.decision_id] + "\n"
                else:
                    tutoring_state[QUESTION_DIFFICULTY] = 0
                    logstr = logstr + "decision id is: " + self.decision_id + " question_difficulty is 0 (not seen in training)\n"

            #get Gender
            elif REGISTER_USER_INFO in msg.getVerb():
                #logInfo('{0} received gender update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)

                gend = msg.getObject()
                if gend ==  FEMALE:
                    tutoring_state[GENDER] = RFEMALE
                elif gend == MALE:
                    tutoring_state[GENDER] = RMALE
                logstr = logstr + "updateStateRLCoach: REGISTER_USER_INFO msg. Gender = " + str(tutoring_state[GENDER]) + "\n"
                logstr = logstr + str(tutoring_state) + "\n"
            
            #update response time
            #verb should be GameLog, the object should be PracticeEnvironment and the result should be RandomizedChoices
            elif msg.getVerb() == GAME_LOG and msg.getObject() == PRACTICE_ENVIRONMENT and msg.getResult() == RANDOMIZED_CHOICES:
                #logInfo('{0} received start timestamp update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                self.start = msg.getTimestamp()
                logstr = logstr + "updateStateRLCoach: GAME_LOG, PRACTICE_ENVIRONMENT, RANDOMIZED_CHOICES msg. start = " + str(self.start) + "\n"
                logstr = logstr + str(tutoring_state) + "\n"
            
            #once the participant answers
            elif TRANSCRIPT_UPDATE in msg.getVerb():
                #logInfo('{0} received transcript update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                logstr = logstr + self.messageToString(msg) + "\n"

                # update AAR item offset
                item = int(msg.getContextValue(ORDER))

                tmp_offset = item - self.decision_index
                if (self.AAR_item_offset == -1):
                    self.AAR_item_offset = tmp_offset
                elif not(tmp_offset == self.AAR_item_offset):
                    logstr = logstr + "ERROR: current offset: " + str(tmp_offset) + " different than initial one: " + str(self.AAR_item_offset) + "\n"
                    logstr = logstr + "\t sticking with initial offset. item = " + str(item) + " decision_index = " + str(self.decision_index) + "\n"

                #store unique ID of node
                if tutoring_state[SCENARIO_NUMBER] == 1:
                    logInfo('{0} received question store message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                    node_id = msg.getContextValue(NODE_ID_CONTEXT_KEY)
                    node = [node_id, 0] #quality null - will be updated when checked for correctness
                    self.questions.append(node)
            
                #check if Chen's Utterances stored before
                elif tutoring_state[SCENARIO_NUMBER] == 2:
                    logInfo('{0} received if seen before message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                    node_id = msg.getContextValue(NODE_ID_CONTEXT_KEY)
                    for question in self.questions:
                        if question[0] == node_id:
                            tutoring_state[SEEN_BEFORE] = 1
                            tutoring_state[QUALITY_PREV_IF_SEEN] = question[1]
                            break
                        else:
                            tutoring_state[SEEN_BEFORE] = 0
                            tutoring_state[QUALITY_PREV_IF_SEEN] = RNULL
            
                self.dynamic_state.append(dict())

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
                    logstr = logstr + "ERROR: decision end seen, but not beginning\n"
                
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

                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RINCORRECT

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RINCORRECT
                
                elif msg.getResult() == MIXED:
                    tutoring_state[QUALITY_ANSWER] = RMIXED
                    
                    self.num_mixed_response = 1 if self.num_mixed_response is None else self.num_mixed_response + 1
                    tutoring_state[NUMBER_OF_MIXED] = self.interval.get(int(self.num_mixed_response),5)
                    
                    self.sum_time_mixed = self.time_taken if self.sum_time_mixed is None else self.sum_time_mixed + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_MIXED] = self.time_interval.get(ceil(self.sum_time_mixed/self.num_mixed_response),5)

                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RMIXED

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RMIXED
                    
                elif msg.getResult() == CORRECT:
                    tutoring_state[QUALITY_ANSWER] = RCORRECT 
                    
                    self.num_correct_response = 1 if self.num_correct_response is None else self.num_correct_response + 1
                    tutoring_state[NUMBER_OF_CORRECT] = self.interval.get(int(self.num_correct_response),5)
                    
                    self.sum_time_correct = self.time_taken if self.sum_time_correct is None else self.sum_time_correct + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_CORRECT] = self.time_interval.get(ceil(self.sum_time_correct/self.num_correct_response),5)
                    
                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RCORRECT

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RCORRECT
                else:
                    logstr = logstr + "ERROR: Incorrect Correctness value\n"
                
                #update quality_state
                tutoring_state[RESP_QUALITY_AFTER_RESPONSE] = self.quality_state[(tutoring_state[QUALITY_ANSWER], tutoring_state[AFTER_USERRESPONSE_STATE])]

                #get score
                scr = tutoring_state[NUMBER_OF_CORRECT] + (0.5 * tutoring_state[NUMBER_OF_MIXED]) 
                tutoring_state[SCORE] = self.interval.get(ceil(float(scr)),5)

                self.decision_index = self.decision_index + 1

                logstr = logstr + str(tutoring_state) + "\n"
                
        except:
            #logInfo('{0} received RL Coach update message exception: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            logstr = logstr + 'ERROR: Exception in updateStateRLCoach: ' + str(sys.exc_info()[0]) + '\n'
                       
        self.writeDiagnostic(logstr)


    def getState(self):
        return tutoring_state   #can also be accessed directly as a global variable       
    
    #receive message and take appropriate action by looking at the message attributes like verb         
    def receiveMessage(self, msg):
        super(RLServiceMessaging, self).receiveMessage(msg)

        logstr = ""
                        
        #if message asks for the next agenda item in AAR
        if GET_NEXT_AGENDA_ITEM in msg.getVerb():
            
            #logstr = logstr + "receiveMessage: GET_NEXT_AGENDA_ITEM msg.\n"
            try:
                if (self.next_AAR_item == -1):
                    item = -1
                    action = DONE
                    self.end_scenario()
                    logstr = logstr + 'receiveMessage: send PERFORM_ACTION: DONE\n'
                else:
                    item = self.next_AAR_item + self.AAR_item_offset
                    action = self.next_AAR_action
                    logstr = logstr + 'receiveMessage: send PERFORM_ACTION: ' + action + ' index= ' + str(item) + '\n'

                    # update next_AAR_item and next_AAR_action
                    self.calculate_next_AAR_info(self.next_AAR_item + 1)
             
                #send message   
                reply_msg = self._createRequestReply(msg)
                reply_msg.setResult(action)
                reply_msg.setVerb(PERFORM_ACTION)
                reply_msg.setObject(item)
            
                if reply_msg is not None:
                    #logInfo('{0} is sending reply for AAR agenda item:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply_msg)), 2)
                    self.sendMessage(reply_msg)            
            except:
                logstr = logstr + 'ERROR: Exception handling GET_NEXT_AGENGA_ITEM: ' + str(sys.exc_info()[0]) + '\n'
        
        #if Elite asks for coaching action
        elif REQUEST_COACHING_ACTIONS in msg.getVerb():
            #logInfo('{0} received request coaching action message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            #logstr = logstr + 'receiveMessage: REQUEST_COACHING_ACTIONS msg.\n'
            
            #for random RL
            if self.experimentCondition=="A":
                action = self.getELITEcoachAction()
            
            else:
                #for trained policy based RL
                try:
                    action = self.getTopCoachAction()
                except:
                    logstr = logstr + "ERROR: Action set to DO_NOTHING. Exception in getTopCoachAction: " + str(sys.exc_info()[0]) + "\n"
                    action = DO_NOTHING
                
            #send message   
            reply_msg = self._createRequestReply(msg)
            reply_msg.setResult(action)
            reply_msg.setVerb(COACHING_ACTIONS)
            
            if reply_msg is not None:
                logstr = logstr + 'receiveMessage: send COACHING_ACTIONS: ' + action + '\n'
                #logInfo('{0} is sending reply for coaching request:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply_msg)), 2)
                self.sendMessage(reply_msg)  
            
        #consider message for state update  - can also reuse TRANSCRIPT_UPDATE for correctness ???
        else:
            #logInfo('{0} received state update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            
            #update RL coach state based on the message
            self.updateStateRLCoach(msg)
        
        self.writeDiagnostic(logstr)
