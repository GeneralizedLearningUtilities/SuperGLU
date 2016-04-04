from gludb.simple import DBObject, Field, Index
from SuperGLU.Core.Messaging import Message
from datetime import datetime
"""
Module for storing the class that persists the messaging objects into the database.
"""
from SuperGLU.Util.SerializationGLUDB import DBSerializable, GLUDB_BRIDGE_NAME
from SuperGLU.Util.ErrorHandling import logInfo

LOADED_VERB = "Loaded";
ELECTRONIX_TUTOR_TASK_UPLOAD_VERB = 'ElectronixTutorTaskUpload'
HEARTBEAT_VERB = "Heartbeat"
    
COMPLETED_VERB = 'Completed'                       # Finished task, return result (e.g., score)
COMPLETED_ALL_STEPS_VERB = 'CompletedAllSteps'     # Completed all steps (true/false/% steps completed)
COMPLETED_STEP_VERB = 'CompletedStep'              # Completed a given task step
KC_SCORE_VERB = 'KnowledgeComponentScore'          # A score for a KC (e.g., performance on a given task)

# Task Adaptive Support Verbs
TASK_HELP_VERB = 'TaskHelp'                        # User received some other type of help on a task
TASK_HINT_VERB = 'TaskHint'                        # User received a hint (e.g., next step) on a task
TASK_FEEDBACK_VERB = 'TaskFeedback'                # User received reactive feedback (e.g., error correction, approval)
TASK_DECOMPOSITION_VERB = 'TaskDecomposition'      # User received a decomposed task (i.e., broken into subtasks)
    
# Task User Input Verbs
PRESENTED_VERB = 'Presented'                       # User was presented with some element
SELECTED_OPTION_VERB = 'SelectedOption'            # User selected some option or element
SUBMITTED_ANSWER_VERB = 'SubmittedAnswer'          # An answer submitted by a user
MISCONCEPTION_VERB = 'Misconception'               # User demonstrated a specific bug or misconception
TASK_SUPPORT_VERB = 'TaskSupport'                  # Overall level of support given to the user during task
TASK_HELP_COUNT_VERB = 'TaskHelpCount'             # Overall number of hints user received during the task.
 
#Peripheral Metrics Verbs - Calculated by Task
WORDS_PER_SECOND_VERB = 'WordsPerSecond'           # # Words per second, for text-input interactions (e.g., natural language ITS)
ACTIONS_PER_SECOND_VERB = 'ActionsPerSecond'       # # Actions per second (e.g., selecting choices, attempting to answer) 
ANSWER_SEMANTIC_MATCH_VERB = 'AnswerSemanticMatch' # Match of an answer for the user to some ideal(s)
PERSISTENCE_VERB = 'Persistence'                   # Metric for persistence (e.g., continuing despite failure)
IMPETUOUSNESS_VERB = 'Impetuousness'               # Metric for impetuousness (e.g., answering overly quickly, carelessness)
GAMING_SYSTEM_VERB = 'GamingTheSystem'             # Metric for gaming the system (e.g., hint abuse)
WHEELSPINNING_VERB = 'WheelSpinning'               # Metric for wheel spinning (e.g., continued failure on similar skills w/o improvement)
CONFUSION_VERB = 'Confusion'                       # Metric for confusion (e.g., moderate delays, poor answer cohesion, video metrics)
DISENGAGEMENT_VERB = 'Disengagement'               # Metric for disengagement (e.g., long delays, inattentive gaze, leaning back in chair)
MASTERY_VERB = 'Mastery'

#Context Keys
CLASS_ID_CONTEXT_KEY = 'classId'
SESSION_ID_CONTEXT_KEY = 'sessionId'
USER_ID_CONTEXT_KEY = 'userId'                             # Unique identifier for the user
DURATION_CONTEXT_KEY = 'duration'                          # Duration spent on the task, 
TASK_ID_CONTEXT_KEY = 'taskId'                             # ID for the task being performed
STEP_ID_CONTEXT_KEY = 'stepId'                             # Unique ID for the current step or state.
ACTIVITY_TYPE_CONTEXT_KEY = 'activityType'                 # Type of activity being performed
KC_RELEVANCE_CONTEXT_KEY = 'KCRelevance'                   # Knowledge component relevance
HELP_TYPE_CONTEXT_KEY = 'helpType'                         # Type of the help provided (e.g., Positive, Negative, neutral)
RESULT_CONTENT_TYPE_CONTEXT_KEY = 'resultContentType'      # Type for the content of the help or other media (e.g., 'text', 'html', 'jpg')     
    
