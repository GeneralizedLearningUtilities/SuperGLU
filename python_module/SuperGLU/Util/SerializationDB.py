# -*- coding: utf-8 -*-
"""
SerializationDB Package
-----------------------------------
Description: This package is an an addon to the Serialization package,
providing save/load functionality for Serializable objects

The following objects are included:
    * SerializableDBWrapper: Base class for wrapping a database connection
    * SerializableMongoWrapper: Concrete implementation of
      SerializableDBWrapper for writing to a MongoDB collection using
      pymongo
    * DBSerialized: class decorator for Serializables that adds the wrapper
      methods to the class
    * ReadWriteChecking: class decorator for unittest.TestCase's that adds
      two helpful asserts for unit testing Serializable's that are decorated
      with DBSerialized

Basic usage would include start configuration and decorating classes
with DBSerialized.  On startup you would configure the wrapper you
wanted and then configure the wrapper factory.  For instance, if you
were to use the MongoDB wrapper:

    MONGO_URI = "mongodb://127.0.0.1:27017/mydb"
    SerializableMongoWrapper.configureConnection(MONGO_URI)

    def makeMongo(collection):
        return SerializableMongoWrapper(collection)

    SerializableDBWrapper.setWrapperFactory(makeMongo)

Then you can decorate Serializable classes and use the helper methods:

    @DBSerialized("Entities")
    class MyEntity(SuperGlu_Serializable):
        def __init__(self, value=None):
            super(MyEntity, self).__init__()
            self._value = value;

        def initializeFromToken(self, token, context=None):
            super(MyEntity, self).initializeFromToken(token, context)
            self._value = token.__getitem__('value', True, None)

        def saveToToken(self):
            token = super(MyEntity, self).saveToToken()
            token['value'] = self._value
            return token

    #Create
    x = MyEntity('x')
    x.save()

    #Read/Update
    y = MyEntity.read(x.getId())
    y._value = 'y'
    y.save()

    #Iterate
    for i in MyEntity.objects():
        print i.getId(), i._value

IMPORTANT NOTE ON COLLECTIONS: by default, the collection name is specified
by DEFAULT_SERIALIZABLES_COLLECTION in this module.  So if you just create
a default wrapper instance of, say, the MongoDB wrapper, then everything
you save with that wrapper will end up in that collection.  On the other
hand, the DBSerialized decorator assumes that the default collection should
be class ID of the class being decorated.  Basically, if you use the decorator
with no collection specified, look in the collection with the same name as
the class.  If you use a wrapper directly, then look in the collection that
you manually specify.  If you use a wrapper directly but don't specify a
collection, then look in DEFAULT_SERIALIZABLES_COLLECTION.

In addition, the wrapper supports indexing.  Please keep in mind that how
indexes are handled is managed by individual wrapper implementations. In
general, a Serializable class should provide the class variable INDEXES.
It should either be an iterable of strings or a function that eventually
returns an iterable of strings.  Also note that if the Serializable is also
decorated with DBSerialized, checkIndexes will be called automatically.

This package also provides the decorator ReadWriteChecking for enhancing
unittest.TestCase instances for testing Serializable's, including a simple
read/write/compare test.
"""

import json

from SuperGLU.Util.Serialization import (
    untokenizeObject,
    tokenizeObject,
    nativizeObject,
    makeSerialized,
    makeNative,
    SuperGlu_Serializable,
)

from SuperGLU.Util.Attr import get_prop

from pymongo import MongoClient

# Database Format Constants
MONGO_FORMAT = 'mongodb'
VALID_DB_FORMATS = (MONGO_FORMAT,)

#Default collection collection serializables are stored in
DEFAULT_SERIALIZABLES_COLLECTION = 'Serializables'
BASIC_ID_KEY = 'id'
MONGO_ID_KEY = '_id'
CLASS_ID_KEY = 'classId'
INDEXES_KEY = 'INDEXES'


