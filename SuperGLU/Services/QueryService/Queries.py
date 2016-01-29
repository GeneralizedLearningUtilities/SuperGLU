# -*- coding: utf-8 -*-
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingDB import DBLoggedMessage

#These classes are intended to allow the user to access data stored from the messages.

class LearnerDataQueryBase (BaseService) :
        
    def runQuery(self, value):
        raise NotImplementedError("this class is abstract, use the subclasses")
    
    #return results of query as a list of Message objects, not DBLoggedMessage objects.
    def runQueryInternal(self, indexName, value):
        dbLoggedMessageList = DBLoggedMessage.find_by_index(indexName, value)
        result = [dbLoggedMessage.toMessage() for dbLoggedMessage in dbLoggedMessageList
                  if dbLoggedMessage is not None]
        return result
        
        
#Basic Queries
        
class LearnerDataQueryByActor(LearnerDataQueryBase):  
    def runQuery(self, value):
        return super(LearnerDataQueryByActor, self).runQueryInternal('actorIndex', value);
        
        
class LearnerDataQueryByVerb(LearnerDataQueryBase):
    def runQuery(self, value):
        return super(LearnerDataQueryByVerb, self).runQueryInternal('verbIndex', value)
        
        
class LearnerDataQueryByObject(LearnerDataQueryBase):
    def runQuery(self, value):
        return super(LearnerDataQueryByObject, self).runQueryInternal('objectIndex', value)
        
        
#More advanced Queries

#class SingleStudentQueryBy(LearnerDataQueryBase):
 #   def runQuery(self, value):