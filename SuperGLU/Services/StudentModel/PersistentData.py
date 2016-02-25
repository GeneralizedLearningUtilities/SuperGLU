import uuid
import hashlib
from datetime import datetime
from gludb.simple import DBObject, Field, Index
from SuperGLU.Services.QueryService.Queries import getKCsForAGivenUserAndTask, getAllHintsForSingleUserAndTask, getAllFeedbackForSingleUserAndTask
from SuperGLU.Util.ErrorHandling import logInfo
"""
This module contains secondary database objects that contain data derived from the logged messages
"""

def initDerivedDataTables():
    DBSystem.ensure_table()
    DBTask.ensure_table()
    DBTopic.ensure_table()
    DBSession.ensure_table()
    DBStudent.ensure_table()
    DBClass.ensure_table()
    DBStudentModel.ensure_table()
    DBClassModel.ensure_table()
    DBStudentAlias.ensure_table()

@DBObject(table_name="Systems")
class DBSystem(object):
    uuid              = Field('00000000-0000-0000-0000-000000000000')
    ids               = Field(list)
    name              = Field('')
    contactEmails     = Field(list)
    description       = Field('')
    metadata          = Field(dict)
    tasks             = Field(list)
    baseURL           = Field('')
    authoringURL      = Field('')
    taskListURL       = Field('')
    deliveryURL       = Field('')
    authenticationURL = Field('')
    
    #Non-persistant fields
    taskCache = []
    
    def __repr__(self):
        return self.uuid + "|" + str(self.ids) + "|" + self.name + "|" + str(self.contactEmails) + "|" + self.description + "|" + str(self.metadata) + "|" + str(self.tasks) + "|" + self.baseURL + "|" + self.authoringURL + "|" + self.taskListURL + "|" + self.deliveryURL + "|" + self.authenticationURL

    def getTasks(self, useCachedValue=False):
        if not useCachedValue:
            self.taskCache = [DBTask.find_one(x) for x in self.tasks]
        return self.taskCache
    
    def addTasks(self, newTask):
        if newTask is None:
            return #don't bother adding null values
        self.taskCache.append(newTask)
        if newTask.id is None:
            newTask.save()
        self.tasks.append(newTask.id)
    
@DBObject(table_name="Tasks")
class DBTask(object):
    ids  = Field(list)
    name = Field('')
    kcs  = Field(list)
    url  = Field('')
    
    def __repr__(self):
        return str(self.ids) + "|" + self.name + "|" + str(self.kcs) + "|" + self.url
        
        
        
@DBObject(table_name="Topics")
class DBTopic(object):
    kcList       = Field(list)
    resourceList = Field(list)
    
    def __repr__(self):
        return str(self.kcList) + "|" + str(self.resourceList)
        

