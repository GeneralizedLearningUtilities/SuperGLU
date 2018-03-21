import hashlib
from datetime import datetime
from icalendar import Calendar
from gludb.simple import DBObject, Field, Index
from SuperGLU.Util.Serialization import SuperGlu_Serializable, tokenizeObject, untokenizeObject, makeSerialized
from SuperGLU.Services.QueryService.Queries import getKCsForAGivenUserAndTask, getAllHintsForSingleUserAndTask, getAllFeedbackForSingleUserAndTask
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Util.SerializationGLUDB import DBSerializable, GLUDB_BRIDGE_NAME
from SuperGLU.Core.MessagingDB import DBLoggedMessage
from uuid import uuid4
import uuid

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
    DBKCTaskAssociations.ensure_table()
    DBAssistmentsItem.ensure_table()
    DBClasssAlias.ensure_table()
    DBLoggedMessage.ensure_table()
    DBCalendarData.ensure_table()


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
            self.taskCache = [DBTask.find_by_index("taskIdIndex", x)  for x in self.tasks]
        return self.taskCache

    def addTasks(self, newTask):
        if newTask is None:
            return #don't bother adding null values
        self.taskCache.append(newTask)
        if newTask.id is None:
            newTask.save()
        self.tasks.append(newTask.id)


class SerializableAssistmentsItem(SuperGlu_Serializable):

    #Keys
    ITEM_ID_KEY = 'itemId'
    PROBLEM_SET_ID_KEY = 'problemSetId'
    PROBLEM_SET_NAME_KEY = 'problemSetName'
    ASSIGNMENTS_KEY = 'assignments'
    ASSIGNMENT_NUMBER_KEY = "assignmentNumber"

    def __init__(self, itemId=None, problemSetId=None, problemSetName=None,
                 assignments=None, assignmentNumber=None, anId=None):
        super(SerializableAssistmentsItem, self).__init__(anId)
        if assignments is None: assignments = []
        self._itemId = itemId
        self._problemSetId = problemSetId
        self._problemSetName = problemSetName
        self._assignmentNumber = assignmentNumber
        #list of tuples containing id, name, url
        self._assignments = assignments

    def getActiveAssignmentURL(self):
        if (self._assignmentNumber < len(self._assignments) and
            len(self._assignments[self._assignmentNumber]) >= 3):
            return self._assignments[self._assignmentNumber][2]
        else:
            return None

    def saveToToken(self):
        token = super(SerializableAssistmentsItem, self).saveToToken()
        if self._assignmentNumber is not None:
            token[self.ASSIGNMENT_NUMBER_KEY] = tokenizeObject(self._assignmentNumber)
        if self._itemId is not None:
            token[self.ITEM_ID_KEY] = tokenizeObject(self._itemId)
        if self._problemSetId is not None:
            token[self.PROBLEM_SET_ID_KEY] = tokenizeObject(self._problemSetId)
        if self._problemSetName is not None:
            token[self.PROBLEM_SET_NAME_KEY] = tokenizeObject(self._problemSetName)
        if self._assignments is not None:
            token[self.ASSIGNMENTS_KEY] = tokenizeObject(self._assignments)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableAssistmentsItem, self).initializeFromToken(token, context)
        self._assignmentNumber = untokenizeObject(token.get(self.ASSIGNMENT_NUMBER_KEY, None), context)
        self._itemId = untokenizeObject(token.get(self.ITEM_ID_KEY, None), context)
        self._problemSetId = untokenizeObject(token.get(self.PROBLEM_SET_ID_KEY, None), context)
        self._problemSetName = untokenizeObject(token.get(self.PROBLEM_SET_NAME_KEY, None), context)
        self._assignments = untokenizeObject(token.get(self.ASSIGNMENTS_KEY, []), context)

    def __repr__(self):
        return self._itemId + "|||" + self._problemSetId + "|||" + self._problemSetName + "|||" + str(self._assignments) + "|||" + str(self._assignmentNumber)

