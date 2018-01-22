from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Services.StudentModel.PersistentData import DBStudentModel, DBSession, DBTask

"""
    this is an abstract class that creates a DBStudentModel object according to some algorithm to be implemented in a subclass
"""
from SuperGLU.Core.MessagingDB import NEGATIVE_HELP_TYPE
import math
class StudentModelFactoryBase(object):
    
    #arguments: DBStudent
    #returnVal: DBStudentModel
    def buildStudentModel(self, student):
        raise NotImplementedError("use a subclass of StudentModelFactoryBase instead")


class BasicStudentModelFactory(StudentModelFactoryBase):
    
    
    def buildStudentModel(self, student):
        #List<DBSession>
        self.sessionList = student.getSessions(False)
        
        if len(self.sessionList) == 0:
            logInfo('student {0} has not started any sessions.  cannot build student model'.format(student.studentId), 2)
            return None
        
        #Dictionary<string, tuple(float totalScore, int numberOfEntries)>
        kcScoreTotals = {}
        
        logInfo('building student model for student {0}'.format(student.studentId), 3)
        
        for session in self.sessionList:
            #sanity check to make sure the student took part in the session.
            if student.studentId not in session.performance:
                logInfo('student {0} was attached to session {1}, but no kc score was ever recorded'.format(student.studentId, session.sessionId), 2)
            else:
                studentPerformance =  session.performance[student.studentId]
                for kc in studentPerformance.keys():
                    kcSessionValue = studentPerformance[kc]
                    
                    kcScoreTotal = None
                    if kc not in kcScoreTotals:
                        kcScoreTotal = (kcSessionValue, 1)
                    else:
                        oldKCScoreTotal = kcScoreTotals[kc]
                        kcScoreTotal = (oldKCScoreTotal[0] + kcSessionValue, oldKCScoreTotal[1] + 1)
                        
                    kcScoreTotals[kc] = kcScoreTotal
        
        result = DBStudentModel()
        result.studentId = student.studentId
        result.kcMastery = {}
        
        #note it should not be possible to get a divide by zero error here since the denominator is always > 1
        for kc in kcScoreTotals.keys():
            kcScoreTotal = kcScoreTotals[kc]
            result.kcMastery[kc] = kcScoreTotal[0] / kcScoreTotal[1]
        
        logInfo('built student model for student {0}'.format(student.studentId), 3)
        
        student.addStudentModel(result)
        return result

class WeightedStudentModelFactory (BasicStudentModelFactory):
    
    def addHintWeights(self, studentModel, student):
        
        sessionList = student.getSessions(True)
        
        for  currentSession in sessionList:
            #DBTask
            currentSessionTask = currentSession.getTask(False)
            
            #if there is no task associated with the session then ignore it
            if currentSessionTask is None:
                continue
            
            numberOfHintsInCurrentSession = len(currentSession.hints)
            
            #don't count past six hints
            if numberOfHintsInCurrentSession > 6:
                numberOfHintsInCurrentSession = 6
            
            for kc in currentSessionTask.kcs:
                if kc in studentModel.kcMastery.keys():
                    studentModel.kcMastery[kc] = studentModel.kcMastery[kc] - numberOfHintsInCurrentSession * .3
        
        return studentModel
    
    def addFeedbackWeights(self, studentModel, student):
        sessionList = student.getSessions(True)
        
        for  currentSession in sessionList:
            #DBTask
            currentSessionTask = currentSession.getTask(True)
            
            #if there is no task associated with the session then ignore it
            if currentSessionTask is None:
                continue
            
            numberOfNegativeFeedbacks = 0;
            
            for (feedbackText, feedbackType) in currentSession.feedback:
                if feedbackType == NEGATIVE_HELP_TYPE:
                    numberOfNegativeFeedbacks = numberOfNegativeFeedbacks + 1
            
            if numberOfNegativeFeedbacks > 6:
                numberOfNegativeFeedbacks = 6
            
            for kc in currentSessionTask.kcs:
                if kc in studentModel.kcMastery.keys():
                    studentModel.kcMastery[kc] = studentModel.kcMastery[kc] - numberOfNegativeFeedbacks * .3
            
        return studentModel
    
    def addTimeSpentWeights(self, studentModel, student):
        sessionList = student.getSessions(True)
        
        for  currentSession in sessionList:
            #DBTask
            currentSessionTask = currentSession.getTask(True)
            
            #if there is no task associated with the session then ignore it
            #if we don't know the duration then skip this session.
            if currentSessionTask is None or currentSession.duration == -1.0:
                continue
            
            if currentSession.duration > 180:
                x = currentSession.duration - 180
                kcDelta = -.1 * (1 / (1 + math.exp(1/600*(x-600))))
            else:
                kcDelta = 0
                
            for kc in currentSessionTask.kcs:
                if kc in studentModel.kcMastery.keys():
                    studentModel.kcMastery[kc] = studentModel.kcMastery[kc] + kcDelta
            
        return studentModel
    
    def buildStudentModel(self, student):
        studentModel = BasicStudentModelFactory.buildStudentModel(self, student)
        studentModel = self.addHintWeights(studentModel, student)
        studentModel = self.addFeedbackWeights(studentModel, student)
        studentModel = self.addTimeSpentWeights(studentModel, student)
        return studentModel
        