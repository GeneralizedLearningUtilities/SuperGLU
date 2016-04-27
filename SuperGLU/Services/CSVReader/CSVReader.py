'''
Created on Mar 18, 2016
This module is responsible for converting the tasks csv file to tasks objects and sends them out to the storage service
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.StudentModel.PersistentData import SerializableTask, SerializableAssistmentsItem
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.Messaging import Message
from SuperGLU.Services.Authentication.UserDataService import VALUE_VERB
from SuperGLU.Util.Serialization import serializeObject
from SuperGLU.Core.MessagingDB import ELECTRONIX_TUTOR_TASK_UPLOAD_VERB


CSV_READER_SERVICE_NAME = "CSV Reader Service"
TASKS_OBJECT = "tasks"

class CSVReader (BaseService):
    
    LINE_DELIMITER = '\n'
    CELL_DELIMITER = ','
    PIPE_DELIMITER = '|||'
    
    
    
    
    
    def receiveMessage(self, msg):
        #depending on the content of the message react differently
        logInfo('Entering CSVReader.receiveMessage', 5)
        
        reply = None
        #Only considering 
        if msg.getSpeechAct() == INFORM_ACT:
        
            if msg.getVerb() == ELECTRONIX_TUTOR_TASK_UPLOAD_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(CSV_READER_SERVICE_NAME, ELECTRONIX_TUTOR_TASK_UPLOAD_VERB, INFORM_ACT), 4)
                
                csvString = msg.getResult()
                taskList = self.processCSVFile(csvString)
                
                reply = Message()
                reply.setSpeechAct(INFORM_ACT)
                reply.setVerb(VALUE_VERB)
                reply.setObject(TASKS_OBJECT)
                reply.setResult(taskList)    
        
        
        if reply is not None:
            logInfo('{0} is broadcasting a {1}, {2} message'.format(CSV_READER_SERVICE_NAME, INFORM_ACT, VALUE_VERB), 4)
            self.sendMessage(reply)
    
    def processCSVFile(self, csvString):
        #List of strings
        logInfo('Entering CSVReader.processCSVFile', 4)
        lines = csvString.split(sep=self.LINE_DELIMITER)
        
        relatedTasks = dict()
        
        #list of tasks
        result = []
        
        #remove the line containing the labels
        lines.pop(0)
        
        for line in lines:
            
            logInfo('{0} is splitting the line into cells'.format(CSV_READER_SERVICE_NAME), 5)
            cells = line.split(sep=self.CELL_DELIMITER)
            
            logInfo(len(cells), 6)
            
            if len(cells) > 1:
            
                task = SerializableTask()
                task._ids = []
                
                logInfo('{0} is extracting the knowledge components'.format(CSV_READER_SERVICE_NAME), 5)
                kcCell = cells[14]
                kcs = kcCell.split(self.PIPE_DELIMITER)
                
                while '' in kcs:#need to remove the empty kc cells.
                    kcs.remove('')
                
                
                logInfo('{0} is constructing the next serializable task object'.format(CSV_READER_SERVICE_NAME), 5)
                task._kcs = kcs
                
                if cells[2] is not None or cells[2] != "":
                    task._name = cells[1]
                else:
                    task._name = cells[2]
                
                if cells[3] is not None or cells[3] != "":
                    task._description = cells[3]
                else:
                    task._description = task._name
                
                task._ids.append(cells[1])
                task._baseURL = cells[7]
                
                #if there is an assismentsItem associated with this task
                if cells[15] is not None and cells[15] is not '':
                    assistmentsItem = SerializableAssistmentsItem()
                    assistmentsItem._itemID = cells[15]
                    assistmentsItem._problemSetID = cells[16]
                    assistmentsItem._problemSetName = cells[17]
                    assistmentsItem._assignments = []
                    
                    logInfo('{0} is checking for assistments data'.format(CSV_READER_SERVICE_NAME), 5)
                    if cells[18] is not None and cells[18] is not '':
                        assistmentsItem._assignments.append(cells[18])
                    if cells[19] is not None and cells[19] is not '':
                        assistmentsItem._assignments.append(cells[19])
                    if cells[20] is not None and cells[20] is not '':
                        assistmentsItem._assignments.append(cells[20])
                    
                    task._assistmentsItem = assistmentsItem 
                else:
                    task._assistmentsItem = None 
                
                #this could cause performance trouble so only use this log if you need to.
                #logInfo('{0} constructed task: {1}'.format(CSV_READER_SERVICE_NAME, serializeObject(task)), 5)
                logInfo('{0} constructed task with name: {1}'.format(CSV_READER_SERVICE_NAME, task._name), 5)
                result.append(task)
                
                #make additional tasks to represent combined tasks
                if task._assistmentsItem._problemSetID not in relatedTasks.keys():
                    relatedTasks[task._assistmentsItem._problemSetID] = []
                
                relatedTasks[task._assistmentsItem._problemSetID].append(task)
                    
        
        for key in relatedTasks.keys():
            relatedTaskList = relatedTasks[key]
            if len(relatedTaskList) > 1:
                collectedTask = SerializableTask()

                collectedTask._ids = []
                collectedTask._ids.append()#What's going on here?
                
                kcSet = set()
                assignmentSet = set()
                collectedAssistmentsItem = SerializableAssistmentsItem()
                
                for relatedTask in relatedTaskList:
                    relatedTask._canBeRecommendedIndividually = False
                    # Subtask ids instead of ids field
                    collectedTask._subtasks.append(relatedTask._ids[0])
                    
                    if len(collectedTask._ids == 0):
                        collectedTask._ids.append(relatedTask._ids[0])
                    else:
                        collectedTask._ids[0].append("~")
                        collectedTask._ids[0].append(relatedTask._ids[0])
                    
                    if not collectedTask._name:
                        collectedTask._name = relatedTask._name
                    if not collectedTask._baseURL:
                        collectedTask._baseURL = relatedTask._baseURL
                    if not collectedTask._description:
                        collectedTask._description = relatedTask._description
                    if not collectedAssistmentsItem._itemID:
                        collectedAssistmentsItem._itemID = relatedTask._assistmentsItem._itemID
                    if not collectedAssistmentsItem._problemSetID:
                        collectedAssistmentsItem._problemSetID = relatedTask._assistmentsItem._problemSetID
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
            