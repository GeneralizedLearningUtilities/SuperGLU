'''
Created on Jun 6, 2016

@author: skarumbaiah
'''
# -*- coding: utf-8 -*-
#AAR RL service
SKIP = 'skip'           #Skip AAR item
DIAGNOSE ='diagnose'    #Diagnose
DOOVER ='do_over'       #Do Over
ORDER = 'order'         #Order of AAR items
DONE = 'done'           #End of AAR Item
#Verbs
PERFORM_ACTION = 'PerformAction'                #Verb for AAR Item action - reply message
GET_NEXT_AGENDA_ITEM = 'GetNextAgendaItem'      #Ask for next AAR item - update message
TRANSCRIPT_UPDATE = 'TranscriptUpdate'          #Update AAR dictionary with items - update message
BEGIN_AAR = 'BeginAAR'                          #End of session message

#RL Coach 
## State variables to define a tutoring system's status
SCENARIO_NUMBER = "scenario_number"                         #Scenario number (1/2) (default 1)
GENDER = "gender"                                           #gender of the participant (0(null)/1(male)/2(female)) (default 0)
NUMBER_OF_RESPONSE_PREV = "num_responses_prevscenario_class"         #Number of responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_CORRECT_PREV = "num_correctresponses_prevscenario_class"           #Number of correct responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_MIXED_PREV = "num_mixedresponses_prevscenario_class"               #Number of mixed responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_INCORRECT_PREV = "num_incorrectresponses_prevscenario_class"       #Number of incorrect responses in previous scenario (clustered in 6 classes) (default 0)
SCORE_PREV = "score_prevscenario_class"                                   #Score in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_PREV = "avg_responsetime_prevscenario_class"           #Average user response time for all responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_CORRECT_PREV = "avg_correctresponsetime_prevscenario_class"       #Average user response time for correct responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_MIXED_PREV = "avg_mixedresponsetime_prevscenario_class"           #Average user response time for mixed responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_INCORRECT_PREV = "avg_incorrectresponsetime_prevscenario_class"   #Average user response time for incorrect responses in previous scenario (clustered in 6 classes) (default 0)
SEEN_BEFORE = "has_question_appeared_in_prevscenario_class"                     #Has the system question appeared in the previous scenario? (0(no)/1(yes)) (default 0)
QUALITY_PREV_IF_SEEN = "responsequality_appearedbefore_class"   #Quality of response in the previous scenario if the same question has appeared (0(null)/1(Incorrect)/2(Mixed)/3(Correct)) (default 0)
QUALITY_ANSWER = "responsequality_prevquestion_class"                  #correctness of the previous answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
QUALITY_ANSWER_LAST = "responsequality_prev2question_class"        #correctness of the 2nd last answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
QUALITY_ANSWER_LAST_LAST = "responsequality_prev3question_class"        #correctness of the 3rd last answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
NUMBER_OF_RESPONSE = "num_responses_sofar_class"                       #Number of responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_CORRECT = "num_correctresponses_sofar_class"       #Number of correct responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_MIXED = "num_mixedresponses_sofar_class"           #Number of mixed responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_INCORRECT = "num_incorrectresponses_sofar_class"   #Number of incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
SCORE = "score_sofar_class"                         #Score in current scenario so far (clustered in 6 classes) (default 0)
RESPONSE_TIME = "responsetime_prevquestion_class"                         #User response time for previous question (clustered in 6 classes) (default 0)
RESPONSE_TIME_LAST = "responsetime_prev2question_class"               #User response time for 2nd last question (clustered in 6 classes) (default 0)
RESPONSE_TIME_LAST_LAST = "responsetime_prev3question_class"     #User response time for 3rd last question (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME = "avg_responsetime_sofar_class"                       #Average user response time for all responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_CORRECT = "avg_correctresponsetime_sofar_class"      #Average user response time for correct responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_MIXED = "avg_mixedresponsetime_sofar_class"           #Average user response time for mixed responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_INCORRECT = "avg_incorrectresponsetime_sofar_class"   #Average user response time for incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
AFTER_USERRESPONSE_STATE = "after_userresponse_state"  #1 after the user has responded (before there’s potential for feedback), and 0 before the new system prompt (before there’s potential for hints)
RESP_QUALITY_AFTER_RESPONSE = "responsequality_prevquestion_class-after_userresponse_state"
FINAL_STATE = "final_state"

#State Updates
CORRECTNESS = 'Correctness'     #Correctness of the learner's response
#Quality of previous answer
MIXED = 'MIXED'                 #Mixed answer       
CORRECT = 'CORRECT'             #Correct answer
INCORRECT = 'INCORRECT'         #Incorrect answer
#Gender
FEMALE = 'Female'
MALE = 'Male'
#Unique Id
NODE_ID_CONTEXT_KEY = "dialogNodeId"        #node id to check for seen before
#Response Verbs
DO_NOTHING = 'do_nothing'                   #No hint or feedback
GIVE_HINT = 'give_hint'                     #Display hint
GIVE_FEEDBACK = 'give_feedback'             #Display feedback
GIVE_HINT_FEEDBACK = 'give_hint_feedback'   #Display feedback and hint --decided against having this
#Message verbs 
COACHING_ACTIONS = 'CoachingActions'                    #prescribe a coaching action to ELITE
REQUEST_COACHING_ACTIONS = 'RequestCoachingActions'     #ELITE requests a coaching action
REGISTER_USER_INFO = "RegisterUserInfo"                 #pass gender
VR_EXPRESS = "vrExpress"                                #chen's uuterance
#get timestamp for response
GAME_LOG = 'GameLog'                            #verb
PRACTICE_ENVIRONMENT = 'PracticeEnvironment'    #object
RANDOMIZED_CHOICES = 'RandomizedChoices'        #result

#policy actions 
DONOTHING = DO_NOTHING
FEEDBACK = GIVE_FEEDBACK
HINT = GIVE_HINT
FEEDBACK_HINT = GIVE_HINT_FEEDBACK