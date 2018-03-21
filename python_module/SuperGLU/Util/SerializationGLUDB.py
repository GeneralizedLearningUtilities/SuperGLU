'''
Created on Mar 15, 2016
This module contains the generic code for translating json serializable objects to database serializable objects
@author: auerbach
'''
import abc
from SuperGLU.Util.Serialization import DEFAULT_BRIDGE_NAME, SuperGlu_Serializable,\
    serializeObject
from gludb.simple import DBObject, Field, Index
from SuperGLU.Util.ErrorHandling import logInfo

GLUDB_BRIDGE_NAME = 'gludb'




class DBSerializableFactoryMetaclass(abc.ABCMeta):
    """
    Metaclass for binding storage bridges together
    """
    _BRIDGE_MAP = {}
    BRIDGE_NAME_KEY = "BRIDGE_NAME"
    SOURCE_CLASS_KEY = "SOURCE_CLASS"

    def __new__(self, name, bases, dct):
        cls = super(DBSerializableFactoryMetaclass, self).__new__(self, name, bases, dct)
        sourceClass = dct.get(self.SOURCE_CLASS_KEY, None)
        bridgeName = dct.get(self.BRIDGE_NAME_KEY, None)
        if sourceClass is not None:
            sourceClass._registerStorageBridge(cls, bridgeName)
            #self._setBridgeClass(sourceClass, cls, bridgeName)
            if sourceClass not in self._BRIDGE_MAP.keys():
                self._BRIDGE_MAP[sourceClass] = {}
            self._BRIDGE_MAP[sourceClass][bridgeName] = cls
        return cls

    def _getBridgeClass(self, sourceClass, bridgeName=DEFAULT_BRIDGE_NAME):
        """ Get a bridge class from the class factory. """
        return self._BRIDGE_MAP.get(sourceClass, {}).get(bridgeName, None)



class DBSerializable(object, metaclass=DBSerializableFactoryMetaclass):
    """
    Parent class for gludb (and possibly other) storage bridges
    """

    BRIDGE_NAME = GLUDB_BRIDGE_NAME
    SOURCE_CLASS = SuperGlu_Serializable

    @classmethod
    def convert(cls, sourceObject):#TODO: Handle lists of serializable objects
        if isinstance(sourceObject, list):
            result = list()
            for obj in sourceObject:
                if isinstance(obj, SuperGlu_Serializable):

                    bridgeClass = obj.getStorageBridge(cls.BRIDGE_NAME)
                    resultPart = bridgeClass(obj)
                    resultPart.create(obj)
                    result.append(resultPart)
                else:
                    result.append(obj)

            return result
        else:
            if isinstance(sourceObject, SuperGlu_Serializable):
                bridgeClass = sourceObject.getStorageBridge(cls.BRIDGE_NAME)
                result = bridgeClass(sourceObject)
                result.create(sourceObject)
                return result
            else:
                return sourceObject

    def saveToDB(self):
        raise NotImplementedError



@DBObject(table_name="unknownJSON")
class JSONtoDBSerializable(object):
    """
    If no other class is available just store the JSON to the database
    """

    jsonString = Field('')
    classId    = Field('')

    def create(self, serializableObject=None):
        if serializableObject is not None:
            self.jsonString = serializeObject(serializableObject)
            self.classId = serializableObject.getClassId()

    @Index
    def classIdIndex(self):
        return self.classId


    def saveToDB(self):
        self.save()
