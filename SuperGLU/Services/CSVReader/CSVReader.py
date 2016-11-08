'''
Created on Mar 18, 2016
This module is responsible for converting the tasks csv file to tasks objects and sends them out to the storage service
@author: auerbach
'''
import csv
import io
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.StudentModel.PersistentData import LearningTask, SerializableAssistmentsItem, DBAssistmentsItem, DBTask
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.Messaging import Message
from SuperGLU.Services.StorageService.Storage_Service_Interface import VALUE_VERB, STORAGE_SERVICE_NAME
from SuperGLU.Util.Serialization import serializeObject
from SuperGLU.Core.MessagingDB import ELECTRONIX_TUTOR_TASK_UPLOAD_VERB


CSV_READER_SERVICE_NAME = "CSV Reader Service"
TASKS_OBJECT = "tasks"

SYSTEM_COL_NAME = "System"
TASK_ID_COL_NAME = "Problem ID (Name)"
TASK_DISPLAY_COL_NAME = "Problem Display Name"
DESCRIPTION_COL_NAME = "Description"
TOPIC_COL_NAME = "Topic"
TYPE_COL_NAME = "Type"
DATE_COL_NAME = "Curriculum Week+Day"
BASE_URL_COL_NAME = "Base Link (Original)"
KC_SET_COL_NAME = "KC Set"
ASSISTMENTS_PROB_ID_COL_NAME = "ASSISTments Problem ID (Single Item)"
ASSISTMENTS_SET_ID_COL_NAME = "ASSISTments Problem Set ID"
ASSISTMENTS_SET_NAME_COL_NAME = "ASSISTments Problem Set Name"
ASSISTMENTS_ASSIGN_COL_NAMES =("ASSISTments Assign 1 URL", "ASSISTments Assign 2 URL",
                               "ASSISTments Set 3 URL")
ENABLED_COL_NAME = "Enabled"

