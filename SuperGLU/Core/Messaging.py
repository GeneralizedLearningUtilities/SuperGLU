# -*- coding: utf-8 -*-
"""
Module for defining messages, which are used to communicate between services
"""
from datetime import datetime
#from dateutil import parser
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, SPEECH_ACT_SET
from SuperGLU.Util.Serialization import Serializable, tokenizeObject, untokenizeObject, makeSerialized, StorageToken, makeNative
from gludb.simple import DBObject, Field, Index


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
        return self.actor + "|" + self.verb + "|" + self.object + "\n"# + self.result.__repr__() + "|" + self.speechAct + "|" + self.context.__repr__() + "|" +self.timestamp + "\n"

class Message(Serializable):
    """
    A message class, for passing data between components.  Messages with special
    meaning or messages intended to fit specific specifications should subclass
    this message class.  This message that expands on the Tin Can API, in terms
    of information available.
    """
    # Main Keys
    ID_KEY = 'id'
    ACTOR_KEY = "actor"
    VERB_KEY = "verb"
    OBJECT_KEY = "object"
    RESULT_KEY = "result"
    SPEECH_ACT_KEY = "speechAct"
    TIMESTAMP_KEY = "timestamp"
    CONTEXT_KEY = "context"

    # Special Context Keys
    AUTHORIZATION_KEY = "authorization"
    AUTHENTICATION_KEY = "authentication"
    AUTHENTICATION_USER_KEY = 'authenticationUser'
    NAME_KEY = 'name'
    SESSION_ID_KEY = "sessionId"
    CONTEXT_CONVERSATION_ID_KEY = "conversation-id"
    CONTEXT_IN_REPLY_TO_KEY = "in-reply-to"
    CONTEXT_REPLY_WITH_KEY = "reply-with"
    CONTEXT_REPLY_BY_KEY = "reply-by"

    # Content Description Keys
    CONTEXT_LANGUAGE_KEY = 'language'
    CONTEXT_ONTOLOGY_KEY = 'ontology'

    # Default Flat Message Settings
    DEFAULT_HEADERS = (ID_KEY, SPEECH_ACT_KEY, ACTOR_KEY, VERB_KEY,
                       OBJECT_KEY, RESULT_KEY, TIMESTAMP_KEY)
    DEFAULT_CONTEXT = (CONTEXT_CONVERSATION_ID_KEY, CONTEXT_IN_REPLY_TO_KEY,
                       CONTEXT_REPLY_WITH_KEY, CONTEXT_REPLY_BY_KEY,
                       CONTEXT_LANGUAGE_KEY, CONTEXT_ONTOLOGY_KEY,
                       SESSION_ID_KEY, AUTHORIZATION_KEY, AUTHENTICATION_KEY)

    def __init__(self, actor=None, verb=None, obj=None, result=None,
                 speechAct=INFORM_ACT, context=None, timestamp=None, anId=None):
        """
        Initialize the message
        @param actor: The actor performing the verb
        @type actor: str or Serializable
        @param verb: A verb, which is an action that is occurring or has occurred
        @type verb: str or Serializable
        @param obj: A target of the verb action, being acted upon or relating the actor and object
        @type obj: str or Serializable
        @param result: The outcome of this interaction
        @type result: str or Serializable
        @param speechAct: A speech act declaring the intent of this message, from SPEECH_ACT_SET
        @type speechAct: str
        @param context: Additional context for the message
        @type context: Serializable
        @param timestamp: The timestamp for when this message refers to, ISO 8601 formatted
        @type timestamp: str
        @param anId: A unique ID (GUID) for the message, for later reference.
        @type anId: str
        """
        super(Message, self).__init__(anId)
        if context is None: context = {}
        self.validateSpeechAct(speechAct)
        self._actor = actor
        self._verb = verb
        self._object = obj
        self._result = result
        self._speechAct = speechAct
        self._context = context
        self._timestamp = timestamp

    # Accessors for Standard Message Data
    #---------------------------------------------
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

    def getSpeechAct(self):
        return self._speechAct
    
    def setSpeechAct(self, value):
        self.validateSpeechAct(value)
        self._speechAct = value

    def validateSpeechAct(self, speechAct):
        if speechAct not in SPEECH_ACT_SET:
            raise ValueError("%s was not in the speech act set."%(speechAct,))

    def getTimestamp(self):
        return self._timestamp

    def setTimestamp(self, value):
        self._timestamp = value

    def updateTimestamp(self):
        self._timestamp = datetime.now().isoformat()

    # Accessors to Custom Context Data
    #-------------------------------------
    def hasContextValue(self, key):
        return key in self._context
        
    def getContext(self):
        return self._context

    def getContextKeys(self):
        return list(self._context.keys())

    def getContextValue(self, key, default=None):
        return self._context.get(key, default)
    
    def setContextValue(self, key, value):
        self._context[key] = value

    def delContextValue(self, key):
        del self._context[key]

    # Operators
    #--------------------------------------
    def __hash__(self):
        """
        Generate a hash value for the message.  This does not take the context into account,
        as the context does not have a static set of values.
        """
        return (hash(Message) ^ hash(self._id) ^ hash(self._actor) ^ hash(self._verb) ^
                hash(self._object) ^ hash(self._result) ^ hash(self._speechAct) ^ hash(self._timestamp))
    
    def __eq__(self, other):
        return (isinstance(other, Message) and
                self._id == other._id and self._actor == other._actor and 
                self._verb == other._verb and self._object == other._object and
                self._result == other._result and self._speechAct == other._speechAct and
                self._timestamp == other._timestamp and self._context == other._context)

    def __ne__(self, other):
        return not self.__eq__(other)

    def isEquivalent(self, other):
        return (isinstance(other, Message) and
                self._actor == other._actor and 
                self._verb == other._verb and self._object == other._object and
                self._result == other._result and self._speechAct == other._speechAct and
                self._timestamp == other._timestamp and self._context == other._context)

    # Conversion to Standards-Based Messages
    #---------------------------------------------
    def makeFlatMessage(self, headers=None, context=None, sFormat=None):
        if headers is None: headers = self.DEFAULT_HEADERS
        if context is None: context = self.DEFAULT_CONTEXT
        token = self.saveToToken()
        # First Headers, then Context Specifics, then Lumped-Context
        data = [makeSerialized(token.get(h, ''), sFormat) for h in headers]
        data += [makeSerialized(self.getContextValue(h,''), sFormat) for h in context]
        data += [makeSerialized(token.get(self.CONTEXT_KEY,{}), sFormat)]
        return data 

    #if something went wrong return false , otherwise return true and the data already in the self object
    @classmethod
    def makeFromFlatMessage(cls, flatmessage, headers=None, context=None, sFormat='json'):
        if headers is None: headers = cls.DEFAULT_HEADERS
        if context is None: context = cls.DEFAULT_CONTEXT
        if len(flatmessage) != len(headers) + len(context) + 1:
            print('Flat message was invalid')
            print((len(flatmessage), len(headers) + len(context) + 1))
            print(flatmessage)
            return None
        #make the message
        token = StorageToken()
        headerData = dict([(name, makeNative(flatmessage[i], sFormat)) for i, name in enumerate(headers)])
        contextData = makeNative(flatmessage[-1], sFormat)
        for name, val in list(headerData.items()):
            token[name] = val
        token[cls.CONTEXT_KEY] = contextData
        msg = cls()
        msg.initializeFromToken(token)
        return msg
        
    def makeTinCanMessage(self, protocolData=None):
        """
        Create an xAPI-compliant (Tin Can API) version of this message
        If not possible, raise an error.
        """
        raise NotImplementedError

    def makeFIPAMessage(self, protocolData=None):
        """
        Try to create an FIPA-compliant (e.g., JADE/SPADE) version of this message.
        If not possible, raise an error.
        """
        raise NotImplementedError

    # Serialization
    #---------------------------------------------
    def saveToToken(self):
        token = super(Message, self).saveToToken()
        if self._actor is not None:
            token[self.ACTOR_KEY] = tokenizeObject(self._actor)
        if self._verb is not None:
            token[self.VERB_KEY] = tokenizeObject(self._verb)
        if self._object is not None:
            token[self.OBJECT_KEY] = tokenizeObject(self._object)
        if self._result is not None:
            token[self.RESULT_KEY] = tokenizeObject(self._result)
        if self._speechAct is not None:
            token[self.SPEECH_ACT_KEY] = tokenizeObject(self._speechAct)
        if self._timestamp is not None:
            token[self.TIMESTAMP_KEY] = tokenizeObject(self._timestamp)
        if len(self._context) > 0:
            token[self.CONTEXT_KEY] = dict([(tokenizeObject(key), tokenizeObject(value))
                                             for key, value in list(self._context.items())])
        return token

    def initializeFromToken(self, token, context=None):
        super(Message, self).initializeFromToken(token, context)
        self._actor = untokenizeObject(token.get(self.ACTOR_KEY, None))
        self._verb = untokenizeObject(token.get(self.VERB_KEY, None))
        self._object = untokenizeObject(token.get(self.OBJECT_KEY, None))
        self._result = untokenizeObject(token.get(self.RESULT_KEY, None))
        self._speechAct = untokenizeObject(token.get(self.SPEECH_ACT_KEY, None))
        self._timestamp = untokenizeObject(token.get(self.TIMESTAMP_KEY, None))
        self._context = untokenizeObject(token.get(self.CONTEXT_KEY, {}))
