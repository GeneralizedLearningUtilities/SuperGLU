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

    # if mbox_host != None
    #  learner agent
    #    mbox = userName@mbox_host
    # elif homePage != None
    #  learner agent account:
    #     name = userId. In the case of Engage it is a UUID.
    #     homePage is a URL associated with the account.
    def __init__(self, gateway=None, userId=None, userName=None, homePage=None, mboxHost=None):
        self._Activity_Tree = ActivityTree()
        
        super(xAPILearnLogger, self).__init__()

        self._gateway = gateway
        self._userId = userId
        self._userName = userName
        self._home_page = homePage
        self._mbox_host = mboxHost
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

    def create_watched_verb(self):
        return Verb(id = "http://activitystrea.ms/schema/1.0/watch", display=LanguageMap({'en-US': 'watched'}))

    # ************** ACTIVITIES *************************************
    def createSession(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://id.tincanapi.com/activitytype/tutor-session",\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) } ))

    def createLesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://adlnet.gov/expapi/activities/lesson",\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) }))

    def createSublesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= self._url + "sublesson",\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) }))

    def createTask(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://activitystrea.ms/schema/1.0/task",\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) }))

    def createStep(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= "http://id.tincanapi.com/activitytype/step",\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) }))

    def createVideo(self):
        return Activity( id = "http://activitystrea.ms/schema/1.0/video", object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': "video"}),\
                                                         description=LanguageMap({'en-US': "Video content of any kind"}),\
                                                         extensions= { self._url + "activityid" : str(uuid.uuid4()) }))

    def createAgent(self):
        if self._mbox_host != None:
            return Agent ( object_type = 'Agent', name = self._userName,\
                           mbox = "mailto:" + self._userName + "@" + self._mbox_host)
        elif self._home_page != None:
            return Agent ( object_type = 'Agent', name = self._userName,\
                           account = AgentAccount (name = self._userId, home_page = self._home_page) )
        else:
            return Agent ( object_type = 'Agent', name = self._userName )

    # ************** STARTING AND STOPPING *********************************

    def sendStartSession(self, activityID, name, description, contextDict, timestamp = None):
        activity = self.createSession(activityID,name,description)
        actor = self.createAgent()
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
        actor = self.createAgent()
        result = Result(success = True,)
        
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSublesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createSublesson(activityID,name,description)
        actor = self.createAgent()
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
        actor = self.createAgent()
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartStep(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createStep(activityID,name,description)
        actor = self.createAgent()
        result = Result(success = True,)

        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)


    def sendTerminatedSession(self, contextDict, timestamp=None):
        actor = self.createAgent()
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
        actor = self.createAgent()
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
        actor = self.createAgent()
        result = Result(response = '',)

        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self, contextDict, timestamp=None):
        actor = self.createAgent()
        result = Result(response = '',)

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    # work in progress.
    # If a raw_score is provided then a max_score must be provided too.
    # Might want to provide more detailed information relating to the knowledge components involved in the step.
    def sendCompletedStep(self, choice, contextDict, resultExtDict=None, raw_score=-1, max_score=-1, min_score=0, timestamp=None):
        actor = self.createAgent()

        if resultExtDict==None:
            myExtensions = None
        else:
            myExtensions = Extensions(resultExtDict)

        if (raw_score != -1):
            result = Result(response=choice,
                            score = Score(raw=raw_score, min=min_score, max=max_score),
                            extensions =  myExtensions)
        else:
            result = Result(response=choice,
                            extensions = myExtensions)

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        self._Activity_Tree.ExitActivity()
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_completed_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    # ***********************************************************************************

    def sendWatchedVideo(self, contextDict, timestamp=None):
        actor = self.createAgent()

        activity = self.createVideo()
        result = Result(response = '',)

        # This is an atomic action: no start and end points. Just a start point.
        # Of course in reality, the video will have a length. We just don't have that information.

        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_watched_verb(), object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    '''
    Add context to the message.  

    In addition to context extensions in tempExtensions,
    add serialized activity tree.

    @param tempExtensions: Dictionary of key-value items to add to the message context.
    @return: context object
    '''

    def addContext(self, tempExtensions = {}):
        
        tempExtensions[self._url + ACTIVITY_TREE_KEY] = self._Activity_Tree.saveXAPItoJSON()
                                        
        mygrouping = self._Activity_Tree.convertPathToGrouping()
        myparent = self._Activity_Tree.findParentActivity()

        #Defining a TinCan Context object
        if len(mygrouping)==0 and myparent == None:
            context = Context(
                extensions = Extensions(tempExtensions))
        else:
            if len(mygrouping)==0:
                mycontextActivities = ContextActivities(parent = myparent)
            else:
                mycontextActivities = ContextActivities(parent = myparent, 
                                                        grouping = ActivityList(mygrouping))
            context = Context(
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