@DBObject(table_name="Sessions")
class DBSession(object):
    sessionId      = Field('')
    students       = Field(list)
    system         = Field('')
    task           = Field('')
    startTime      = Field('')
    duration       = Field(-1.0)
    endCondition   = Field('')
    performance    = Field(dict)
    classId        = Field('')
    hints          = Field(list)
    feedback       = Field(list)
    messageIds     = Field(list)
    sourceDataN    = Field(-1)
    sourceDataHash = Field(-1)
    
    #Non-persistent Fields
    studentCache = []
    
    #keeping this method here as an example of how to query based on UUID
    @classmethod
    def getSessionFromUUID(self, sessionId):
        return DBSession.find_one(sessionId)
    
    @Index
    def SessionIdIndex(self):
        return self.sessionId
    
    def getStudents(self, useCachedValue = False):
        if not useCachedValue:
            self.studentCache = [DBStudent.find_one(x) for x in self.students]
        return self.studentCache
    
    #takes a DBStudent object as an argument
    def addStudent(self, newStudent):
        if newStudent is None:
            return
        
        if newStudent.id in self.students:
            return
        
        if newStudent.id is None:
            newStudent.save()
            
        self.studentCache.append(newStudent)
        self.students.append(newStudent.id)        
    
    def setStartTime(self, sTime):
        self.startTime = sTime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
    def getStartTime(self):
        if(self.startTime != ''):
            return datetime.strptime(self.startTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            
        return None
        
    def getPerformance(self, useCachedValue = False):
        if not useCachedValue:
            self.performance = dict()
            
            if self.task is None or self.startTime is None:
                return self.performance
            
            for currentDBStudent in self.students:
                self.performance[currentDBStudent] = dict()
                kcList = getKCsForAGivenUserAndTask(currentDBStudent, self.task, self.startTime, False)
                for kcMessage in kcList:
                    self.performance[currentDBStudent][kcMessage.object] = kcMessage.result
                    if kcMessage.id not in self.messageIds:
                        self.messageIds.append(kcMessage.id)
        
        return self.performance
        
    def getHints(self, useCachedValue = False):
        if not useCachedValue:
            self.hints = list()
            
            if self.task is None or self.startTime is None:
                return self.hints
                
            for currentDBStudent in self.students:
                studentHints = getAllHintsForSingleUserAndTask(currentDBStudent, self.task, self.startTime, False)
                for currentHint in studentHints:         
                    self.hints.append(currentHint)
                    if currentHint.id not in self.messageIds:
                        self.messageIds.append(currentHint)
        return self.hints
            
    def getFeedback(self, useCachedValue = False):
        if not useCachedValue:
            self.feedback = list()
            
            if self.task is None or self.startTime is None:
                return self.feedback
                
            for currentDBStudent in self.students:
                studentFeedback = getAllFeedbackForSingleUserAndTask(currentDBStudent, self.task, self.startTime, False)
                for currentFeedback in studentFeedback:         
                    self.feedback.append(currentFeedback)
                    if currentFeedback.id not in self.messageIds:
                        self.messageIds.append(currentFeedback)
        return self.feedback
            
            
    def getSourceDataN(self, useCachedValue = False):
        if not useCachedValue:
            self.sourceDataN = len(self.messageIds)
        return self.sourceDataN
        
    
    def getSourceDataHash(self, useCachedValue = False):
        if not useCachedValue:
            uuidsAsString = ''.join(self.messageIds)
            uuidsAsBytes = uuidsAsString.encode()
            self.sourceDataHash = str(hashlib.sha256(uuidsAsBytes).hexdigest())
        return self.sourceDataHash
            

@DBObject(table_name="Students")
class DBStudent (object):
    studentId       = Field('')
    sessionIds      = Field(list)
    oAuthIds        = Field(dict)
    studentModelIds = Field(list)
    kcGoals         = Field(dict)
    
    #non-persistant fields
    sessionCache = []
    studentModelCache = []
    
    @Index
    def StudentIDIndex(self):
        return self.studentId
    
    def getSessions(self, useCachedValue):
        if not useCachedValue:
            self.sessionCache = [DBSession.find_one(x) for x in self.sessionIds]
        return self.sessionCache
               
    def addSession(self, newSession):
        if newSession is None:
            return
        
        if newSession.sessionId in self.sessionIds:
            return
        
        if newSession.id is None or newSession.id is '':
            newSession.save()
        self.sessionCache.append(newSession)
        self.sessionIds.append(newSession.sessionId)
        self.save()
            
    def getStudentModels(self, useCachedValue):
        if not useCachedValue:
            self.studentModelCache = [DBStudentModel.find_one(x) for x in self.studentModelIds]
        return self.studentModelCache
        
    def addStudentModel(self, newStudentModel):
        logInfo("Entering DBStudent.addStudentModel", 5)
        if newStudentModel is None:
            return
        if newStudentModel.id is None or newStudentModel.id is '':
            newStudentModel.save()
        
        self.studentModelCache.append(newStudentModel)
        if self.studentModelIds is None:
            self.studentModelIds = []
        self.studentModelIds.append(newStudentModel.id)
        self.save()
        
        
@DBObject(table_name="StudentAliases")
class DBStudentAlias (object):
    trueId = Field('')
    alias  = Field('')
    
    @Index
    def AliasIndex(self):
        return self.alias
    
    def getStudent(self):
        student = DBStudent.find_by_index("StudentIDIndex", self.trueId)
        return student
        

@DBObject(table_name="Classes")
class DBClass (object):
    ids      = Field(list)
    name     = Field('')
    roles    = Field(dict)
    students = Field(list)
    topics   = Field(list)
    kcs      = Field(list)
    #TODO: Add schedule
    
    #Non-persistent Fields
    studentCache = []
    topicsCache = []
    
    def getStudents(self, useCachedValue = False):
        if not useCachedValue:
            self.studentCache = [DBStudent.find_one(x) for x in self.students]
        return self.studentCache
    
    def addStudent(self, newStudent):
        if newStudent is None:
            return
        if newStudent.id is None:
            newStudent.save()
        self.studentCache.append(newStudent)
        self.students.append(newStudent.id)
    
    def getTopics(self, useCachedValue = False):
        if not useCachedValue:
            self.topicsCache = [DBTopic.find_one(x) for x in self.topics]
        return self.topicsCache
    
    def addTopic(self, newTopic):
        if newTopic is None:
            return
        if newTopic.id is None:
            newTopic.save()
        self.topicsCache.append(newTopic)
        self.topics.append(newTopic.id)
            
@DBObject(table_name="StudentModels")
class DBStudentModel (object):
    studentId = Field('') #string
    kcMastery = Field(dict) #Dictionary<string, float>
    
    studentCache = None #type:DBStudent
    
    @Index
    def sudentIdIndex(self):
        return self.studentId
    
    def getStudent(self, useCachedValue= False):
        if self.studentId is not '':
            if not useCachedValue:
                self.studentCache = DBStudent.find_one(self.studentId)
            return self.studentCache
        else:
            return None
        

@DBObject(table_name="ClassModels")
class DBClassModel(object):
    studentIds = Field(list)
    kcMastery  = Field(dict)
    
    def getStudents(self, useCachedValue = False):
        if not useCachedValue:
            self.studentCache = [DBStudent.find_one(x) for x in self.students]
        return self.studentCache