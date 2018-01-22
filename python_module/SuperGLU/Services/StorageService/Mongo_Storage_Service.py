# -*- coding: utf-8 -*-
import base64
import uuid

#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
#from boto.exception import S3ResponseError
from mongoengine import (connect, Document, DictField, MapField, 
                         ListField, StringField, IntField, URLField,
                         DynamicField)
from SuperGLU.Services.StorageService.Storage_Service_Interface import (SerializedStorage,
    DATA_TYPE_DB, DATA_TYPE_MEDIA, SERIALIZABLE_DATA_TYPE)
from SuperGLU.Util.ErrorHandling import logError, logWarning
from SuperGLU.Util.Serialization import nativizeObject, serializeObject, NamedSerializable, JSON_FORMAT

VALID_STORAGE_TYPES = (DATA_TYPE_DB, DATA_TYPE_MEDIA)
CONTENT_TYPES = {'image/jpeg': 'jpg',
                 'application/json': 'json'}

# WARNING: In dealing with MongoEngine, all objects are cached views
#          If you have multiple such views, they will NOT be informed
#          when you change the other views.  Be advised.

class StorageObject(Document):
    """
    Data in the storage service
    @param key: A unique id (GUID) for the object
    @param name: A name for the object.  Should be unique within bucket.
    @param value: Stored value
    @param description: Description of this value
    @param content_type: A content type (e.g., Serializable)
    """
    key = StringField(unique=True, primary_key=True)
    name = StringField(unique=True)
    value = DynamicField()
    data_type = StringField()
    description = StringField()

class S3StorageObject(Document):
    """
    Stub for data in the S3 Storage service
    """
    key = StringField(unique=True, primary_key=True)
    name = StringField(unique=True)
    value = DynamicField()
    data_type = StringField()
    description = StringField()
    link = URLField()

class MongoStorageService(SerializedStorage):
    """ Service that wraps Mongo-backed Buckets """

    def __init__(self, conn=None, *args, **kwds):
        super(MongoStorageService, self).__init__(*args, **kwds)
        if isinstance(conn, str):
            conn = connect(conn)
        self._conn = conn

    def hasBucket(self, name):
        return (name in self.getBucketNames())

    def getBucket(self, name):
        return Bucket.objects(bucket_name=name).first()

    def getBucketNames(self):
        return [bucket.bucket_name for bucket in Bucket.objects]

    def addBucket(self, name):
        if not self.hasBucket(name):
            bucket = Bucket.make(name)
            bucket.save()

    def _renameBucket(self, oldName, newName):
        bucket = self.getBucket(oldName)
        if bucket:
            bucket.setBucketName(newName)
        else:
            logWarning("Could not rename missing bucket: %s"(oldName,))

    def delBucket(self, name):
        if name is not None:
            buckets = Bucket.objects(bucket_name=name)
            buckets.delete()
        else:
            logWarning("Could not remove missing bucket: %s"(name,))
        

