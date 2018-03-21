from SuperGLU.Util.Serialization import (SuperGlu_Serializable, untokenizeObject, tokenizeObject)
from SuperGLU.Core.BlackWhiteListEntry import BlackWhiteListEntry

class ServiceConfiguration(SuperGlu_Serializable):

    TYPE_KEY = "type";
    PARAMS_KEY = "params";
    NODES_KEY = "nodes";
    WHITE_LIST_KEY ="whiteList";
    BLACK_LIST_KEY = "blackList";
    ACTIVEMQ_PARAM_KEY = "activeMQConfig";
    SOCKETIO_PARAM_KEY = "socketIOConfig";

    def __init__(self,anId = None, tipe = None, params = {}, nodes = [], blacklist = [], whitelist = [] ):
        super(ServiceConfiguration, self).__init__(anId)
        self.type = tipe
        self.params = params
        self.nodes = nodes
        self.blacklist = blacklist
        self.whitelist = whitelist

    def importBlackWhiteList(self, listOfStrings):
        result = []
        for entryAsString in listOfStrings:
            entry = BlackWhiteListEntry(entryAsString)
            result.append(entry)
        return result

    def initializeFromToken(self, token, context=None):
        super(ServiceConfiguration, self).initializeFromToken(token, context)


        self.type = untokenizeObject(token.get(self.TYPE_KEY), None)

        self.params = untokenizeObject(token.get(self.PARAMS_KEY, {}))
        self.nodes = untokenizeObject(token.get(self.NODES_KEY, []))

        blackListAsString = untokenizeObject(token.get(self.BLACK_LIST_KEY, []))
        self.blacklist = self.importBlackWhiteList(blackListAsString)

        whitelistAsString = untokenizeObject(token.get(self.WHITE_LIST_KEY, []))
        self.whitelist = self.importBlackWhiteList(whitelistAsString)

    def exportBlackWhiteList(self, listOfEntries):
        result = []
        for entry in listOfEntries:
            result.append(str(entry))
        return result

    def saveToToken(self):
        token = super(ServiceConfiguration, self).saveToToken()

        if self.type is not None:
            token[self.TYPE_KEY] = tokenizeObject(self.type)

        if self.params is not None:
            token[self.PARAMS_KEY] = tokenizeObject(self.params)

        if self.nodes is not None:
            token[self.NODES_KEY] = tokenizeObject(self.nodes)

        if self.blacklist is not None:
            blackListAsStrings = self.exportBlackWhiteList(self.blacklist)
            token[self.BLACK_LIST_KEY] = tokenizeObject(blackListAsStrings)

        if self.whitelist is not None:
            whiteListAsStrings = self.exportBlackWhiteList(self.whitelist)
            token[self.WHITE_LIST_KEY] = tokenizeObject(whiteListAsStrings)

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
        return self.whitelist

    def setWhiteList(self, whitelist):
        self.whitelist = whitelist

    def getBlackList(self):
        return self.blacklist

    def setBlackList(self, blacklist):
        self.blacklist = blacklist

    def getClass(self, classPath):
        pathComponents = classPath.split('.')
        module = __import__(pathComponents[0])
        for eachComponenet in pathComponents[1:]:
            module = getattr(module, eachComponenet)
        return module

    def getType(self):
        return self.type



class ServiceConfigurationCollection(SuperGlu_Serializable):

    SERVICE_CONFIG_MAP_KEY = "serviceConfigurations"

    def __init__(self, anId = None, serviceConfigurations={}):
        super(ServiceConfigurationCollection, self).__init__(anId)
        self._serviceConfigurations = serviceConfigurations

    def saveToToken(self):
        token = super(ServiceConfigurationCollection, self).saveToToken()

        if self._serviceConfigurations is not None:
            token[self.SERVICE_CONFIG_MAP_KEY] = tokenizeObject(self._serviceConfigurations)
        return token

    def initializeFromToken(self, token, context=None):
        super(ServiceConfigurationCollection, self).initializeFromToken(token, context)
        self._serviceConfigurations = untokenizeObject(token.get(self.SERVICE_CONFIG_MAP_KEY, {}), context)

    def getServiceConfiguration(self, configurationName):
        return self._serviceConfigurations[configurationName]

    def getServiceConfigurationKeys(self):
        return self._serviceConfigurations.keys()
