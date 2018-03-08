from SuperGLU.Util.Serialization import (Serializable, untokenizeObject, tokenizeObject)
from edu.usc.ict.superglu.core.blackwhitelist import BlackWhiteListEntry

class ServiceConfiguration(Serializable):
    
    TYPE_KEY = "type";
    PARAMS_KEY = "params";
    NODES_KEY = "nodes";
    WHITE_LIST_KEY ="whiteList";
    BLACK_LIST_KEY = "blackList";
    ACTIVEMQ_PARAM_KEY = "activeMQConfig";
    SOCKETIO_PARAM_KEY = "socketIOConfig";
    
    def __init__(self,id = "", type = None, params = {}, nodes = [], blacklist = [], whitelist = [] ):
        super(ServiceConfiguration, self).__init__(id)
        self.type = type
        self.params = params
        self.nodes = nodes
        self.blacklist = blacklist
        self.whitelist = whitelist
        
    def importBlackkWhiteList(self, listOfStrings):
        result = []
        for entryAsString in listOfStrings:
            entry = BlackWhiteListEntry(entryAsString)
            result.append(entry)
        return result
    
    def initializeFromToken(self, token):
        super(ServiceConfiguration, self).initiazlizeFromToken(token)
        
        
        try:
            self.type = getClass(token.get(self.TYPE_KEY))
        except:
            self.type = None
        
        self.params = untokenizeObject(token.get(self.PARAMS_KEY, {}))
        self.nodes = untokenizeObject(token.get(self.NODES_KEY, []))
        
        blackListAsString = untokenizeObject(token.get(self.BLACK_LIST_KEY, []))
        self.blacklist = importBlackWhiteList(blackListAsString)
        
        whitelistAsString = untokenizeObject(token.get(self.WHITE_LIST_KEY, []))
        self.whitelist = importBlackWhiteList(whitelistAsString)
        
    def exportBlackWhiteList(self, listOfEntries):
        result = []
        for entry in listOfEntries:
            result.append(str(entry))
        return result
    
    def saveToToken(self):
        token = super(ServiceConfiguration, self).saveToToken()
        
        if self.type is not None:
            className = self.type.__name__
            token[TYPE_KEY] = className
        
        if self.params is not None:
            token[PARAMS_KEY] = tokenizeObject(self.params)
        
        if self.nodes is not None:
            token[NODES_KEY] = tokenizeObject(self.nodes)
        
        if self.blacklist is not None:
            blackListAsStrings = self.exportBlackWhiteList(blacklist)
            token[BLACK_LIST_KEY] = tokenizeObject(blackListAsStrings)
            
        if self.whitelist is not None:
            whiteListAsStrings = self.exportBlackWhiteList(whitelist)
            token[WHITE_LIST_KEY] = tokenizeObject(whiteListAsStrings)
            
        return token
    
    def getParams(self):
        return self.params
    
    def setParams(self, params):
        self.params = params
        
    def getNodes(self):
        return self.nodes
    
    def setNodes(self, nodes):
        self.nodes = nodes
        
    def getWhiteList(self):
        return whitelist
        
    def setWhiteList(self, whitelist):
        self.whitelist = whitelist
        
    def getBlackList(self):
        return blacklist
        
    def setBlackList(self, blacklist):
        self.blacklist = blacklist
        
    def getClass(classPath):
        pathComponents = classPath.split('.')
        module = __import__(pathComponents[0])
        for eachComponenet in pathComponents[1:]:
            module = getattr(module, eachComponenet)
        return module
        
    