class CSVReader (BaseService):
    
    LINE_DELIMITER = '\n'
    CELL_DELIMITER = ','
    PIPE_DELIMITER = '|||'
    
    def receiveMessage(self, msg):
        #depending on the content of the message react differently
        #logInfo('Entering CSVReader.receiveMessage', 5)
        
        reply = None
        #Only considering 
        if msg.getSpeechAct() == INFORM_ACT:
        
            if msg.getVerb() == ELECTRONIX_TUTOR_TASK_UPLOAD_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(CSV_READER_SERVICE_NAME, ELECTRONIX_TUTOR_TASK_UPLOAD_VERB, INFORM_ACT), 4)
                csvString = msg.getResult()
                taskList = self.processCSVFile(csvString)
                print("STORAGE SERVICE NAME: %s"%(STORAGE_SERVICE_NAME))
                reply = Message(STORAGE_SERVICE_NAME, VALUE_VERB, TASKS_OBJECT, taskList)
        
        if msg.getSpeechAct() == REQUEST_ACT:
            if msg.getVerb() == ELECTRONIX_TUTOR_TASK_UPLOAD_VERB:
                dbtaskList = DBTask.find_all()
                dbassistmentItemsList = DBAssistmentsItem.find_all()
                
                for dbTask in dbtaskList:
                    if dbTask.assistmentsItemId is not None and dbTask.assistmentsItemId is not '':
                        for dbassistmentsItem in dbassistmentItemsList:
                            if  dbassistmentsItem.id == dbTask.assistmentsItemId:
                                dbTask.assistmentsItemCache = dbassistmentsItem
                                break
                
                taskList = [x.toSerializable() for x in dbtaskList]
                reply = Message(CSV_READER_SERVICE_NAME, ELECTRONIX_TUTOR_TASK_UPLOAD_VERB, None, taskList, INFORM_ACT, msg.getContext())
        
        if reply is not None:
            logInfo('{0} is broadcasting a {1}, {2} message'.format(CSV_READER_SERVICE_NAME, INFORM_ACT, VALUE_VERB), 4)
            self.sendMessage(reply)

    def hasCellData(self, s):
        return s is not None and s != ''
    
    def processCSVFile(self, csvString):
        #List of strings
        dictLines = csv.DictReader(io.StringIO(csvString))
        lines = [a for a in dictLines]
        
        relatedTasks = dict()
        #list of tasks
        result = []

        for row in lines:
            # Extract Row Data
            systemId = row.get(SYSTEM_COL_NAME, '')
            taskId = row.get(TASK_ID_COL_NAME, '')
            taskDisplayName = row.get(TASK_DISPLAY_COL_NAME, '')
            description = row.get(DESCRIPTION_COL_NAME, '')
            baseURL = row.get(BASE_URL_COL_NAME, '')
            assistmentsItemId = row.get(ASSISTMENTS_PROB_ID_COL_NAME, '') 
            assistmentsSetId = row.get(ASSISTMENTS_SET_ID_COL_NAME, '')
            assistmentsSetName = row.get(ASSISTMENTS_SET_NAME_COL_NAME, '')
            kcCell = row.get(KC_SET_COL_NAME, '')
                
            isEnabled = True
            if row.get(ENABLED_COL_NAME, 'True') == 'FALSE':
                isEnabled = False
        
            if isEnabled and (self.hasCellData(taskId) or self.hasCellData(taskDisplayName)):
                # Create the Task
                # logInfo('{0} is constructing the next serializable task object'.format(CSV_READER_SERVICE_NAME), 5)
                task = LearningTask()
                task._aliasIds = []
                task._system = systemId
                # logInfo('{0} is extracting the knowledge components'.format(CSV_READER_SERVICE_NAME), 5)
                task._kcs = [a for a in kcCell.split(self.PIPE_DELIMITER) if a != '']

                task._taskId = taskId
                task._name = taskDisplayName
                if not self.hasCellData(taskDisplayName):
                    task._name = task._taskId
                elif not self.hasCellData(taskId):
                    task._taskId = taskId

                task._displayName = taskDisplayName  
                
                if self.hasCellData(description):
                    task._description = description
                else:
                    task._description = task._name
                
                task._aliasIds.append(taskId)
                task._baseURL = baseURL
                
                #if there is an assismentsItem associated with this task
                if self.hasCellData(assistmentsItemId):
                    assistmentsItem = SerializableAssistmentsItem()
                    assistmentsItem._itemId = assistmentsItemId
                    assistmentsItem._problemSetId = assistmentsSetId
                    assistmentsItem._problemSetName = assistmentsSetName
                    assistmentsItem._assignments = []
                    logInfo('{0} is checking for assistments data'.format(CSV_READER_SERVICE_NAME), 5)
                    for colName in ASSISTMENTS_ASSIGN_COL_NAMES:
                        colData = row.get(colName, '')
                        if self.hasCellData(colData):
                            assistmentsItem._assignments.append(colData)
                    task._assistmentsItem = assistmentsItem
                else:
                    task._assistmentsItem = None
                
                #this could cause performance trouble so only use this log if you need to.
                #logInfo('{0} constructed task: {1}'.format(CSV_READER_SERVICE_NAME, serializeObject(task)), 5)
                # logInfo('{0} constructed task with name: {1}'.format(CSV_READER_SERVICE_NAME, task._name), 5)
                if isEnabled:
                    result.append(task)
                    #make additional tasks to represent combined tasks
                    if (task._assistmentsItem):
                        if (task._assistmentsItem._problemSetId not in relatedTasks):
                            relatedTasks[task._assistmentsItem._problemSetId] = []
                        relatedTasks[task._assistmentsItem._problemSetId].append(task)
                    
        
        for key in relatedTasks.keys():
            relatedTaskList = relatedTasks[key]
            if len(relatedTaskList) > 1:
                collectedTask = LearningTask()

                collectedTask._ids = []
                #collectedTask._ids.append()#What's going on here?
                
                kcSet = set()
                assignmentSet = set()
                collectedAssistmentsItem = SerializableAssistmentsItem()
                
                for relatedTask in relatedTaskList:
                    relatedTask._canBeRecommendedIndividually = False
                    # Subtask ids instead of ids field
                    collectedTask._subtasks.append(relatedTask._taskId)
                    
                    if len(collectedTask._ids) == 0:
                        collectedTask._ids.append(relatedTask._taskId)
                    else:
                        collectedTask._ids[0] += "~" + relatedTask._taskId
                    
                    if not collectedTask._name:
                        collectedTask._name = relatedTask._name
                    if not collectedTask._baseURL:
                        collectedTask._baseURL = relatedTask._baseURL
                    if not collectedTask._description:
                        collectedTask._description = relatedTask._description
                    if not collectedAssistmentsItem._itemId:
                        collectedAssistmentsItem._itemId = relatedTask._assistmentsItem._itemId
                    if not collectedAssistmentsItem._problemSetId:
                        collectedAssistmentsItem._problemSetId = relatedTask._assistmentsItem._problemSetId
                    if not collectedAssistmentsItem._problemSetName:
                        collectedAssistmentsItem._problemSetName = relatedTask._assistmentsItem._problemSetName 
                    # Add all the data
                    
                    for kc in relatedTask._kcs:
                        kcSet.add(kc)
                    
                    if relatedTask._assistmentsItem is not None:
                        for assignment in relatedTask._assistmentsItem._assignments:
                            assignmentSet.add(assignment)
                    
                
                collectedTask._kcs = list(kcSet) # This is the complete set accumulated from all subtasks
                collectedAssistmentsItem._assignments = list(assignmentSet)# The assignments inside of this should be the set of all non-duplicate, non-empty ASSISTments assignments from the subtasks
                
                collectedTask._assistmentsItem = collectedAssistmentsItem
                    
                result.append(collectedTask)

        
        logInfo('Exiting CSVReader.processCSVFile', 4)    
        return result
            
