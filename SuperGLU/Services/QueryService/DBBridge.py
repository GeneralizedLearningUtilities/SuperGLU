'''
Created on Apr 11, 2016

@author: auerbach
'''
from SuperGLU.Util.ErrorHandling import logInfo, logWarning
from uuid import uuid4
from SuperGLU.Services.StudentModel.PersistentData import DBStudent, DBStudentAlias, DBSession, DBClass, DBClasssAlias, DBCalendarData, DBTask, DBTopic, DBAssistmentsItem
from SuperGLU.Core.MessagingDB import SESSION_ID_CONTEXT_KEY, DATE_TIME_FORMAT, TASK_ID_CONTEXT_KEY, USER_ID_CONTEXT_KEY
from datetime import datetime
from SuperGLU.Services.StudentModel.StudentModelFactories import BasicStudentModelFactory

class DBBridge(object):
    studentCache = {}
    sessionCache = {}
    classCache = {}
    taskCache = {}
    topicCache = {}
    calendarCache = {}

    serviceName = ''
    
    def __init__(self, serviceName):
        self.serviceName = serviceName
        self.taskASSISTmentsDictionary = None
        
    def populateTaskAssistmentsDictionary(self):
        result = {}
        tasks = DBTask.find_all()
        assistmentsItems = DBAssistmentsItem.find_all()
        
        for task in tasks:
            if task.assistmentsItemId is not '':
                for assistmentsItem in assistmentsItems:
                    if assistmentsItem.id == task.assistmentsItemId:
                        result[assistmentsItem.id] = task.taskId
                        break
        
        return result

    def createStudent(self, studentId, msg):
        logInfo('{0} could not find student with id: {1} in database.  Creating new student'.format(self.serviceName, studentId), 3)
        studentUUID = str(uuid4())
        student = DBStudent(id=studentUUID, studentId=studentId, sessionIds=[], oAuthIds={}, studentModelIds={}, kcGoals={})
        student.save()
        self.studentCache[studentId] = student
        newStudentAlias = DBStudentAlias(trueId=studentUUID, alias=studentId)
        newStudentAlias.save()
        return student
    
    def createSession(self, msg):
        logInfo("Could not find session with id:{0}.  Creating new Session".format(msg.getContextValue(SESSION_ID_CONTEXT_KEY)), 3)
        userId = msg.getContextValue(USER_ID_CONTEXT_KEY)
        if userId is not None:
            student = self.retrieveStudentFromCacheOrDB(userId, msg, True)
        else:
            student = None
        session = DBSession(sessionId = msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        session.messageIds = []
        session.hints = []
        session.feedback = []
        session.performance = {}
        session.startTime = datetime.utcnow().strftime(DATE_TIME_FORMAT)
        session.duration = 0
        session.subtaskNumber = -1
        session.id = msg.getContextValue(SESSION_ID_CONTEXT_KEY)
        session.task = msg.getContextValue(TASK_ID_CONTEXT_KEY)
        
        if session.task in self.taskASSISTmentsDictionary.keys():
            session.task = self.taskASSISTmentsDictionary[session.task]
        
        if student is not None:
            student.sessionIds.append(session.id)
            session.students.append(student.studentId)
            student.save()
        session.save()
        self.sessionCache[session.id] = session
        return session
    
    def createClass(self, classId, msg):
        logInfo('{0} could not find class with id: {1} in database.  Creating new class'.format(self.serviceName, classId), 3)
        classUUID = str(uuid4())
        clazz = DBClass(id=classUUID, ids=[classId], name='', roles={}, students=[], kcs=[])
        clazz.save()
        self.classCache[classId] = clazz
        newClassAlias = DBClasssAlias(trueId=classUUID, alias=classId)
        newClassAlias.save()
        return clazz    
    
    
    def updateSession(self, msg, session):
        session.messageIds.append(msg.getId())
        startTime = datetime.strptime(session.startTime, DATE_TIME_FORMAT)
        msgTimestamp = datetime.strptime(msg.getTimestamp(), DATE_TIME_FORMAT)
        delta = msgTimestamp - startTime
        if session.task is None or session.task is "":
            taskId = msg.getContextValue(TASK_ID_CONTEXT_KEY)
            sessionTask = self.retrieveTaskFromCacheOrDB(taskId, True)
            session.task = sessionTask.id
        #only update if the duration increases
        if delta.seconds > session.duration:
            session.duration = delta.seconds
    
    
    def retrieveTaskFromCacheOrDB(self, taskId, useCache=True):
        if taskId is None:
            return None
        
        if taskId in self.taskCache.keys() and useCache:
            logInfo('{0} found cached task object with id:{1}'.format(self.serviceName, taskId), 4)
            return self.taskCache[taskId]
        else:
            logInfo('{0} could not find cached task object with id: {1}.  Falling back to database.'.format(self.serviceName, taskId), 3)
            dbTaskList = DBTask.find_by_index("taskIdIndex", taskId)
            task = None
            if len(dbTaskList) > 0:
                task = dbTaskList[0]
            else:
                logInfo('{0} could not find cached task object with id: {1}.  attempting to find by ASSISTments item Id.'.format(self.serviceName, taskId), 3)
                if self.taskASSISTmentsDictionary is not None and taskId in self.taskASSISTmentsDictionary.keys():
                    dbTaskList = DBTask.find_by_index("taskIdIndex", self.taskASSISTmentsDictionary[taskId])
                    if len(dbTaskList) > 0:
                        task = dbTaskList[0]
                        #Cache the result so we don't need to worry about looking it up again.
                        self.taskCache[taskId] = task            
            return task
    
    
    def retrieveTopicFromCacheOrDB(self, topicId, useCache=True):
        if topicId is None:
            return None
        
        if topicId in self.taskCache.keys() and useCache:
            logInfo('{0} found cached task object with id:{1}'.format(self.serviceName, topicId), 4)
            return self.taskCache[topicId]
        else:
            logInfo('{0} could not find cached topic object with id: {1}.  Falling back to database.'.format(self.serviceName, topicId), 3)
            dbTopicList = DBTopic.find_by_index("topicIdIndex", topicId)
            
            if len(dbTopicList) > 0:
                task = dbTopicList[0]
                #Cache the result so we don't need to worry about looking it up again.
                self.taskCache[topicId] = task
                return task
            else:
                return None
          
        
    def retrieveSessionFromCacheOrDB(self, sessionId, useCache=True):
        if sessionId is None:
            return None
        
        if sessionId in self.sessionCache.keys() and useCache:
            logInfo('{0} found cached session object with id:{1}'.format(self.serviceName, sessionId), 4)
            return self.sessionCache[sessionId]
        
        logInfo('{0} could not find cached session object with id: {1}.  Falling back to database.'.format(self.serviceName, sessionId), 3)
        session = DBSession.find_one(sessionId)
        
        if session is not None:
            logInfo('{0} found session {1}.  Storing in Cache'.format(self.serviceName, session.sessionId), 5)
            self.sessionCache[session.id] = session 
                    
        return session
                
    def retrieveStudentFromCacheOrDB(self, studentId, msg, useCache=True):
        logInfo("Entering retrieveStudentFromCacheOrDB", 5)
        student = self.studentCache.get(studentId)
        if student is not None and useCache:
            logInfo('{0} found student object with id:{1}'.format(self.serviceName, studentId), 4)
            return student
        else:
            logInfo('{0} could not find cached student object with id: {1}.  Falling back to database.'.format(self.serviceName, studentId), 3)
            studentAliasList = DBStudentAlias.find_by_index("AliasIndex", studentId)
            
            if len(studentAliasList) > 0:
                #there should only be one object returned, should put it a log statement if that isn't correct.
                for studentAlias in studentAliasList:
                    student = studentAlias.getStudent()
                    
            if student is None:
                student = self.createStudent(studentId, msg)
            #Cache the result so we don't need to worry about looking it up again.
            self.studentCache[studentId] = student
            return student
        
        
    def retrieveClassFromCacheOrDB(self, classId, msg, useCache=True):
        logInfo("Entering retrieveClassFromCacheOrDB with arguments {0}".format(classId), 5)
        if classId is None or classId == '':
            return None
        clazz = self.studentCache.get(classId)
        if clazz is not None and useCache:
            logInfo('{0} found classroom object with id:{1}'.format(self.serviceName, clazz), 4)
            return clazz
        else:
            logInfo('{0} could not find cached classroom object with id: {1}.  Falling back to database.'.format(self.serviceName, classId), 3)
            classAliasList = DBClasssAlias.find_by_index("AliasIndex", classId)
            if len(classAliasList) > 0:
                #there should only be one object returned, should put it a log statement if that isn't correct.
                for classAlias in classAliasList:
                    clazz = classAlias.getStudent()
                    
            if clazz is None:
                clazz = self.createClass(classId, msg)
            #Cache the result so we don't need to worry about looking it up again.
            self.classCache[classId] = clazz
            return clazz
        
    def getCalendarFromOwnerId(self, ownerId=None, useCache=True):
        if ownerId is None:
            logWarning("NO OWNER ID WAS GIVEN WHEN ATTEMPTING TO LOOK UP CALENDAR")
            return None
        
        if useCache:
            result = self.calendarCache.get(ownerId, None)
            if result is not None:
                return result;
        
        foundCalendars = DBCalendarData.find_by_index("ownerIdIndex", [])
        calendarData = None
        if len(foundCalendars) == 0:
            logInfo("No calendar found, creating a new calendar for owner:{0}".format(ownerId), 1)
            calendarData = DBCalendarData()
            calendarData.setCalendarData(ownerId)
        elif len(foundCalendars) == 1:
            calendarData = foundCalendars[0]
        elif len(foundCalendars) > 1:
            logWarning("{0} owns more than a single calendar.  Database may be corrupted.  Defaulting to the first value".format(ownerId))
            calendarData = foundCalendars[0]
        self.calendarCache[ownerId] = calendarData
        return calendarData