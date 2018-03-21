# -*- coding: utf-8 -*-
"""
Serialization Package
-----------------------------------
Description: This package is intended to allow serializing and unserializing
between Python objects and various serial/string representations (e.g., JSON, XML).
The following objects are included:
    * Serializable: Base class for serializable objects, needed for custom serialization
    * StorageToken: Intermediate representation of a serializable object
    * TokenRWFormats: Serializes and recovers storage tokens and primatives to specific formats (e.g., JSON)
"""
import abc
import collections
import json
import pickle
import sys
import types
import uuid
from SuperGLU.Util.ErrorHandling import tryRaiseError

try:
    import lxml.builder
    import lxml.etree
    XML_FROMSTRING = lxml.etree.fromstring
    XML_TOSTRING = lxml.etree.tostring
    XML_ELEMENT_MAKER = lxml.builder.ElementMaker
    ENABLE_XML = True
except ImportError:
    # Dummy vals to allow class to build
    def raiseXMLNotImplemented(*args, **kwds):
        raise NotImplementedError("lxml library not installed.  Cannot use xml serialization.")
    def getRaiseXMLNotImplemented(*args, **kwds):
        return raiseXMLNotImplemented
    XML_FROMSTRING = raiseXMLNotImplemented
    XML_TOSTRING = raiseXMLNotImplemented
    XML_ELEMENT_MAKER = getRaiseXMLNotImplemented
    ENABLE_XML = False

class SerializationError(Exception): pass
class InvalidTokenClassError(SerializationError): pass

# Serialization Format Constants
DEFAULT_BRIDGE_NAME = 'DefaultDBSerializable'

JSON_FORMAT = 'json'
JSON_STANDARD_FORMAT = 'json_standard'
XML_FORMAT = 'xml'
PICKLE_FORMAT = 'pickle'
VALID_SERIAL_FORMATS = (JSON_FORMAT, PICKLE_FORMAT, XML_FORMAT)

# Convenience functions to fully serialize and unserialize
#---------------------------------------------
def serializeObject(obj, sFormat=JSON_FORMAT):
    obj = tokenizeObject(obj)
    return makeSerialized(obj, sFormat)

def nativizeObject(obj, context=None, sFormat=JSON_FORMAT):
    obj = makeNative(obj, sFormat)
    return untokenizeObject(obj, context)

# Convenience functions to serialize and unserialize
#---------------------------------------------
def makeSerialized(storageToken, sFormat=JSON_FORMAT):
    """ Serialize some object(s) Must already be tokenized """
    if sFormat is None:
        sFormat = JSON_FORMAT
    if sFormat == JSON_FORMAT:
        return JSONRWFormat.serialize(storageToken)
    elif sFormat == XML_FORMAT:
        return XMLRWFormat.serialize(storageToken)
    elif sFormat == PICKLE_FORMAT:
        return PickleRWFormat.serialize(storageToken)
    elif sFormat == JSON_STANDARD_FORMAT:
        return JSONStandardRWFormat.serialize(storageToken)
    else:
        raise TypeError("No serialization format of type: %s"%(sFormat,))

def makeNative(string, sFormat=JSON_FORMAT):
    """ Unserialize some object(s) into tokens """
    if sFormat == JSON_FORMAT:
        return JSONRWFormat.parse(string)
    elif sFormat == XML_FORMAT:
        return XMLRWFormat.parse(string)
    elif sFormat == PICKLE_FORMAT:
        return PickleRWFormat.parse(string)
    elif sFormat == JSON_STANDARD_FORMAT:
        return JSONStandardRWFormat.parse(string)
    else:
        raise TypeError("No serialization format of type: %s"%(sFormat,))

# Convenience Function to Tokenize and Un-Tokenize Objects
#----------------------------------------------------------
def tokenizeObject(obj):
    """ Generic function to tokenize an object """
    if isinstance(obj, SuperGlu_Serializable):
        return obj.saveToToken()
    elif isinstance(obj, TokenRWFormat.VALID_SEQUENCE_VALUE_TYPES):
        return type(obj)([tokenizeObject(x) for x in obj])
    elif isinstance(obj, TokenRWFormat.VALID_MAPPING_VALUE_TYPES):
        return type(obj)([(tokenizeObject(key), tokenizeObject(val))
                          for key, val in obj.items()])
    else:
        return obj

