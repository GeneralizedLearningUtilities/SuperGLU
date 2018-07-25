import datetime
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
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

class xAPILearnLogger(BaseService):

    def __init__(self, gateway=None, userId=None, userName=None):
        self._Activity_Tree = ActivityTree()
        
        super(xAPILearnLogger, self).__init__()

        self._gateway = gateway
        self._userId = userId
        self._userName = userName
        self._url = "https://github.com/GeneralizedLearningUtilities/SuperGLU/"

    def setUserId(self,userId):
        self._userId = userId

    def setUserName(self,userName):
        self._userName = userName

    def getTimestamp(self):
        timestamp = datetime.datetime.utcnow()
        return timestamp

    # ***************** VERBS ***************************************
    def create_completed_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/complete", display=LanguageMap({'en-US': 'completed'}))

    def create_started_verb(self):
        return Verb(id =  "http://activitystrea.ms/schema/1.0/start", display=LanguageMap({'en-US': 'started'}))

    def create_terminated_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/terminate", display=LanguageMap({'en-US': 'terminated'}))

    def create_presented_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/present", display=LanguageMap({'en-US': 'presented'}))

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

    def createVideo(self):
        return Activity( id = "http://activitystrea.ms/schema/1.0/video", object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': "video"}),\
                                                         description=LanguageMap({'en-US': "Video content of any kind"})))

    # ************** STARTING AND STOPPING *********************************

    def sendStartSession(self, activityID, name, description, contextDict, timestamp = None):
        activity = self.createSession(activityID,name,description)
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')
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
        actor = Agent( object_type = 'Agent', name = self._userName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)
        
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSublesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createSublesson(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._userName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
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
        actor = Agent( object_type = 'Agent', name = self._userName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartStep(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createStep(activityID,name,description)
        actor = Agent( object_type = 'Agent', name = self._userName, openid = self._userId, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendTerminatedSession(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)
        
        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_terminated_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedLesson(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')
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
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')
        result = Result(response = '',)

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    # work in progress. currently requires custom_score_URI and custom_score but not all applications will have this.
    # If a raw_score is provided then a max_score must be provided too.
    # Might want to provide more detailed information relating to the knowledge components involved in the step.
    def sendCompletedStep(self, choice, custom_score_URI, custom_score, contextDict, raw_score=-1, max_score=-1, min_score=0, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')

        if (raw_score != -1):
            result = Result(response=choice,
                            score = Score(raw=raw_score, min=min_score, max=max_score),
                            extensions = Extensions({ custom_score_URI : custom_score}) )
        else:
            result = Result(response=choice,
                            extensions = Extensions({ custom_score_URI : custom_score}) )

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    # ***********************************************************************************

    def sendPresentedVideo(self, contextDict, timestamp=None):
        actor = Agent( object_type = 'Agent', openid = self._userId, name = self._userName, mbox='mailto:SMART-E@ict.usc.edu')

        activity = self.createVideo()
        result = Result(response = '',)

        # This is an atomic action: no start and end points. Just a start point.
        # Of course in reality, the video will have a length. We just don't have that information.

        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_presented_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    '''
    Add context to the message.  
    Currently, registration attribute is a random UUID.

    In addition to context extensions in tempExtensions,
    add serialized activity tree.

    @param tempExtensions: Dictionary of key-value items to add to the message context.
    @return: context object
    '''

    def addContext(self, tempExtensions = {}):
        
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
