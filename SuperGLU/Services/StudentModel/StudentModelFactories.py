from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Services.StudentModel.PersistentData import DBStudentModel

"""
    this is an abstract class that creates a DBStudentModel object according to some algorithm to be implemented in a subclass
"""
class StudentModelFactoryBase(object):
    
    #arguments: DBStudent
    #returnVal: DBStudentModel
    def buildStudentModel(self, student):
        raise NotImplementedError("use a subclass of StudentModelFactoryBase instead")


class BasicStudentModelFactory(StudentModelFactoryBase):
    
    def buildStudentModel(self, student):
        #List<DBSession>
        sessionList = student.getSessions(False)
        
        if len(sessionList) == 0:
            logInfo('student {0} has not started any sessions.  cannot build student model'.format(student.studentId), 2)
            return None
        
        #Dictionary<string, tuple(float totalScore, int numberOfEntries)>
        kcScoreTotals = {}
        
        logInfo('building student model for student {0}'.format(student.studentId), 3)
        
        for session in sessionList:
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