from gludb.simple import DBObject, Field, Index

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
        
    def __repr__(self):
        return self.actor + "|" + self.verb + "|" + self.object + "|" + self.result.__repr__() + "|" + self.speechAct + "|" + self.context.__repr__() + "|" +self.timestamp + "\n"