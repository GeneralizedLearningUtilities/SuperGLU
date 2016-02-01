# -*- coding: utf-8 -*-
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingDB import DBLoggedMessage
from itertools import filterfalse

#These classes are intended to allow the user to access data stored from the messages.

class LearnerDataQueryBase (BaseService) :
        
    def runQuery(self, value):
        raise NotImplementedError("this class is abstract, use the subclasses")

    #filter the results of a query to match a partially filled out message
    def filterQueryResults(self, queryResults, filter):
        filterfalse(lambda x : filter.matchOnPartial(x), queryResults)
        return queryResults
        
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
        dbLoggedMessageList = super(LearnerDataQueryByActor, self).runQueryInternal('actorIndex', value);
        print(dbLoggedMessageList)
        filter = DBLoggedMessage(actor=None, verb="Completed", object=None, result=None, speechAct=None, context=None)
        print (super(LearnerDataQueryByActor, self).filterQueryResults(dbLoggedMessageList, filter))
        
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

