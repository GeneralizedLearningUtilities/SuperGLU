'''
Created on May 18, 2016
This Module contains the service for handling the initial receipt of iCal strings from a client
The strings are converted to serializable objects and sent off to the GLUDB storage service to be stored.
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Core.MessagingDB import ELECTRONIX_TUTOR_UPLOAD_CALENDAR_VERB, CALENDAR_ACCESS_PERMISSIONS_KEY, ADD_TASK_TO_CALENDAR_VERB, CALENDAR_EVENT_START_TIME_KEY, CALENDAR_EVENT_END_TIME_KEY,\
    CALENDAR_EVENT_DURATION_KEY, DATE_TIME_FORMAT
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo, logWarning, logError
from SuperGLU.Services.StudentModel.PersistentData import SerializableCalendarData, PUBLIC_PERMISSION, DBCalendarData, STUDENT_OWNER_TYPE, LearningTask
from SuperGLU.Services.StorageService.Storage_Service_Interface import STORAGE_SERVICE_NAME, VALUE_VERB
from SuperGLU.Services.QueryService.DBBridge import DBBridge
from icalendar import Calendar, Event
from time import strptime
from datetime import datetime

ICAL_READER_SERVICE_NAME = "iCalReader"

ICAL_OBJECT_TYPE = "iCalendar"

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
    
    def getCalendarFromOwnerId(self, ownerId=None):
        if ownerId is None:
            logWarning("NO OWNER ID WAS GIVEN WHEN ATTEMPTING TO LOOK UP CALENDAR")
            return None
        
        foundCalendars = DBCalendarData.find_by_index("ownerIdIndex", [])
        
        calendarData = None
        
        if len(foundCalendars) == 0:
            logInfo("no calendar found, creating a new calendar for owner:{0}".format(ownerId), 1)
            calendarData = self.createCalendarData(ownerId)
            return calendarData
            
        if len(foundCalendars) > 1:
            logWarning("{0} owns more than a single calendar.  Database may be corrupted.  Defaulting to the first value".format(ownerId))
        
        calendarData = foundCalendars[0]
        return calendarData
    
    def addTaskToCalendar(self, task, calendarData, startTime, endTime=None, duration=None):
        if startTime is None:
            logInfo("startTime not found, will not add task to ", 3)
            return
        
        calenderAsObject = Calendar.from_ical(calendarData.calendarData)
        newEvent = Event()
        newEvent.add('summary', task.displayName)
        newEvent.add('comment', "taskId = {0}".format(task.taskId))
        
        
        startTimeAsDateTime = datetime.strptime(startTime, DATE_TIME_FORMAT)
        newEvent.add('dtstart', startTimeAsDateTime)
        
        if endTime is not None:
            endTimeAsDateTime = datetime.strptime(endTime, DATE_TIME_FORMAT)
            newEvent.add('dtend', endTimeAsDateTime)
            
        elif duration is not None:
            newEvent.add('duration', duration)
            
        calenderAsObject.add_component(newEvent)
        calendarData.calendarData = calenderAsObject.to_ical()
        return
            
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
                calendarData.calendarData = msg.getResult()
                reply = Message(actor=STORAGE_SERVICE_NAME, verb=VALUE_VERB, object=ICAL_OBJECT_TYPE, result=calendarData)
            
        if msg.getSpeechAct() == REQUEST_ACT:
            """
            message format for adding a task to a calendar:
            actor = ICAL_READER_SERVICE_NAME
            verb = addTaskToCalendar
            object = ownerId
            result = task data
            context = startTime (required), endTime(optional), duration(optional)
            """
            if msg.getVerb() == ADD_TASK_TO_CALENDAR_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(ICAL_READER_SERVICE_NAME, ADD_TASK_TO_CALENDAR_VERB, REQUEST_ACT), 4)
                startTime = msg.getContextValue(CALENDAR_EVENT_START_TIME_KEY, None)
                calendarData = self.getCalendarFromOwnerId(msg.getObject())
                endTime = msg.getContextValue(CALENDAR_EVENT_END_TIME_KEY, None)
                duration = msg.getContextValue(CALENDAR_EVENT_DURATION_KEY, None)
                if isinstance(msg.getResult(), LearningTask):
                    self.addTaskToCalendar(msg.getResult(), calendarData, startTime, endTime, duration)
                else:
                    logInfo("no task given, cannot create event", 2)
                 
        if reply is not None:
            logInfo('{0} is broadcasting a {1}, {2} message'.format(ICAL_READER_SERVICE_NAME, INFORM_ACT, VALUE_VERB), 4)
            self.sendMessage(reply)   