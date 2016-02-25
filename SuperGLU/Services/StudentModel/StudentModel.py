from uuid import uuid4
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.MessagingDB import KC_SCORE_VERB, SESSION_ID_CONTEXT_KEY, DATE_TIME_FORMAT, TASK_ID_CONTEXT_KEY, TASK_HINT_VERB, TASK_FEEDBACK_VERB
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT
from SuperGLU.Services.StudentModel.PersistentData import DBStudentAlias, DBStudentModel, DBStudent, DBSession
from SuperGLU.Services.StudentModel.StudentModelFactories import BasicStudentModelFactory
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
        
        if msg is not None:
            reply = self.routeMessage(msg)
        
        if reply is not None:
            logInfo('{0} is sending reply:{1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(reply)), 1)
        
    def routeMessage(self, msg):
        #depending on the content of the message react differently
        logInfo('Entering StudentModelMessaging.routeMessage', 5)
        
        
        #Only considering 
        if msg.getSpeechAct() == INFORM_ACT:
        
            if msg.getVerb() == KC_SCORE_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB, INFORM_ACT), 4)
                session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        
                if session is None:
                    session = self.createSession(msg)
            
                self.updateSession(msg, session)
                
                student = self.retrieveStudentFromCacheOrDB(msg.getActor(), msg)
                student.addSession(session)
                session.addStudent(student)
                
                if student.studentId not in session.performance.keys():
                    session.performance[student.studentId] = {}
                
                session.performance[student.studentId][msg.getObject()] = msg.getResult()
                
                session.save()    
                logInfo('{0} finished processing {1},{2}'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB, INFORM_ACT), 4)
            elif msg.getVerb() == TASK_HINT_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, TASK_HINT_VERB, INFORM_ACT), 4)
                session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        
                if session is None:
                    session = self.createSession(msg)
            
                self.updateSession(msg, session)
                
                session.hints.append(msg.getResult())
                session.save()
                logInfo('{0} finished processing {1},{2}'.format(STUDENT_MODEL_SERVICE_NAME, TASK_HINT_VERB, INFORM_ACT), 4)
            elif msg.getVerb() == TASK_FEEDBACK_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, TASK_FEEDBACK_VERB, INFORM_ACT), 4)
                session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        
                if session is None:
                    session = self.createSession(msg)
            
                self.updateSession(msg, session)
                session.feedback.append(msg.getResult())
                session.save()
                logInfo('{0} finished processing {1}, {2}'.format(STUDENT_MODEL_SERVICE_NAME, TASK_FEEDBACK_VERB, INFORM_ACT), 4)
                
            
            
            
    
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
        session.duration = 0
        session.id = msg.getContextValue(SESSION_ID_CONTEXT_KEY)
        session.task = msg.getContextValue(TASK_ID_CONTEXT_KEY)
        session.save()
        self.sessionCache[session.id] = session
        return session
    
    
    def createNewStudentModel(self, studentId):
        #DBStudentAlias List
        studentsWithId = DBStudentAlias.find_by_index("AliasIndex", studentId)
        
        for studentAlias in studentsWithId:
            student = DBStudent.find_one(studentAlias.trueId)
            
            if student is None:
                logInfo('failed to find student with Id: {0} and alias {1}'.format(studentAlias.trueId, studentAlias.alias), 1)
            else:
                BasicStudentModelFactory().buildStudentModel(student)
    
    
    
    def updateSession(self, msg, session):
        session.messageIds.append(msg.getId())
        startTime = datetime.strptime(session.startTime, DATE_TIME_FORMAT)
        msgTimestamp = datetime.strptime(msg.getTimestamp(), DATE_TIME_FORMAT)
        delta = msgTimestamp - startTime
        #only update if the duration increases
        if delta.seconds > session.duration:
            session.duration = delta.seconds
        
    def retrieveSessionFromCacheOrDB(self, sessionId, useCache=True):
        if sessionId is None:
            return None
        
        if sessionId in self.sessionCache.keys() and useCache:
            logInfo('{0} found cached session object with id:{1}'.format(STUDENT_MODEL_SERVICE_NAME, sessionId), 4)
            return self.sessionCache[sessionId]
        
        logInfo('{0} could not find cached session object with id: {1}.  Falling back to database.'.format(STUDENT_MODEL_SERVICE_NAME, sessionId), 3)
        session = DBSession.find_one(sessionId)
        
        if session is not None:
            logInfo('{0} found session {1}.  Storing in Cache'.format(STUDENT_MODEL_SERVICE_NAME, session.sessionId), 5)
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