# -*- coding: utf-8 -*-
"""
    Tests are intended to be run individually
    >>> python -m unittest bucket_tests.BucketTests.test_create_bucket
"""
import pymongo
import unittest
from mongoengine.connection import connect, disconnect

from SuperGLU.Services.StorageService.Mongo_Storage_Service import (MongoStorageService,
    Bucket, StorageObject)
from SuperGLU.Services.StorageService.Storage_Service_Interface import (BaseStorageService,
    DATA_TYPE_DB, DATA_TYPE_MEDIA)
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, INFORM_REF_ACT, REQUEST_ACT
from SuperGLU.Core.Messaging import Message


class MongoStorageServiceUnitTests(unittest.TestCase):
    BUCKET_KEY = BaseStorageService.BUCKET_KEY
    TYPE_KEY = BaseStorageService.TYPE_KEY
    TAGS_KEY = BaseStorageService.TAGS_KEY
    ALLOW_CREATE_KEY = BaseStorageService.ALLOW_CREATE_KEY
    NAME_KEY = BaseStorageService.NAME_KEY
    DESCRIPTION_KEY = BaseStorageService.DESCRIPTION_KEY
    DATA_TYPE_KEY = BaseStorageService.DATA_TYPE_KEY
    
    VALUE_VERB = BaseStorageService.VALUE_VERB
    VOID_VERB = BaseStorageService.VOID_VERB
    HAS_ELEMENT_VERB = BaseStorageService.HAS_ELEMENT_VERB
    CONTAINS_VERB = BaseStorageService.CONTAINS_VERB
    ASSIGNED_URI_VERB = BaseStorageService.ASSIGNED_URI_VERB

    def setUp(self):
        self.dropdb()
        self.connection = connect('storage_service_test')

    def tearDown(self):
        self.connection.close()
        disconnect()
        self.dropdb()

    def dropdb(self):
        client = pymongo.MongoClient()
        client.drop_database('storage_service_test')
        client.close()

    def makeClient(self):
        # self.client = StorageServiceClient(null, self.bucketName);
        # self.gateway = MessagingGateway("ProcessGateway", [self.client, self.storage]);
        return None

    def populate(self):
        self.serviceName = "StorageService"
        self.dbType = 0;
        self.mediaType = 1;
        self.dataLink = "prod.x-in-y.com";   # Default link for now
        self.bucketName = "ONR";
        self.storage = MongoStorageService(self.serviceName, None);
        self.storage.addBucket(self.bucketName);
        # Populate some storage values
        bucket = self.storage.getBucket(self.bucketName);
        self.keyExists = "Mad Max";
        self.keyExistsName = self.keyExists + "_NAME";
        self.keyExistsVal = "Mel Gibson";
        self.mediaKeyExists = "IMDB";
        self.tag1 = "Cop";
        self.tag2 = "Movie";
        bucket.setValue(self.keyExists, self.keyExistsVal, self.keyExistsName,
                        "Guy in a leather jacket", [self.tag1, self.tag2], self.dbType)
        bucket.setValue(self.mediaKeyExists, "www.imdb.com",
                        self.mediaKeyExists, "", [self.tag2], self.mediaType)
        #Note: original test used None for name BUT name has a unique index
        bucket.setValue("Pallindrome", "Emordnillap", "Eman", "", None, self.dbType)
        self.keyMissing = "Missing"
        self.keys = [self.keyExists, "IMDB", "Pallindrome"]
        self.tags1 = [self.keyExists]
        self.tags2 = [self.keyExists, "IMDB"]
        bucket.save()
        

    def simpleTest(self):
        self.populate()
        x = Bucket.objects(bucket_name="ONR").first()
        print "*"*20
        print Bucket.objects()
        print x.getBucketName()
        print "*"*20
        testKey = "AAAAAAAAA"
        testVal = 10
        x.adaptor_map[testKey] = testVal
        x.aSave()
        print x.adaptor_map.keys()
        y = Bucket.objects(bucket_name="ONR").first()
        print "Added"
        print x.adaptor_map.keys()
        print y.adaptor_map.keys()
        del y.adaptor_map[testKey]
        y.aSave()
        print "Deleted"
        z = Bucket.objects(bucket_name="ONR").first()
        print x.adaptor_map.keys()
        print y.adaptor_map.keys()
        print z.adaptor_map.keys()
        

    def makeMessageContext(self, bucket=None, tags=None, type=None, allowCreate=None,
                           name=None, description=None, dataType=None):
        if (bucket is None): bucket = self.bucketName
        context = {}
        context[self.BUCKET_KEY] = bucket
        if (type is not None): context[self.TYPE_KEY] = type
        if (tags is not None): context[self.TAGS_KEY] = tags
        if (allowCreate is not None): context[self.ALLOW_CREATE_KEY] = allowCreate
        if (name is not None): context[self.NAME_KEY] = name
        if (description is not None): context[self.DESCRIPTION_KEY] = description
        if (dataType is not None): context[self.DATA_TYPE_KEY] = dataType
        return context

    def testPopulateMacro(self):
        self.populate()

    def testAddData_ByMsg(self):
        self.populate()
        key = "Big"
        value = "Ben"
        context = self.makeMessageContext(allowCreate=True)
        msg = Message(self.serviceName, self.VALUE_VERB, key, value,
                      INFORM_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.VALUE_VERB, key)
        self.assertEqual(val, value)

    def testSetData_ByMsg(self):
        self.populate()
        key = self.keyExists
        value = "Ben"
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.VALUE_VERB, key, value,
                      INFORM_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.VALUE_VERB, key)
        self.assertEqual(val, value)

    def testGetData_Exists_ByMsg(self):
        self.populate()
        key = self.keyExists
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.VALUE_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.VALUE_VERB, key)
        self.assertEqual(val, self.keyExistsVal)

    def testGetData_Missing_ByMsg(self):
        self.populate()
        key = self.keyMissing
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.VALUE_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.VALUE_VERB, key)
        self.assertIsNone(val)

    def testDelData_Exists_ByMsg(self):
        self.populate()
        key = self.keyExists
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.VOID_VERB, key, None,
                      INFORM_ACT, context=context)
        bucket = self.storage.getBucket(self.bucketName)
        print bucket.to_json()
        oldBucket = self.storage.getBucket(self.bucketName)
        self.assertTrue(self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key))
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        self.assertFalse(bucket.delValue(key))
        self.assertFalse(self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key))

    def testDelData_Missing_ByMsg(self):
        self.populate()
        key = self.keyMissing
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.VOID_VERB, key, None,
                      INFORM_ACT, context=context)
        bucket = self.storage.getBucket(self.bucketName)
        self.assertFalse(self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key))
        self.storage.receiveMessage(msg)
        self.assertFalse(self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key))

    def testHasDataKey_True_ByMsg(self):
        self.populate()
        key = self.keyExists
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.HAS_ELEMENT_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key)
        self.assertTrue(val)

    def testHasDataKey_False_ByMsg(self):
        self.populate()
        key = self.keyMissing
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.HAS_ELEMENT_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.HAS_ELEMENT_VERB, key)
        self.assertFalse(val)

    def testGetDataKeys_ByMsg(self):
        self.populate()
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.CONTAINS_VERB, None, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.CONTAINS_VERB)
        self.assertItemsEqual(val, self.keys)

    def testGetDataKeys_Tags1(self):
        self.populate()
        context = self.makeMessageContext(tags=[self.tag1])
        msg = Message(self.serviceName, self.CONTAINS_VERB, None, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.CONTAINS_VERB, tags=[self.tag1])
        self.assertItemsEqual(val, self.tags1)

    def testGetDataKeys_Tags2(self):
        self.populate()
        context = self.makeMessageContext(tags=[self.tag2])
        msg = Message(self.serviceName, self.CONTAINS_VERB, None, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.CONTAINS_VERB, tags=[self.tag2])
        self.assertItemsEqual(val, self.tags2)

    def testGetDataKeys_Tags2_DB(self):
        self.populate()
        context = self.makeMessageContext(tags=[self.tag2], type=DATA_TYPE_DB)
        msg = Message(self.serviceName, self.CONTAINS_VERB, None, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.CONTAINS_VERB, tags=[self.tag2], aType=DATA_TYPE_DB)
        self.assertItemsEqual(val, [self.keyExists])

    def testGetDataKeys_Tags2_Media(self):
        self.populate()
        context = self.makeMessageContext(tags=[self.tag2], type=DATA_TYPE_DB)
        msg = Message(self.serviceName, self.CONTAINS_VERB, None, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.CONTAINS_VERB, tags=[self.tag2], aType=DATA_TYPE_MEDIA)
        self.assertItemsEqual(val, [self.mediaKeyExists])

    def testGetDataLink(self):
        self.populate()
        key = self.mediaKeyExists
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.ASSIGNED_URI_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.ASSIGNED_URI_VERB, key)
        self.assertEqual(val, self.dataLink)
    
    def testGetDataLink_NonMedia(self):
        self.populate()
        key = self.keyExists
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.ASSIGNED_URI_VERB, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        val = self.storage.processStorageRequest(bucket, self.ASSIGNED_URI_VERB, key)
        self.assertIsNone(val)

    def testRename(self):
        self.populate()
        key = self.keyExists
        newName = "SomeNewName"
        context = self.makeMessageContext()
        msg = Message(self.serviceName, self.HAS_ELEMENT_VERB, key, newName,
                      INFORM_REF_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        valKey, valName = self.storage.processStorageRequest(bucket, INFORM_REF_ACT, key)
        self.assertEqual(valName, newName)

    def testGetDataName(self):
        self.populate()
        key = self.keyExists
        newName = "SomeNewName"
        context = self.makeMessageContext()
        msg = Message(self.serviceName, INFORM_REF_ACT, key, None,
                      REQUEST_ACT, context=context)
        self.storage.receiveMessage(msg)
        bucket = self.storage.getBucket(self.bucketName)
        valKey, valName = self.storage.processStorageRequest(bucket, INFORM_REF_ACT, key)
        self.assertEqual(valKey, self.keyExists)
        self.assertEqual(valName, self.keyExistsName)


class BucketTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect('storage_service_test')

    def tearDown(self):
        self.connection.close()
        disconnect()
        client = pymongo.MongoClient()
        client.drop_database('storage_service_test')
        client.close()

    def test_create_bucket(self):
        bucket_name = 'test_bucket_create'
        bucket = Bucket.make(bucket_name)
        storageService = MongoStorageService()
        bucket.bucket_name = bucket_name
        bucket.save()

        bucket = None
        bucket = storageService.getBucket(bucket_name)
        self.assertIsNotNone(bucket)
        self.assertEqual(bucket.bucket_name, bucket_name)
        self.assertEqual(bucket.tag_maps, {})
        self.assertEqual(bucket.name_map, {})
        self.assertEqual(bucket.adaptor_map, {})

    def test_mongo(self):
        bucket_name = 'test_bucket_mongo'
        bucket = Bucket()
        bucket.bucket_name = bucket_name
        bucket.save()

        key = 'my_test_key'
        value = 'my test value'
        name = "my name"
        description = 'something meaningful here'
        tags = ['testing', 'development']

        isSaved = bucket.setValue(key, value, name, description, tags=tags)
        obj = bucket._getData(key)

        self.assertIsNotNone(obj)
        self.assertEqual(obj.key, key)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.data_type, '')
        
        self.assertTrue(bucket.hasKey(key))
        for tag in tags:
            self.assertTrue(bucket.hasTag(tag))
            self.assertTrue(bucket.hasTagKey(tag, key))

if __name__ == '__main__':
    unittest.main()
