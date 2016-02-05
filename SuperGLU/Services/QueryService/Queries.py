# -*- coding: utf-8 -*-
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingDB import DBLoggedMessage, KC_SCORE_VERB, USER_ID_CONTEXT_KEY, TASK_ID_CONTEXT_KEY, TASK_HINT_VERB, TASK_FEEDBACK_VERB
from itertools import filterfalse

#These classes are intended to allow the user to access data stored from the messages.

class LearnerDataQueryBase (BaseService) :
        
    def runQuery(self, value):
        raise NotImplementedError("this class is abstract, use the subclasses")

    #filter the results of a query to match a partially filled out message
    def filterQueryResults(self, queryResults, filter, timestampOperator="=="):
        result = [x for x in queryResults if x is not None 
					and filter.matchOnPartial(x, timestampOperator)]
        return result
        
    #return results of query as a list of DBLoggedMessage objects.
    def runQueryInternal(self, indexName, value):
        return DBLoggedMessage.find_by_index(indexName, value)
        
        
    #convert results from DBLoggedMessage to Message
    def convertResultsToMessageList(self, dbLoggedMessageList):
        result = [dbLoggedMessage.toMessage() for dbLoggedMessage in dbLoggedMessageList
                    if dbLoggedMessage is not None]
        return result
        
#Basic Queries
        
class LearnerDataQueryByActor(LearnerDataQueryBase):  
    def runQuery(self, value):
        dbLoggedMessageList = super(LearnerDataQueryByActor, self).runQueryInternal('actorIndex', value)
        return super(LearnerDataQueryByActor, self).convertResultsToMessageList(dbLoggedMessageList)
        
class LearnerDataQueryByVerb(LearnerDataQueryBase):
    def runQuery(self, value):
        dbLoggedMessageList = super(LearnerDataQueryByVerb, self).runQueryInternal('verbIndex', value)
        return super(LearnerDataQueryByVerb, self).convertResultsToMessageList(dbLoggedMessageList)
        
        
class LearnerDataQueryByObject(LearnerDataQueryBase):
    def runQuery(self, value):
        dbLoggedMessageList = super(LearnerDataQueryByObject, self).runQueryInternal('objectIndex', value)
        return super(LearnerDataQueryByObject, self).convertResultsToMessageList(dbLoggedMessageList)
        
        
#More advanced Queries

class KCForUserAfterAGivenTimeQuery(LearnerDataQueryBase):
    #value should be a filter message
    def runQuery(self, value):
        dbLoggedMessageList = super(KCForUserAfterAGivenTimeQuery, self).runQueryInternal('actorVerbObjIndex', (value.actor, value.verb, value.object))
        #print(dbLoggedMessageList)
        filteredMessages = super(KCForUserAfterAGivenTimeQuery, self).filterQueryResults(dbLoggedMessageList, value, "<")
        #print(filteredMessages)
        return super(KCForUserAfterAGivenTimeQuery, self).convertResultsToMessageList(filteredMessages)
        
        
def getKCsForUserAfterAGivenTime(user, kc, time):
    filter = DBLoggedMessage(actor=user, verb=KC_SCORE_VERB, object=kc, result=None, speechAct=None, context=None, timestamp=time)
    return KCForUserAfterAGivenTimeQuery().runQuery(filter)

    
def getAverageKCScoreAfterAGivenTime(user, kc,time):
    kcScores = getKCsForUserAfterAGivenTime(user, kc, time)
    result = 0;
    if len(kcScores) != 0:
        total = sum([x.getResult() for x in kcScores])
        result = total / len(kcScores)
    return result
    
   
class UserTaskQuery (LearnerDataQueryBase):

    def runQuery(self, value):
        #for the sake of clarity, I'm going to raise an error with specific information if you don't pass in a None value
        if not USER_ID_CONTEXT_KEY in value.context or not TASK_ID_CONTEXT_KEY in value.context:
            raise RuntimeError("userId and TaskId cannot be None")
        
        dbLoggedMessageList = super(UserTaskQuery, self).runQueryInternal('userTaskIndex', (value.context[USER_ID_CONTEXT_KEY], value.context[TASK_ID_CONTEXT_KEY]))
        #print(dbLoggedMessageList)
        filteredMessages = super(UserTaskQuery, self).filterQueryResults(dbLoggedMessageList, value, "<")
        #print(filteredMessages)
        return super(UserTaskQuery, self).convertResultsToMessageList(filteredMessages)
        
def getTotalScoreForAGivenUserAndTask(user, task, timestamp=None):
    context = {USER_ID_CONTEXT_KEY: user, TASK_ID_CONTEXT_KEY: task}
    filter = DBLoggedMessage(actor=user, verb=KC_SCORE_VERB, object=None, result=None, speechAct=None, context=context, timestamp=timestamp)
    kcScores = UserTaskQuery().runQuery(filter)
    return sum([x.getResult() for x in kcScores])
    
def getTotalScoreForAGivenUserTaskAndKC(user, task, kc, timestamp=None):
    context = {USER_ID_CONTEXT_KEY: user, TASK_ID_CONTEXT_KEY: task}
    filter = DBLoggedMessage(actor=user, verb=KC_SCORE_VERB, object=kc, result=None, speechAct=None, context=context, timestamp=timestamp)
    kcScores = UserTaskQuery().runQuery(filter)
    return sum([x.getResult() for x in kcScores])
    
def getAllHintsForSingleUserAndTask(user, task, timestamp=None):
    context = {USER_ID_CONTEXT_KEY: user, TASK_ID_CONTEXT_KEY: task}
    filter = DBLoggedMessage(actor=user, verb=TASK_HINT_VERB, object=None, result=None, speechAct=None, context=context, timestamp=timestamp)
    hints = UserTaskQuery().runQuery(filter)

def getAllFeedbackForSingleUserAndTask(user, task, timestamp=None):
    context = {USER_ID_CONTEXT_KEY: user, TASK_ID_CONTEXT_KEY: task}
    filter = DBLoggedMessage(actor=user, verb=TASK_FEEDBACK_VERB, object=None, result=None, speechAct=None, context=context, timestamp=timestamp)
    hints = UserTaskQuery().runQuery(filter)    