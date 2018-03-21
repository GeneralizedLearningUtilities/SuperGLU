# -*- coding: utf-8 -*-
from SuperGLU.Core.FIPA.SpeechActs import (INFORM_ACT, INFORM_REF_ACT,
    CONFIRM_ACT, DISCONFIRM_ACT, REQUEST_ACT,)
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Util.ErrorHandling import logError, logWarning, logInfo
from SuperGLU.Util.Serialization import (SuperGlu_Serializable, NamedSerializable,
    nativizeObject, serializeObject, JSON_FORMAT)

STORAGE_SERVICE_NAME = "StorageService"
SERIALIZABLE_DATA_TYPE = "SuperGlu_Serializable"

VALUE_VERB = "Value"

DATA_TYPE_DB = 0
DATA_TYPE_MEDIA = 1

class BaseStorageService(BaseService):

    BUCKET_KEY = "bucket"
    DESCRIPTION_KEY = "description"
    NAME_KEY = "name"
    TAGS_KEY = "tags"
    TYPE_KEY = "type"
    DATA_TYPE_KEY = "dataType"
    ALLOW_CREATE_KEY = "allowCreate"

    HAS_ELEMENT_VERB = "HasElement"
    CONTAINS_VERB = "Contains"
    VALUE_VERB = VALUE_VERB
    ASSIGNED_TAGS = "AssignedTags"
    ASSIGNED_URI_VERB = "AssignedURI"
    VOID_VERB = "Void"

    def hasBucket(self, name):
        raise NotImplementedError

    def getBucket(self, name):
        raise NotImplementedError

    def addBucket(self, name):
        raise NotImplementedError

    def getBucketNames(self):
        raise NotImplementedError

    def renameBucket(self, oldName, newName):
        if not self.hasBucket(oldName):
            raise NameError("Bucket named '" + oldName + "' did not exist, could not rename.")
        elif self.hasBucket(newName):
            raise NameError("New bucket name '" + newName + "' already exists in storage.")
        else:
            self._renameBucket(oldName, newName)

    def _renameBucket(self, oldName, newName):
        raise NotImplementedError

    def delBucket(self, name):
        raise NotImplementedError

    def exportBucket(self, name):
        bucket = self.getBucket(name)
        return bucket.exportData()

    def receiveMessage(self, msg):
        # TODO: Restore bucket management
        #if ((msg.getActor() == STORAGE_SERVICE_NAME) and
        #    (msg.getContextValue(self.BUCKET_KEY, None) is not None) and
        #    (self.hasBucket(msg.getContextValue(self.BUCKET_KEY)))):
        print("STORAGE RECEIVED MESSAGE: %s"%(msg,))
        if (msg.getActor() == STORAGE_SERVICE_NAME):
            bucket = self.getBucket(msg.getContextValue(self.BUCKET_KEY))
            # Inform: Set some value(s)
            if (msg.getSpeechAct() == INFORM_ACT):
                try:
                    logWarning("INFORMING")
                    value = self.processStorageInform(bucket, 
                                                      msg.getVerb(), 
                                                      msg.getObject(), 
                                                      msg.getResult(), 
                                                      msg.getContextValue(self.TAGS_KEY, None), 
                                                      msg.getContextValue(self.TYPE_KEY, None),
                                                      msg.getContextValue(self.ALLOW_CREATE_KEY, True),
                                                      msg.getContextValue(self.NAME_KEY, None),
                                                      msg.getContextValue(self.DESCRIPTION_KEY, None),
                                                      msg.getContextValue(self.DATA_TYPE_KEY, None))
                    if (value == True):
                        response = self.makeConfirmMessage(msg)
                    else:
                        response = self.makeDisconfirmMessage(msg)
                except Exception:
                    self.sendMessage(self.makeDisconfirmMessage(msg))
                    raise
                self.sendMessage(response)
            # Request: get some value(s)
            elif (msg.getSpeechAct() == REQUEST_ACT):
                try:
                    value = self.processStorageRequest(bucket,
                                                       msg.getVerb(),
                                                       msg.getObject(),
                                                       msg.getContextValue(self.TAGS_KEY, None),
                                                       msg.getContextValue(self.TYPE_KEY, None),
                                                       msg.getContextValue(self.NAME_KEY, None))
                    if msg.getVerb() == self.CONTAINS_VERB:
                        response = self.makeReplyToContainsMessage(msg, value[0], value[1]);
                    elif msg.getVerb() != INFORM_REF_ACT or value is None:
                        response = self.makeRequestAnswerMessage(msg, value)
                    else:
                        response = self.makeReplyToInformRefMessage(msg, value[0], value[1])
                except Exception:
                    self.sendMessage(self.makeDisconfirmMessage(msg))
                    raise
                self.sendMessage(response)
            # Inform about the name of a value (rename)
            elif (msg.getSpeechAct() == INFORM_REF_ACT):
                try:
                    value = self.processStorageRename(bucket,
                                                      msg.getVerb(),
                                                      msg.getObject(),
                                                      msg.getResult(),
                                                      msg.getContextValue(self.NAME_KEY, None))
                    if (value == True):
                        response = self.makeConfirmMessage(msg)
                    else:
                        response = self.makeDisconfirmMessage(msg)
                except Exception:
                    self.sendMessage(self.makeDisconfirmMessage(msg))
                    raise
                self.sendMessage(response)
            else:
                logWarning("COULD NOT PROCESS (%s): %s"%(self.getId(), serializeObject(msg)))

    def processStorageInform(self, bucket, verb, key=None, value=None,
                             tags=None, aType=None, allowCreate=None,
                             name=None, description=None, dataType=None):
        raise NotImplementedError

    def processStorageRequest(self, bucket, verb, key=None,
                              tags=None, aType=None, name=None):
        logInfo("No handlers for REQUEST messages available", 5)


    def getValue(self, bucket, key=None, name=None):
        raise NotImplementedError

    def processStorageRename(self, bucket, verb, key, newName, name):
        if verb == self.HAS_ELEMENT_VERB:
            bucket.changeName(newName, key, name)
        else:
            return False

    def makeConfirmMessage(self, msg):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setSpeechAct(CONFIRM_ACT)
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg

    def makeDisconfirmMessage(self, msg):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setSpeechAct(DISCONFIRM_ACT)
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg

    def makeRequestAnswerMessage(self, msg, result):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setSpeechAct(INFORM_ACT)
        msg.setResult(result)
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg

    def makeReplyToContainsMessage(self, msg, keys, names):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setSpeechAct(INFORM_ACT)
        msg.setResult(keys)
        msg.setContextValue(Message.NAME_KEY, names)
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg

    def makeReplyToInformRefMessage(self, msg, key, name):
        oldId = msg.getId()
        msg = msg.clone()
        msg.updateId()
        msg.setSpeechAct(INFORM_ACT)
        msg.setObject(key)
        msg.setResult(name)
        msg.setContextValue(Message.NAME_KEY, name)
        msg.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        return msg



