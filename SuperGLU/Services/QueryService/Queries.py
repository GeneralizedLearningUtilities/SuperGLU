# -*- coding: utf-8 -*-
from SuperGLU.Util.Serialization import Serializable
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.Messaging import Message, MessageLite

class LearnerDataQueryBase (BaseService) :
    
    def receiveMessage(self, msg):
        raise NotImplementedError("No message handling to be done yet")
        
    def runQuery(self, value):
        raise NotImplementedError("this class is abstract, use the subclasses")
        
        
class LearnerDataQueryByActor(LearnerDataQueryBase):
    
    
    def runQuery(self, value):
        return MessageLite.find_by_index('actorIndex', value)