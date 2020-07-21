from datetime import datetime, timezone, timedelta
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

from SuperGLU.Util.Serialization import makeSerialized
from SuperGLU.Services.LoggingService.ActivityTree import ActivityTree

BASE_URI = "https://github.com/GeneralizedLearningUtilities/SuperGLU/"

# ACTIVITY TYPES
SESSION_TYPE = "http://id.tincanapi.com/activitytype/tutor-session"
LESSON_TYPE = "http://adlnet.gov/expapi/activities/lesson"
SUBLESSON_TYPE = BASE_URI + "sublesson"
TASK_TYPE = "http://activitystrea.ms/schema/1.0/task"
STEP_TYPE = "http://id.tincanapi.com/activitytype/step"

# VERBS
START_URI = "http://activitystrea.ms/schema/1.0/start"
COMPLETED_URI = "http://activitystrea.ms/schema/1.0/complete"
TERMINATED_URI = "http://activitystrea.ms/schema/1.0/terminate"
WATCHED_URI = "http://activitystrea.ms/schema/1.0/watch"

# ACTIVITY DEFINITION EXTENSION
ACTIVITY_ID_URI = BASE_URI + "activityid"

# CONTEXT EXTENSIONS
RECOVERED_URI = BASE_URI + "recovered"
MISSING_COMPS_URI = BASE_URI + "missingCompletions"
ACTIVITY_TREE_URI = BASE_URI + 'serialized_activitytree'

