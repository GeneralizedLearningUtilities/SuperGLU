from uuid import uuid4
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.MessagingDB import KC_SCORE_VERB, SESSION_ID_CONTEXT_KEY, DATE_TIME_FORMAT
from SuperGLU.Services.StudentModel.PersistentData import DBStudentAlias, DBStudentModel, DBStudent, DBSession
from datetime import datetime


"""
    This module contains the message handling code for building and modifying student models.  May also contain code for querying the student model.
"""

STUDENT_MODEL_SERVICE_NAME = "Student Model Service"


class StudentModelMessaging(BaseService):
    
    studentCache = {}
    sessionCache = {}
                
    def receiveMessage(self, msg):
        logInfo('{0} received message: {1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(msg)), 1)
        reply = self.routeMessage(msg)
        
        if reply is not None:
            logInfo('{0} is sending reply:{1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(reply)), 1)
        
    def routeMessage(self, msg):
        #depending on the content of the message react differently
        logInfo('Entering StudentModelMessaging.routeMessage', 5)
        
        session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        if session is None:
            session = self.createSession(msg)
        else:
            logInfo('found session {0}'.format(session.sessionId), 5)
        
        if(msg.getVerb() == KC_SCORE_VERB):
            logInfo('{0} is processing a {1} message'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB), 4)
            student = self.retrieveStudentFromCacheOrDB(msg.getActor(), msg)
            student.addSession(session)
           
                                            
            if len(student.studentModelIds) == 0:
                logInfo('No student model associated with student {0}.  Creating a new one'.format(msg.getActor()), 3)
                student.addStudentModel(DBStudentModel(studentId=student.id))
            
            for ii in student.getStudentModels(False):
                ii.kcMastery[msg.getObject()] = msg.getResult()
                
            logInfo('finished processing {0}'.format(KC_SCORE_VERB), 4)
            
    
    def createStudent(self, studentId, msg):
        logInfo('{0} could not find student with id: {1} in database.  Creating new student'.format(STUDENT_MODEL_SERVICE_NAME, studentId), 3)
        studentUUID = str(uuid4())
        student = DBStudent(id=studentUUID, sessionIds=[], oAuthIds={}, studentModelIds=[], kcGoals={})
        student.save()
        self.studentCache[studentId] = student
        newStudentAlias = DBStudentAlias(trueId=studentUUID, alias=studentId)
        newStudentAlias.save()
        return student
    
    def createSession(self, msg):
        logInfo("Could not find session with id:{0}.  Creating new Session".format(msg.getContextValue(SESSION_ID_CONTEXT_KEY)), 3)
        session = DBSession(sessionId = msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        session.messageIds = []
        session.hints = []
        session.feedback = []
        session.performance = {}
        session.startTime = datetime.utcnow().strftime(DATE_TIME_FORMAT)
        session.id = msg.getContextValue(SESSION_ID_CONTEXT_KEY)
        session.save()
        self.sessionCache[session.id] = session
        return session
    
    def updateSession(self, msg, session):
        session.messageIds.append(msg.getId())
        startTime = datetime.strptime(session.startTime, DATE_TIME_FORMAT)
        delta = datetime.utcnow() - startTime
        session.duration = delta.seconds
        
    def retrieveSessionFromCacheOrDB(self, sessionId, useCache=True):
        if sessionId is None:
            return None
        
        if sessionId in self.sessionCache.keys() and useCache:
            return self.sessionCache[sessionId]
        
        session = DBSession.find_one(sessionId)
        
        if session is not None:
            self.sessionCache[session.id] = session 
                    
        return session
                
    def retrieveStudentFromCacheOrDB(self, studentId, msg, useCache=True):
        logInfo("Entering retrieveStudentFromCacheOrDB", 5)
        student = self.studentCache.get(studentId)
        if student is not None and useCache:
            logInfo('{0} found student object with id:{1}'.format(STUDENT_MODEL_SERVICE_NAME, studentId), 4)
            return student
        else:
            logInfo('{0} could not find cached student object with id: {1}.  Falling back to database.'.format(STUDENT_MODEL_SERVICE_NAME, studentId), 3)
            studentAliasList = DBStudentAlias.find_by_index("StudentIDIndex", studentId)
            if len(studentAliasList) > 0:
                #there should only be one object returned, should put it a log statement if that isn't correct.
                for studentAlias in studentAliasList:
                    student = studentAlias.getStudent()
                    
            if student is None:
                student = self.createStudent(studentId, msg)
            #Cache the result so we don't need to worry about looking it up again.
            self.studentCache[studentId] = student
            return student  