@DBObject(table_name="AssistmentsAssignmentItems")
class DBAssistmentsItem(DBSerializable):

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableAssistmentsItem

    _itemId = Field('')
    _problemSetId = Field('')
    _problemSetName = Field('')
    _assignments = Field(list) #list of tuples containing id, name, baseURL


    @Index
    def itemIdIndex(self):
        return self._itemId

    def create(self, serializableDBAssismentsAssignment = None):
        if serializableDBAssismentsAssignment is not None:
            self._itemId = serializableDBAssismentsAssignment._itemId
            self._problemSetId = serializableDBAssismentsAssignment._problemSetId
            self._problemSetName = serializableDBAssismentsAssignment._problemSetName
            self._assignments = serializableDBAssismentsAssignment._assignments

        return self


    def __repr__(self):
        return self._itemId + "|||" + self._problemSetId + "|||" + self._problemSetName + "|||" + str(self._assignments)

    def toSerializable(self):
        result = SerializableAssistmentsItem()

        result._itemId = self._itemId
        result._problemSetId = self._problemSetId
        result._problemSetName = self._problemSetName
        result._assignments = self._assignments

        return result

    def saveToDB(self):
        self.save()

class LearningTask(SuperGlu_Serializable):

    # Main Keys
    TASK_ID_KEY = "taskId"
    SYSTEM_KEY = "system"
    ALIAS_IDS_KEY = "aliasIds"
    NAME_KEY = "name"
    DISPLAY_NAME_KEY = "displayName"
    KCS_KEY = "kcs"
    BASE_URL_KEY = "baseURL"
    ASSISTMENTS_ITEM_KEY = "assistmentsItem"
    DESCRIPTION_KEY = "description"
    CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY = "canBeRecommendedIndividually"
    SUBTASKS_KEY ="subtasks"

    def __init__(self, taskId=None, aliasIds=None, name=None, displayName=None, description=None,
                 system=None, subtasks=None, kcs=None, baseURL=None, assistmentsItem=None,
                 canRecommendIndividually = True, anId=None):
        super(LearningTask, self).__init__(anId)
        if aliasIds is None: aliasIds = []
        if subtasks is None: subtasks = []
        if kcs is None: kcs = []
        self._taskId = taskId
        self._aliasIds = aliasIds
        self._name = name
        self._displayName = displayName
        self._description = description
        self._system = system
        self._subtasks = subtasks
        self._kcs = kcs
        self._baseURL = baseURL
        self._assistmentsItem = assistmentsItem
        self._canBeRecommendedIndividually = canRecommendIndividually

    def saveToToken(self):
        token = super(LearningTask, self).saveToToken()
        if self._taskId is not None:
            token[self.TASK_ID_KEY] = tokenizeObject(self._taskId)
        if self._aliasIds is not None:
            token[self.ALIAS_IDS_KEY] = tokenizeObject(self._aliasIds)
        if self._name is not None:
            token[self.NAME_KEY] = tokenizeObject(self._name)
        if self._displayName is not None:
            token[self.DISPLAY_NAME_KEY] = tokenizeObject(self._displayName)
        if self._system is not None:
            token[self.SYSTEM_KEY] = tokenizeObject(self._system)
        if self._subtasks is not []:
            token[self.SUBTASKS_KEY] = tokenizeObject(self._subtasks)
        if self._kcs is not None:
            token[self.KCS_KEY] = tokenizeObject(self._kcs)
        if self._baseURL is not None:
            token[self.BASE_URL_KEY] = tokenizeObject(self._baseURL)
        if self._assistmentsItem is not None:
            token[self.ASSISTMENTS_ITEM_KEY] = tokenizeObject(self._assistmentsItem)
        if self._description is not None:
            token[self.DESCRIPTION_KEY] = tokenizeObject(self._description)
        if self._canBeRecommendedIndividually is not None:
            token[self.CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY] = tokenizeObject(self._canBeRecommendedIndividually)
        return token

    def initializeFromToken(self, token, context=None):
        super(LearningTask, self).initializeFromToken(token, context)
        self._taskId = untokenizeObject(token.get(self.TASK_ID_KEY, None), context)
        self._aliasIds = untokenizeObject(token.get(self.ALIAS_IDS_KEY, []), context)
        self._name = untokenizeObject(token.get(self.NAME_KEY, None))
        self._displayName = untokenizeObject(token.get(self.DISPLAY_NAME_KEY, None), context)
        self._description = untokenizeObject(token.get(self.DESCRIPTION_KEY, None), context)
        self._system = untokenizeObject(token.get(self.SYSTEM_KEY, None), context)
        self._subtasks = untokenizeObject(token.get(self.SUBTASKS_KEY, []), context)
        self._kcs = untokenizeObject(token.get(self.KCS_KEY, []), context)
        self._baseURL = untokenizeObject(token.get(self.BASE_URL_KEY, None), context)
        self._assistmentsItem = untokenizeObject(token.get(self.ASSISTMENTS_ITEM_KEY, None), context)
        self._canBeRecommendedIndividually = untokenizeObject(token.get(self.CAN_BE_RECOMMENDED_INDIVIDUALLY_KEY, True), context)

    def toDB(self):
        result = DBTask()
        result.system = self._system
        result.ids = self._aliasIds
        result.subtasks = self._subtasks
        result.taskId = self._taskId
        result.name = self._name
        result.displayName = self._displayName
        result.kcs = self._kcs
        result.baseURL = self._baseURL
        result.assistmentsItemCache = self._assistmentsItem
        result.description = self._description
        result.canBeRecommendedIndividually = self._canBeRecommendedIndividually
        return result

    def initializeFromDBTask(self, dbTask):
        self._taskId = dbTask.taskId
        self._aliasIds = dbTask.ids
        self._subtasks = dbTask.subtasks
        self._name = dbTask.name
        self._displayName = dbTask.displayName
        self._kcs = dbTask.kcs
        self._baseURL = dbTask.baseURL
        self._system = dbTask.system
        if dbTask.assistmentsItemCache is not None:
            self._assistmentsItem = dbTask.assistmentsItemCache.toSerializable()
        else:
            self._assistmentsItem = None
        self._description = dbTask.description
        self._canBeRecommendedIndividually = dbTask.canBeRecommendedIndividually

    # TODO: Figure out why we need this as such, rather than __str__?
    def __repr__(self):
        return "taskId:{0}|ids:{1}|subtasks:{2}|name:{3}|kcs:{4}|baseURL:{5}|assistmentItem:{6}|description:{7}|individualRecommend:{8}|displayName:{9}".format(
            self._taskId, self._aliasIds, self._subtasks, self._name, self._kcs, self._baseURL,
            self._assistmentsItem, self._description, self._canBeRecommendedIndividually, self._displayName)


