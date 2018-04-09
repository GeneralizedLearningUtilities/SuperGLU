#!/usr/bin/env python

'''Python 3 script: RLPlayer.py 

Version 1.x: fall 2017 updates by Mark Core
Documentation: https://docs.google.com/document/d/1ugSHaWLXTKXawXAGkdsGblTAGnew-wZOGedYdvqVhQk/edit?usp=sharing

Contains class RLServiceMessaging which deals with SuperGLU messages coming from the Engage
system which are:

1. state updates
2. requests for next coaching action. 
3. requests for next AAR action.

Original version created on May 19, 2016 by
@author: skarumbaiah
Documentation here: https://docs.google.com/document/d/1RfX9zMZEjgFuY31qRXaRPC_b64N0yOLxdXTuean8K2s/edit#

KNOWN ISSUE: Although this is a class, it has many global variables so if you created multiple instances
      of the class then bad things would happen.

'''

import sys
import random as rand
from datetime import datetime
import csv,os
from SuperGLU.Core.MessagingGateway import BaseService, BaseMessagingNode, ORIGINATING_SERVICE_ID_KEY
from SuperGLU.Util.ErrorHandling import logInfo, tryRaiseError
#from SuperGLU.Services.LoggingService  import LoggingService  
from SuperGLU.Services.RLService.Constants import *
from math import ceil
from SuperGLU.Util.Representation.Classes import Speech
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT

# BEGIN initialization of global, module variables
# These global variables are initialized the first time an import command references this module

RL_SERVICE_NAME = "RL Service"