class xAPILearnLogger(BaseService):

    # if mbox_host != None
    #  learner agent
    #    mbox = userName@mbox_host
    # elif homePage != None
    #  learner agent account:
    #     name = userId. In the case of Engage it is a UUID.
    #     homePage is a URL associated with the account.
    def __init__(self, gateway=None, userId=None, userName=None, homePage=None, mboxHost=None, outputFileName=None):
        self._Activity_Tree = ActivityTree()
        
        super(xAPILearnLogger, self).__init__()

        self._gateway = gateway
        self._userId = userId
        self._userName = userName
        self._home_page = homePage
        self._mbox_host = mboxHost
        self.outputFileName = outputFileName
        self._errorLogName = "xapi_learn_logger_errorLog.txt"
        # If log file ends suddenly, this is our guess of how many seconds passed since last message recorded
        self._secondsAfterLastTimeStamp = 1

    def generateFakeTimeStamp(self,lastTimeStampStr):
        return (datetime.fromisoformat(lastTimeStampStr) +\
                             timedelta(seconds=self._secondsAfterLastTimeStamp)).isoformat()
    
    def resetActivityTree(self,activityTreeStr):
        self._Activity_Tree.initializeFromXAPI_JSON(activityTreeStr)

    def setUserId(self,userId):
        self._userId = userId

    def setUserName(self,userName):
        self._userName = userName

    def getTimestamp(self):
        timestamp = datetime.now(timezone.utc)
        return timestamp

    # ***************** VERBS ***************************************
    def create_completed_verb(self):
        return Verb(id = COMPLETED_URI, display=LanguageMap({'en-US': 'completed'}))

    def create_started_verb(self):
        return Verb(id = START_URI , display=LanguageMap({'en-US': 'started'}))

    def create_terminated_verb(self):
        return Verb(id = TERMINATED_URI, display=LanguageMap({'en-US': 'terminated'}))

    def create_watched_verb(self):
        return Verb(id = WATCHED_URI, display=LanguageMap({'en-US': 'watched'}))

    # ************** ACTIVITIES *************************************
    def createSession(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= SESSION_TYPE,\
                                                         extensions= { ACTIVITY_ID_URI  : str(uuid.uuid4()) } ))

    def createLesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= LESSON_TYPE,\
                                                         extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) }))

    def createSublesson(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= SUBLESSON_TYPE,\
                                                         extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) }))

    def createTask(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= TASK_TYPE,\
                                                         extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) }))

    def createStep(self, activityID, name, description):
        return Activity( id = activityID, object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': name }),\
                                                         description=LanguageMap({'en-US': description}),\
                                                         type= STEP_TYPE,\
                                                         extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) }))

    def createVideo(self):
        return Activity( id = "http://activitystrea.ms/schema/1.0/video", object_type = 'Activity',\
                         definition = ActivityDefinition(name=LanguageMap({'en-US': "video"}),\
                                                         description=LanguageMap({'en-US': "Video content of any kind"}),\
                                                         extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) }))

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
        
        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(activity = activity, label = None)

        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartLesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createLesson(activityID,name,description)
        actor = self.createAgent()
        
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartSublesson(self, activityID, name, description, contextDict, timestamp=None):
        activity = self.createSublesson(activityID,name,description)
        actor = self.createAgent()

        #Implementing Activity Tree into context
        self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartTask(self, activityID, name, description, contextDict, timestamp=None, parentActivityName=None):
        activity = self.createTask(activityID,name,description)
        actor = self.createAgent()

        if parentActivityName == None:
            self._Activity_Tree.EnterActivity(label = None, activity = activity)
        else:
            parentActivity = self._Activity_Tree.findActivityByName(parentActivityName)
            self._Activity_Tree.EnterActivity(label= None, activity = activity, children=None, parentLabel=None, parentActivity=parentActivity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendStartStep(self, activityID, name, description, contextDict, timestamp=None, parentTaskName=None):
        activity = self.createStep(activityID,name,description)
        actor = self.createAgent()

        if parentTaskName != None:
            parentTask = self._Activity_Tree.findActivityByName(parentTaskName)
            self._Activity_Tree.EnterActivity(label= None, activity = activity, children=None, parentLabel=None, parentActivity=parentTask)
        else:    
            self._Activity_Tree.EnterActivity(label = None, activity = activity)
              
        context = self.addContext(contextDict)
        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_started_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def createFakeContextDict(self):
        return { RECOVERED_URI : "activity" }

    def sendFakeTerminatedSession(self, contextDict, timestamp):
        with open(self._errorLogName, 'a') as f:
            fakeTimeStamp = self.generateFakeTimeStamp(timestamp)
            f.write("Generating fake end of session statement. Last timestamp is " + timestamp + "\n")
            f.write("Fake timestamp is " + fakeTimeStamp + "\n")
            self.sendTerminatedSession(contextDict,fakeTimeStamp)

    def sendTerminatedSession(self, contextDict, timestamp=None):
        actor = self.createAgent()
        
        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()

        missingData = False

        if timestamp is None:
            timestamp = self.getTimestamp()
                
        while activity != None and activity.definition.type != SESSION_TYPE:
            with open(self._errorLogName, 'a') as f:
                missingData = True
                f.write("Processing: terminate session but " + activity.definition.type + " is current activity\n")
                f.write("\tuser name = " + self._userName + "\n")

                if activity.definition.type == LESSON_TYPE:
                    f.write("Sending terminate " + activity.definition.type + " statement\n")
                    self.sendCompletedLesson(contextDict =  self.createFakeContextDict(), timestamp=timestamp,fake=True)
                elif activity.definition.type == SUBLESSON_TYPE:
                    f.write("Sending terminate " + activity.definition.type + " statement\n")
                    self.sendCompletedSublesson(contextDict = self.createFakeContextDict(), timestamp=timestamp,fake=True)
                elif activity.definition.type == TASK_TYPE:
                    f.write("Sending terminate " + activity.definition.type + " statement\n")
                    self.sendCompletedTask(contextDict = self.createFakeContextDict(), timestamp=timestamp,fake=True)
                elif activity.definition.type == STEP_TYPE:
                    f.write("Sending terminate " + activity.definition.type + " statement\n")
                    self.sendCompletedStep(choice="UNKNOWN",contextDict=self.createFakeContextDict(),timestamp=timestamp,fake=True)
                else:
                    f.write("No statement to complete/terminate this activity. Simply removing from activity tree\n")
                    self._Activity_Tree.ExitActivity()
                activity = self._Activity_Tree.findCurrentActivity()

        if activity == None:
            with open(self._errorLogName, 'a') as f:
                f.write("Terminate session received but no current activity. Sending placeholder session data in terminate statement.\n")
                f.write("\tuser name = " + self._userName + "\n")
                activity = Activity( id = SESSION_TYPE, object_type = 'Activity',\
                                     definition = ActivityDefinition(name=LanguageMap({'en-US': "tutor session" }),\
                                                                     description=LanguageMap({'en-US': "This represents a tutoring session."}),\
                                                                     extensions= { ACTIVITY_ID_URI : str(uuid.uuid4()) } ))
                contextDict[RECOVERED_URI] = "activityPlusContext"

        if missingData:
            contextDict[MISSING_COMPS_URI] = "True"

        context = self.addContext(contextDict)

        self._Activity_Tree.ExitActivity()
          
        statement = Statement(actor=actor, verb=self.create_terminated_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedLesson(self, contextDict, timestamp=None, fake=False, winner=None):
        actor = self.createAgent()

        #Implementing Activity Tree into context
        activity = self._Activity_Tree.findCurrentActivity()
        context = self.addContext(contextDict)

        self._Activity_Tree.ExitActivity()
        
        if winner !=None:
            result = Result(response=winner)
        else:
            result = None
              
        if timestamp is None:
            timestamp = self.getTimestamp()
        if fake:
            verb = self.create_terminated_verb()
        else:
            verb = self.create_completed_verb()
        statement = Statement(actor=actor, verb=verb, object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedSublesson(self, contextDict, timestamp=None, fake=False):
        actor = self.createAgent()

        activity = self._Activity_Tree.findCurrentActivity()
        context = self.addContext(contextDict)

        self._Activity_Tree.ExitActivity()
           
        if timestamp is None:
            timestamp = self.getTimestamp()
        if fake:
            verb = self.create_terminated_verb()
        else:
            verb = self.create_completed_verb()
        statement = Statement(actor=actor, verb=verb, object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    def sendCompletedTask(self,choice=None, contextDict={}, resultExtDict=None, raw_score=-1, min_score=0, max_score=-1, timestamp=None, fake=False, taskName=None):
        actor = self.createAgent()

        if resultExtDict==None:
            myExtensions = None
        else:
            myExtensions = Extensions(resultExtDict)

        if (raw_score != -1):
            result = Result(response=choice,
                            score = Score(raw=raw_score, min=min_score, max=max_score),
                            extensions =  myExtensions)
        elif choice is not None:
            result = Result(response=choice,
                            extensions = myExtensions)
        else:
            result = None

        #Implementing Activity Tree into context
        if taskName is not None:
            activity = self._Activity_Tree.findActivityByName(taskName)
        else:
            activity = self._Activity_Tree.findCurrentActivity()
        context = self.addContext(contextDict, activity)

        self._Activity_Tree.ExitActivity(activity=activity)
              
        if timestamp is None:
            timestamp = self.getTimestamp()
        if fake:
            verb = self.create_terminated_verb()
        else:
            verb = self.create_completed_verb()
        statement = Statement(actor=actor, verb=verb, object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)

    # work in progress.
    # If a raw_score is provided then a max_score must be provided too.
    # Might want to provide more detailed information relating to the knowledge components involved in the step.
    def sendCompletedStep(self, choice, contextDict, resultExtDict=None, raw_score=-1, max_score=-1, min_score=0, timestamp=None,fake=False,stepName=None):
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
        if stepName != None:
            activity = self._Activity_Tree.findActivityByName(stepName)
        else:   
            activity = self._Activity_Tree.findCurrentActivity()
        context = self.addContext(contextDict)

        self._Activity_Tree.ExitActivity(activity=activity)
              
        if timestamp is None:
            timestamp = self.getTimestamp()
        if fake:
            verb = self.create_terminated_verb()
        else:
            verb = self.create_completed_verb()
        statement = Statement(actor=actor, verb=verb, object=activity, result=result, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    # ***********************************************************************************

    def sendWatchedVideo(self, contextDict, timestamp=None):
        actor = self.createAgent()

        activity = self.createVideo()

        self._Activity_Tree.EnterActivity(label = None, activity=activity)

        # This is an atomic action: no start and end points. Just a start point.
        # Of course in reality, the video will have a length. We just don't have that information.
        # So we enter the activity, calculate the context, and then exit.

        context = self.addContext(contextDict)

        self._Activity_Tree.ExitActivity()

        if timestamp is None:
            timestamp = self.getTimestamp()
        statement = Statement(actor=actor, verb=self.create_watched_verb(), object=activity, result=None, context=context, timestamp=timestamp)
        self.sendLoggingMessage(statement)      

    '''
    Add context to the message.  

    In addition to context extensions in tempExtensions,
    add serialized activity tree and potentially parent and grouping.

    @param tempExtensions: Dictionary of key-value items to add to the message context.
    @return: context object
    '''

    def addContext(self, tempExtensions = {}, currentActivity=None):

        tempExtensions[ACTIVITY_TREE_URI] = self._Activity_Tree.saveXAPItoJSON()
                                        
        mygrouping = self._Activity_Tree.convertPathToGrouping(currentActivity)
        if currentActivity == None:
            myparent = self._Activity_Tree.findParentActivity()
        else:
            myparent = self._Activity_Tree.findParentActivityByChild(currentActivity) 

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
        if self.outputFileName:
            with open(self.outputFileName, "a") as file:
                file.write(statement.to_json() + "\n")
        self.sendMessage(message)
