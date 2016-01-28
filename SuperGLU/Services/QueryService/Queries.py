# -*- coding: utf-8 -*-
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message, MessageLite

class LearnerDataQueryBase (BaseService) :
    
    def receiveMessage(self, msg):
        raise NotImplementedError("No message handling to be done yet")
        
    def runQuery(self, value):
        raise NotImplementedError("this class is abstract, use the subclasses")
        
    def runQueryInternal(self, indexName, value):
        messageLiteList = MessageLite.find_by_index(indexName, value)
        result = [];
        for messageLite in messageLiteList:
            result.append(messageLite.toMessage())
        return result;
        
class LearnerDataQueryByActor(LearnerDataQueryBase):  
    def runQuery(self, value):
        return super(LearnerDataQueryByActor, self).runQueryInternal('actorIndex', value);
        
        
class LearnerDataQueryByVerb(LearnerDataQueryBase):
    def runQuery(self, value):
        return super(LearnerDataQueryByVerb, self).runQueryInternal('verbIndex', value)
        
        
class LearnerDataQueryByObject(LearnerDataQueryBase):
    def runQuery(self, value):
        return super(LearnerDataQueryByObject, self).runQueryInternal('objectIndex', value)