class SerializableDBWrapper(object):
    """ Base class for wrapping a database connection for load/save
    of Serializable's.  Inheritors should (at a minimum) implement
    _find, _save, getKeys, and getObjects.  Unless otherwise specified,
    objects returned from the database will be nativized (i.e. not in
    the DB format or in StorageToken form

    This class is also the home of the wrapper factory used by classes
    decorated with the DBSerialized decorator.  It will be called lazily,
    but it needs to be set before using any of the methods supplied by
    the decorator.  IMPORTANT: currently it can only be set once at
    startup.  In-flight reconfiguration is not currently supported """

    WRAPPER_FACTORY = None

    @classmethod
    def setWrapperFactory(cls, aCallable):
        cls.WRAPPER_FACTORY = staticmethod(aCallable)

    def __init__(self, connection, collection=DEFAULT_SERIALIZABLES_COLLECTION):
        self._connection = connection
        self._collectionName = collection

    def read(self, key, context=None):
        """ Return an unserialized/nativized object from the datastore
        corresponding to the given key.
        @param key the key to be used for locating the object in the DB
        @param context object passed to Serialization routines"""
        obj = self._find(key)
        return untokenizeObject(obj, context)

    def save(self, obj):
        """ Save the given Serializable to the database
        @param obj Object which must have Serializable as a base class"""
        self._save(obj)

    def getKeys(self, **kwrdQuery):
        """ Return the key for all objects available in DB.  Keywords
        supplied are interpreted by the implementor (but they should
        generally describe a query/filter). """
        raise NotImplementedError

    def getObjects(self, **kwrdQuery):
        """ Return all objects available in DB.  Keywords supplied are
        interpreted by the implementor (but they should generally describe
        a query/filter). """
        raise NotImplementedError

    def _find(self, key):
        """ Find and return a single object
        @param key the key to be used for locating the object in the DB """
        raise NotImplementedError

    def _save(self, obj):
        """ Persist a single object to the database.  Note that implementers
        are probably going to want to call tokenizeObject on obj relatively
        early.
        @param obj the object implenting Serializable to saved in the database"""
        raise NotImplementedError

    def checkIndexes(self, cls):
        """ Insure index existence by checking for any specified indexes
        and then insure that they exist in the datastore. Obviously
        HIGHLY dependent on the wrapper implementation and the backend.
        NOTE: if your class is decorated with DBSerialized then this
        function will be called for you automatically.
        @param a class that implements Serializable"""
        raise NotImplementedError

    def _listIndexes(self, cls):
        """ Helper to examine the given class and identifying all index
        names.  Note that the meaning of the name is probably a field in
        the class, the backend, or both... BUT it is dependent on the
        implementing wrapper and the backend.
        @param a class that implements Serializable"""
        indexes = get_prop(cls, INDEXES_KEY, list)
        return indexes or []


