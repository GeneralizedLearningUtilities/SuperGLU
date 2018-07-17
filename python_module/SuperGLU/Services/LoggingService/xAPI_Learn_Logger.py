from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Base_Learn_Logger import BaseLearnLogger
from SuperGLU.Services.LoggingService.Constants import *
import json
import time
from tincan import (
    Statement,
    Agent,
    Verb,
    Result,
    Activity,
    ActivityList,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
    Extensions,
    AgentAccount
)
import uuid
from context_activities import ContextActivities
import context_activities
from tincan.typed_list import TypedList
from representation.ActivityTree import ActivityTree
from SuperGLU.Util.Serialization import makeSerialized

class xAPILearnLogger(BaseLearnLogger):

    URIBase = "https://github.com/GeneralizedLearningUtilities/SuperGLU/"

    def __init__(self, gateway=None, userId=None, name=None, classroomId=None, taskId=None, url=None, activityType='', context={}, anId=None):
        self._Activity_Tree = ActivityTree()
        
        #Initializing count variables to count the decisions, choices, AARs etc..
        self._SessionCount = 0
        self._VideoLessonCount = 0
        self._VideoSublessonCount = 0
        self._ScenarioCount = 0
        self._DialogueCount = 0
        self._DecisionCount = 0
        self._ChoiceCount = 0
        self._AARCount = 0
        self._VideoAARCount= 0
        self._QuestionCount = 0
        self._AnswerCount = 0
        self._HintCount = 0
        
        super(xAPILearnLogger, self).__init__(gateway, userId, name, classroomId, taskId, url, activityType, context, anId)
        self._keyObjectExtensions = self.URIBase + "object/extensions/"

    def create_completed_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/complete", display=LanguageMap({'en-US': 'completed'}))

    def create_started_verb(self):
        return Verb(id =  "http://activitystrea.ms/schema/1.0/start", display=LanguageMap({'en-US': 'started'}))

    def create_terminated_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/terminate", display=LanguageMap({'en-US': 'terminated'}))

    def createSession(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://id.tincanapi.com/activitytype/tutor-session"))

    def createLesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://adlnet.gov/expapi/activities/lesson"))

    def createSublesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= self._url + "sublesson"))

    def createTask(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://activitystrea.ms/schema/1.0/task"))

    # there is http://id.tincanapi.com/activitytype/step but this is the general sense of the word
    def createStep(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://id.tincanapi.com/activitytype/step"))


       
    '''Send the loaded message, for when the task is ready to start.
        Message Data: <frameName> | Loaded | <url> | true
        @param frameName: The name for the current window
        @type frameName: string
    '''

    def sendStartSession(self, activity, timestamp = None):
        Subtype = "Session"
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = 'User started a new Session',)
        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(activity = activity, label = None)

        context = self.addContext(Subtype=Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartTopic(self, timestamp = None):
        Objecttype = "Topic"
        Subtype = "Topic"        
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Topic'}), description=LanguageMap({'en-US':'User Started a new Topic'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + AppStart, display=LanguageMap({'en-US': 'started'}))
        result = Result(response = 'User started a new Topic',)
        
        #self._Activity_Tree.EnterActivity(label = "Topic", activity = "User started a new Topic", parentLabel="Session")
        parentLabel = "Session"
        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = "Topic", activity = "Topic")
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)
                
        context = self.addContext(parentLabel, Subtype, ContextActivityTree= jsonDictActivityTree)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartLesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Lesson'}),
            description=LanguageMap({'en-US':'User Started Lesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        
        parentLabel = "Session"        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = "Lesson", activity = "Lesson")
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)
                
        context = self.addContext(parentLabel, ContextActivityTree= jsonDictActivityTree)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSublesson(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Sublesson'}),
            description=LanguageMap({'en-US':'User Started Sublesson'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        
        #self._Activity_Tree.EnterActivity(label = "Sublesson", activity = "User started a new Sublesson", parentLabel= "Lesson")        
        parentLabel = "Lesson"
        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = "Sublesson", activity = "Sublesson")
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)
                
        context = self.addContext(parentLabel, ContextActivityTree= jsonDictActivityTree)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendNewTask(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Task'}),
            description=LanguageMap({'en-US':'User Started new Task'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
       
        parentLabel = "Sublesson"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = "Task", activity = "Task")
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)
                
        context = self.addContext(parentLabel, ContextActivityTree= jsonDictActivityTree)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendNewStep(self, timestamp=None):

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': 'Step'}),
            description=LanguageMap({'en-US':'User Started new Step'})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        parentLabel = "Task"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = "Step", activity = "Step")
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)
                
        context = self.addContext(parentLabel, ContextActivityTree= jsonDictActivityTree)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendStartVideoLesson(self, activity, timestamp=None):
        self._VideoLessonCount += 1
        Objecttype = "lesson" 
        Subtype = "VideoLesson" + str(self._VideoLessonCount)

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Session"
        
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartVideoSublesson(self, activity, timestamp=None):
        self._VideoSublessonCount += 1
        Objecttype = "lesson"
        Subtype = "VideoSublesson"+ str(self._VideoSublessonCount)     

        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Video Lesson"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartScenario(self, activity, timestamp=None):
        self._ScenarioCount += 1
        Objecttype = "Lesson"
        Subtype = "Scenario" + str(self._ScenarioCount)
        parentLabel = "Session"        
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        
        #self._Activity_Tree.EnterActivity(label = "Scenario", activity = "User started a new Scenario", parentLabel= "Session")

        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartDialogue(self, activity, timestamp=None):
        self._DialogueCount += 1
        Objecttype = "Sublesson"
        Subtype = "Dialogue" + str(self._DialogueCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Scenario"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartDecision(self, activity, timestamp=None):
        self._DecisionCount += 1
        Objecttype = "Task"
        Subtype = "Decision" + str(self._DecisionCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Dialogue"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartChoice(self, activity, timestamp=None):
        self._ChoiceCount += 1
        Objecttype = "Step"
        Subtype = "Choice" + str(self._ChoiceCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Decision"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartAAR(self, activity, timestamp=None):
        self._AARCount += 1
        Objecttype = "Sublesson"
        Subtype = "AAR" + str(self._AARCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Scenario"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartQuestion(self, activity, timestamp=None):
        self._QuestionCount += 1
        Objecttype = "Task"
        Subtype = "Question" + str(self._QuestionCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "AAR"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartAnswer(self, activity, timestamp=None):
        self._AnswerCount += 1
        Objecttype = "Step"
        Subtype = "Answer" + str(self._AnswerCount)
        
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        parentLabel = "Question"
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendLoadedTask(self, frameName, sysComp = '', description='', timestamp=None):
        self._VideoAARCount += 1
        Objecttype = "Lesson"
        Subtype = "Video/AAR" + str(self._VideoAARcount)
        parentLabel = "Session"
                
        actor = Agent( object_type = 'Agent', name = frameName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url,
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}),
            description=LanguageMap({'en-US':description})
                ),
            )
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + LOADED_VERB, display=LanguageMap({'en-US': LOADED_VERB}))
        result = Result(success = True,)
        #self._Activity_Tree.EnterActivity(label = "Video Lesson", activity = "User started Video", parentLabel="Session")

        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = Objecttype, activity = Subtype)
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)         
        jsonDictCurrentPath = json.loads(ActivityTreeSerialized)['ActivityTree']['currentPath']    
              
        context = self.addContext(parentLabel, Subtype, ContextActivityTree= jsonDictActivityTree, ContextCurrentPath = jsonDictCurrentPath)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)



    '''
    Send the task completed message
        Message Data: <userId> | Completed | <taskId> | <score>
        @param score: A score between 0 and 1. Scores outside this range will be clipped to fit. If score None, task presumed incomplete/invalid.
        @type score: float
    '''
    def sendTerminatedSession(self, activity, timestamp=None):
        Objecttype = "Session"
        Subtype = "Session" + str(self._SessionCount)
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + Exiting, display=LanguageMap({'en-US': Exiting}))
        result = Result(response = '',)
        
        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedLesson(self, timestamp=None):
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = Objecttype, definition = ActivityDefinition(name=LanguageMap({'en-US': 'Lesson'}), description=LanguageMap({'en-US':'User Completed Lesson'})))
        result = Result(response = '',)

        parentLabel = "Session"
        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_terminated_verb(), object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedSublesson(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = Objecttype, definition = ActivityDefinition(name=LanguageMap({'en-US': 'Sublesson'}), description=LanguageMap({'en-US':'User Completed Sublesson'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        parentLabel = "Lesson"
        
        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
        jsonActivityTree = self._Activity_Tree.saveToToken()
        ActivityTreeSerialized = makeSerialized(jsonActivityTree)
        jsonDictActivityTree = json.loads(ActivityTreeSerialized)   
        jsonDictCurrentPath = json.loads(ActivityTreeSerialized)['ActivityTree']['currentPath']    
              
        context = self.addContext(parentLabel, Subtype, ContextActivityTree= jsonDictActivityTree, ContextCurrentPath = jsonDictCurrentPath)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedVideoLesson(self, activity, timestamp=None):
        Objecttype = "Lesson"
        Subtype = "VideoLesson" + str(self._VideoLessonCount)
        parentLabel = "Session"        
                
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedVideoSublesson(self, activity, timestamp=None):
        Objecttype = "Sublesson"
        Subtype = "VideoSublesson" + str(self._VideoSublessonCount)
        parentLabel = "Video Lesson"
                        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedScenario(self, activity, timestamp=None):
        Objecttype = "lesson"
        Subtype = "Scenario" + str(self._ScenarioCount)
        parentLabel = "Video Lesson"
                        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        parentLabel = "Session"
        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedDialogue(self, activity, timestamp=None):
        Objecttype = "Sublesson"
        Subtype = "Dialogue" + str(self._DialogueCount)      
        parentLabel = "Scenario"
                
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedDecision(self, activity, timestamp=None):
        Objecttype = "Task"
        Subtype = "Decision" + str(self._DecisionCount)
        parentLabel = "Dialogue"
                        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedChoice(self, activity, timestamp=None):
        Objecttype = "Step"
        Subtype = "Choice" + str(self._ChoiceCount)
        parentLabel = "Decision"
                
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedAAR(self, activity, timestamp=None):
        Objecttype = "Sublesson"
        Subtype = "AAR" + str(self._AARCount)
        parentLabel = "Scenario"
                        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedQuestion(self, activity, timestamp=None):
        Objecttype = "Task"
        Subtype = "Question" + str(self._QuestionCount)       
        parentLabel = "AAR"
                
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendCompletedAnswer(self, activity, timestamp=None):
        Objecttype = "Step"
        Subtype = "Answer" + str(self._AnswerCount)     
        parentLabel = "Question"
                
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(parentLabel, Subtype)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTheTask(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Task'}), description=LanguageMap({'en-US':'User Completed Task'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)   
              
        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self, score, sysComp = '', description='', timestamp=None):     
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()),
            object_type = 'Activity',
            definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}),
            description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(score = self.clampToUnitValue(score),) 
              
        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send if all steps completed message (or % complete, if unfinished)
        Message Data: <userId> | CompletedAllSteps | <taskId> | <percentComplete>
        @param percentComplete: The percentage of steps that were completed. In [0,1]. If None, assumed 100%.
        @param percentComplete: float
    '''
    def sendCompletedAllSteps(self, percentComplete, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_ALL_STEPS_VERB , display=LanguageMap({'en-US': COMPLETED_ALL_STEPS_VERB}))

        if percentComplete == None:
            percentComplete = 1.0
        percentComplete = self.clampToUnitValue(percentComplete)
        result = Result(score = percentComplete*1.0,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send a message that a step was completed (or marked incomplete, alternatively).
        Message Data: <userId> | CompletedStep | <stepId> | <percentComplete>
        @param stepId: An id that represents the task situation (e.g., decision point) that the user completed or failed to complete. Uniquely represents some decision point in the current task.
        @type stepId: string
        @param isComplete: The amount of the step that was completed, from 0 (nothing completed) to 1 (fully complete).
        @type isComplete: float
    '''

    def sendCompletedTheStep(self, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url + str(uuid.uuid4()), object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': 'Step'}), description=LanguageMap({'en-US':'User Completed Step'})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_VERB, display=LanguageMap({'en-US': COMPLETED_VERB}))
        result = Result(response = '',)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)



    def sendCompletedStep(self, stepId, isComplete, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = stepId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + COMPLETED_STEP_VERB, display=LanguageMap({'en-US': COMPLETED_STEP_VERB}))

        if isComplete == None:
            isComplete = 1.0
        isComplete = self.clampToUnitValue(isComplete);
        result = Result(score = isComplete*1.0,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendTerminatedMessage(self, anId, response, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + Exiting, display=LanguageMap({'en-US': Exiting}))
        result = Result(response = response,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendStartMessage(self, anId, response, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + AppStart, display=LanguageMap({'en-US': AppStart}))
        result = Result(response = response,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendResponse(self, anId, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + SendResponse, display=LanguageMap({'en-US': SendResponse}))
        result = Result(score = score,)
        
        #self._Activity_Tree.EnterActivity(label = "Decision", activity = "User started a new Decision", parentLabel="Session")

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendSelectedItem(self, anId, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + ClickedItem, display=LanguageMap({'en-US': ClickedItem}))
        result = Result(score = score,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendLog(self, anId, verb, score, sysComp = '', description='', timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = anId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(score = score,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send a KC Score about performance on a specific skill during the activity.
        KC scores override any default KC scores inferred from a task's Completed message
        (e.g., which might be assumed that KC's used to recommend the task are also those that
        are assessed by that same task).  Relevance is intended to be used to determine the level
        of confidence for each assessment, and can be left undefined if all scores have high confidence
        and all KC's used to select a task have been assessed by that task.
        Message Data: <userId> | KCScore | <kcName> | <score>
        @param kcName: The name of the knowledge component that was assessed during this task.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param relevance: The credit or confidence of your assessment of that KC, from 0 (irrelevant) to 1 (strong confidence in this assessment).  Relevance of 0 should be used if a KC that is associated with choosing this task was not encountered during the task. Typically, relevance can be left undefined, which will default to 1.
        @type relevance: float
    '''

    def sendKCScore(self, kcName, score, relevance, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = kcName, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + KC_SCORE_VERB, display=LanguageMap({'en-US': KC_SCORE_VERB}))

        if relevance == None:
            relevance = 1.0
        relevance = self.clampToUnitValue(relevance)
        score = self.clampToUnitValue(score)

        result = Result(score = score,)

        tempContext = {}
        tempContext[KC_RELEVANCE_KEY] = relevance

        context = self.addContext(tempContext)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)

        self.sendLoggingMessage(statement);

    '''
    Send a Mastery score, which is a claim by a system about a user's overall knowledge
        about a knowledge component. This score is expected to be based on all evidence available
        to the system at the time when the KC mastery was calculated.
        Message Data: <userId> | Mastery | <kcName> | <score>
        @param kcName: The name of the knowledge component whose mastery level was estimated.
        @type kcName: string
        @param score: The score the system gave for this KC, from 0 to 1.
        @type score: float
        @param numObservations: A weighted sum for the number of observations that supports this estimate. Some observations might be worth less than one (e.g., because the context was only partly relevant), while other observations might be worth more than one (e.g., because they were received from systems which reported a large number of observations).
        @type numObservations: float
    '''
    def sendMastery(self, kcName, score, numObservations, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = kcName, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + MASTERED_VERB, display=LanguageMap({'en-US': MASTERED_VERB}))

        score = self.clampToUnitValue(score)

        result = Result(score = score,)

        tempContext = {}
        if numObservations != None and numObservations > 0:
            tempContext[NUM_OBSERVATIONS_KEY] = numObservations

        context = self.addContext(tempContext)

        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)

        self.sendLoggingMessage(statement);


    '''
    Notify that a hint was presented
        Message Data: <taskId> | TaskHint | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHint(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(ProcessCoachHint, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that feedback was presented
        Message Data: <taskId> | TaskFeedback | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the feedback.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendFeedback(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(ProcessCoachFeedback, content, stepId, helpType, contentType, sysComp, description, timestamp)

    #Notify that positive feedback was presented
    def sendPositiveFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, POSITIVE_HELP_TYPE, contentType, sysComp, description, timestamp)

    #Notify that neutral feedback was presented
    def sendNeutralFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, NEUTRAL_HELP_TYPE, contentType, sysComp, description, timestamp)

    #Notify that negative feedback was presented
    def sendNegativeFeedback(self, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self.sendFeedback(content, stepId, NEGATIVE_HELP_TYPE, contentType, sysComp, description, timestamp)

    '''
    Notify that task was decomposed
        Message Data: <taskId> | TaskDecomposition | <stepId> | <content>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner decomposed the task.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''

    def sendTaskDecomposed(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(TASK_DECOMPOSITION_VERB, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that some other help was presented. In general, this should be used
        only when more specific verbs such as Feedback or Hint are not appropriate.
        Message Data: <userId> | TaskHelp | <stepId> | <score>
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, negative feedback, etc.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendHelp(self, content, stepId, helpType, contentType, sysComp = '', description='', timestamp=None):
        self._sendHelpMessage(TASK_HELP_VERB, content, stepId, helpType, contentType, sysComp, description, timestamp)

    '''
    Notify that task presented some content. This can be at any time that
        new content was presented (e.g., moving to a new panel, etc.).
        Message Data: <taskId> | Presented | <elementId> | <content>
        @param elementId: The HTML element where the content was displayed (if relevant)
        @type elementId: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the help.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendPresented(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + PRESENTED_VERB, display=LanguageMap({'en-US': PRESENTED_VERB}))

        if contentType == None and content != None:
            contentType = 'text'
            content = str(content)

        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType
        
        context = self.addContext()

        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Notify that user selected some element (e.g., in terms of HTML: making active)
        This should be used when the user has selected a choice or option, but has not
        necessarily submitted it (e.g., picking a dropdown but before hitting "Submit",
        or writing a text answer before submitting it or clearing it).
        Message Data: <userId> | SelectedOption | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSelectedOption(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self._sendInputMessage(SELECTED_OPTION_VERB, elementId, content, stepId, contentType, sysComp, description, timestamp)

    '''
    Notify that user submitted an answer or choice.
        Message Data: <userId> | SubmittedAnswer | <elementId> | <content>
        @param elementId: The HTML element where the option was selected or provided.
        @type elementId: string
        @param content: The content of the submission or choice locked in (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner submitted the value.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def sendSubmittedAnswer(self, elementId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
        self._sendInputMessage(SUBMITTED_ANSWER_VERB, elementId, content, stepId, contentType, sysComp, description, timestamp)

        '''
        Notify that user demonstrated a misconception.
            This requires the misconception ID, rather than the element.
            Message Data: <userId> | SubmittedAnswer | <misconceptionId> | <content>
            @param misconceptionId: An id that uniquely identifies this misconception across a variety of problems.
            @type misconceptionId: string
            @param content: The content of the submission or choice locked in (e.g., the option or value)
            @type: string
            @param stepId: An id that represents the task situation (e.g., decision point) where the learner's misconception was shown. Optional.
            @type stepId: string
            @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
            @type contentType: string
        '''
        def sendMisconception(self, misconceptionId, content, stepId, contentType, sysComp = '', description='', timestamp=None):
            self._sendInputMessage(MISCONCEPTION_VERB, misconceptionId, content, stepId, contentType, sysComp, description, timestamp)

    '''Send the overall level of system support given to the user for this task.
        This is the system's assessment of the level of support that was provided.
        Message Data: <userId> | TaskSupport | <taskId> | <supportLevel>
        @param supportLevel: Fraction of the total support given to the user during the task, in [0,1].
        @type supportLevel: float
    '''
    def sendTaskSupport(self, supportLevel, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + TASK_SUPPORT_VERB, display=LanguageMap({'en-US': TASK_SUPPORT_VERB}))

        supportLevel = self.clampToUnitValue(supportLevel)
        result = Result(score=supportLevel,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send the overall number of help acts given. To be used when individual hints cannot be logged, but the aggregate can be.
        No need to use this if help actions can be logged individually.
        Message Data: <userId> | TaskHelpCount | <taskId> | <numHelpActs>
        @param numHelpActs: The total number of help acts provided during the task.
        @type numHelpActs: int
    '''
    def sendTaskHelpCount(self, numHelpActs, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = self._url+self._taskId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + TASK_HELP_COUNT_VERB, display=LanguageMap({'en-US': TASK_HELP_COUNT_VERB}))

        if numHelpActs < 0:
            numHelpActs = 0

        result = Result(score=numHelpActs,)

        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Send the words per second when user was expected to enter content
        Message Data: <userId>, WordsPerSecond, <evidence>, <value>
        @param value: The number of words per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'text' : '...', 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the text input given to this task.
        @type stepId: string
    '''
    def sendWordsPerSecond(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
            if value < 0:
                value = 0
            self._sendMetricMessage(WORDS_PER_SECOND_VERB, value, evidence, stepId, False, sysComp, description, timestamp)

    '''
    Send the actions per second when user was expected to interact with the system
        Message Data: <userId>, ActionsPerSecond, <evidence>, <value>
        @param value: The number of actions per second, during times when input was expected.
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'actions' : ['a1', 'a2'], 'duration' : '5.4'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendActionsPerSecond(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
            if value < 0:
                value = 0
            self._sendMetricMessage(ACTIONS_PER_SECOND_VERB, value, evidence, stepId, False, sysComp, description, timestamp)

    '''
    Send the semantic match for content submitted. Can be either for a single step (if stepId given)
        or for the whole task (if no stepId given).
        Message Data: <userId>, AnswerSemanticMatch, <evidence>, <value>
        @param value: The semantic match score, in [0,1]
        @type value: float
        @param evidence: Raw data used to infer this value, such as a list of [{'match' : 0.6, 'ideal' : 'pen', 'answer' : 'pencil'}, ...]. Stored archivally, to allow recalculating differently, if needed.
        @type evidence: any JSON-serializable or Serialization.Serializable object
        @param stepId: An id that represents the task situation (e.g., decision point) where this evidence was collected. Optional.  If not given, this message should represent all the actions given to this task.
        @type stepId: string
    '''
    def sendAnswerSemanticMatch(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(ANSWER_SEMANTIC_MATCH_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendPersistence(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(PERSISTENCE_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendImpetuousness(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(IMPETUOUSNESS_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendGamingTheSystem(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(GAMING_SYSTEM_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendConfusion(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(CONFUSION_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendDisengagement(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(DISENGAGEMENT_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    def sendWheelspinning(self, value, evidence, stepId, sysComp = '', description='', timestamp=None):
        self._sendMetricMessage(WHEELSPINNING_VERB, value, evidence, stepId, True, sysComp, description, timestamp)

    #ToDo
    def sendRequestRecommendedTasks(self, userName, numberOfRecommendations, sysComp = '', description='', timestamp=None):

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = numberOfRecommendations, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + RECOMMENDED_TASKS_VERB, display=LanguageMap({'en-US': RECOMMENDED_TASKS_VERB}))

        statement = Message(actor, verb, anObject, "", "Request")
        self.sendLoggingMessage(statement)


    '''
    Internal function to notify server that user submitted input
        @param verb: The verb to use for the user input message
        @type verb: string
        @param elementId: The HTML element where the user performed the interaction.
        @type elementId: string
        @param content: The content of the selection chosen (e.g., the option or value)
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner selected the option. Optional.
        @type stepId: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML).
        @type contentType: string
    '''
    def _sendInputMessage(self, verb, elementId, content, stepId, contentType, sysComp, description, timestamp):     
        
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = elementId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))

        if contentType == None and content != None:
            contentType = 'text'
            content = str(content)

        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType
              
        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    '''
    Internal Function to notify server that some help message was presented
        @param verb: The verb to use for the help log message
        @type verb: string
        @param content: The content of the help given, such as text, raw HTML, a URL, an image link, or other data.
        @type: string
        @param stepId: An id that represents the task situation (e.g., decision point) where the learner received the hint. Optional.
        @type stepId: string
        @param helpType: The pedagogical intent of help that was given, such as positive feedback, a prompt, etc. Optional.
        @type helpType: string
        @param contentType: The type of content that was presented (e.g., text, image, video, HTML). Defaults to text.
        @type contentType: string
    '''
    def _sendHelpMessage(self, verb, content, stepId, helpType, contentType, sysComp, description, timestamp):
        self._HintCount += 1
        
        if (contentType == None) and content != None:
            contentType = 'text'
            content = str(content)
        if helpType == None:
            helpType = NEUTRAL_HELP_TYPE

        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        anObject = Activity( id = stepId, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(response=content,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        tempContext[HELP_TYPE_KEY] = helpType
        tempContext[RESULT_CONTENT_TYPE_KEY] = contentType     
        
        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Internal function for sending metric values
        @param verb: The verb to use for the metric message
        @type verb: string
        @param value: Value of the metric to send.
        @type value: numeric
        @param stepId: The stepId that the metric applies to. If None, applies to the task overall.
        @type stepId: string
        @param clampToUnit: If true, adjust value to fit between 0 and 1. Null values are not changed.
        @type clampToUnit: bool
    '''
    def _sendMetricMessage(self, verb, value, evidence,  stepId, clampToUnit, sysComp, description, timestamp):
        
        if evidence == None:
            evidence = []
        if clampToUnit:
            value = self.clampToUnitValue(value)

        actor = Agent( object_type = 'Agent', openid = self ._userId)
        anObject = Activity( id = evidence, object_type = 'Activity', definition = ActivityDefinition(name=LanguageMap({'en-US': sysComp}), description=LanguageMap({'en-US':description})))
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + verb, display=LanguageMap({'en-US': verb}))
        result = Result(response=value,)

        tempContext = {}
        tempContext[STEP_ID_KEY] = stepId
        
        context = self.addContext()
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=anObject, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    '''
    Add context to the message.  This adds the userId, taskId, classroomId,
        activityType, and duration so far. It also adds any service context items,
        followed by the parameter context. Context within the context parameter does
        not override any existing message context.
        @param msg: The original message to modify by adding context data.
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
        @return: Modified message in msg
        @rtype: Messaging.Message
    '''

    def addContext(self, parentLabel  = "Session", Subtype = "Session"):
        
        #defining context dictionary
        tempExtensions = {}
        #tempExtensions[USER_ID_KEY] = self._userId
        #tempExtensions[TASK_ID_KEY] = self._taskId
        #tempExtensions[CLASSROOM_ID_KEY] = self._classroomId
        tempExtensions[self._url + ACTIVITY_TYPE_KEY] = Subtype
        #        tempExtensions[DURATION_KEY] = self.calcDuration()
        tempExtensions[self._url + ACTIVITY_TREE_KEY] = self._Activity_Tree.saveXAPItoJSON()
                                        
        #Used as an instructor agent in context
        agentAccount = AgentAccount(name = "dummyName", home_page="http://dummyHomepage.com")

        mygrouping = self._Activity_Tree.convertPathToGrouping()
        myparent = self._Activity_Tree.findParentActivity()

        #Defining a TinCan Context object
        if len(mygrouping)==0 and myparent == None:
            context = Context(
                registration=str(uuid.uuid4()),
                instructor=Agent(
                    account=agentAccount
                ), 
                extensions = Extensions(tempExtensions))
        else:
            if len(mygrouping)==0:
                mycontextActivities = ContextActivities(parent = myparent)
            else:
                mycontextActivities = ContextActivities(parent = myparent, 
                                                        grouping = ActivityList(mygrouping))
            context = Context(
                registration=str(uuid.uuid4()),
                instructor=Agent(
                    account=agentAccount
                ), 
                extensions = Extensions(tempExtensions),
                context_activities = mycontextActivities
            )        

        return context

    '''
    Finalize any post-processing of the message and then send it
        @param msg: Message to send
        @type msg: Messaging.Message
        @param context: Dictionary of key-value items to add to the message context. Not used if keys already exist.
        @type context: object
    '''
    # send message to json file (to-do: connecting to learn locker)
    def sendLoggingMessage(self, statement):
        message = Message(actor="logger", verb=XAPI_LOG_VERB, obj=None, result=statement.to_json())
        self.sendMessage(message)

    # values to fit within a [0,1] range
    def clampToUnitValue(self, val):
        if val != None:
            return min(max(val, 0.0), 1.0)
        return val
