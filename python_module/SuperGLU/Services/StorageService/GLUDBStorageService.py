'''
Created on Mar 10, 2016
This storage service provides the functionality to manually store data
@author: auerbach
'''

from SuperGLU.Services.StorageService.Storage_Service_Interface import BaseStorageService
from SuperGLU.Services.StudentModel.PersistentData import DBTask, LearningTask
from SuperGLU.Util.ErrorHandling import logWarning, logInfo
from SuperGLU.Util.Serialization import SuperGlu_Serializable, NamedSerializable
from SuperGLU.Util.SerializationGLUDB import DBSerializable,\
    JSONtoDBSerializable


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
            if isinstance(value, SuperGlu_Serializable):
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
                #NOTE we are assuming that the value class and dbValue class have the toDB and saveToDB functions respectively.
                #If they do not have them they must be implemented or the system will not save the data.
            try:

                if isinstance(value, list):
                    for valueObject in value:
                        logInfo("saving task {0} to database".format(valueObject._name), 4)
                        dbValue = DBSerializable.convert(valueObject)
                        dbValue.saveToDB()
                                        
            except NotImplementedError:
                logInfo('failed to serialize object', 1)
                dbValue = JSONtoDBSerializable(value)
                dbValue.saveToDB()
            return True

        #GLUDB does not currently allow for deletion of items so this should always return false
        elif verb == self.VOID_VERB:
            return False
            #return bucket.delValue(key, name)
