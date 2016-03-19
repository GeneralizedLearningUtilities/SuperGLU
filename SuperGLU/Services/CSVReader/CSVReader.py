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


CSV_READER_SERVICE_NAME = "CSV Reader Service"

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
        
            if True:
                logInfo('{0} is processing a {1},{2} message'.format(CSV_READER_SERVICE_NAME, CSV_READER_SERVICE_NAME, INFORM_ACT), 4)
                
                csvString = msg.getResult()
                taskList = self.processCSVFile(csvString)
                
                reply = Message()
                reply.setSpeechAct(INFORM_ACT)
                reply.setVerb(VALUE_VERB)
                reply.setObject(taskList)    
        
        
        if reply is not None:
            logInfo('{0} is broadcasting a {1}, {2} message'.format(CSV_READER_SERVICE_NAME, INFORM_ACT, VALUE_VERB), 4)
            self.sendMessage(reply)
    
    def processCSVFile(self, csvString):
        #List of strings
        logInfo('Entering CSVReader.processCSVFile', 4)
        lines = csvString.split(sep=self.LINE_DELIMITER)
        
        #list of tasks
        result = []
        
        #remove the line containing the labels
        lines.pop(0)
        
        for line in lines:
            
            logInfo('{0} is splitting the line into cells'.format(CSV_READER_SERVICE_NAME), 5)
            cells = line.split(sep=self.CELL_DELIMITER)
            
            task = SerializableTask()
            
            
            logInfo('{0} is extracting the knowledge components'.format(CSV_READER_SERVICE_NAME), 5)
            kcCell = cells[10]
            kcs = kcCell.split(self.PIPE_DELIMITER)
            
            logInfo('{0} is constructing the next serializable task object'.format(CSV_READER_SERVICE_NAME), 5)
            task._kcs = kcs
            
            task._name = cells[2]
            task._taskId = cells[1]
            task._baseURL = cells[6]
            
            #if there is an assismentsItem associated with this task
            if cells[11] is not None and cells[11] is not '':
                assistmentsItem = SerializableAssistmentsItem()
                assistmentsItem._itemID = cells[11]
                assistmentsItem._problemSetID = cells[12]
                assistmentsItem._problemSetName = cells[13]
                assistmentsItem._assignments = []
                
                logInfo('{0} is checking for assistments data'.format(CSV_READER_SERVICE_NAME), 5)
                if cells[14] is not None and cells[14] is not '':
                    assistmentsItem._assignments.append((cells[14], cells[15], cells[16]))
                if cells[17] is not None and cells[17] is not '':
                    assistmentsItem._assignments.append((cells[17], cells[18], cells[19]))
                if cells[20] is not None and cells[20] is not '':
                    assistmentsItem._assignments.append((cells[20], cells[21], cells[22]))
                
                task._assistmentsItem = assistmentsItem 
            else:
                task._assistmentsItem = None 
            
            #this could cause performance trouble so only use this log if you need to.
            #logInfo('{0} constructed task: {1}'.format(CSV_READER_SERVICE_NAME, serializeObject(task)), 5)
            logInfo('{0} constructed task with name: {1}'.format(CSV_READER_SERVICE_NAME, task._name), 5)
            result.append(task)
        
        logInfo('Exiting CSVReader.processCSVFile', 4)    
        return result
            