#tutoring state for RL coach
tutoring_state = {  
    # Scenario number (1/2/3) (default 1)
    SCENARIO_NUMBER : 1,                  
    # gender of the participant (RMALE | RFEMALE)
    GENDER : RMALE,
    # 0 = hint possible state
    # 1 = feedback possible state            
    AFTER_USERRESPONSE_STATE: 1,           
    FINAL_STATE: 0,                       # always 0.
    # quality_state(quality of answer,AFTER_USERRESPONSE_STATE)
    RESP_QUALITY_AFTER_RESPONSE : 0       
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

    # count of AAR actions (clustered in 6 classes) (default 0)
    tutoring_state[NUM_DOOVER] = 0
    tutoring_state[NUM_DIAGNOSE] = 0

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

SCORE_THRESH_LOW = 1
SCORE_THRESH_LOWMID = 3
SCORE_THRESH_MID = 6
SCORE_THRESH_MIDHIGH = 11
SCORE_THRESH_HIGH = 18

def calScoreClass(num):
    value = 0
    if (num>=0 and num<=SCORE_THRESH_LOW):
        value = 1
    elif (num>SCORE_THRESH_LOW and num<=SCORE_THRESH_LOWMID):
        value = 2
    elif (num>SCORE_THRESH_LOWMID and num<=SCORE_THRESH_MID):
        value = 3
    elif (num>SCORE_THRESH_MID and num<=SCORE_THRESH_MIDHIGH):
        value = 4
    elif (num > SCORE_THRESH_MIDHIGH):
        value = 5
    return value

TIME_THRESH_LOW = 3
TIME_THRESH_LOWMID = 5
TIME_THRESH_MID = 10
TIME_THRESH_MIDHIGH = 17
TIME_THRESH_HIGH = 28

def calTimeClass(time):
    value = 0
    if (time>=0 and time<=TIME_THRESH_LOW):
        value = 1
    elif (time>TIME_THRESH_LOW and time<=TIME_THRESH_LOWMID):
        value = 2
    elif (time>TIME_THRESH_LOWMID and time<=TIME_THRESH_MID):
        value = 3
    elif (time>TIME_THRESH_MID and time<=TIME_THRESH_MIDHIGH):
        value = 4
    elif (time > TIME_THRESH_MIDHIGH):
        value = 5
    return value

AAR_THRESH_LOW = 2
AAR_THRESH_LOWMID = 4
AAR_THRESH_MID = 6
AAR_THRESH_MIDHIGH = 8
AAR_THRESH_HIGH = 10

def calAARcount(count):
    value = 0
    if (count>0 and count<=AAR_THRESH_LOW):
        value = 1
    elif (count>AAR_THRESH_LOW and count<=AAR_THRESH_LOWMID):
        value = 2
    elif (count>AAR_THRESH_LOWMID and count<=AAR_THRESH_MID):
        value = 3
    elif (count>AAR_THRESH_MID and count<=AAR_THRESH_MIDHIGH):
        value = 4
    elif (count>AAR_THRESH_MIDHIGH):
        value = 5
    return value

#handles incoming and outgoing messages     
class RLServiceMessaging(BaseService):

    #csvLog = LoggingService.CSVLoggingService("RLPlayerLog.csv")
    serializeMsg = BaseMessagingNode()

    # initialize or reset object variables for local context
    def init_local_context(self):

        self.state = "NOT AAR"
        self.num_response = 0
        self.num_correct_response = 0
        self.num_incorrect_response = 0
        self.num_mixed_response = 0
        self.start = None
        self.end = None
        self.time_taken = 0
        self.sum_time_taken = 0
        self.sum_time_correct = 0
        self.sum_time_mixed = 0
        self.sum_time_incorrect = 0

        self.decision_index = 0
        self.AAR_item_offset = -1
        self.next_AAR_item = -1
        self.next_AAR_action = DONE
        self.num_do_over = 0
        self.num_diagnose = 0
        self.dynamic_state = []
        self.decision_id = "UNKNOWN"

    def writeDiagnostic(self,msg_str):
        if (msg_str != ""):
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
        self.questions = []

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
    def getRLcoachAction(self):

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

    def isGiveFeedback(self,feedback_action,hint_action):
        if (feedback_action == GIVE_FEEDBACK):
            return True
        elif (hint_action == GIVE_FEEDBACK):
            return True
        else:
            return False

    def isGiveHint(self,feedback_action,hint_action):
        if (feedback_action == GIVE_HINT):
            return True
        elif (hint_action == GIVE_HINT):
            return True
        else:
            return False


    def getTopCoachAction(self):
        feedback_action = self.getRLcoachAction()
        
        tutoring_state[AFTER_USERRESPONSE_STATE] = 0
        tutoring_state[RESP_QUALITY_AFTER_RESPONSE] = self.quality_state[(tutoring_state[QUALITY_ANSWER], tutoring_state[AFTER_USERRESPONSE_STATE])]
        
        hint_action = self.getRLcoachAction()
        tutoring_state[AFTER_USERRESPONSE_STATE] = 1
        
        if (self.isGiveFeedback(feedback_action,hint_action) and self.isGiveHint(feedback_action,hint_action)):
            return GIVE_HINT_FEEDBACK
        elif (self.isGiveFeedback(feedback_action,hint_action)):
            return GIVE_FEEDBACK
        elif (self.isGiveHint(feedback_action,hint_action)):
            return GIVE_HINT
        else:
            return DO_NOTHING

    #get top action from the trained policy for the AAR   
    def getTopAAR_Action(self,decision_index):

        action = {DIAGNOSE:0, DOOVER:0}
        logstr = ""

        # set following state variables to appropriate variables for decision_index:
        tutoring_state[QUESTION_DIFFICULTY] = self.dynamic_state[decision_index][QUESTION_DIFFICULTY]
        tutoring_state[RESPONSE_TIME] = self.dynamic_state[decision_index][RESPONSE_TIME]
        tutoring_state[QUALITY_ANSWER] = self.dynamic_state[decision_index][QUALITY_ANSWER]

        if (tutoring_state[SCENARIO_NUMBER] == 2):
            tutoring_state[SEEN_BEFORE] = self.dynamic_state[decision_index][SEEN_BEFORE]
            tutoring_state[QUALITY_PREV_IF_SEEN] = self.dynamic_state[decision_index][QUALITY_PREV_IF_SEEN]
        # else either scenario == 1 or 3 and these variables will correctly have their initial values

        # set following state variables to null values (meaning not applicable):
        tutoring_state[QUALITY_ANSWER_LAST] = RNULL
        tutoring_state[QUALITY_ANSWER_LAST_LAST] = RNULL
        tutoring_state[RESPONSE_TIME_LAST] = 0
        tutoring_state[RESPONSE_TIME_LAST_LAST] = 0

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

        logstr = logstr + "AAR RL policy says next action = " + top_action + " index = " + str(decision_index) + " based on the following state: \n"
        logstr = logstr + str(tutoring_state) + "\n"
        
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
                # we only use random choice for condition A
                if (self.experimentCondition=="A"):
                    self.next_AAR_action = self.getRandomAAR_Action()
                    self.writeDiagnostic("AAR random choice says next action = " + self.next_AAR_action + " index = " + str(self.next_AAR_item) + "\n")
                else:
                    try:
                        self.next_AAR_action = self.getTopAAR_Action(self.next_AAR_item)
                    except:
                        self.writeDiagnostic("ERROR: AAR Action set to DOOVER. Exception in getTopAAR_Action: " + str(sys.exc_info()[0]) + "\n")
                        self.next_AAR_action = DOOVER
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
                # write diagnostic before calculate_next_AAR_info
                self.writeDiagnostic("BEGIN_AAR -> updateStateRLCoach\n")
                self.state = "AAR"
                self.calculate_next_AAR_info(0)
            
            elif msg.getVerb() == VR_EXPRESS:
                if (self.state != "AAR"):
                    self.dynamic_state.append(dict())            

                    result = msg.getResult()
                    self.decision_id = result.ref


                    if (self.decision_id in self.difficulty_dict):
                        tutoring_state[QUESTION_DIFFICULTY] = self.difficulty_dict[self.decision_id]
                        self.dynamic_state[self.decision_index][QUESTION_DIFFICULTY] = self.difficulty_dict[self.decision_id]
                    else:
                        tutoring_state[QUESTION_DIFFICULTY] = 0
                        self.dynamic_state[self.decision_index][QUESTION_DIFFICULTY] = 0
                    logstr = logstr + "VR_EXPRESS (" + self.decision_id + ") -> question_difficulty = " + str(tutoring_state[QUESTION_DIFFICULTY]) + "\n"

            #get Gender
            elif REGISTER_USER_INFO in msg.getVerb():
                #logInfo('{0} received gender update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)

                gend = msg.getObject()
                if gend ==  FEMALE:
                    tutoring_state[GENDER] = RFEMALE
                elif gend == MALE:
                    tutoring_state[GENDER] = RMALE
                logstr = logstr + "REGISTER_USER_INFO -> Gender = " + str(tutoring_state[GENDER]) + "\n"
            
            #update response time
            #verb should be GameLog, the object should be PracticeEnvironment and the result should be RandomizedChoices
            elif msg.getVerb() == GAME_LOG and msg.getObject() == PRACTICE_ENVIRONMENT and msg.getResult() == RANDOMIZED_CHOICES:
                #logInfo('{0} received start timestamp update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                self.start = msg.getTimestamp()
                logstr = logstr + "GAME_LOG, PRACTICE_ENVIRONMENT, RANDOMIZED_CHOICES -> start = " + str(self.start) + "\n"
            
            #once the participant answers
            elif TRANSCRIPT_UPDATE in msg.getVerb():
                #logInfo('{0} received transcript update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
                logstr = logstr + "TRANSCRIPT_UPDATE -> updating state (see msg and new state)\n"
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
                    
                    tutoring_state[SEEN_BEFORE] = 0
                    tutoring_state[QUALITY_PREV_IF_SEEN] = RNULL
                    self.dynamic_state[self.decision_index][SEEN_BEFORE] = 0
                    self.dynamic_state[self.decision_index][QUALITY_PREV_IF_SEEN] = RNULL
                    for question in self.questions:
                        if question[0] == node_id:
                            tutoring_state[SEEN_BEFORE] = 1
                            tutoring_state[QUALITY_PREV_IF_SEEN] = question[1]
                            self.dynamic_state[self.decision_index][SEEN_BEFORE] = 1
                            self.dynamic_state[self.decision_index][QUALITY_PREV_IF_SEEN] = question[1]
                            break
            
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
                    self.time_taken = 0
                
                #get counts and averages
                self.num_response = self.num_response + 1
                tutoring_state[NUMBER_OF_RESPONSE] = calScoreClass(int(self.num_response)) 
                
                self.sum_time_taken = self.sum_time_taken + self.time_taken
                tutoring_state[RESPONSE_TIME] = calTimeClass(ceil(self.time_taken))
                self.dynamic_state[self.decision_index][RESPONSE_TIME] = tutoring_state[RESPONSE_TIME]
                tutoring_state[AVG_RESPONSE_TIME] = calTimeClass(ceil(self.sum_time_taken/self.num_response))
                
                #correctness based responses
                if msg.getResult() == INCORRECT:
                    tutoring_state[QUALITY_ANSWER] = RINCORRECT
                    
                    self.num_incorrect_response = self.num_incorrect_response + 1
                    tutoring_state[NUMBER_OF_INCORRECT] = calScoreClass(int(self.num_incorrect_response)) 
                    
                    self.sum_time_incorrect = self.sum_time_incorrect + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_INCORRECT] = calTimeClass(ceil(self.sum_time_incorrect/self.num_incorrect_response))

                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RINCORRECT

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RINCORRECT
                
                elif msg.getResult() == MIXED:
                    tutoring_state[QUALITY_ANSWER] = RMIXED
                    
                    self.num_mixed_response = self.num_mixed_response + 1
                    tutoring_state[NUMBER_OF_MIXED] = calScoreClass(int(self.num_mixed_response))
                    
                    self.sum_time_mixed = self.sum_time_mixed + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_MIXED] = calTimeClass(ceil(self.sum_time_mixed/self.num_mixed_response))

                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RMIXED

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RMIXED
                    
                elif msg.getResult() == CORRECT:
                    tutoring_state[QUALITY_ANSWER] = RCORRECT 
                    
                    self.num_correct_response = self.num_correct_response + 1
                    tutoring_state[NUMBER_OF_CORRECT] = calScoreClass(int(self.num_correct_response))
                    
                    self.sum_time_correct = self.sum_time_correct + self.time_taken
                    tutoring_state[AVG_RESPONSE_TIME_CORRECT] = calTimeClass(ceil(self.sum_time_correct/self.num_correct_response))
                    
                    self.dynamic_state[self.decision_index][QUALITY_ANSWER] = RCORRECT

                    if tutoring_state[SCENARIO_NUMBER] == 1:
                        self.questions[-1][1] = RCORRECT
                else:
                    logstr = logstr + "ERROR: Incorrect Correctness value\n"
                
                #update quality_state
                tutoring_state[RESP_QUALITY_AFTER_RESPONSE] = self.quality_state[(tutoring_state[QUALITY_ANSWER], tutoring_state[AFTER_USERRESPONSE_STATE])]

                #get score
                scr = self.num_correct_response + (0.5 * self.num_mixed_response) 
                tutoring_state[SCORE] = calScoreClass(ceil(float(scr)))

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
                    # print diagnostic before calculate_next_AAR_info prints diagnostics
                    self.writeDiagnostic('GET_NEXT_AGENDA_ITEM -> PERFORM_ACTION (DONE)\n')
                else:
                    item = self.next_AAR_item + self.AAR_item_offset
                    action = self.next_AAR_action
                    self.writeDiagnostic('GET_NEXT_AGENDA_ITEM -> PERFORM_ACTION (action= ' + action + ' index= ' + str(item) + ')\n')
                    if (action == DOOVER):
                        self.num_do_over = self.num_do_over + 1
                        tutoring_state[NUM_DOOVER] = calAARcount(self.num_do_over)
                    elif (action == DIAGNOSE):
                        self.num_diagnose = self.num_diagnose + 1
                        tutoring_state[NUM_DIAGNOSE] = calAARcount(self.num_diagnose)

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
                logstr = logstr + 'REQUEST_COACHING_ACTIONS -> ELITE Coach -> COACHING_ACTIONS (' + action + ')\n'
            else:
                # coach is turned off for scenario 3, and RL policy is
                # not trained to produce sensible actions for scenario 3.
                if (tutoring_state[SCENARIO_NUMBER] == 3):
                    action = DO_NOTHING
                    logstr = logstr + 'REQUEST_COACHING_ACTIONS -> 3rd scenario / RL Coach -> COACHING_ACTIONS (always DO_NOTHING)\n'
                else:
                    #for trained policy based RL
                    try:
                        action = self.getTopCoachAction()
                        logstr = logstr + 'REQUEST_COACHING_ACTIONS -> RL Coach -> COACHING_ACTIONS (' + action + ')\n'                                            
                    except:
                        logstr = logstr + "ERROR: Action set to DO_NOTHING. Exception in getTopCoachAction: " + str(sys.exc_info()[0]) + "\n"
                        action = DO_NOTHING
                
            #send message   
            reply_msg = self._createRequestReply(msg)
            reply_msg.setResult(action)
            reply_msg.setVerb(COACHING_ACTIONS)
            reply_msg.setSpeechAct(INFORM_ACT)
            reply_msg.setContextValue(ORIGINATING_SERVICE_ID_KEY, self.getId())
            
            if reply_msg is not None:
                
                #logInfo('{0} is sending reply for coaching request:{1}'.format(RL_SERVICE_NAME, self.messageToString(reply_msg)), 2)
                self.sendMessage(reply_msg)  
            
        #consider message for state update  - can also reuse TRANSCRIPT_UPDATE for correctness ???
        else:
            #logInfo('{0} received state update message: {1}'.format(RL_SERVICE_NAME, self.messageToString(msg)), 2)
            
            #update RL coach state based on the message
            self.updateStateRLCoach(msg)
        
        self.writeDiagnostic(logstr)