class SerializableMongoWrapper(SerializableDBWrapper):
    """ Concrete implmentation of SerializableDBWrapper for using MongoDB
    as the datastore (via pymongo).

    Please note that SerializableMongoWrapper.configureConnection should
    be called with the correct MongoDB URI as specified by
    http://api.mongodb.org/java/current/com/mongodb/MongoURI.html"""

    #Per the pymongo docs, we should use the same MongoClient (which
    #has concurrency support and connection pooling)
    CLIENT = None

    @classmethod
    def configureConnection(cls, uri):
        if uri:
            SerializableMongoWrapper.CLIENT = MongoClient(uri)
        else:
            SerializableMongoWrapper.CLIENT = None

    def __init__(self, collection=DEFAULT_SERIALIZABLES_COLLECTION):
        """ Note that the class method SerializableMongoWrapper.configureConnection
        should be called before creating an instance of this wrapper
        """
        super(SerializableMongoWrapper, self).__init__(self.CLIENT, collection)
        self._db = self._connection.get_default_database()
        self._collection = self._db[self._collectionName]

    def getKeys(self, **kwrdQuery):
        if kwrdQuery:
            query = kwrdQuery
        else:
            query = {}
        return [k[MONGO_ID_KEY] for k in self._collection.find(query, {})]

    def getObjects(self, **kwrdQuery):
        if kwrdQuery:
            objs = self._collection.find(kwrdQuery)
        else:
            objs = self._collection.find()
        return [self.nativizeReadObject(obj) for obj in objs]

    def nativizeReadObject(self, dbobj, context=None):
        """ Helper for nativizing an object read from the DB. The main
        work is removing anything added as part of the _save routine """
        if not dbobj:
            return None

        #Remove mods done in _save... including the index names we add
        #as top-level properties.  Basically, remove everything but the
        #classId key:
        if MONGO_ID_KEY in dbobj:
            del dbobj[MONGO_ID_KEY]

        classId = dbobj.get(CLASS_ID_KEY, None)
        if classId:
            del dbobj[CLASS_ID_KEY]
            keys = set(dbobj.keys())
            keys.remove(classId) #the actual class id - not the literal
            for k in keys:
                del dbobj[k]

        js = json.dumps(dbobj)
        return nativizeObject(js)

    def checkIndexes(self, cls):
        """Each string in the class variable INDEXES will be treated as
        an index field name and will be stored as a top-level property
        in Mongo DB.  Indexes are checked by calling ensure_index.  Note
        that the property values are extracted from the object via
        Util.Attr.get_prop so you have options for naming.  Finally, the
        index names id, _id, and classId are automatically removed from
        the index list, but _id and classId will always be indexed."""

        #Note that we force indexing on classId - because we add
        #it for all objects
        for key in list(self._listIndexes(cls)) + [CLASS_ID_KEY]:
            self._collection.ensure_index(key)

    #Override - we return a set instead of a list (no dups!) with our
    #disallowed index names removed.
    def _listIndexes(self, cls):
        indexes = super(SerializableMongoWrapper, self)._listIndexes(cls)
        return set(indexes) - set([BASIC_ID_KEY, MONGO_ID_KEY, CLASS_ID_KEY])

    def _find(self, key):
        dbobj = self._collection.find_one({MONGO_ID_KEY : key})
        return self.nativizeReadObject(dbobj)

    def _save(self, obj):
        if obj.getId() is None:
            obj.updateId()
        token = tokenizeObject(obj)
        js = makeSerialized(token)
        dbobj = json.loads(js)
        dbobj[MONGO_ID_KEY] = token.getId()
        dbobj[CLASS_ID_KEY] = token.getClassId()

        #Set index values - note that we use the original object and
        #not the token
        idxList = self._listIndexes(obj.__class__)
        for indexName in idxList:
            dbobj[indexName] = get_prop(obj, indexName)

        self._collection.update({MONGO_ID_KEY: dbobj[MONGO_ID_KEY]}, dbobj, upsert=True)


#######################################################################
# BEGIN DBSerialized decorator (including supporting helpers)

# These functions are meant to be applied to a class as methods (all
# but _read with be classmethods's). It is assumed (and verified) that
# the class will inherit from Serializable. In addition, the class will
# be updated to have the class variables _dbFactoryArgs and _dbWrapper.
# Note that _dbWrapper is created lazily via the function _lazyWrapper.

# This is really ONLY for testing
_lazyWrapperClasses = set()
def _flushLazyWrappers():
    global _lazyWrapperClasses
    for cls in _lazyWrapperClasses:
        cls._dbWrapper = None
    _lazyWrapperClasses = set()

def _lazyWrapper(cls):
    if not cls._dbWrapper:
        global _lazyWrapperClasses
        _lazyWrapperClasses.add(cls)

        cls._dbWrapper = SerializableDBWrapper.WRAPPER_FACTORY(*cls._dbFactoryArgs)
        try:
            cls._dbWrapper.checkIndexes(cls)
        except:
            pass #Might not be implemented

#Our one instance method - the others will be class methods
def _save(self):
    self._lazyWrapper()
    self._dbWrapper.save(self)

