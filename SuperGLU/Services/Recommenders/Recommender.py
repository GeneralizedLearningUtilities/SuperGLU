'''
Created on Mar 7, 2016
This Module contains the first cut of the recommender service
@author: auerbach
'''
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.QueryService.DBBridge import DBBridge
from SuperGLU.Services.StudentModel import StudentModel
from SuperGLU.Services.StudentModel.PersistentData import DBTask
from SuperGLU.Services.StudentModel.StudentModelFactories import BasicStudentModelFactory
from SuperGLU.Core.MessagingDB import RECOMMENDED_TASKS_VERB, MASTERY_VERB

RECOMMENDER_SERVICE_NAME = "Recommender"

class Recommender(DBBridge):
    
    def calculateMasteryOfTask(self, task, studentModel):
        total = 0.0
        for kc in task._kcs:
            taskMastery = 0.0
            if kc in studentModel.kcMastery.keys():
                taskMastery = studentModel.kcMastery[kc]
            total += 1 - taskMastery
            
        if len(task._kcs) > 0:#really wish I didn't have to do this, but math is math
            result = total / len(task._kcs)
        else:
            result = 1.0#what should we do if a task has no knowledge components associated with it?
            
        return result
            
    
    
    def getRecommendedTasks(self, studentId, studentModel, numberOfTasksRequested):
        
        taskMastery = list()
        
        dbtaskList = DBTask.find_all()
        taskList = [x.toSerializable() for x in dbtaskList]
        
        for task in taskList:
            taskMastery.append((self.calculateMasteryOfTask(task, studentModel), task))
            
        sortedTaskMastery = sorted(taskMastery, 0, True)
        
        result = sortedTaskMastery[0-numberOfTasksRequested]
        
        return result


class RecommenderMessaging (BaseService):
    
    recommender = Recommender(RECOMMENDER_SERVICE_NAME)

    def studentModelCallBack(self, msg):
        logInfo("Entering Recommender.studentModelCallback", 5)
        recommendedTasks = self.recommender.getRecommendedTasks(msg.getObject(), msg.getResult(), 3)
        outMsg = self._createRequestReply(msg)#need to make sure this how we send the reply
        outMsg.setSpeechAct(INFORM_ACT)
        outMsg.setVerb(RECOMMENDED_TASKS_VERB)
        outMsg.setResult(recommendedTasks)
        self.sendMessage(outMsg)
        
        
    
    def receiveMessage(self, msg):
        super(RecommenderMessaging, self).receiveMessage(msg)
        #depending on the content of the message react differently
        logInfo('Entering Reccomender.receiveMessage', 5)
        
        if msg.getSpeechAct() == REQUEST_ACT:
            if msg.getVerb() == RECOMMENDED_TASKS_VERB:
                outMsg = self._createRequestReply(msg)
                outMsg.setVerb(MASTERY_VERB)
                outMsg.setObject(msg.getActor())
                self._makeRequest(outMsg, self.studentModelCallBack)
        
            
    
    
    