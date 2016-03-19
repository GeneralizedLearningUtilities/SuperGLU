import hashlib
from datetime import datetime
from gludb.simple import DBObject, Field, Index
from SuperGLU.Util.Serialization import Serializable, tokenizeObject, untokenizeObject
from SuperGLU.Services.QueryService.Queries import getKCsForAGivenUserAndTask, getAllHintsForSingleUserAndTask, getAllFeedbackForSingleUserAndTask
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Util.SerializationGLUDB import DBSerializable, GLUDB_BRIDGE_NAME
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
    DBClasssAlias.ensure_table()
    DBKCTaskAssociations.ensure_table()

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


class SerializableAssistmentsItem(Serializable):
    
    #Keys
    ITEM_ID_KEY = 'itemID'
    PROBLEM_SET_ID_KEY = 'problemSetID'
    PROBLEM_SET_NAME_KEY = 'problemSetName'
    ASSIGNMENTS_KEY = 'assignments'
    
    _itemID = None
    _problemSetID = None
    _problemSetName = None
    _assignments = [] #list of tuples containing id, name, baseURL

    def saveToToken(self):
        token = super(SerializableAssistmentsItem, self).saveToToken()
        if self._itemID is not None:
            token[self.ITEM_ID_KEY] = tokenizeObject(self._itemID)
        if self._problemSetID is not None:
            token[self.PROBLEM_SET_ID_KEY] = tokenizeObject(self._problemSetID)
        if self._problemSetName is not None:
            token[self.PROBLEM_SET_NAME_KEY] = tokenizeObject(self._problemSetName)
        if self._assignments is not None:
            token[self.ASSIGNMENTS_KEY] = tokenizeObject(self._assignments)
        return token
    
    def initializeFromToken(self, token, context=None):
        super(SerializableAssistmentsItem, self).initializeFromToken(token, context)
        self._itemID = untokenizeObject(token.get(self.ITEM_ID_KEY, None))
        self._problemSetID = untokenizeObject(token.get(self.PROBLEM_SET_ID_KEY, None))
        self._problemSetName = untokenizeObject(token.get(self.PROBLEM_SET_NAME_KEY, None))
        self._assignments = untokenizeObject(token.get(self.ASSIGNMENTS_KEY, []))


#Does this need to be it's own separate table?
@DBObject(table_name="AssistmentsAssignmentItems")
class DBAssistmentsItem(DBSerializable):
    
    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableAssistmentsItem
    
    _itemID = Field('')
    _problemSetID = Field('')
    _problemSetName = Field('')
    _assignments = Field(list) #list of tuples containing id, name, baseURL
    
    
    def DBAssistmentsItem(self, serializableDBAssismentsAssignment = None):
        if serializableDBAssismentsAssignment is not None:
            self._itemID = serializableDBAssismentsAssignment._itemID
            self._problemSetID = serializableDBAssismentsAssignment._problemSetID
            self._problemSetName = serializableDBAssismentsAssignment._problemSetName
            self._assignments = serializableDBAssismentsAssignment._assignments
    
        
    def toSerializable(self):
        result = SerializableAssistmentsItem()
        
        result._itemID = self._itemID
        result._problemSetID = self._problemSetID
        result._problemSetName = self._problemSetName
        result._assignments = self._assignments 
        
        return result
    
    def saveToDB(self):
        self.save()

class SerializableTask(Serializable):

    # Main Keys
    TASK_ID_KEY = "taskId"
    IDS_KEY = "ids"
    NAME_KEY = "name"
    KCS_KEY = "kcs"
    BASE_URL_KEY = "baseURL"
    ASSISTMENTS_ITEM_KEY = "assistmentsItem"

    
    _taskId = None
    _ids = []
    _name = None
    _kcs = []
    _baseURL = None
    _assistmentsItem = None
    
    
    def saveToToken(self):
        token = super(SerializableTask, self).saveToToken()
        if self._taskId is not None:
            token[self.TASK_ID_KEY] = tokenizeObject(self._taskId)
        if self._ids is not None:
            token[self.IDS_KEY] = tokenizeObject(self._ids)
        if self._object is not None:
            token[self.NAME_KEY] = tokenizeObject(self._name)
        if self._result is not None:
            token[self.KCS_KEY] = tokenizeObject(self._kcs)
        if self._speechAct is not None:
            token[self.BASE_URL_KEY] = tokenizeObject(self._baseURL)
        if self._assistmentsItem is not None:
            token[self.ASSISTMENTS_ITEM_KEY] = tokenizeObject(self._assistmentsItem)
        return token
    
    def initializeFromToken(self, token, context=None):
        super(SerializableTask, self).initializeFromToken(token, context)
        self._taskId = untokenizeObject(token.get(self.TASK_ID_KEY, None))
        self._ids = untokenizeObject(token.get(self.IDS_KEY, []))
        self._name = untokenizeObject(token.get(self.NAME_KEY, None))
        self._kcs = untokenizeObject(token.get(self.KCS_KEY, []))
        self._baseURL = untokenizeObject(token.get(self.BASE_URL_KEY, None))
        self._assistmentsItem = untokenizeObject(token.get(self.ASSISTMENTS_ITEM_KEY), None)
        
    
    def toDB(self):
        result = DBTask()
        result.ids = self._ids
        result.id = self._taskId
        result.name = self._name
        result.kcs = self._kcs
        result.baseURL = self._baseURL
        result.assistmentsItem = self._assistmentsItem
        return result
    
    def initializeFromDBTask(self, dbTask):
        self._taskId = dbTask.id
        self._ids = dbTask.ids
        self._name = dbTask.name
        self._kcs = dbTask.kcs
        self._baseURL = dbTask.baseURL
        self._assistmentsItem = dbTask.assistmentsItem
                 
                     
@DBObject(table_name="Tasks")
class DBTask(DBSerializable):
    ids  = Field(list)
    name = Field('')
    kcs  = Field(list)
    baseURL  = Field('')
    assistmentsItem = Field('')
    
    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableTask
    
    def DBTask(self, serializableDBTask = None):
        if serializableDBTask is not None:
            self.id = serializableDBTask.taskID
            self.ids = serializableDBTask._ids
            self.name = serializableDBTask._name
            self.kcs = serializableDBTask._kcs
            self.baseURL = serializableDBTask._baseURL
            self.assistmentsItem = serializableDBTask._assistmentsItem
    
    def __repr__(self):
        return str(self.ids) + "|" + self.name + "|" + str(self.kcs) + "|" + self.baseURL
    
    
    def toSerializable(self):
        result = SerializableTask()
        result.initializeFromDBTask(self)
        return result
    
    def saveToDB(self):
        self.save()
        for kc in self.kcs:
            alias = DBKCTaskAssociations()
            alias.kc = kc
            alias.taskID = self.id
            alias.save()

    

@DBObject(table_name="KC_TaskAssociations")
class DBKCTaskAssociations(object):
    kc = Field('')
    taskID = Field('')
    
    @Index
    def kcIndex(self):
        return self.kc
        
        
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
        student = DBStudent.find_one(self.trueId)
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
        

@DBObject(table_name="ClassAliases")
class DBClasssAlias:
    trueId = Field('')
    alias  = Field('')
    
    @Index
    def AliasIndex(self):
        return self.alias
    
    def getClass(self):
        clazz = DBClass.find_one(self.trueId)
        return clazz
            
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