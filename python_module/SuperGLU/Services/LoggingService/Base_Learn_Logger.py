import datetime
import time
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService

class BaseLearnLogger(BaseService):

    '''
    Initialize the standard ITS logger service
        @param gateway: The parent gateway for this service
        @type gateway: Messaging_Gateway.MessagingGateway
        @param userId: Unique ID for the user
        @type userId: uuid string
        @param classroomId: Unique ID for the classroom cohort (optional). Leave as None if unknown.
        @type classroomId: uuid string
        @param taskId: Unique ID for the task being performed.
        @type taskId: uuid string
        @param url: The current base URL for the task that is being performed. This should not include situational parameters like the user id.
        @type url: url string
        @param activityType: The type of activity. This should be a unique system UUID (e.g., "AutoTutor_asdf2332gsa" or "www.autotutor.com/asdf2332gsa"). This ID should be the same for all activities presented by this system, since it will be used to query their results.
        @type activityType: uuid string
        @param id: The UUID for this service. If left blank, this will use a random UUID (recommended).
        @type id: string
    '''

    def __init__(self, gateway, userId, name, classroomId, taskId, url, activityType, context, anId):
        super(BaseLearnLogger, self).__init__()
        self._gateway = gateway
        self._userId = userId
        self._name = name
        self._classroomId = classroomId
        self._taskId = taskId
        self._url = url
        self._activityType = activityType
        self._context = context
        self._startTime = time.time()
        self._id = anId

    '''
    Calculate the duration so far
        @param startTime: The start time to calculate the duration against. If blank, uses the default start time for this service.
        @param startTime: Date
        @param endTime: The end time to calculate the duration against. If blank, uses the current time.
        @param endTime: Date
        @returns: Duration since the start time (endTime-startTime), in seconds.
        @rtype: float
    '''

    def calcDuration(self, startTime=None, endTime=None):
        if startTime == None:
            startTime = self._startTime
        if endTime == None:
            endTime = time.time()
        duration = (endTime - startTime)/1000.0;
        if duration < 0:
            print("Warning: Calculated duration was less than zero.")
        return duration;

    def getTimestamp(self):
        timestamp = datetime.datetime.utcnow()
        return timestamp

    '''
    Reset the start time for this service, for the purpose of calculating the duration
        @param startTime: The new default start time for the service.
        @type startTime: Date
    '''

    def resetStartTime(self, startTime):
        if startTime == None:
            startTime = time.time()
        self._startTime = startTime

    '''
    Reset the task ID for this service
        @param taskId: The unique taskId for the current activity. If None, gives an unknown ID based on the URL.
        @type taskId: uuid string
    '''

    def resetTaskId(self, taskId):
        self._taskId = taskId

    def setContextValue(self, key, value):
        self._context[key] = value

    def hasContextValue(self, key):
        return key in self._context
