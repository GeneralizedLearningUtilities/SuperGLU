from uuid import uuid4
from SuperGLU.Util.Serialization import SuperGlu_Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Util.ErrorHandling import logInfo
from SuperGLU.Core.MessagingDB import KC_SCORE_VERB, SESSION_ID_CONTEXT_KEY, DATE_TIME_FORMAT, TASK_ID_CONTEXT_KEY, TASK_HINT_VERB, TASK_FEEDBACK_VERB, MASTERY_VERB, CLASS_ID_CONTEXT_KEY,\
    HEARTBEAT_VERB, HELP_TYPE_CONTEXT_KEY, LEARNER_SESSIONS_VERB, COMPLETED_VERB
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, REQUEST_ACT
from SuperGLU.Services.StudentModel.PersistentData import DBStudentAlias, DBStudentModel, DBStudent, DBSession, DBClasssAlias, DBClass
from SuperGLU.Services.StudentModel.StudentModelFactories import BasicStudentModelFactory, WeightedStudentModelFactory
from datetime import datetime
from SuperGLU.Services.QueryService.DBBridge import DBBridge


"""
    This module contains the message handling code for building and modifying student models.  May also contain code for querying the student model.
"""

STUDENT_MODEL_SERVICE_NAME = "Student Model Service"


class StudentModel(DBBridge):

    def __init__(self):
        super(StudentModel, self).__init__(STUDENT_MODEL_SERVICE_NAME)

    def countAssistmentAssignments(self, student, task):
        if task.assistmentsItem == None:
            return None

        sessions = student.getSessions(False)
        latestTask = 0
        for session in sessions:
            sessionTask = session.getTask()
            if sessionTask.name == task.name:
                latestTask = session.assignmentNumber

        return latestTask

    #TODO: remove this hack and replace it with a more stable
    def addAssignmentNumber(self, session, student):
        sessionTask = session.getTask(False)
        if session.assignmentNumber == -1 and sessionTask.assistmentsItem is not None:
            numberOfAssistmentAssignments = self.countAssistmentAssignments(student, sessionTask)
            session.assignmentNumber = numberOfAssistmentAssignments + 1


    def createNewStudentModel(self, studentId):
        #DBStudentAlias List
        studentsWithId = DBStudentAlias.find_by_index("AliasIndex", studentId)

        if len(studentsWithId) == 0:
            logInfo('failed to find student alias {0}'.format(studentId), 1)
            student = self.createStudent(studentId, None)
            return WeightedStudentModelFactory().buildStudentModel(student)

        for studentAlias in studentsWithId:
            student = DBStudent.find_one(studentAlias.trueId)

            if student is None:
                logInfo('failed to find student with Id: {0} and alias {1}'.format(studentAlias.trueId, studentAlias.alias), 1)
                student = self.createStudent(studentId, None)
                return WeightedStudentModelFactory().buildStudentModel(student)
            else:
                return WeightedStudentModelFactory().buildStudentModel(student)


    def informKCScoreVerb(self, msg):
        session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        clazz = self.retrieveClassFromCacheOrDB(msg.getContextValue(CLASS_ID_CONTEXT_KEY), msg)

        if session is None:
            session = self.createSession(msg)

        self.updateSession(msg, session)



        student = self.retrieveStudentFromCacheOrDB(msg.getActor(), msg)


        self.addAssignmentNumber(session, student)

        student.addSession(session)
        session.addStudent(student)

        if clazz is not None:
            if student.studentId not in clazz.students:
                clazz.addStudent(student)
            if msg.getObject() not in clazz.kcs:
                clazz.kcs.append(msg.getObject)
            clazz.save()

        if student.studentId not in session.performance.keys():
            session.performance[student.studentId] = {}

        session.performance[student.studentId][msg.getObject()] = msg.getResult()

        session.save()


    def informTaskHintVerb(self, msg):
        session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))

        if session is None:
            session = self.createSession(msg)

        self.updateSession(msg, session)

        session.hints.append(msg.getResult())
        session.save()


    def informTaskFeedBackVerb(self, msg):
        session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))

        if session is None:
            session = self.createSession(msg)

        self.updateSession(msg, session)
        session.feedback.append((msg.getResult(), msg.getContextValue(HELP_TYPE_CONTEXT_KEY)))
        session.save()

    def informCompleteVerb(self, msg):
        session = self.retrieveSessionFromCacheOrDB(msg.getContextValue(SESSION_ID_CONTEXT_KEY))
        clazz = self.retrieveClassFromCacheOrDB(msg.getContextValue(CLASS_ID_CONTEXT_KEY), msg)

        if session is None:
            session = self.createSession(msg)

        self.updateSession(msg, session)

        student = self.retrieveStudentFromCacheOrDB(msg.getActor(), msg)

        self.addAssignmentNumber(session, student)

        student.addSession(session)
        session.addStudent(student)

        task = self.retrieveTaskFromCacheOrDB(session.task)

        for kc in task.kcs:
            if clazz is not None:
                if student.studentId not in clazz.students:
                    clazz.addStudent(student)
                if msg.getObject() not in clazz.kcs:
                    clazz.kcs.append(msg.getObject)
                clazz.save()

            if student.studentId not in session.performance.keys():
                session.performance[student.studentId] = {}

            session.performance[student.studentId][kc] = msg.getResult()

        session.save()

    def getStudent(self, msg):
        if msg.getObject() is not None:
            dbStudent = self.retrieveStudentFromCacheOrDB(msg.getObject(), msg, False)
            serializableStudent = dbStudent.toSerializable()
            return serializableStudent
        else:
            dbSessions = DBSession.find_all()
            serializableSessions = [x.toSerializable() for x in dbSessions]
            return serializableSessions

