from SuperGLU.Util.Serialization import Serializable, untokenizeObject, tokenizeObject

"""
 * This class represents a single entry in the black or white lists.
 * 
 * The each of these fields can be filled with a value or a wildcard (*)
 * 
 * @author auerbach
"""
from edu.usc.ict.superglu.core import GIFTMessage, VHMessage
from SuperGLU.Core.Messaging import Message


class BlackWhiteListEntry(Serializable):

    MESSAGE_TYPE_KEY = "messageType";
    VERSION_KEY = "version";
    MESSAGE_NAME_KEY = "messageName";
    
    WILDCARD = "*";
    
    GIFT_MESSAGE_TYPE = "GIFT";
    SUPERGLU_MESSAGE_TYPE = "SuperGLU";
    VHUMAN_MESSAGE_TYPE = "VHuman";
    


    def __init__(self, messageType="", version="", messageName=""):
        super(BlackWhiteListEntry, self).__init__()
        self._messageType = messageType
        self._version = version
        self._messageName = messageName
        
        
    def __eq__(self, other):
        if super(BlackWhiteListEntry, self).__eq__(self, other) is False:
            return False
        if self._messageName is not other._messageName:
            return False
        if self._messageType is not other._messageType:
            return False
        if self._version is not other._version:
            return False
        
        return True
    
    
    def getMessageType(self):
        return self._messageType
    
    def getMessageName(self):
        return self._messageName
    
    def getVersion(self):
        return self._version
    
    
    def initializeFromToken(self, token, context=None):
        super(BlackWhiteListEntry, self).initializeFromToken(token, context)
        self._messageName = untokenizeObject(token.get(self.MESSAGE_NAME_KEY, ""))
        self._messageType = untokenizeObject(token.get(self.MESSAGE_TYPE_KEY, ""))
        self._version = untokenizeObject(token.get(self.VERSION_KEY))
        
        
    def saveToToken(self):
        token = super(BlackWhiteListEntry, self).saveToToken()
        if self._messageName is not None:
            token[MESSAGE_NAME_KEY] = tokenizeObject(self._messageName)
            
        if self._messageType is not None:
            token[MESSAGE_TYPE_KEY] = tokenizeObject(self._messageType)
            
        if self._version is not None:
            token[VERSION_KEY] = tokenizeObject(self._version)
            
            
    def evaluateMessageType(self, msg):
        if self._messageType == self.GIFT_MESSAGE_TYPE:
            return isinstance(msg, GIFTMessage)
        if self._messageType == self.VHUMAN_MESSAGE_TYPE:
            return isinstance(msg, VHMessage)
        if self._messageType == self.SUPERGLU_MESSAGE_TYPE:
            return isinstance(msg, Message)
        if self._messageType == self.WILDCARD:
            return True
        
        return false
    
    def evaluateMessageVersion(self, msg):
        #for now just accept wildcards until all messages have versions.
        if self._version == self.WILDCARD:
            return True
        
        return false
    
    
    def evaluateMessageName(self, msg):
        if self._messageName == self.WILDCARD:
            return true
        
        if isinstance(msg, VHMessage):
            return self._messageName == msg.getFirstWord()
        
        if isinstance(msg, GIFTMessage):
            return self._messageName == msg.getHeader()
        
        if isinstance(msg, Message):
            return self._messageName == msg.getVerb()
        
        return False
    
    
    def evaluateMessage(self, msg):
        
        if not self.evaluateMessageType(msg):
            return False
        
        if not self.evaluateMessageName(msg):
            return False
        
        if not self.evaluateMessageVersion(msg):
            return False
        
        return True
        