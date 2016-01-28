from gludb.simple import DBObject, Field, Index

"""
Module for storing the class that persists the messaging objects into the database.
"""

@DBObject(table_name='Messages')
class MessageLite(object):
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
        
    def toMessage(self):
        return Message(self.actor, self.verb, self.object, self.result, self.speechAct, self.context, self.timestamp)
        
    def __repr__(self):
        return self.actor + "|" + self.verb + "|" + self.object + "|" + self.result.__repr__() + "|" + self.speechAct + "|" + self.context.__repr__() + "|" +self.timestamp + "\n"