class Bucket(Document):
    """
    A bucket (e.g., project) where data is stored
    """
    STORAGE_ADAPTORS = (StorageObject, S3StorageObject)
    bucket_name = StringField(max_length=120, unique=True,
                              required=True, primary_key=True)
    name_map = MapField(StringField())              # {name: key} (Can just search for this, if needed)
    adaptor_map = MapField(IntField())              # {key: STORAGE_ADAPTORS index}
    tag_maps = MapField(ListField(StringField()))   # {tag_name: keys[]}
    
    @classmethod
    def make(cls, bucketName, tagMaps=None, adaptorMap=None, nameMap=None,
                 storageAdaptors=None):
        if tagMaps is None: tagMaps = {}
        if adaptorMap is None: adaptorMap = {}
        if nameMap is None: nameMap = {}
        return cls(**{'bucket_name' : bucketName, 'tag_maps' : tagMaps,
                    'name_map' : nameMap, 'adaptor_map' : adaptorMap})

    # Bucket Naming
    def getBucketName(self):
        return self.bucket_name

    def setBucketName(self, name):
        self.reload()
        self.bucket_name = name
        self.save()
        self.reload()

    # Resolving Reference ID's and Names
    def hasKey(self, key):
        return isinstance(key, basestring) and key in self.adaptor_map

    def hasName(self, name):
        return isinstance(name, basestring) and name in self.name_map

    def hasRef(self, key=None, name=None):
        key = self.resolveRef(key, name)
        return self.hasKey(key)

    def resolveRef(self, key=None, name=None):
        ref = None
        if name == '':
            name = None
        if (key is not None or name is not None):
            if ((name is None and self.hasKey(key)) or
                ((name is not None) and (self.getName(key) == name))):
                ref = key
            elif (key is None and self.hasName(name)):
                ref = self.name_map[name]
        return ref

    def getMatchingKeys(self, tags=None, storageType=None):
        if tags is not None:
            keys = set()
            for tag in tags:
                if isinstance(tag, basestring) and tag in self.tag_maps:
                    keys.update([k for k in self.tag_maps[tag] if
                                 ((storageType is None) or
                                  (storageType == self.adaptor_map.get(k, None)))])
            keys = list(keys)
        elif (storageType is not None):
            keys = [k for k in self.adaptor_map.keys() if
                    (storageType == self.adaptor_map.get(k, None))]
        else: 
            keys = self.adaptor_map.keys()
        return keys

    # Managing Tags
    def hasTag(self, tag):
        return isinstance(tag, basestring) and tag in self.tag_maps

    def hasTagKey(self, tag, key=None, name=None):
        key = self.resolveRef(key, name)
        if self.hasTag(tag) and self.hasKey(key):
            return key in self.tag_maps[tag]
        return False

    def getObjectTags(self, key=None, name=None):
        key = self.resolveRef(key, name)
        if self.hasKey(key):
            tags = [tag for tag in self.tag_maps
                    if key in self.tag_maps[tag]]
            return tags
        else:
            return []

    def addTagKey(self, tag, key=None, name=None, delaySave=False):
        if not delaySave:
            self.reload()
        key = self.resolveRef(key, name)
        try:
            tag = str(tag)
        except Exception:
            logWarning("ERROR: Invalid tag couldn't convert from unicode")
            tag = None
        if key is not None and isinstance(tag, str) and not self.hasTagKey(tag, key):
            if self.hasTag(tag):
                self.tag_maps[tag].append(key)
            else:
                self.tag_maps[tag] = [key]
            if not delaySave:
                self.save()
                self.reload()

    def delTagKey(self, tag, key=None, name=None, delaySave=False):
        if not delaySave:
            self.reload()
        key = self.resolveRef(key, name)
        if self.hasTagKey(tag, key):
            self.tag_maps[tag].remove(key)
            if not delaySave:
                self.save()
                self.reload()

    def changeTags(self, tags, key=None, name=None, delaySave=False):
        if not delaySave:
            self.reload()
        key = self.resolveRef(key, name)
        oldTags = self.getObjectTags(key)
        obseleteTags = set(oldTags)
        # Add New Tags
        for tag in tags:
            self.addTagKey(tag, key, delaySave=delaySave)
            if tag in obseleteTags:
                obseleteTags.remove(tag)
        # Remove ones not in the new set
        for tag in obseleteTags:
            self.delTagKey(tag, key, delaySave=delaySave)
        if not delaySave:
            self.save()
            self.reload()
        
    def getStorageAdaptor(self, key=None, name=None):
        if name is not None:
            key = self.resolveRef(key, name)
        if self.hasKey(key):
            adaptorId = self.adaptor_map[key]
            return self.STORAGE_ADAPTORS[adaptorId]
        return None

    def _getData(self, key):
        if key is None:
            return None
        storage = self.getStorageAdaptor(key)
        if storage is not None:
            data = storage.objects(key=key).first()
            if data is None: logWarning("No data for: ", key)
            return data
        logWarning("No data for: ", key)
        return None       

    def getValue(self, key=None, name=None):
        key = self.resolveRef(key, name)
        data = self._getData(key)
        if data is not None:
            return data.value
        else:
            return None

    def getLink(self, key=None, name=None):
        key = self.resolveRef(key, name)
        data = self._getData(key)
        if data is not None and isinstance(data, S3StorageObject):
            # Replace this with the S3 link in the future
            return "prod.x-in-y.com"
        else:
            return None

    def getName(self, key):
        data = self._getData(key)
        if data is not None:
            if data.name != '':
                return data.name
            else:
                return None
        else:
            return None

    def changeName(self, newName, key=None, name=None):
        self.reload()
        key = self.resolveRef(key, name)
        data = self._getData(key)
        isChanged, data = self._changeName(newName, data)
        if isChanged:
            data.save()
            self.save()
            self.reload()
            return True
        else:
            return False

    def _changeName(self, newName, data):
        if newName is None:
            newName = ''
        if ((data is not None) and
            (newName == '' or not self.hasName(newName))):
            key = data.key
            name = self.getName(key)
            # Update any internal naming data
            if data.data_type == SERIALIZABLE_DATA_TYPE:
                value = data.value
                value = nativizeObject(value, None, JSON_FORMAT)
                if isinstance(value, NamedSerializable):
                    if newName == '':
                        value.setName(None)
                    else:
                        value.setName(newName)
                value = serializeObject(value, JSON_FORMAT)
                data.value = value
            # Update the storage service data
            data.name = newName
            if (name is not None):
                del self.name_map[name]
            if newName != '':
                self.name_map[newName] = key
            isChanged = True
        else:
            isChanged = False
        return isChanged, data

    def getDescription(self, key=None, name=None):
        key = self.resolveRef(key, name)
        data = self._getData(key)
        if data is not None:
            return data.description
        else:
            return None

    def getDataType(self, key=None, name=None):
        key = self.resolveRef(key, name)
        data = self._getData(key)
        if data is not None:
            return data.data_type
        else:
            return None  

    def setValue(self, key=None, value=None, name=None, description=None, tags=None,
                 storageType=None, dataType=None, allowOverwrite=False, allowCreate=True):
        self.reload()
        logWarning("SETTING VALUE")
        hasKey = self.hasKey(key)
        hasName = self.hasName(name)
        ref = self.resolveRef(key, name)
        # Make sure reference is valid, if any given
        if (ref is None) and ((hasKey and hasName) or
                              (hasName and key is not None)):
            logWarning("INVALID: Mismatched unique keys in set value: (key=%s, name=%s)"%(key, name))
            return False
        # Overwrite existing data
        # This is aborted if another entry uses has the new 'name'
        elif (ref is not None) and allowOverwrite:
            return self._updateValue(key, value, name, description,
                                     tags, storageType, dataType)
        # Create a new entry
        # The key must not already exist and a non-None value must be given
        elif (ref is None) and allowCreate:
                return self._createValue(key, value, name, description,
                                         tags, storageType, dataType)
        else:
            logWarning('INVALID CONDITION')
            return False

    def _updateValue(self, key, value=None, name=None, description=None, tags=None,
                     storageType=None, dataType=None):
        key = self.resolveRef(key, name)
        currentName = self.getName(key)
        data = self._getData(key)
        if key is not None and data is not None:
            if name is not None and currentName != name:
                isChanged, data = self._changeName(name, data)
                if not isChanged:
                    # Failed on change name attempt
                    logWarning("Failed to update, rename failed: ", name)
                    return False
            if value is not None:
                data.value = value
            if dataType is not None:
                data.data_type = dataType
            if description is not None:
                data.description = description
            if storageType is not None:
                # @TODO: Fix this so it works appropriately
                # (e.g., changes the stored object type)
                # For now, no-op
                # self.adaptor_map[key] = storageType
                pass
            if tags is not None:
                self.changeTags(tags, key, delaySave=True)
            data.save()
            self.save()
            self.reload()
            return True
        else:
            logWarning("Error in updateValue. Couldn't get rename for: " + str(key))
            return False

    def _createValue(self, key, value, name='', description='', tags=None,
                     storageType=DATA_TYPE_DB, dataType=''):
        # Force Valid Default values
        if name is None: name = ''
        if description is None: description = ''
        if tags is None: tags = []
        if dataType is None: dataType = ''
        if storageType is None: storageType = DATA_TYPE_DB
        
        # Must be a valid storage type
        if (key is not None and
            isinstance(key, basestring) and
            isinstance(storageType, int) and
            storageType in VALID_STORAGE_TYPES):
            storageData = {'key' : key, 'value' : value,
                           'name' : name, 'data_type' : dataType,
                           'description' : description}
            storageClass = self.STORAGE_ADAPTORS[storageType]
            data = storageClass(**storageData)
            if name != '':
                self.name_map[name] = key
            self.adaptor_map[key] = storageType
            for tag in tags:
                self.addTagKey(tag, key, delaySave=True)
            data.save()
            self.save()
            self.reload()
            return True
        else:
            logWarning("Couldn't create :" + str(key))
            return False

    def delValue(self, key=None, name=None):
        self.reload()
        key = self.resolveRef(key, name)
        if key is not None and self.hasKey(key):
            name = self.getName(key)
            data = self._getData(key)
            if name is not None:
                del self.name_map[name]
            del self.adaptor_map[key]
            self.changeTags([], key, delaySave=True)
            data.delete()
            self.save()
            self.reload()
            return True
        else:
            return False

    def exportData(self):
        keys = self.adaptor_map.keys()
        outData = []
        for key in keys:
            value = self.getValue(key)
            name = self.getName(key)
            tags = self.getObjectTags(key)
            description = self.getDescription(key)
            storageType = self.adaptor_map[key]
            dataType = self.getDataType(key)
            outData.append([key, value, name, tags, storageType, dataType])
        return outData

    def resolveInconsistencies(self, deleteBad=False):
        self.name_map.clear()
        self.save()
        for key in self.adaptor_map.keys():
            data = self._getData(key)
            if data is None:
                badKeys.append(key)
            else:
                name = data.name
                if name == '':
                    name = None
                self.name_map[name] = key
                self._changeName(name, data)
        self.save()
        return StorageObject.objects, self.adaptor_map, self.name_map
        

if __name__ == '__main__':
    # Backup to files
    if False:
        outDataFile = 'StorageServiceBackup.log'
        conn = connect("StorageService_DB")
        try:
            storageService = MongoStorageService(conn)
            outData = storageService.exportBucket('ONR')
        except Exception, exc:
            logWarning(exc)
        finally:
            conn.close()
        outStr = serializeObject(outData)
        with open(outDataFile, 'wb') as aFile:
            aFile.write(outStr)
    if False:
        conn = connect("StorageService_DB")
        try:
            storageService = MongoStorageService(conn)
            bucket = storageService.getBucket("ONR")
            bucket.resolveInconsistencies()
        #except Exception as exc:
        #    logWarning("EXCEPT: ", exc)
        finally:
            conn.close()

        
