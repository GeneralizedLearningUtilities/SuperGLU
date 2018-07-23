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
    AgentAccount,
    Score,
    TypedList,
    ContextActivities
)
import uuid
from representation.ActivityTree import ActivityTree
from SuperGLU.Util.Serialization import makeSerialized

class xAPILearnLogger(BaseLearnLogger):

    URIBase = "https://github.com/GeneralizedLearningUtilities/SuperGLU/"

    def __init__(self, gateway=None, userId=None, name=None, classroomId=None, taskId=None, url=None, activityType='', context={}, anId=None):
        self._Activity_Tree = ActivityTree()
        
        super(xAPILearnLogger, self).__init__(gateway, userId, name, classroomId, taskId, url, activityType, context, anId)
        self._keyObjectExtensions = self.URIBase + "object/extensions/"

        self._HintCount = 0

    # ***************** VERBS ***************************************
    def create_completed_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/complete", display=LanguageMap({'en-US': 'completed'}))

    def create_started_verb(self):
        return Verb(id =  "http://activitystrea.ms/schema/1.0/start", display=LanguageMap({'en-US': 'started'}))

    def create_terminated_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/terminate", display=LanguageMap({'en-US': 'terminated'}))

    # ************** ACTIVITIES *************************************
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

    def createStep(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://id.tincanapi.com/activitytype/step"))

    # ************** STARTING AND STOPPING *********************************

    def sendStartSession(self, activityID, name, description, contextDict, timestamp = None):
        activity = self.createSession(activityID,name,description)
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = 'User started a new Session',)
        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(activity = activity, label = None)

        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartLesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createLesson(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSublesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createSublesson(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)

        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartTask(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createTask(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartStep(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createStep(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._name, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendTerminatedSession(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        verb = Verb(id =  self.URIBase + "xAPI/verb/" + Exiting, display=LanguageMap({'en-US': Exiting}))
        result = Result(response = '',)
        
        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=verb, object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedLesson(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedSublesson(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedStep(self, choice, raw_score, max_score, custom_score_URI, custom_score, contextDict, min_score=0, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response=choice,
                        score = Score(raw=raw_score, min=min_score, max=max_score),
                        extensions = Extensions({ custom_score_URI : custom_score}) )

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    # TO DO: merge into sendCompletedStep
    def sendCompletedAnswer(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._name, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    # ***********************************************************************************


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

    def addContext(self, tempExtensions = {}):
        
        #adding to context dictionary
        #tempExtensions[USER_ID_KEY] = self._userId
        #tempExtensions[TASK_ID_KEY] = self._taskId
        #tempExtensions[CLASSROOM_ID_KEY] = self._classroomId
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