@DBObject(table_name="Tasks")
class DBTask(DBSerializable):
    ids  = Field(list)
    system = Field('')
    subtasks = Field(list)
    taskId = Field('')
    name = Field('')
    displayName = Field('')
    kcs  = Field(list)
    baseURL  = Field('')
    assistmentsItemId = Field('')
    description = Field('')
    canBeRecommendedIndividually = Field(True)

    assistmentsItemCache = None

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = LearningTask

    def create(self, serializableDBTask = None):
        logInfo("found DBTask constructor", 5)
        if serializableDBTask is not None:
            self.taskId = serializableDBTask._taskId
            self.system = serializableDBTask._system
            self.ids = serializableDBTask._aliasIds
            self.subtasks = serializableDBTask._subtasks
            self.name = serializableDBTask._name
            self.displayName = serializableDBTask._displayName
            self.kcs = serializableDBTask._kcs
            self.baseURL = serializableDBTask._baseURL
            if serializableDBTask._assistmentsItem is not None:
                self.assistmentsItemCache = DBSerializable.convert(serializableDBTask._assistmentsItem)
                self.assistmentsItemId = serializableDBTask._assistmentsItem.getId()
            else:
                self.assistmentsItemCache = None
                self.assistmentsItemId = None
            self.description = serializableDBTask._description
            self.canBeRecommendedIndividually = serializableDBTask._canBeRecommendedIndividually
        return self

    def getAssistementsItem(self, useCachedValue=False):
        if not useCachedValue:
            logInfo("assistmentItemId={0}".format(self.assistmentsItemId), 6)
            if self.assistmentsItemId is not None:
                return DBAssistmentsItem.find_one(self.assistmentsItemId)
            else:
                return None
        else:
            return self.assistmentsItemCache

    def __repr__(self):
        return str(self.ids) + "|" + self.name + "|" + str(self.kcs) + "|" + self.baseURL

    @Index
    def nameIndex(self):
        return self.name

    @Index
    def taskIdIndex(self):
        return self.taskId

    def toSerializable(self):
        if self.assistmentsItemCache is None:
            self.assistmentsItemCache = self.getAssistementsItem(True)
        result = LearningTask()
        result.initializeFromDBTask(self)
        return result

    def saveToDB(self):
        existingTasksWithSameName = DBTask.find_by_index('nameIndex', self.name)
        existingTask = None
        logInfo("assistmentsItemcacheValue2 = {0}".format(self.assistmentsItemCache), 6)
        for possibleExistingTask in existingTasksWithSameName:
            if self.ids == possibleExistingTask.ids:
                existingTask = possibleExistingTask

        if existingTask is None:
            logInfo("task with name {0} does not yet exist".format(self.name), 3)
            if self.assistmentsItemCache:
                self.assistmentsItemCache.saveToDB()
                self.assistmentsItemId = self.assistmentsItemCache.id
            logInfo("assistmentsItemId = {0}".format(self.assistmentsItemId), 6)
            logInfo("assistmentsItemcacheValue4 = {0}".format(self.assistmentsItemCache), 6)
            self.save()
            for kc in self.kcs:#TODO: figure out what tod do with these
                alias = DBKCTaskAssociations()
                alias.kc = kc
                alias.taskId = self.id
                alias.save()

        else:
            logInfo("task with name {0} already exists, overwriting".format(self.name), 3)
            existingTask.name = self.name
            existingTask.displayName = self.displayName
            existingTask.ids = self.ids
            existingTask.kcs = self.kcs
            existingTask.baseURL = self.baseURL
            existingTask.description = self.description
            existingTask.canBeRecommendedIndividually = self.canBeRecommendedIndividually

            self.assistmentsItemCache.id = existingTask.assistmentsItemId
            existingTask.assistmentsItemCache = self.assistmentsItemCache
            if existingTask.assistmentsItemCache:
                existingTask.assistmentsItemCache.saveToDB()
            existingTask.assistmentsItemId = existingTask.assistmentsItemCache.id
            logInfo("assistmentsItemcacheValue3 = {0}".format(existingTask.assistmentsItemCache), 6)
            logInfo("assistmentsItemId = {0}".format(existingTask.assistmentsItemId), 6)
            existingTask.save()

        return self.id