def untokenizeObject(obj, context=None):
    """ Generic function to create an object from a token """
    if isinstance(obj, StorageToken):
        return SuperGlu_Serializable.createFromToken(obj, context)
    elif isinstance(obj, TokenRWFormat.VALID_SEQUENCE_VALUE_TYPES):
        return type(obj)([untokenizeObject(x, context) for x in obj])
    elif isinstance(obj, TokenRWFormat.VALID_MAPPING_VALUE_TYPES):
        return type(obj)([(untokenizeObject(key, context), untokenizeObject(val, context))
                          for key, val in obj.items()])
    else:
        return obj

# Base class for serializable objects
#---------------------------------------------
class SerializableFactoryMetaclass(abc.ABCMeta):
    """
    Metaclass for a factory mapping that is used when
    unpacking serialized objects.  Serializable classes
    without a class id will raise an error when declared.
    While not enforced explicitly, the CLASS_ID should not
    be a reserved word used by the particular serialization
    used (e.g., no "list" or "xs:boolean")
    """
    _FACTORY_MAP = {}
    RESERVED_CLASS_NAMES = []
    CLASS_ID_KEY = "CLASS_ID"
    STORAGE_BRIDGES_KEY = "_STORAGE_BRIDGES"

    def __new__(self, name, bases, dct):
        if self.CLASS_ID_KEY in dct:
            classId = dct[self.CLASS_ID_KEY]
        else:
            classId = name
            dct[self.CLASS_ID_KEY] = classId
            #error = TypeError("Serializable <%s> did not have a class id for the factory: %s"%(name, self))
            #tryRaiseError(error, 1)
        if self.STORAGE_BRIDGES_KEY not in dct:
            dct[self.STORAGE_BRIDGES_KEY] = {}
        return super(SerializableFactoryMetaclass, self).__new__(self, name, bases, dct)

    def __init__(self, name, bases, dct):
        super(SerializableFactoryMetaclass, self).__init__(name, bases, dct)
        self._FACTORY_MAP[dct[self.CLASS_ID_KEY]] = self

    def _getFactoryClass(self, classId):
        """ Get a class from the class factory. """
        return self._FACTORY_MAP.get(classId, None)


class SuperGlu_Serializable(object, metaclass=SerializableFactoryMetaclass):
    """
    A serializable object, that can be saved to token and opened from token
    """
    # Stores a registry of storage bridge connections
    _STORAGE_BRIDGES = {}

    def __init__(self, id=None):
        if id is None:
            self._id = str(uuid.uuid4())
        elif isinstance(id, uuid.UUID):
            self._id = str(id)
        else:
            self._id = str(id)

    def __eq__(self, other):
        return type(self) == type(other) and self._id == other._id

    def __ne__(self, other):
        return not self.__eq__(other)

    def getId(self):
        return self._id

    def updateId(self, id=None):
        if id is None:
            self._id = str(uuid.uuid4())
        elif isinstance(id, uuid.UUID):
            self._id = str(id)
        else:
            self._id = str(id)

    def getClassId(self):
        return self.CLASS_ID

    def initializeFromToken(self, token, context=None):
        if token.getId() is None:
            self._id = None
        else:
            self._id = str(token.getId())

    def saveToToken(self):
        if self.getId() is None:
            anId = None
        else:
            anId = str(self.getId())
        token = StorageToken(anId, self.getClassId())
        return token

    def saveToSerialized(self, sFormat=JSON_FORMAT):
        return makeSerialized(self.saveToToken(), sFormat)

    def clone(self, context=None, newId=True):
        token = self.saveToToken()
        x = self.createFromToken(token, context)
        if newId:
            x.updateId()
        return x

    @classmethod
    def createFromToken(cls, token, context=None, onMissingClass=None):
        """
        Create a serializable instance from an arbitrary storage token
        @param token: Storage token
        @param context: Mutable context for the loading process
        """
        anId = token.getId()
        if context and anId in context:
            instance = context[anId]
        else:
            # Need to import the right class
            classId = token.getClassId()
            aClass = cls._getFactoryClass(classId)
            if aClass is not None:
                instance = aClass()
                instance.initializeFromToken(token, context)
            else:
                if onMissingClass is None:
                    onMissingClass = cls.defaultOnMissingClass
                instance = onMissingClass(token)
        return instance

    @classmethod
    def defaultOnMissingClass(cls, token, errorOnMissing=False):
        if errorOnMissing:
            raise InvalidTokenClassError("%s failed to import: %s"%(token.getClassId(), token), sys.exc_info()[2])
        else:
            return token

    @classmethod
    def getStorageBridge(cls, bridgeName=DEFAULT_BRIDGE_NAME):
        return cls._STORAGE_BRIDGES.get(bridgeName, None)

    @classmethod
    def _registerStorageBridge(cls, bridgeClass, bridgeName=DEFAULT_BRIDGE_NAME):
        cls._STORAGE_BRIDGES[bridgeName] = bridgeClass


