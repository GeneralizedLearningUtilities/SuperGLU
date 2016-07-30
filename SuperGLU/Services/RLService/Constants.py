'''
Created on Jun 6, 2016

@author: skarumbaiah
'''
# -*- coding: utf-8 -*-
# State variables to define a tutoring system's status
TUTOR_STATE_QUALITY_PREV_ANSWER = "qual_prev_answer"        #correctness of the previous answer
TUTOR_STATE_STUDENT_AVG_PERFORMANCE = "student_quality"     #average of all answers

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
#State Updates
CORRECTNESS = 'Correctness'     #Correctness of the learner's response
#Quality of previous answer
MIXED = 'mixed'                 #Mixed answer       
CORRECT = 'correct'             #Correct answer
INCORRECT = 'incorrect'         #Incorrect answer
#Student levels
GOOD = 'good'                   
AVERGAE = 'average'
POOR = 'poor'
#Response Verbs
DO_NOTHING = 'do_nothing'                   #No hint or feedback
GIVE_HINT = 'give_hint'                     #Display hint
GIVE_FEEDBACK = 'give_feedback'             #Display feedback
GIVE_HINT_FEEDBACK = 'give_hint_feedback'   #Display feedback and hint
#Message verbs 
COACHING_ACTIONS = 'coaching_actions'                   #prescribe a coaching action to ELITE
REQUEST_COACHING_ACTIONS = 'request_coaching_actions'   #ELITE requests a coaching action