@DBObject(table_name="KC_TaskAssociations")
class DBKCTaskAssociations(object):
    kc = Field('')
    taskId = Field('')

    @Index
    def kcIndex(self):
        return self.kc

    @Index
    def taskIdIndex(self):
        return self.taskId


class SerializableTopic(SuperGlu_Serializable):
    # Main Keys
    TOPIC_ID_KEY = "topicId"
    TOPIC_DESCRIPTION_KEY = "topicDescription"
    KC_LIST_KEY = "kcList"
    RESOURCE_LIST_KEY = "resourceList"

    topicId = ''
    description = ''
    kcList       = []
    resourceList = []

    def __init__(self, topicId = None, description=None,  kcList = None, resourceList = None, anId=None):
        super(SerializableTopic, self).__init__(anId)

        if topicId == None:
            topicId = ''
        if kcList == None:
            kcList = []
        if resourceList == None:
            resourceList = []

        self.topicId = topicId
        self.kcList = kcList
        self.description = description
        self.resourceList = resourceList


    def saveToToken(self):
        token = super(SerializableTopic, self).saveToToken()
        if self.topicId is not None:
            token[self.TOPIC_ID_KEY] = tokenizeObject(self.topicId)
        if self.description is not None:
            token[self.TOPIC_DESCRIPTION_KEY] = tokenizeObject(self.description)
        if self.kcList is not None:
            token[self.KC_LIST_KEY] = tokenizeObject(self.kcList)
        if self.resourceList is not None:
            token[self.RESOURCE_LIST_KEY] = tokenizeObject(self.resourceList)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableTopic, self).initializeFromToken(token, context)
        self.description = untokenizeObject(token.get(self.TOPIC_DESCRIPTION_KEY, None))
        self.topicId = untokenizeObject(token.get(self.TOPIC_ID_KEY, None), context)
        self.kcList = untokenizeObject(token.get(self.KC_LIST_KEY, []), context)
        self.resourceList = untokenizeObject(token.get(self.RESOURCE_LIST_KEY, []))


    def toDB(self):
        result = DBTopic()
        result.topicId = self.topicId
        result.kcList = self.kcList
        result.description = self.description
        result.resourceList = self.resourceList
        return result

    def initializeFromDBTopic(self, dbTopic):
        self.topicId = dbTopic.topicId
        self.kcList = dbTopic.kcList
        self.description = dbTopic.description
        self.resourceList = dbTopic.resourceList


@DBObject(table_name="Topics")
class DBTopic(DBSerializable):

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableTopic

    topicId      = Field('')
    description  = Field('')
    kcList       = Field(list)
    resourceList = Field(list)

    def create(self, serializableTopic = None):
        if serializableTopic is not None:
            self.kcList = serializableTopic.kcList
            self.resourceList = serializableTopic.resourceList
            self.topicId = serializableTopic.topicId
            self.description = serializableTopic.description
        return self


    @Index
    def topicIdIndex(self):
        return self.topicId

    def toSerializable(self):
        result = SerializableTopic()
        result.initializeFromDBTask(self)
        return result

    def saveToDB(self):
        self.save()

    def __repr__(self):
        return str(self.kcList) + "|" + str(self.resourceList)