def _read(cls, key, context=None):
    cls._lazyWrapper()
    return cls._dbWrapper.read(key, context)

def _objects(cls, **kwrdQuery):
    cls._lazyWrapper()
    #This is a helper method for classes, so "no query" defaults to
    #checking class ID. Luckily we're used on Serializables, so the
    #metaclass factory tracks class ID's
    if not kwrdQuery:
        kwrdQuery = {CLASS_ID_KEY: cls.CLASS_ID}
    return cls._dbWrapper.getObjects(**kwrdQuery)

def _keys(cls, **kwrdQuery):
    cls._lazyWrapper()
    #Same deal as _objects when it comes to the query
    if not kwrdQuery:
        kwrdQuery = {CLASS_ID_KEY: cls.CLASS_ID}
    return cls._dbWrapper.getKeys(**kwrdQuery)


def DBSerialized(*factoryArgs):
    """ Decorates a Serializable class. The decorated class gets an instance
    method save and the classmethods read, objects, and keys. These four
    methods correspond to the SerializableMongoWrapper methods save, read,
    getObjects, and getKeys respectively.

    NOTE that the collection used is optional, but that means that the
    decorator is parameterized. If you wish to use the default collection
    (which is the class ID of the decorated Serializable), then you must
    append empty parentheses to your class def's decorator:

        #MySerial().save() will save to a collection name MySerial in the
        #database connected to via the factory-generated wrapper created
        #by the factory passed to SerializableDBWrapper.setWrapperFactory
        #on startup
        @DBSerialized()
        class MySerial(SuperGlu_Serializable):
            ...

    Note that if the class supports indexing (has the class level variable
    INDEXES), then wrapper.checkIndexes will be called when init happens
    """
    def decorator(aClass):
        if not issubclass(aClass, SuperGlu_Serializable):
            raise NotImplementedError("%s is not a subclass of Serializable" % aClass)

        #Hacky cheat - if they don't specify a collection, we'll use the
        #class ID as the collection name - note that we are relying on
        #the fact that the Mongo factory has single argument and that it
        #is collection name
        realArgs = factoryArgs
        if aClass.CLASS_ID and not factoryArgs:
            realArgs = [aClass.CLASS_ID]

        aClass._dbWrapper = None
        aClass._dbFactoryArgs = tuple(realArgs)
        aClass._lazyWrapper = classmethod(_lazyWrapper)
        aClass.save = _save
        aClass.read = classmethod(_read)
        aClass.objects = classmethod(_objects)
        aClass.keys = classmethod(_keys)

        return aClass
    return decorator

#######################################################################
# BEGIN ReadWriteChecking decorator for classes testing DBSerialized
# classes (see the DBSerialized decorator above)

def _assertSerialEquals(self, obj1, obj2):
    self.assertEquals(obj1, obj2)
    self.assertEquals(tokenizeObject(obj1), tokenizeObject(obj2))

def _assertReadWrite(self, obj):
    obj.save()
    copy = obj.__class__.read(obj.getId())
    self.assertSerialEquals(obj, copy)

def ReadWriteChecking(aClass):
    """Decorates a class descending from unittest.TestCase.  It provides
    two new assertions:

      * assertSerialEquals(self, obj1, obj2) checks the two specified
        Serializable instances for equality AND that their tokeninzed states
        are equal as well. Note that this will work with any Serializable,
        not just classes decorated with DBSerialized

      * assertReadWrite(self, obj) checks that the specified instance of
        a Serializable equals a copy made by saving the instances and then
        reading it back.  Note that this requires that the object be a
        Serializable AND be decorated by DBSerialized

    Please see AWS_Core_Services/Tests/AuthUser_UnitTests.py for an
    example of usage
    """

    import unittest

    if not issubclass(aClass, unittest.TestCase):
        raise NotImplementedError("%s is not a subclass of unittest.TestCase" % str(aClass))

    aClass.assertSerialEquals = _assertSerialEquals
    aClass.assertReadWrite = _assertReadWrite
    return aClass
