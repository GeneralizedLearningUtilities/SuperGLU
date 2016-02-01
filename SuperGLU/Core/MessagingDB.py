from gludb.simple import DBObject, Field, Index
from SuperGLU.Core.Messaging import Message
"""
Module for storing the class that persists the messaging objects into the database.
"""

USER_ID_CONTEXT_KEY = 'userId'
TASK_ID_CONTEXT_KEY = 'taskId'
STEP_ID_CONTEXT_KEY = 'stepId'
# User + Task as an index also

@DBObject(table_name="DBLoggedMessage")
class DBLoggedMessage(object):
    actor = Field('actor')
    verb = Field('verb')
    object = Field('object')
    result = Field('result')
    speechAct = Field('speechAct')
    context = Field('context')
    timestamp = Field('timestamp')
    
    @Index
    def actorIndex(self):
        return self.actor
        
    @Index
    def verbIndex(self):
        return self.verb
        
    @Index
    def objectIndex(self):
        return self.object
        
    @Index
    def actorVerbIndex(self):
        return (self.actor, self.verb)
        
    @Index
    def actorVerbObjIndex(self):
        return (self.actor, self.verb, self.object)
        
    def toMessage(self):
        return Message(self.actor, self.verb, self.object, self.result, self.speechAct, self.context, self.timestamp)
    
    def matchOnPartial(self, current):
        if self.actor is not None and current.actor != self.actor:
            return False
        
        if self.verb is not None and current.verb != self.verb:
            return False
            
        if self.object is not None and current.object != self.object:
            return False
            
        if self.speechAct is not None and current.speechAct != current.speechAct:
            return False
        
        if self.result is not None and current.result != self.result:
            return False
        
        if self.context is not None:
            if current.context is None:
                return False
            
            #Note: I am assuming that the context is a dictionary if that isn't true then I'll need to add a type check and handle all possible types 
            for otherContextKey in self.context.keys:
                if otherContextKey not in current.context and self.context[otherContextKey] != current.context[otherContextKey] :
                    return False
        
        if self.timestamp is not None and current.timestamp != self.timestamp:
            return False;
        
        return True
        
        
    def __repr__(self):
        return self.actor + "|" + self.verb + "|" + self.object + "|" + self.result.__repr__() + "|" + self.speechAct + "|" + self.context.__repr__() + "|" +self.timestamp + "\n"