class SerializableSession(SuperGlu_Serializable):

    SESSION_ID_KEY = "sessionId"
    STUDENTS_KEY = "students"
    SYSTEM_KEY = "system"
    TASK_KEY = "task"
    ASSIGNMENT_NUMBER_KEY = "assignmentNumber"
    START_TIME_KEY = "startTime"
    DURATION_KEY = "duration"
    END_CONDITION_KEY = "endCondition"
    PERFORMANCE_KEY ="performance"
    CLASSROOM_ID_KEY = "classroomId"
    HINTS_KEY = "hints"
    FEEDBACK_KEY = "feedback"
    MESSAGE_IDS_KEY = "messageIds"
    SOURCE_DATA_N_KEY = "sourceDataN"
    SOURCE_DATA_HASH_KEY = "sourceDataHash"

    def __init__(self, sessionId = None, students=[],  system = None, task = None, assignmentNumber=0, startTime = None, duration = None, endCondition = None,
                   performance={}, classroomId=None, hints=[], feedback=[], messageIds = [], sourceDataN = -1, sourceDataHash = -1):
        super(SerializableSession, self).__init__(sessionId)
        self.sessionId = sessionId
        self.students = students
        self.system = system
        self.task = task
        self.assignmentNumber = assignmentNumber
        self.startTime = startTime
        self.duration = duration
        self.endCondition  = endCondition
        self.performance = performance
        self.classroomId = classroomId
        self.hints = hints
        self.feedback = feedback
        self.messageIds = messageIds
        self.sourceDataN = sourceDataN
        self.sourceDataHash = sourceDataHash

    def saveToToken(self):
        token = super(SerializableSession, self).saveToToken()
        if self.sessionId is not None:
            token[self.SESSION_ID_KEY] = tokenizeObject(self.sessionId)
        if self.students is not None:
            token[self.STUDENTS_KEY] = tokenizeObject(self.students)
        if self.system is not None:
            token[self.SYSTEM_KEY] = tokenizeObject(self.system)
        if self.task is not None:
            token[self.TASK_KEY] = tokenizeObject(self.task)
        if self.assignmentNumber is not None:
            token[self.ASSIGNMENT_NUMBER_KEY] = tokenizeObject(self.assignmentNumber)
        if self.startTime is not None:
            token[self.START_TIME_KEY] = tokenizeObject(self.startTime)
        if self.duration is not None:
            token[self.DURATION_KEY] = tokenizeObject(self.duration)
        if self.endCondition is not None:
            token[self.END_CONDITION_KEY] = tokenizeObject(self.endCondition)
        if self.performance is not None:
            token[self.PERFORMANCE_KEY] = tokenizeObject(self.performance)
        if self.classroomId is not None:
            token[self.CLASSROOM_ID_KEY] = tokenizeObject(self.classroomId)
        if self.hints is not None:
            token[self.HINTS_KEY] = tokenizeObject(self.hints)
        if self.feedback is not None:
            token[self.FEEDBACK_KEY] = tokenizeObject(self.feedback)
        if self.messageIds is not None:
            token[self.MESSAGE_IDS_KEY] = tokenizeObject(self.messageIds)
        if self.sourceDataN is not None:
            token[self.SOURCE_DATA_N_KEY] = tokenizeObject(self.sourceDataN)
        if self.sourceDataHash is not None:
            token[self.SOURCE_DATA_HASH_KEY] = tokenizeObject(self.sourceDataHash)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableSession, self).initializeFromToken(token, context)
        self.sessionId = untokenizeObject(token.get(self.SESSION_ID_KEY, None))
        self.students = untokenizeObject(token.get(self.students, []), context)
        self.system = untokenizeObject(token.get(self.SYSTEM_KEY, None), context)
        self.task = untokenizeObject(token.get(self.TASK_KEY, None))
        self.assignmentNumber = untokenizeObject(token.get(self.ASSIGNMENT_NUMBER_KEY, 0), context)
        self.startTime = untokenizeObject(token.get(self.START_TIME_KEY, None), context)
        self.duration = untokenizeObject(token.get(self.DURATION_KEY, 0), context)
        self.endCondition = untokenizeObject(token.get(self.END_CONDITION_KEY, None), context)
        self.performance = untokenizeObject(token.get(self.PERFORMANCE_KEY, None), context)
        self.classroomId = untokenizeObject(token.get(self.CLASSROOM_ID_KEY, None), context)
        self.hints = untokenizeObject(token.get(self.HINTS_KEY, []), context)
        self.feedback = untokenizeObject(token.get(self.FEEDBACK_KEY, []), context)
        self.messageIds = untokenizeObject(token.get(self.MESSAGE_IDS_KEY, []), context)
        self.sourceDataN = untokenizeObject(token.get(self.SOURCE_DATA_N_KEY, None), context)
        self.sourceDataHash = untokenizeObject(token.get(self.SOURCE_DATA_HASH_KEY, None), context)

    def toDB(self):
        result = DBSession()
        result.sessionId = self.sessionId
        result.students = self.students
        if self.task is not None:
            self.task.Save()
            result.task = self.taskId
        result.assignmentNumber = self.assignmentNumber
        result.startTime = self.startTime
        result.duration = self.duration
        result.endCondition = self.endCondition
        result.performance = self.performance
        result.classId = self.classroomId
        result.hints = self.hints
        result.feedback = self.feedback
        result.messageIds = self.messageIds
        result.sourceDataN = self.sourceDataN
        result.sourceDataHash = self.sourceDataHash
        return result

    def initializeFromDBSession(self, dbSession):
        self.sessionId = dbSession.sessionId
        self.students = dbSession.students
        self.assignmentNumber = dbSession.assignmentNumber

        dbTaskList = DBTask.find_by_index("taskIdIndex", dbSession.task)
        if len(dbTaskList) > 0:
            self.task = dbTaskList[0].toSerializable()

        self.startTime = dbSession.startTime
        self.duration = dbSession.duration
        self.endCondition = dbSession.endCondition
        self.performance = dbSession.performance
        self.classroomId = dbSession.classId
        self.hints = dbSession.hints
        self.feedback = dbSession.feedback
        self.messageIds = dbSession.messageIds
        self.sourceDataN = dbSession.sourceDataN
        self.sourceDataHash = dbSession.sourceDataHash