class NamedSerializable(SuperGlu_Serializable):
    """ A serializable with a name """
    CLASS_ID = 'NamedSerializable'
    NAME_KEY = 'name'

    def __init__(self, id=None, name=None):
        super(NamedSerializable, self).__init__(id)
        self._name = name

    def getName(self):
        return self._name

    def setName(self, name):
        if name is None or isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Invalid name type, got: %s"%(name,))

    def __eq__(self, other):
        return (super(NamedSerializable, self).__eq__(other) and
                self._name == other._name)

    def initializeFromToken(self, token, context=None):
        super(NamedSerializable, self).initializeFromToken(token, context)
        self._name = token.__getitem__(self.NAME_KEY, True, None)

    def saveToToken(self):
        token = super(NamedSerializable, self).saveToToken()
        if self._name is not None:
            token[self.NAME_KEY] = self._name
        return token


class StorageToken(collections.MutableMapping):
    """
    An object that stores data in a form that can be serialized
    """
    # Special Keys
    ID_KEY = 'id'
    CLASS_ID_KEY = 'classId'
    RESERVED_KEYS = frozenset([ID_KEY, CLASS_ID_KEY])

    def __init__(self, id=None, classId=None, data=None):
        if data:
            self._data = dict(data)
        else:
            self._data = {}
        if id is not None:
            self.setId(id)
        elif self.ID_KEY not in self._data:
            self.setId(str(uuid.uuid4()))
        if classId is not None:
            self.setClassId(classId)

    # Special Accessors
    def getId(self):
        return self._data.get(self.ID_KEY, None)

    def setId(self, value):
        self._data[self.ID_KEY] = value

    def getClassId(self):
        return self._data.get(self.CLASS_ID_KEY, None)

    def setClassId(self, value):
        self._data[self.CLASS_ID_KEY] = value

    # Convenience Accessor for Named Serializables
    def getName(self):
        return self._data.get(NamedSerializable.NAME_KEY, None)

    def setName(self, value):
        self._data[NamedSerializable.NAME_KEY] = value

    # Generic Accessors
    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key, hasDefault=False, default=None):
        if hasDefault:
            return self._data.get(key, default)
        else:
            return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        keys = sorted(self._data.keys())
        for key in keys:
            yield key

    def __str__(self):
        return makeSerialized(self)

    # Comparison
    def __eq__(self, other):
        return (type(self) == type(other) and self._data == other._data)

    def __ne__(self, other):
        return not self.__eq__(other)

    # Validation
    def isValidKey(self, key):
        return isinstance(key, TokenRWFormat.VALID_KEY_TYPES)

    def isValidValue(self, value):
        return isinstance(value, TokenRWFormat.VALID_VALUE_TYPES)

    def isValid(self):
        # Check that ID is valid
        if not isinstance(self._data.get(self.ID_KEY, None), (int, str)):
            return False
        # Check that class name is valid
        elif not isinstance(self._data.get(self.CLASS_ID_KEY, None), str):
            return False
        elif not isinstance(self._data.get(NamedSerializable.NAME_KEY, None), (type(None), str)):
            return False
        else:
            return True

#-------------------------------------------
# Packing and Unpacking from Serial Formats
#-------------------------------------------
# Generic Format
class TokenRWFormat(object):
    """ Class that writes storage tokens """
    # Valid Types in Storage Token
    VALID_KEY_TYPES = (str, str)

    # Note: Keys of dictionaries should be strings, or else JSON may turn them into strings
    VALID_ATOMIC_VALUE_TYPES = (bool, int, float, str, str, type(None))
    VALID_SEQUENCE_VALUE_TYPES = (list, tuple,)
    VALID_MAPPING_VALUE_TYPES = (dict,)
    VALID_VALUE_TYPES = VALID_ATOMIC_VALUE_TYPES + VALID_SEQUENCE_VALUE_TYPES + \
                        VALID_MAPPING_VALUE_TYPES + (StorageToken,)

    @classmethod
    def parse(cls, string):
        """ Parse a string into python objects """
        raise NotImplementedError

    @classmethod
    def serialize(cls, data):
        """ Serialize python objects into a string form """
        raise NotImplementedError


