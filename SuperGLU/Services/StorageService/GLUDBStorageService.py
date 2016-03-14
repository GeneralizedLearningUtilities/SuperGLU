'''
Created on Mar 10, 2016
This storage service provides the functionality to manually store data 
@author: auerbach
'''

from SuperGLU.Services.StorageService.Storage_Service_Interface import BaseStorageService
from SuperGLU.Services.StudentModel.PersistentData import DBTask, SerializableTask
from SuperGLU.Util.ErrorHandling import logWarning
from SuperGLU.Util.Serialization import Serializable, NamedSerializable





class GLUDBStorageService(BaseStorageService):
    
    #This requires GLUDB to have some concept of Buckets.  Right now it doesn't
    def hasBucket(self, name):
        return True

    def getBucket(self, name):
        return None

    def addBucket(self, name):
        raise NotImplementedError
        
    def getBucketNames(self):
        raise NotImplementedError
    
    def _renameBucket(self, oldName, newName):
        raise NotImplementedError

    def delBucket(self, name):
        raise NotImplementedError
    
    def processStorageInform(self, bucket, verb, key=None, value=None,
                             tags=None, aType=None, allowCreate=None,
                             name=None, description=None, dataType=None):
        if verb == self.VALUE_VERB:
            logWarning("IS SETTING", value)
            if isinstance(value, Serializable):
                logWarning("IS SERIALIZABLE")
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
                dbValue = value.toDB()
                dbValue.saveToDB()
        elif verb == self.VOID_VERB:
            return bucket.delValue(key, name)