@DBObject(table_name="Sessions")
class DBSession(DBSerializable):
    sessionId      = Field('')
    students       = Field(list)
    system         = Field('')
    task           = Field('')
    assignmentNumber= Field('')
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

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableSession

    #Non-persistent Fields
    studentCache = []
    taskCache = None

    def create(self, serializableSession = None):
        if serializableSession is not None:
            self.sessionId = serializableSession.sessionId
            self.students = serializableSession.students
            self.system = serializableSession.system
            self.task = serializableSession.task.taskId
            self.assignmentNumber = serializableSession.assignmentNumber
            self.startTime = serializableSession.startTime
            self.duration = serializableSession.duration
            self.endCondition = serializableSession.endCondition
            self.performance = serializableSession.performance
            self.classId = serializableSession.classId
            self.hints = serializableSession.hints
            self.feedback = serializableSession.feedback
            self.messageIds = serializableSession.messageIds
            self.sourceDataN = serializableSession.sourceDataN
            self.sourceDataHash = serializableSession.sourceDataHash
        return self

    #keeping this method here as an example of how to query based on UUID
    @classmethod
    def getSessionFromUUID(self, sessionId):
        return DBSession.find_one(sessionId)

    @Index
    def SessionIdIndex(self):
        return self.sessionId


    def getTask(self, useCachedValue = False):
        if self.task is None or self.task == '':
            return None

        if not useCachedValue:
            listOfValues = DBTask.find_by_index("taskIdIndex", self.task)
            if len(listOfValues) > 0:
                self.taskCache = listOfValues[0]
        return self.taskCache

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

    def toSerializable(self):
        result = SerializableSession()
        result.initializeFromDBSession(self)
        return result