class StudentModelMessaging(BaseService):

    studentModel_internal = StudentModel()

    def receiveMessage(self, msg):
        super(StudentModelMessaging, self).receiveMessage(msg)

        if self.studentModel_internal.taskASSISTmentsDictionary is None:
            self.studentModel_internal.taskASSISTmentsDictionary = self.studentModel_internal.populateTaskAssistmentsDictionary()

        if msg.getVerb() != HEARTBEAT_VERB:
            logInfo('{0} received message: {1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(msg)), 2)

        if msg is not None:
            reply = self.routeMessage(msg)

        if reply is not None:
            logInfo('{0} is sending reply:{1}'.format(STUDENT_MODEL_SERVICE_NAME, self.messageToString(reply)), 2)
            self.sendMessage(reply)

    def routeMessage(self, msg):
        #depending on the content of the message react differently
        #logInfo('Entering StudentModelMessaging.routeMessage', 5)

        result = None
        #Only considering
        if msg.getSpeechAct() == INFORM_ACT:

            if msg.getVerb() == KC_SCORE_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB, INFORM_ACT), 4)
                self.studentModel_internal.informKCScoreVerb(msg)
                logInfo('{0} finished processing {1},{2}'.format(STUDENT_MODEL_SERVICE_NAME, KC_SCORE_VERB, INFORM_ACT), 4)
            elif msg.getVerb() == TASK_HINT_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, TASK_HINT_VERB, INFORM_ACT), 4)
                self.studentModel_internal.informTaskHintVerb(msg)
                logInfo('{0} finished processing {1},{2}'.format(STUDENT_MODEL_SERVICE_NAME, TASK_HINT_VERB, INFORM_ACT), 4)
            elif msg.getVerb() == TASK_FEEDBACK_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, TASK_FEEDBACK_VERB, INFORM_ACT), 4)
                self.studentModel_internal.informTaskFeedBackVerb(msg)
                logInfo('{0} finished processing {1}, {2}'.format(STUDENT_MODEL_SERVICE_NAME, TASK_FEEDBACK_VERB, INFORM_ACT), 4)
            elif msg.getVerb() == COMPLETED_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(STUDENT_MODEL_SERVICE_NAME, COMPLETED_VERB, INFORM_ACT), 4)
                self.studentModel_internal.informCompleteVerb(msg)
                logInfo('{0} finished processing {1}, {2}'.format(STUDENT_MODEL_SERVICE_NAME, COMPLETED_VERB, INFORM_ACT), 4)
        elif msg.getSpeechAct() == REQUEST_ACT:
            print("REQUEST")
            if msg.getVerb() == LEARNER_SESSIONS_VERB:
                student = self.studentModel_internal.getStudent(msg)
                result = self._createRequestReply(msg)
                result.setActor(STUDENT_MODEL_SERVICE_NAME)
                result.setVerb(LEARNER_SESSIONS_VERB)
                result.setObject(msg.getObject())
                result.setResult(student)
                result.setSpeechAct(INFORM_ACT)
            #I'm going to assume the that the student id is the object, but that may not be the case
            if msg.getVerb() == MASTERY_VERB:
                logInfo('{0} is processing a {1}, {2} message'.format(STUDENT_MODEL_SERVICE_NAME, MASTERY_VERB, REQUEST_ACT), 4)
                newStudentModel = self.studentModel_internal.createNewStudentModel(msg.getObject())
                result = self._createRequestReply(msg)
                result.setActor(STUDENT_MODEL_SERVICE_NAME)
                result.setVerb(MASTERY_VERB)
                result.setSpeechAct(INFORM_ACT)
                result.setObject(msg.getObject())
                if newStudentModel is not None:
                    # This is a hack: need to debug why this is not producing the right serializable.
                    #result.setResult(newStudentModel.toSerializable())
                    result.setResult(newStudentModel.kcMastery)
                else:
                    result.setResult({})
                logInfo('{0} finished processing {1},{2}'.format(STUDENT_MODEL_SERVICE_NAME, MASTERY_VERB, REQUEST_ACT), 4)

        return result
