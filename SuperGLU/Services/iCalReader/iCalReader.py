'''
Created on May 18, 2016
This Module contains the service for handling the initial receipt of iCal strings from a client
The strings are converted to serializable objects and sent off to the GLUDB storage service to be stored.
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Core.MessagingDB import ELECTRONIX_TUTOR_UPLOAD_CALENDAR_VERB, CALENDAR_ACCESS_PERMISSIONS_KEY, ADD_EVENT_TO_CALENDAR_VERB, CALENDAR_EVENT_START_TIME_KEY, CALENDAR_EVENT_END_TIME_KEY,\
    CALENDAR_EVENT_DURATION_KEY, DATE_TIME_FORMAT, CALENDAR_LOOKUP_VERB, CALENDAR_LOOKUP_START_TIME_KEY, CALENDAR_LOOKUP_END_TIME_KEY, CALENDAR_LOOKUP_RELATIVE_TIME_KEY, CALENDAR_LOOKUP_EVENT_TYPE_KEY
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo, logWarning, logError
from SuperGLU.Services.StudentModel.PersistentData import SerializableCalendarData, PUBLIC_PERMISSION, DBCalendarData, STUDENT_OWNER_TYPE, LearningTask, SerializableTopic
from SuperGLU.Services.StorageService.Storage_Service_Interface import STORAGE_SERVICE_NAME, VALUE_VERB
from SuperGLU.Services.QueryService.DBBridge import DBBridge
from icalendar import Calendar, Event
from datetime import datetime

ICAL_READER_SERVICE_NAME = "iCalReader"

ICAL_OBJECT_TYPE = "iCalendar"

TASK_ID = 'taskId'
TOPIC_ID = 'topicId'
COMMENT_KEY = 'comment'
START_TIME_KEY = 'dtstart'

class ICalReader(DBBridge):


    def __init__(self, anId=None):
        """
        Initialize the logging service.
        @param maxMsgSize: The maximum size for a field. 2.5m by default, which is ~2-5 MB of JSON.
        @param maxMsgSize: int
        """
        super(ICalReader, self).__init__(ICAL_READER_SERVICE_NAME)


    def createCalendarData(self, ownerId=None):
        result = DBCalendarData()
        result.ownerId = ownerId
        result.ownerType = STUDENT_OWNER_TYPE
        result.accessPermissions = PUBLIC_PERMISSION
        result.calendarData = Calendar().to_ical()
        result.saveToDB()
        return result
    
    
    
    def addTaskToCalendar(self, task, calendarData, startTime, endTime=None, duration=None):
        if startTime is None:
            logInfo("startTime not found, will not add task to ", 3)
            return
        
        calenderAsObject = Calendar.from_ical(calendarData.calendarData)
        newEvent = Event()
        newEvent.add('summary', task.displayName)
        newEvent.add(COMMENT_KEY, "{0}={1}".format(TASK_ID, task.taskId))
        
        
        startTimeAsDateTime = datetime.strptime(startTime, DATE_TIME_FORMAT)
        newEvent.add(START_TIME_KEY, startTimeAsDateTime)
        
        if endTime is not None:
            endTimeAsDateTime = datetime.strptime(endTime, DATE_TIME_FORMAT)
            newEvent.add('dtend', endTimeAsDateTime)
            
        elif duration is not None:
            newEvent.add('duration', duration)
            
        calenderAsObject.add_component(newEvent)
        calendarData.calendarData = calenderAsObject.to_ical()
        return
    
    def addTopicToCalendar(self, topic, calendarData, startTime, endTime=None, duration=None):
        if startTime is None:
            logInfo("startTime not found, will not add task", 3)
            return
        
        calenderAsObject = Calendar.from_ical(calendarData.calendarData)
        newEvent = Event()
        newEvent.add('summary', topic.topicId)
        newEvent.add(COMMENT_KEY, "{0} = {1}".format(TOPIC_ID, topic.topicId))
        
        
        startTimeAsDateTime = datetime.strptime(startTime, DATE_TIME_FORMAT)
        newEvent.add(START_TIME_KEY, startTimeAsDateTime)
        
        if endTime is not None:
            endTimeAsDateTime = datetime.strptime(endTime, DATE_TIME_FORMAT)
            newEvent.add('dtend', endTimeAsDateTime)
            
        elif duration is not None:
            newEvent.add('duration', duration)
            
        calenderAsObject.add_component(newEvent)
        calendarData.calendarData = calenderAsObject.to_ical()
        return
    
    #This is a tricky little function since we have multiple possible ways to query the calendar
    def findStartTimeAndEndTime(self, eventList, typeOfEventToSearchFor, startTime, endTime, duration):
        
        if startTime != None:
            startTimeAsDateTime = datetime.strptime(startTime, DATE_TIME_FORMAT)
            
        if endTime != None:
            endTimeAsDateTime = datetime.strptime(endTime, DATE_TIME_FORMAT)
        
        if startTime == None:
            startTimeAsDateTime = eventList[0][START_TIME_KEY]
        
        if endTime == None and duration == None:
            endTimeAsDateTime = eventList[len(eventList) - 1][START_TIME_KEY]
            
        elif endTime == None and duration >= 0:
            timeDelta = datetime.timedelta(days=duration)
            endTimeAsDateTime = startTimeAsDateTime + timeDelta
            
        elif endTime == None and duration < 0:
            timeDelta = datetime.timedelta(days=duration)
            endTimeAsDateTime = startTimeAsDateTime + timeDelta
            #now swap start time and end time since we have a negative duration
            tempTime = endTimeAsDateTime
            endTimeAsDateTime = startTimeAsDateTime
            startTimeAsDateTime = tempTime

            
        return (startTimeAsDateTime, endTimeAsDateTime)
    
    
    def getEventName(self, eventString):
        return eventString.split("=")[1]
            
    
    #Need to be careful here since there may be additional events that are unrelated to the tasks and topics.
    def eventMatches(self, event, typeOfEvent, startTime, endTime):
        
        if not event.contains(COMMENT_KEY):
            return False;
        
        commentString = event[COMMENT_KEY]
        tokenizedCommentString = commentString.split("=")
        if len(tokenizedCommentString) < 2:
            return False
        
        elif tokenizedCommentString[0] != typeOfEvent:
            return False
        
        elif event[START_TIME_KEY] >= startTime and event[START_TIME_KEY] <= endTime:
            return True
        
        return False
        
    
    
    def lookupEventInformation(self, calendarData, typeOfEvent, startTime=None, endTime=None, duration=None):
        calenderAsObject = Calendar.from_ical(calendarData.calendarData)
        eventList = calenderAsObject.walk('VEVENT')#grab all the events in the calendar
    
        result = []
        
        if eventList is not None and len(eventList) > 0:
            (actualStartTime, actualEndTime) = self.addEvents(eventList, typeOfEvent, startTime, endTime, duration)
            
            eventNames = [self.getEventName(event[COMMENT_KEY]) for event in eventList if self.eventMatches(event, typeOfEvent, actualStartTime, actualEndTime) ]
            
            if typeOfEvent == TOPIC_ID:
                result = [self.retrieveTopicFromCacheOrDB(topicId, True) for topicId in eventNames]
            elif typeOfEvent == TASK_ID:
                result = [self.retrieveTaskFromCacheOrDB(taskId, True) for taskId in eventNames]
            
        
        return result
            
    def receiveMessage(self, msg):
        
        
        reply = None
        
        if msg.getSpeechAct() == INFORM_ACT:
            """
            message format for loading calendars: 
            actor = className or student name
            verb = electronixTutorUploadCalendarVerb
            object = ownerType
            result = iCal data
            context contains access permissions
            """
            if msg.getVerb() == ELECTRONIX_TUTOR_UPLOAD_CALENDAR_VERB: 
                logInfo('{0} is processing a {1},{2} message'.format(ICAL_READER_SERVICE_NAME, ELECTRONIX_TUTOR_UPLOAD_CALENDAR_VERB, INFORM_ACT), 4)
                calendarData = SerializableCalendarData()
                calendarData.ownerId = msg.getActor()
                calendarData.ownerType = msg.getObject()
                #default to public access if none are given
                calendarData.accessPermissions = msg.getContextValue(CALENDAR_ACCESS_PERMISSIONS_KEY, PUBLIC_PERMISSION)
                calendarData.calendarData = msg.getResult().encode()#need to know if the client is sending us bytes or strings
                reply = Message(actor=STORAGE_SERVICE_NAME, verb=VALUE_VERB, object=ICAL_OBJECT_TYPE, result=calendarData, context=msg.getContext())
            
        if msg.getSpeechAct() == REQUEST_ACT:
            """
            message format for adding a task or topic to a calendar:
            actor = ICAL_READER_SERVICE_NAME
            verb = addTaskToCalendar
            object = ownerId
            result = task or topic data
            context = startTime (required), endTime(optional), duration(optional)
            """
            if msg.getVerb() == ADD_EVENT_TO_CALENDAR_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(ICAL_READER_SERVICE_NAME, ADD_EVENT_TO_CALENDAR_VERB, REQUEST_ACT), 4)
                startTime = msg.getContextValue(CALENDAR_EVENT_START_TIME_KEY, None)
                calendarData = self.getCalendarFromOwnerId(msg.getObject())
                endTime = msg.getContextValue(CALENDAR_EVENT_END_TIME_KEY, None)
                duration = msg.getContextValue(CALENDAR_EVENT_DURATION_KEY, None)
                if isinstance(msg.getResult(), LearningTask):
                    self.addTaskToCalendar(msg.getResult(), calendarData, startTime, endTime, duration)
                    calendarData.saveToDB()
                elif isinstance(msg.getResult(), SerializableTopic):
                    self.addTopicToCalendar(msg.getResult(), calendarData, startTime, endTime, duration)
                    calendarData.saveToDB()
                else:
                    logInfo("no task or topic given, cannot create event", 2)
            """
            message format for lookup up information from a calendar
            actor = ICAL_READER_SERVICE_NAME
            verb = calendarLookup
            object = ownerId
            result = 'taskId' or 'topicId' defaults to taskID
            context = startTime (optional), endTime(optional), duration(optional)
            """                    
            if msg.getVerb() == CALENDAR_LOOKUP_VERB :
                logInfo('{0} is processing a {1},{2} message'.format(ICAL_READER_SERVICE_NAME, CALENDAR_LOOKUP_VERB, REQUEST_ACT), 4)
                startTime = msg.getContextValue(CALENDAR_LOOKUP_START_TIME_KEY, None)
                endTime = msg.getContextValue(CALENDAR_LOOKUP_END_TIME_KEY, None)
                duration = msg.getContextValue(CALENDAR_LOOKUP_RELATIVE_TIME_KEY, None)
                eventType = msg.getContextValue(CALENDAR_LOOKUP_EVENT_TYPE_KEY, TASK_ID)
                calendarData = self.getCalendarFromOwnerId(msg.getObject())
                taskOrTopicList = self.lookupEventInformation(calendarData, eventType, startTime, endTime, duration)
                reply = Message(actor=ICAL_READER_SERVICE_NAME, verb=CALENDAR_LOOKUP_VERB, object=eventType, result=taskOrTopicList, context=msg.getContext())    
                
                
                 
        if reply is not None:
            logInfo('{0} is broadcasting a {1}, {2} message'.format(ICAL_READER_SERVICE_NAME, INFORM_ACT, VALUE_VERB), 4)
            self.sendMessage(reply)   