"""
This is a legacy class that stores data by serializing it
"""
class SerializedStorage(BaseStorageService):


    def processStorageInform(self, bucket, verb, key=None, value=None,
                             tags=None, aType=None, allowCreate=None,
                             name=None, description=None, dataType=None):
        if verb == self.VALUE_VERB:
            logWarning("IS SETTING", value)
            if isinstance(value, SuperGlu_Serializable):
                logWarning("IS SERIALIZABLE")
                dataType = SERIALIZABLE_DATA_TYPE
                if key is None:
                    key = value.getId()
                elif key != value.getId():
                    logWarning('BAD KEY for Storage (%s != %s)'%(key, value.getId()))
                    return False
                if isinstance(value, NamedSerializable):
                    if name is None:
                        name = value.getName()
                    elif name != value.getName():
                        logWarning('BAD NAME for Storage(%s != %s)'%(name, value.getName()))
                        return False
                value = serializeObject(value, JSON_FORMAT)
            return bucket.setValue(key, value, name, description, tags, aType,
                                   dataType, True, allowCreate)
        elif verb == self.VOID_VERB:
            return bucket.delValue(key, name)


    def processStorageRequest(self, bucket, verb, key=None,
                          tags=None, aType=None, name=None):
        if verb == self.HAS_ELEMENT_VERB:
            return bucket.hasRef(key, name)
        elif verb == self.CONTAINS_VERB:
            keys = bucket.getMatchingKeys(tags, aType)
            names = [bucket.getName(aKey) for aKey in keys]
            return keys, names
        elif verb == self.VALUE_VERB:
            if isinstance(key, (tuple, list)):
                values = []
                for k in key:
                    value = bucket.getValue(key, None)
                    if bucket.getDataType(key, None) == SERIALIZABLE_DATA_TYPE:
                        value = nativizeObject(value, JSON_FORMAT)
                    values.append(value)
                return values
            elif isinstance(name, (tuple, list)):
                values = []
                for n in name:
                    value = bucket.getValue(None, n)
                    if bucket.getDataType(None, n) == SERIALIZABLE_DATA_TYPE:
                        value = nativizeObject(value, JSON_FORMAT)
                    values.append(value)
                return values
            else:
                value = bucket.getValue(key, name)
                if bucket.getDataType(key, name) == SERIALIZABLE_DATA_TYPE:
                    value = nativizeObject(value, JSON_FORMAT)
                return value
        elif verb == INFORM_REF_ACT:
            if key is not None:
                return (key, bucket.getName(key))
            elif name is not None:
                return (bucket.resolveRef(None, name), name)
            else:
                return None
        elif verb == self.ASSIGNED_TAGS:
            return bucket.getObjectTags(key, name)
        elif verb == self.ASSIGNED_URI_VERB:
            return bucket.getLink(key, name)
        else:
            return False


    def getValue(self, bucket, key=None, name=None):
        if isinstance(bucket, basestring):
            bucket = self.getBucket(bucket)
        value = bucket.getValue(key, name)
        if bucket.getDataType(key, name) == SERIALIZABLE_DATA_TYPE:
            value = nativizeObject(value, JSON_FORMAT)
        return value