class JSONStandardRWFormat(TokenRWFormat):

    DECODER = json.JSONDecoder().decode
    ENCODER = json.JSONEncoder().encode

    NAME_MAPPING = {'bool': bool,
                    'unicode': str,
                    'int' : int,
                    'float' : float,
                    'null': type(None),
                    'tuple': tuple,
                    'list': list,
                    'map': dict,
                    }

    TYPE_MAPPING = dict([(val, key) for key, val in NAME_MAPPING.items()])
    RESERVED_CLASS_IDS = set(NAME_MAPPING.keys())

    @classmethod
    def isNullOrPrimitive(cls, x):
        if x is None:
            return True

        if type(x) in cls.VALID_ATOMIC_VALUE_TYPES:
            return True

        return False


    @classmethod
    def parse(cls, string):
        decoded =cls.DECODER(string)
        return cls.makeNative(decoded)

    @classmethod
    def serialize(cls, data):
        """ Serialize python objects into a JSON string form """
        serializable = cls.makeSerializable(data)
        return cls.ENCODER(serializable)

    @classmethod
    def makeSerializable(cls, x):
        if x is None:
            return x
        xType = type(x)

        if xType in cls.VALID_ATOMIC_VALUE_TYPES:
            return x
        elif xType in cls.VALID_SEQUENCE_VALUE_TYPES:
            sequenceData = []
            for obj in x:
                sequenceData.append(cls.makeSerializable(obj))
            return sequenceData
        elif xType in cls.VALID_MAPPING_VALUE_TYPES:
            processedMap = {}
            for key in x.keys():
                processedMap[cls.makeSerializable(key)] = cls.makeSerializable(x[key])
                processedMap['isMap'] = True
            return processedMap
        elif xType == StorageToken:
            storageTokenChildren = {}
            for key in x.keys():
                value = x[key]
                storageTokenChildren[key] = cls.makeSerializable(value)
            return storageTokenChildren

        return

    @classmethod
    def makeNative(cls, x):
        if cls.isNullOrPrimitive(x):
            return x

        xType = type(x)

        if xType in cls.VALID_SEQUENCE_VALUE_TYPES:
            result = []
            for item in x:
                result.append(cls.makeNative(item))
            return result
        elif xType in cls.VALID_MAPPING_VALUE_TYPES:
            result = {}
            keys = x.keys()
            if 'isMap' in x.keys():
                for key in x:
                    nativizedKey = cls.makeNative(key)
                    nativizedValue = cls.makeNative(x[key])
                    result[nativizedKey] = nativizedValue
                del result['isMap']
                return result
            else:
                nativizedData = {}
                for key in x.keys():
                    if cls.isNullOrPrimitive(x[key]):
                        nativizedData[key] = x[key]
                    else:
                        nativizedData[key] = cls.makeNative(x[key])

                result = StorageToken(None, nativizedData[StorageToken.CLASS_ID_KEY], nativizedData)
                return result


# JSON Formatting: Use JSONEncoder/JSONDecoder
class JSONRWFormat(TokenRWFormat):
    """ JSON Serialization Format Handler """
    DECODER = json.JSONDecoder().decode
    ENCODER = json.JSONEncoder().encode

    NAME_MAPPING = {'bool': bool,
                    'int': int,
                    'float': float,
                    'unicode': str,
                    'null': type(None),
                    'tuple': tuple,
                    'list': list,
                    'map': dict,
                    }
    TYPE_MAPPING = dict([(val, key) for key, val in NAME_MAPPING.items()])
    RESERVED_CLASS_IDS = set(NAME_MAPPING.keys())

    @classmethod
    def parse(cls, string):
        """ Parse a JSON string into python objects """
        decoded = cls.DECODER(string)
        return cls.makeNative(decoded)

    @classmethod
    def serialize(cls, data):
        """ Serialize python objects into a JSON string form """
        serializable = cls.makeSerializable(data)
        return cls.ENCODER(serializable)

    @classmethod
    def makeSerializable(cls, x):
        xType = type(x)
        if xType in cls.VALID_ATOMIC_VALUE_TYPES:
            return x
        elif xType in cls.VALID_SEQUENCE_VALUE_TYPES:
            return {cls.TYPE_MAPPING[xType] :
                        tuple([cls.makeSerializable(val) for val in x])}
        elif xType in cls.VALID_MAPPING_VALUE_TYPES:
            return {cls.TYPE_MAPPING[xType] :
                        dict([(cls.makeSerializable(key),  cls.makeSerializable(val))
                               for key, val in x.items()])}
        elif xType == StorageToken:
            # Use the Factory Class Id as the type
            return {x.getClassId() :
                        dict([(cls.makeSerializable(key),  cls.makeSerializable(val))
                               for key, val in x.items()])}
        else:
            raise TypeError("Tried to serialize unserializable object of type (%s): %s"%(xType, x))

    @classmethod
    def makeNative(cls, x):
        if not hasattr(x, '__iter__') or isinstance(x, str):
            return x
        dataTypeName = list(x.keys())[0]
        data = x[dataTypeName]
        dataType = cls.NAME_MAPPING.get(dataTypeName, StorageToken)
        if dataType in cls.VALID_SEQUENCE_VALUE_TYPES:
            return dataType([cls.makeNative(val) for val in data])
        elif dataType in cls.VALID_MAPPING_VALUE_TYPES:
            return dataType([(cls.makeNative(key),
                              cls.makeNative(val))
                              for key, val in data.items()])
        elif dataType == StorageToken:
            data = dict([(key,
                          cls.makeNative(val))
                          for key, val in data.items()])
            token = StorageToken(data=data)
            return token

