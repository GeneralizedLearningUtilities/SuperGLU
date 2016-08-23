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
NUMBER_OF_RESPONSE_PREV = "number_of_response_prev"         #Number of responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_CORRECT_PREV = "number_of_correct_prev"           #Number of correct responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_MIXED_PREV = "number_of_mixed_prev"               #Number of mixed responses in previous scenario (clustered in 6 classes) (default 0)
NUMBER_OF_INCORRECT_PREV = "number_of_incorrect_prev"       #Number of incorrect responses in previous scenario (clustered in 6 classes) (default 0)
SCORE_PREV = "score_prev"                                   #Score in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_PREV = "avg_response_time_prev"           #Average user response time for all responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_CORRECT_PREV = "avg_response_time_correct_prev"       #Average user response time for correct responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_MIXED_PREV = "avg_response_time_mixed_prev"           #Average user response time for mixed responses in previous scenario (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_INCORRECT_PREV = "avg_response_time_incorrect_prev"   #Average user response time for incorrect responses in previous scenario (clustered in 6 classes) (default 0)
SEEN_BEFORE = "seen_before"                     #Has the system question appeared in the previous scenario? (0(no)/1(yes)) (default 0)
QUALITY_PREV_IF_SEEN = "quality_prev_if_Seen"   #Quality of response in the previous scenario if the same question has appeared (0(null)/1(Incorrect)/2(Mixed)/3(Correct)) (default 0)
QUALITY_ANSWER = "quality_of_answer"                  #correctness of the previous answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
QUALITY_ANSWER_LAST = "quality_of_answer_last"        #correctness of the 2nd last answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
QUALITY_ANSWER_LAST_LAST = "quality_of_answer_last_last"        #correctness of the 3rd last answer 0(null)/1(Incorrect)/2(Mixed)/3(Correct) (default 0)
NUMBER_OF_RESPONSE = "number_of_response"                       #Number of responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_CORRECT = "number_of_correct"       #Number of correct responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_MIXED = "number_of_mixed"           #Number of mixed responses in current scenario so far (clustered in 6 classes) (default 0)
NUMBER_OF_INCORRECT = "number_of_incorrect"   #Number of incorrect responses in current scenario so far (clustered in 6 classes) (default 0)
SCORE = "score"                         #Score in current scenario so far (clustered in 6 classes) (default 0)
RESPONSE_TIME = "response_time"                         #User response time for previous question (clustered in 6 classes) (default 0)
RESPONSE_TIME_LAST = "response_time_last"               #User response time for 2nd last question (clustered in 6 classes) (default 0)
RESPONSE_TIME_LAST_LAST = "response_time_last_last"     #User response time for 3rd last question (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME = "avg_response_time"                       #Average user response time for all responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_CORRECT = "avg_response_time_correct"      #Average user response time for correct responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_MIXED = "avg_response_time_mixed"           #Average user response time for mixed responses in current scenario so far (clustered in 6 classes) (default 0)
AVG_RESPONSE_TIME_INCORRECT = "avg_response_time_incorrect"   #Average user response time for incorrect responses in current scenario so far (clustered in 6 classes) (default 0)

#State Updates
CORRECTNESS = 'Correctness'     #Correctness of the learner's response
#Quality of previous answer
MIXED = 'Mixed'                 #Mixed answer       
CORRECT = 'Correct'             #Correct answer
INCORRECT = 'Incorrect'         #Incorrect answer
#Gender
FEMALE = 'Female'
MALE = 'Male'
#Response Verbs
DO_NOTHING = 'do_nothing'                   #No hint or feedback
GIVE_HINT = 'give_hint'                     #Display hint
GIVE_FEEDBACK = 'give_feedback'             #Display feedback
GIVE_HINT_FEEDBACK = 'give_hint_feedback'   #Display feedback and hint
#Message verbs 
COACHING_ACTIONS = 'CoachingActions'                    #prescribe a coaching action to ELITE
REQUEST_COACHING_ACTIONS = 'RequestCoachingActions'     #ELITE requests a coaching action
REGISTER_USER_INFO = "RegisterUserInfo"                 #pass gender
VR_EXPRESS = "vrExpress"                                #chen's uuterance
#get timestamp for response
GAME_LOG = 'GameLog'                            #verb
PRACTICE_ENVIRONMENT = 'PracticeEnvironment'    #object
RANDOMIZED_CHOICES = 'RandomizedChoices'        #result