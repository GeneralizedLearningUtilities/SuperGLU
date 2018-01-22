'''
Created on Mar 7, 2016
This Module contains the first cut of the recommender service
@author: auerbach
'''
from SuperGLU.Util.ErrorHandling import logInfo, logWarning, logError
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Services.QueryService.DBBridge import DBBridge
from SuperGLU.Services.StudentModel import StudentModel
from SuperGLU.Services.StudentModel.PersistentData import DBTask, DBAssistmentsItem
from SuperGLU.Services.StudentModel.StudentModelFactories import BasicStudentModelFactory
from SuperGLU.Core.MessagingDB import RECOMMENDED_TASKS_VERB, MASTERY_VERB
from builtins import int
from SuperGLU.Util.Serialization import serializeObject

RECOMMENDER_SERVICE_NAME = "Recommender"

class Recommender(DBBridge):
    
    def calcMaxMasteryGain(self, task, studentModel):
        if studentModel is not None:
            total = 0.0
            for kc in task._kcs:
                taskMastery = 0.0
                if kc in studentModel.keys():
                    taskMastery = studentModel[kc]
                total += 1.0 - taskMastery
                
            if len(task._kcs) > 0:
                #really wish I didn't have to do this, but math is math
                result = total / len(task._kcs)
            else:
                # No KC's so no possible gain.
                result = 0.0
            return result
        else:
            #if no student model exists then mastery all zero, so max gain possible
            return 1.0
            
    # TODO: This isn't weighted properly, instead is excluding repeats
    def checkNovelty(self, studentId, taskList):
        student = self.retrieveStudentFromCacheOrDB(studentId, None, True)
        logInfo("retrievedStudent In check novelty", 1)
        tasksToRemove = []
        if len(student.sessionIds) > 0:
            sessions = student.getSessions(False)
            logInfo("got sessions In check Novelty", 1)
            for task in taskList:
                for session in sessions:
                    #add more conditions to allow us to recommend the same task twice
                    #logInfo("getting Task for session", 1)
                    #sessionTask = session.getTask()
                    #logInfo("gotTask", 1)
                    if session.task is not None and task._taskId == session.task:
                        tasksToRemove.append(task)
        for taskToRemove in tasksToRemove:
            taskList.remove(taskToRemove)
        logInfo("checked novelty", 1) 
        return taskList
    
    #remove erroneous entries from task list.
    #this isn't strictly necessary, but it guards against a corrupted database.
    def validateTasks(self, taskList):
        print("TASK LIST:" + str(taskList))
        validTasks = []
        for task in taskList:
            if len(task._aliasIds) > 0:
                validTasks.append(task)
        return validTasks
    
    def findAssignmentNumber(self, task, sessions):
        possibleTaskNumber = -1
        for session in sessions:
            #sessionTask = session.getTask()
            #logInfo("task id is {0}, and session id is {1}".format(task._taskId, session.task), 1)
        
            if task._taskId == session.task:
                logInfo("found session with previous task", 1)
                if session.assignmentNumber is not None:
                    logInfo("session.assignmentNumber = {0}".format(session.assignmentNumber), 5)
                    try:
                        possibleTaskNumber = int(session.assignmentNumber);
                    except:
                        logWarning("Failed to Find session.assignmentNumber for | {0}".format(session.task))
                        possibleTaskNumber = 0
                else:
                    possibleTaskNumber = 0
        return possibleTaskNumber + 1
    
    def getRecommendedTasks(self, studentId, studentModel, numberOfTasksRequested):
        logInfo("MAKING RECOMMENDATIONS", 1)
        taskMastery = list()
        
        dbtaskList = DBTask.find_all()
        dbassistmentItemsList = DBAssistmentsItem.find_all()
        
        for dbTask in dbtaskList:
            if dbTask.assistmentsItemId is not None and dbTask.assistmentsItemId is not '':
                for dbassistmentsItem in dbassistmentItemsList:
                    if  dbassistmentsItem.id == dbTask.assistmentsItemId:
                        dbTask.assistmentsItemCache = dbassistmentsItem
                        break
        
        taskList = [x.toSerializable() for x in dbtaskList]
        logInfo("RETRIEVED TASKS FROM DATABASE", 1)
        #taskList = self.validateTasks(taskList)
        #taskList = self.checkNovelty(studentId, taskList)
               
        for task in taskList:
            taskMastery.append((self.calcMaxMasteryGain(task, studentModel), task))
            
        sortedTaskMastery = sorted(taskMastery, key=lambda taskMastery : taskMastery[0], reverse=True)
        
        #logInfo("sortedTaskMastery={0}".format(sortedTaskMastery), 6)
        result = sortedTaskMastery
        #print("RESULT: " + str(len(result)))
        student = self.retrieveStudentFromCacheOrDB(studentId, None, True)
        logInfo("retrieved student", 1)
        sessions = student.getSessions(False)
        logInfo("retrieved sessions", 1)
        for gain, task in result:
            if task._assistmentsItem is not None:
                task._assistmentsItem._assignmentNumber = self.findAssignmentNumber(task, sessions)
           # print("TASK: " + str(task))
           #print(str(task._assistmentsItem))

        result = [task for gain, task in result if task._assistmentsItem is not None and
                      task._assistmentsItem.getActiveAssignmentURL() is not None]
        result = result[0:numberOfTasksRequested]
        #print("RESULT:" + str(result))
        logInfo("GOT RESULT", 1)
        return result
        #return taskList[0:numberOfTasksRequested]
    
    

