# -*- coding: utf-8 -*-
from SuperGLU.Core.xAPI.TinCanHelperClasses import TinCanBaseSerializable

class TinCanStatement(TinCanBaseSerializable):
    """ A Tin-Can Compliant Statement """
    
    def __init__(self, anId=None, actor=None, verb=None, obj=None, result=None,
                 context=None, timestamp=None, stored=None, authority=None,
                 version=None, attachments=None):
        super(TinCanStatement, self).__init__(anId)
        self._actor = actor
        self._verb = verb
        self._object = obj
        self._result = result
        self._context = context
        self._timestamp = timestamp
        self._stored = stored
        self._authority = authority
        self._version = version
        self._attachments = attachments
        
    def getActor(self):
        return self._actor
    
    def setActor(self, value):
        self._actor = value

    def getVerb(self):
        return self._verb
    
    def setVerb(self, value):
        self._verb = value

    def getObject(self):
        return self._object
    
    def setObject(self, value):
        self._object = value

    def getResult(self):
        return self._result
    
    def setResult(self, value):
        self._result = value

    def getContext(self):
        return self._context
    
    def setContext(self, value):
        self._context = value

    # Time Stamps
    def getTimestamp(self):
        return self._timestamp

    def setTimestamp(self, value):
        self._timestamp = value

    def updateTimestamp(self):
        self._timestamp = time()

    def getStored(self):
        return self._stored

    def setStored(self, value):
        self._stored = value

    def updateStored(self):
        self._stored = time()

    # Protocol + TinCan Data
    def getAuthority(self):
        return self._authority
    
    def setAuthority(self, value):
        self._authority = value

    def getVersion(self):
        return self._version
    
    def setVersion(self, value):
        self._version = value
        
    def getAttachments(self):
        return self._attachments
    
    def setAttachments(self, value):
        self._attachments = value

    def addAttachment(self, value):
        self._attachments.append(value)

    # Serializion
    def getSerializationAccessors(self):
        return [("id", self.getId, self.setId, None, None),
                ("actor", self.getActor, self.setActor, None, None),
                ("verb", self.getActor, self.setActor, None, None),
                ("object", self._object, None, None),
                ("result", self._result, None, None),
                ("context", self._context, None, None),
                ("timestamp", self._timestamp, None, None),
                ("stored", self._stored, None, None),
                ("authority", self._authority, None, None),
                ("version", self._version, None, None),
                ("attachments", self._attachments, None, None)]
        
    def tinCanSerialize(self):
        data = [(k, get()) for (k, get, set, has, keys)
                in self.getSerializationAccessors()]
        return self._tinCanOutput(data)