class SerializableStudent(SuperGlu_Serializable):

    STUDENT_ID_KEY = "studentId"
    SESSIONS_KEY = "sessions"
    OAUTH_IDS_KEY = "oAuthIds"
    STUDENT_MODELS_KEY = "studentModels"
    KC_GOALS_KEY = "kcGoals"

    studentId       = None
    sessions      = []
    oAuthIds        = {}
    studentModels = {}
    kcGoals         = {}


    def saveToToken(self):
        token = super(SerializableStudent, self).saveToToken()
        if self.studentId is not None:
            token[self.STUDENT_ID_KEY] = tokenizeObject(self.studentId)
        if self.sessions is not []:
            token[self.SESSIONS_KEY] = tokenizeObject(self.sessions)
        if self.oAuthIds is not {}:
            token[self.OAUTH_IDS_KEY] = tokenizeObject(self.oAuthIds)
        if self.studentModelIds is not {}:
            token[self.STUDENT_MODELS_KEY] = tokenizeObject(self.studentModels)
        if self.kcGoals is not {}:
            token[self.KC_GOALS_KEY] = tokenizeObject(self.kcGoals)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableStudent, self).initializeFromToken(token, context)
        self.studentId = untokenizeObject(token.get(self.STUDENT_ID_KEY, None))
        self.sessions = untokenizeObject(token.get(self.SESSIONS_KEY, []), context)
        self.oAuthIds = untokenizeObject(token.get(self.OAUTH_IDS_KEY,{}), context)
        self.studentModels = untokenizeObject(token.get(self.STUDENT_MODELS_KEY, {}), context)
        self.kcGoals = untokenizeObject(token.get(self.KC_GOALS_KEY, {}))

    def toDB(self):
        result = DBStudent()
        result.studentId = self.studentId
        result.sessionIds = [x.id for x in self.sessions]
        result.oAuthIds = self.oAuthIds
        result.studentModelIds = [x.id for x in self.studentModels]
        result.kcGoals = self.kcGoals
        return result

    def initializeFromDBTask(self, dbStudent):
        self.studentId = dbStudent.studentId
        self.sessions = [x.toSerializable() for x in dbStudent.getSessions(False)]
        self.oAuthIds = dbStudent.oAuthIds
        self.studentModelIds = dbStudent.getStudentModels()
        self.kcGoals = dbStudent.kcGoals




@DBObject(table_name="Students")
class DBStudent (object):

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableStudent

    studentId       = Field('')
    sessionIds      = Field(list)
    oAuthIds        = Field(dict)
    studentModelIds = Field(dict)
    kcGoals         = Field(dict)

    #non-persistant fields
    sessionCache = []
    # One per each subclass of student model allowed
    studentModelCache = {}

    @Index
    def StudentIdIndex(self):
        return self.studentId

    def getSessions(self, useCachedValue = False):
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

    def getStudentModels(self, useCachedValue = False):
        if not useCachedValue:
            self.studentModelCache = {x:DBStudentModel.find_one(self.studentModelIds[x]) for x in self.studentModelIds.keys()}
        return self.studentModelCache

    def addStudentModel(self, newStudentModel):
        logInfo("Entering DBStudent.addStudentModel", 5)
        if newStudentModel is None:
            return
        if newStudentModel.id is None or newStudentModel.id is '':
            newStudentModel.save()

        self.studentModelCache[newStudentModel.id] = newStudentModel
        if self.studentModelIds is None or isinstance(self.studentModelIds, list):
            self.studentModelIds = {}
        self.studentModelIds[newStudentModel.__class__.__name__] = newStudentModel.id
        self.save()


    def toSerializable(self):
        result = SerializableStudent()
        result.initializeFromDBTask(self)
        return result


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
    def Alias2Index(self):
        return self.alias

    def getClass(self):
        clazz = DBClass.find_one(self.trueId)
        return clazz


class SerializableStudentModel(SuperGlu_Serializable):
    # Main Keys
    STUDENT_ID_KEY = "studentId"
    KC_MASTERY_KEY = "kcMastery"


    _studentId = None
    _kcMastery = {}


    def saveToToken(self):
        token = super(SerializableStudentModel, self).saveToToken()
        if self._studentId is not None:
            token[self.STUDENT_ID_KEY] = tokenizeObject(self._studentId)
        if self._kcMastery is not None:
            token[self.KC_MASTERY_KEY] = tokenizeObject(self._kcMastery)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableStudentModel, self).initializeFromToken(token, context)
        self._studentId = untokenizeObject(token.get(self.STUDENT_ID_KEY, None))
        self._kcMastery = untokenizeObject(token.get(self.KC_MASTERY_KEY, {}))

    def toDB(self):
        result = DBStudentModel()
        result.studentId = self._studentId
        result.kcMastery = self._kcMastery
        return result

    def initializeFromDBTask(self, dbTask):
        self._studentId = dbTask.studentId
        self._kcMastery = dbTask.kcMastery