class RecommenderMessaging(BaseService):

    ORIGINAL_MESSAGE_KEY = "OriginalRecommendationMessage"
    recommender = Recommender(RECOMMENDER_SERVICE_NAME)

    def studentModelCallBack(self, msg, oldMsg):
        logInfo("Entering Recommender.studentModelCallback", 5)
        
        #hack instrumentation
        student = self.recommender.retrieveStudentFromCacheOrDB(msg.getObject(), None, True)
        #logInfo("dbStudentRecord = {0}".format(student), 6)
        serializableStudent = student.toSerializable()
        logInfo("student record = {0}".format(serializableStudent.saveToSerialized()), 2)
        
        # Make sure that it is the right student's score for the request
        recMsg = oldMsg.getContextValue(self.ORIGINAL_MESSAGE_KEY, Message())
        if (msg.getVerb() == MASTERY_VERB and
            msg.getSpeechAct() == INFORM_ACT and
            msg.getObject() == recMsg.getActor()):
            
            if isinstance(recMsg.getObject(), (int, float)):
                numberOfRecommendations = int(recMsg.getObject())
            else:
                numberOfRecommendations = 3
            
            recommendedTasks = self.recommender.getRecommendedTasks(msg.getObject(), msg.getResult(), numberOfRecommendations)
            self.sendRecommendations(recommendedTasks, recMsg)

    def sendRecommendations(self, recommendedTasks, msgTemplate=None):

        if msgTemplate is None: msgTemplate = Message()
        #need to make sure this how we send the reply
        outMsg = self._createRequestReply(msgTemplate)
        outMsg.setSpeechAct(INFORM_ACT)
        outMsg.setVerb(RECOMMENDED_TASKS_VERB)
        outMsg.setResult(recommendedTasks)
        # @TODO: This shouldn't be a problem, yet it seems to be on the JS side when it is stored as a storage token?
        if outMsg.hasContextValue(self.ORIGINAL_MESSAGE_KEY):
            outMsg.delContextValue(self.ORIGINAL_MESSAGE_KEY)
        self.sendMessage(outMsg)
    
    def receiveMessage(self, msg):
        super(RecommenderMessaging, self).receiveMessage(msg)
        #depending on the content of the message react differently
        logInfo('Entering Recommender.receiveMessage', 5)
        
        if self.recommender.taskASSISTmentsDictionary is None:
            self.recommender.taskASSISTmentsDictionary = self.recommender.populateTaskAssistmentsDictionary() 
        
        if (msg.getSpeechAct() == REQUEST_ACT and
            msg.getVerb() == RECOMMENDED_TASKS_VERB):
            outMsg = Message(None, MASTERY_VERB, msg.getActor(), msg.getObject(), REQUEST_ACT)
            #TODO: Replace with the ability to store context w/ the request in the base recommender class
            outMsg.setContextValue(self.ORIGINAL_MESSAGE_KEY, msg)
            self._makeRequest(outMsg, self.studentModelCallBack)
        
            
    
    
    
