'''
Created on Mar 18, 2016
This module is responsible for converting the tasks csv file to tasks objects and sends them out to the storage service
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.StudentModel.PersistentData import SerializableTask,\
    SerializableAssistmentsItem

class CSVReader (BaseService):
    
    LINE_DELIMITER = '\n'
    CELL_DELIMITER = ','
    PIPE_DELIMITER = '|||'
    
    
    def receiveMessage(self, msg):
        #TODO: implementation
        raise NotImplementedError
    
    
    def processCSVFile(self, csvString):
        #List of strings
        lines = csvString.split(sep=self.LINE_DELIMITER)
        
        #list of tasks
        result = []
        
        #remove the line containing the labels
        lines.pop(0)
        
        for line in lines:
            cells = line.split(sep=self.CELL_DELIMITER)
            
            task = SerializableTask()
            
            
            kcCell = cells[10]
            kcs = kcCell.split(self.PIPE_DELIMITER)
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
                
                if cells[14] is not None and cells[14] is not '':
                    assistmentsItem._assignments.append((cells[14], cells[15], cells[16]))
                if cells[17] is not None and cells[17] is not '':
                    assistmentsItem._assignments.append((cells[17], cells[18], cells[19]))
                if cells[20] is not None and cells[20] is not '':
                    assistmentsItem._assignments.append((cells[20], cells[21], cells[22]))
                
                task._assistmentsItem = assistmentsItem 
            else:
                task._assistmentsItem = None 
            
            
            result.append(task)
            
        return result
            