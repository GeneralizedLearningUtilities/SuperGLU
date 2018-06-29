'''
Created on Jun 6, 2016

@author: skarumbaiah
'''
# -*- coding: utf-8 -*-

# 1. MESSAGES COMING IN

BEGIN_AAR = 'BeginAAR'                          #End of session message
VR_EXPRESS = "vrExpress"                        #VH utterance

#Gender
REGISTER_USER_INFO = "RegisterUserInfo"                 #pass gender
FEMALE = 'Female'
MALE = 'Male'

#get start timestamp for user response
GAME_LOG = 'GameLog'
GAME_LOG2 ='GameLog2'                            #verb
PRACTICE_ENVIRONMENT = 'PracticeEnvironment'    #object
RANDOMIZED_CHOICES = 'RandomizedChoices'        #result

# user responds
TRANSCRIPT_UPDATE = 'TranscriptUpdate'          
ORDER = 'order'         #Order of AAR items
NODE_ID_CONTEXT_KEY = "dialogNodeId" #node id to check for seen before
#Quality of previous answer
MIXED = 'MIXED'                 #Mixed answer       
CORRECT = 'CORRECT'             #Correct answer
INCORRECT = 'INCORRECT'         #Incorrect answer

#ELITE requests a coaching action
REQUEST_COACHING_ACTIONS = 'RequestCoachingActions'     
GET_NEXT_AGENDA_ITEM = 'GetNextAgendaItem'      #Ask for next AAR item

# 2. MESSAGES GOING OUT

COACHING_ACTIONS = 'CoachingActions' #send a coaching action to ELITE
PERFORM_ACTION = 'PerformAction'     #send an AAR action to ELITE


# AAR actions
DIAGNOSE ='diagnose'    #Diagnose
DOOVER ='do_over'       #Do Over
DONE = 'done'           #End of AAR Item

# coach actions
DO_NOTHING = 'do_nothing'                   #No hint or feedback
GIVE_HINT = 'give_hint'                     #Display hint
GIVE_FEEDBACK = 'give_feedback'             #Display feedback
GIVE_HINT_FEEDBACK = 'give_hint_feedback'   #Display feedback and hint


# 3.  RL constants 
# State variables to define a tutoring system's status

SCENARIO_NUMBER = "scenario_number"
GENDER = "gender"                                       
RMALE = 1
RFEMALE = 2
AFTER_USERRESPONSE_STATE = "after_userresponse_state"  
FINAL_STATE = "final_state"
RESP_QUALITY_AFTER_RESPONSE = "responsequality_prevquestion_class-after_userresponse_state"

# QUALITY FEATURES
QUALITY_PREV_IF_SEEN = "responsequality_appearedbefore_class"    
QUALITY_ANSWER = "responsequality_prevquestion_class"            
QUALITY_ANSWER_LAST = "responsequality_prev2question_class"       
QUALITY_ANSWER_LAST_LAST = "responsequality_prev3question_class"  
RNULL = 0
RINCORRECT = 1
RMIXED = 2
RCORRECT = 3
SEEN_BEFORE = "has_question_appeared_in_prevscenario_class"                     

QUESTION_DIFFICULTY = "question_difficulty_class"                  
SCORE = "score_sofar_class"                         

NUMBER_OF_RESPONSE = "num_responses_sofar_class"                       
NUMBER_OF_CORRECT = "num_correctresponses_sofar_class"       
NUMBER_OF_MIXED = "num_mixedresponses_sofar_class"           
NUMBER_OF_INCORRECT = "num_incorrectresponses_sofar_class"   

RESPONSE_TIME = "responsetime_prevquestion_class"                         
RESPONSE_TIME_LAST = "responsetime_prev2question_class"               
RESPONSE_TIME_LAST_LAST = "responsetime_prev3question_class"     
AVG_RESPONSE_TIME = "avg_responsetime_sofar_class"                       
AVG_RESPONSE_TIME_CORRECT = "avg_correctresponsetime_sofar_class"      
AVG_RESPONSE_TIME_MIXED = "avg_mixedresponsetime_sofar_class"           
AVG_RESPONSE_TIME_INCORRECT = "avg_incorrectresponsetime_sofar_class"   

SCORE_PREV = "score_prevscenario_class"                                   

NUMBER_OF_RESPONSE_PREV = "num_responses_prevscenario_class"         
NUMBER_OF_CORRECT_PREV = "num_correctresponses_prevscenario_class"           
NUMBER_OF_MIXED_PREV = "num_mixedresponses_prevscenario_class"               
NUMBER_OF_INCORRECT_PREV = "num_incorrectresponses_prevscenario_class"       

AVG_RESPONSE_TIME_PREV = "avg_responsetime_prevscenario_class"           
AVG_RESPONSE_TIME_CORRECT_PREV = "avg_correctresponsetime_prevscenario_class"       
AVG_RESPONSE_TIME_MIXED_PREV = "avg_mixedresponsetime_prevscenario_class"           
AVG_RESPONSE_TIME_INCORRECT_PREV = "avg_incorrectresponsetime_prevscenario_class"   

NUM_DOOVER = "numdoover_sofar_class"
NUM_DIAGNOSE = "numdiagnose_sofar_class"

#policy actions 
RDONOTHING = DO_NOTHING
RFEEDBACK = GIVE_FEEDBACK
RHINT = GIVE_HINT
RHINT_FEEDBACK = GIVE_HINT_FEEDBACK
RDIAGNOSE = DIAGNOSE
RDOOVER = "doover"

