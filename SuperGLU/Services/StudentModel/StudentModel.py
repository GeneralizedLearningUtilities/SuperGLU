from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.MessagingDB import KC_SCORE_VERB
from SuperGLU.Services.StudentModel.PersistentData import DBStudent


"""
    This module contains the message handling code for building and modifying student models.  May also contain code for querying the student model.
"""

STUDENT_MODEL_SERVICE_NAME = "Student Model Service"


class StudentModelMessaging(BaseService):
    
    studentCache = {}
    
    def retriveSessionFromCacheOrDB(self, studentId):
        student = self.studentCache.get(studentId)
        if student is not None:
            logInfo('{0} found student object with id:{1}'.format(STUDENT_MODEL_SERVICE_NAME, studentId), 4)
            return student
        else:
            logInfo('{0} could not find cached student object with id: {1}.  Falling back to database.'.format(STUDENT_MODEL_SERVICE_NAME, studentId), 3)
            #student = DBStudent.
            
    
    def receiveMessage(self, msg):
        logInfo('{0} received message: {1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(msg)), 1)
        reply = self.routeMessage(msg)
        
        if reply is not None:
            logInfo('{0} is sending reply:{1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(reply)), 1)
        
    def routeMessage(self, msg):
        #depending on the content of the mess
        
        if(msg.getVerb() == KC_SCORE_VERB):
            logInfo('{0} is processing a {1} message'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB), 3)
            