# XML Formatting: Use LXML etree
class XMLRWFormat(TokenRWFormat):
    """ XML Serialization Format Handler """
    DECODER = staticmethod(XML_FROMSTRING)
    ENCODER = staticmethod(XML_TOSTRING)
    ELEMENT_MAKER = XML_ELEMENT_MAKER()

    # Entity Names
    ELEMENT_NAME = 'element'
    LIST_NAME = 'list'
    TUPLE_NAME = 'tuple'
    DICT_NAME = 'map'
    DICT_ENTRY_NAME = 'dict_item'

    # Attribute Names
    TYPE_ATTR_NAME = 'type'
    NIL_ATTR_NAME = 'nil'
    VALUE_ATTR_NAME = 'value'

    # Attribute Values: Types
    BOOL_TYPE_VALUE = 'xs:boolean'
    INT_TYPE_VALUE = 'xs:long'
    FLOAT_TYPE_VALUE ='xs:double'
    STR_TYPE_VALUE ='xs:string'
    SEQ_TYPE_VALUE ='xs:sequence'
    DICT_TYPE_VALUE ='map'
    ELEMENT_TYPE_VALUE = 'xs:element'

    # Attribute Values: Other
    ROOT_NODE = 'root'
    TRUE_VALUE = '"true"'


    ATTR_MAPPING = {(TYPE_ATTR_NAME, BOOL_TYPE_VALUE): bool,
                    (TYPE_ATTR_NAME, INT_TYPE_VALUE): int,
                    (TYPE_ATTR_NAME, FLOAT_TYPE_VALUE): float,
                    (TYPE_ATTR_NAME, STR_TYPE_VALUE): str,
                    (NIL_ATTR_NAME, TRUE_VALUE): type(None),
                    (TYPE_ATTR_NAME, SEQ_TYPE_VALUE): list,
                    (TYPE_ATTR_NAME, DICT_TYPE_VALUE): dict,         # No equivalent XSD type
                    (TYPE_ATTR_NAME, None): StorageToken
                    }
    TYPE_MAPPING = dict([(val, key) for key, val in ATTR_MAPPING.items()])
    TYPE_MAPPING[str] = (TYPE_ATTR_NAME, STR_TYPE_VALUE)
    TYPE_MAPPING[tuple] = (TYPE_ATTR_NAME, STR_TYPE_VALUE)

    @classmethod
    def parse(cls, string):
        elementTree = cls.DECODER(string)
        return cls.makeNative(elementTree)

    @classmethod
    def serialize(cls, data, root=None):
        elementTree = cls.makeSerializable(data, root)
        return cls.ENCODER(elementTree)

    @classmethod
    def makeSerializable(cls, x, root=None):
        if root is None:
            root = lxml.etree.Element(cls.ROOT_NODE)
        return cls._makeSerializable(x, root)

    @classmethod
    def _makeSerializable(cls, x, root):
        xType = type(x)
        if xType in cls.VALID_VALUE_TYPES:
            attrs = dict([cls.TYPE_MAPPING[xType]])
            # If Storage Token, follows a dictionary format
            if cls.TYPE_ATTR_NAME in attrs and attrs[cls.TYPE_ATTR_NAME] is None:
                attrs[cls.TYPE_ATTR_NAME] = x.getClassId()
            # Serialize atomic types
            if xType in cls.VALID_ATOMIC_VALUE_TYPES:
                print((cls.ELEMENT_NAME, attrs))
                node = cls.ELEMENT_MAKER(cls.ELEMENT_NAME, **attrs)
                if x is not None:
                    node.text = repr(x)
            # Serialize sequences
            elif xType in cls.VALID_SEQUENCE_VALUE_TYPES:
                if xType == tuple:
                    node = cls.ELEMENT_MAKER(cls.TUPLE_NAME, **attrs)
                else:
                    node = cls.ELEMENT_MAKER(cls.LIST_NAME, **attrs)
                #node.extend([cls._makeSerializable(val, node) for val in x])
                for val in x:
                    cls._makeSerializable(val, node)
            # Serialize mappings
            elif xType in cls.VALID_MAPPING_VALUE_TYPES:
                node = cls.ELEMENT_MAKER(cls.DICT_NAME, **attrs)
                listAttrs = dict([cls.TYPE_MAPPING[list]])
                for key, val in x.items():
                    keyPair = cls.ELEMENT_MAKER(cls.DICT_ENTRY_NAME, **listAttrs)
                    cls._makeSerializable(key, keyPair)
                    cls._makeSerializable(val, keyPair)
                    node.append(keyPair)
            # Serialize Storage Tokens
            elif xType == StorageToken:
                node = cls.ELEMENT_MAKER(x.getClassId(), **attrs)
                listAttrs = dict([cls.TYPE_MAPPING[list]])
                for key, val in x.items():
                    keyPair = cls.ELEMENT_MAKER(cls.DICT_ENTRY_NAME, **listAttrs)
                    cls._makeSerializable(key, keyPair)
                    cls._makeSerializable(val, keyPair)
                    node.append(keyPair)
            else:
                # Should never hit this if VALID_VALUE_TYPES is proper union
                raise TypeError("Tried to serialize unserializable object of type (%s): %s"%(xType, x))
            root.append(node)
            return root
        else:
            raise TypeError("Tried to serialize unserializable object of type (%s): %s"%(xType, x))

    @classmethod
    def getXMLNodePythonType(cls, node):
        name = node.tag
        if node.get(cls.NIL_ATTR_NAME, False) == cls.TRUE_VALUE:
            return type(None)
        else:
            typeAttr = node.get(cls.TYPE_ATTR_NAME, None)
            if typeAttr == cls.BOOL_TYPE_VALUE:
                return bool
            elif typeAttr == cls.INT_TYPE_VALUE:
                return int
            elif typeAttr == cls.FLOAT_TYPE_VALUE:
                return float
            elif typeAttr == cls.STR_TYPE_VALUE:
                return str
            elif typeAttr == cls.SEQ_TYPE_VALUE:
                if name == cls.TUPLE_NAME:
                    return tuple
                elif name == cls.LIST_NAME or name == cls.DICT_ENTRY_NAME:
                    return list
                else:
                    raise TypeError("Could not resolve python type for node: %s"%(node,))
            elif typeAttr == cls.DICT_TYPE_VALUE:
                return dict
            else:
                return StorageToken

    @classmethod
    def makeNative(cls, x):
        return cls._makeNative(x[0])

    @classmethod
    def _makeNative(cls, x):
        dataType = cls.getXMLNodePythonType(x)
        if dataType == type(None):
            return None
        elif dataType in cls.VALID_ATOMIC_VALUE_TYPES:
            if issubclass(dataType, str):
                return dataType(x.text[1:-1])
            else:
                return dataType(eval(x.text))
        elif dataType in cls.VALID_SEQUENCE_VALUE_TYPES:
            return dataType([cls._makeNative(val) for val in x])
        elif dataType in cls.VALID_MAPPING_VALUE_TYPES:
            return dataType([cls._makeNative(val) for val in x])
        elif dataType == StorageToken:
            data = dict([cls._makeNative(val) for val in x])
            token = StorageToken(data=data)
            return token
        else:
            raise TypeError("Tried to unserialize unrecognized type (%s): %s"%(type(x), x))

# Pickle Formatting: Use pickle
class PickleRWFormat(TokenRWFormat):
    """ Pickle Serialization Format Handler """
    DECODER = staticmethod(pickle.loads)
    ENCODER = staticmethod(pickle.dumps)

    @classmethod
    def parse(cls, string):
        return cls.DECODER(string)

    @classmethod
    def serialize(cls, data):
        return cls.ENCODER(data)