#Other Constants
UNKNOWN_PREFIX = 'Unknown'
POSITIVE_HELP_TYPE = 'Positive'
NEUTRAL_HELP_TYPE = 'Neutral'
NEGATIVE_HELP_TYPE = 'Negative'
 

#DateTime Format
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

@DBObject(table_name="DBLoggedMessage")
class DBLoggedMessage(DBSerializable):
    actor = Field('actor')
    verb = Field('verb')
    object = Field('object')
    result = Field('result')
    speechAct = Field('speechAct')
    context = Field('context')
    timestamp = Field('timestamp')
    
    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = Message
    
    def create(self, message=None):
        if message is not None:
            self.actor     = message.getActor()
            self.verb      = message.getVerb()
            self.object    = message.getObject()
            self.result    = str(message.getResult())#DBSerializable.convert(message.getResult())
            self.speechAct = message.getSpeechAct()
            self.context   = message.getContext()
            self.timestamp = message.getTimestamp()
    
    @Index
    def actorIndex(self):
        return self.actor
        
    @Index
    def verbIndex(self):
        return self.verb
        
    @Index
    def objectIndex(self):
        return self.object
        
    @Index
    def actorVerbIndex(self):
        return (self.actor, self.verb)
        
    @Index
    def actorVerbObjIndex(self):
        return (self.actor, self.verb, self.object)
        
    @Index
    def userIdIndex(self):
        if USER_ID_CONTEXT_KEY in self.context:
            return self.context[USER_ID_CONTEXT_KEY]
        else:
            return None
    @Index
    def taskIdIndex(self):
        if TASK_ID_CONTEXT_KEY in self.context:
            return self.context[TASK_ID_CONTEXT_KEY]
        else:
            return None
    @Index
    def stepIdIndex(self):
        if STEP_ID_CONTEXT_KEY in self.context:
            return self.context[STEP_ID_CONTEXT_KEY]
        else:
            return None
    @Index
    def userTaskIndex(self):
        if USER_ID_CONTEXT_KEY in self.context and TASK_ID_CONTEXT_KEY in self.context:
            return (self.context[USER_ID_CONTEXT_KEY], self.context[TASK_ID_CONTEXT_KEY])
        else:
            return None
            
    def toMessage(self):
        return Message(self.actor, self.verb, self.object, self.result, self.speechAct, self.context, self.timestamp)
    
    def matchOnPartial(self, current, timestampOperator):
        if self.actor is not None and current.actor != self.actor:
            return False
        
        if self.verb is not None and current.verb != self.verb:
            return False
            
        if self.object is not None and current.object != self.object:
            return False
            
        if self.speechAct is not None and current.speechAct != current.speechAct:
            return False
        
        if self.result is not None and current.result != self.result:
            return False
        
        if self.context is not None:
            if current.context is None:
                return False
            
            #Note: I am assuming that the context is a dictionary if that isn't true then I'll need to add a type check and handle all possible types 
            for filterContextKey in self.context.keys():
                if filterContextKey not in current.context.keys():
                    return False;
                
                currentValue = current.context[filterContextKey]
                filterValue = self.context[filterContextKey]
                if filterValue is not None:
                    if isinstance(currentValue, list) and filterValue not in currentValue:
                        return False
                
                    if currentValue != filterValue:
                        return False
        
        
        if self.timestamp is not None and current.timestamp != "timestamp":
            parsedTimestamp = datetime.strptime(current.timestamp, DATE_TIME_FORMAT)
            parsedFilterTimestamp = datetime.strptime(self.timestamp, DATE_TIME_FORMAT)
            
            if timestampOperator == "<" and parsedTimestamp < parsedFilterTimestamp:
                #print(current.timestamp + " < " + self.timestamp)
                return False;
            if timestampOperator == ">" and parsedFilterTimestamp < parsedTimestamp:
                return False;
            if timestampOperator == "==" and parsedFilterTimestamp != parsedTimestamp:
                return False;
        
        return True
        
        
    def __repr__(self):
        return self.actor + "|" + self.verb + "|" + self.object + "|" + self.result.__repr__() + "|" + self.speechAct + "|" + self.context.__repr__() + "|" +self.timestamp + "\n"