@DBObject(table_name="StudentModels")
class DBStudentModel (object):

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableStudentModel

    studentId = Field('') #string
    kcMastery = Field(dict) #Dictionary<string, float>

    studentCache = None #type:DBStudent

    @Index
    def studentIdIndex(self):
        return self.studentId

    def getStudent(self, useCachedValue= False):
        if self.studentId is not '':
            if not useCachedValue:
                self.studentCache = DBStudent.find_one(self.studentId)
            return self.studentCache
        else:
            return None

    def toSerializable(self):
        result = SerializableStudentModel()
        result.initializeFromDBTask(self)
        return result

    def saveToDB(self):#TODO: test before using widely
        self.save()



@DBObject(table_name="ClassModels")
class DBClassModel(object):
    studentIds = Field(list)
    kcMastery  = Field(dict)

    def getStudents(self, useCachedValue = False):
        if not useCachedValue:
            self.studentCache = [DBStudent.find_one(x) for x in self.students]
        return self.studentCache


#Owner Type enum:
CLASS_OWNER_TYPE = "class"
STUDENT_OWNER_TYPE = "student"

#Access Permissions enum:
PUBLIC_PERMISSION = "public"
MEMBERS_PERMISSION = "members"
OWNER_ONLY_PERMISSION = "owner only"

class SerializableCalendarData(SuperGlu_Serializable):

    # Main Keys
    OWNER_ID_KEY = "ownerId"
    OWNER_TYPE_KEY = "ownerType"
    PERMISSIONS_KEY = "permissions"
    CALENDAR_DATA_KEY = "calendarData"


    #string
    ownerId = None

    #string (values = {class, student})
    ownerType = None

    #string
    accessPermissions = None

    #ical string
    calendarData = None


    def getICalObject(self):
        return Calendar.from_ical(self.calendarData)


    def setICalObject(self, ical):
        self.calendarData = ical.to_ical()


    def saveToToken(self):
        token = super(SerializableCalendarData, self).saveToToken()
        if self.ownerId is not None:
            token[self.OWNER_ID_KEY] = tokenizeObject(self.ownerId)
        if self.ownerType is not None:
            token[self.OWNER_TYPE_KEY] = tokenizeObject(self.ownerType)
        if self.accessPermissions is not None:
            token[self.PERMISSIONS_KEY] = tokenizeObject(self.accessPermissions)
        if self.calendarData is not None:
            token[self.CALENDAR_DATA_KEY] = tokenizeObject(self.calendarData)
        return token

    def initializeFromToken(self, token, context=None):
        super(SerializableCalendarData, self).initializeFromToken(token, context)
        self.ownerId = untokenizeObject(token.get(self.OWNER_ID_KEY, None))
        self.ownerType = untokenizeObject(token.get(self.OWNER_TYPE_KEY, None))
        self.calendarData = untokenizeObject(token.get(self.CALENDAR_DATA_KEY, None))
        self.accessPermissions = untokenizeObject(token.get(self.PERMISSIONS_KEY, None))

    def toDB(self):
        result = DBCalendarData()
        result.ownerId = self.ownerId
        result.ownerType = self.ownerType
        result.calendarData = self.calendarData
        result.accessPermissions = self.accessPermissions
        return result

    def initializeFromDBCalendarData(self, dbCalendarData):
        self.ownerId = dbCalendarData.ownerId
        self.ownerType = dbCalendarData.ownerType
        self.calendarData = dbCalendarData.calendarData
        self.accessPermissions = dbCalendarData.accessPermissions


@DBObject(table_name="CalendarData")
class DBCalendarData(object):

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SerializableCalendarData

    ownerId = Field('')
    ownerType = Field('')
    calendarData = Field('')
    accessPermissions = Field('')

    #transactional storage (for the future)
    #list stores tuples containing (date, calendarData)
    #calendarHistory = Field(list)

    def setCalendarData(self, ownerId=None, ownerType=None, permissions=None, data=None):
        if ownerType is None: ownerType = STUDENT_OWNER_TYPE
        if permissions is None: permissions = PUBLIC_PERMISSION
        self.ownerId = ownerId
        self.ownerType = ownerType
        self.accessPermissions = permissions
        self.calendarData = data

    ####Place Index data here####
    @Index
    def ownerIdIndex(self):
        return self.ownerId


    def toSerializable(self):
        result = SerializableCalendarData()
        result.initializeFromDBCalendarData(self)
        return result

    def saveToDB(self):#TODO: test before using widely
        self.save()
