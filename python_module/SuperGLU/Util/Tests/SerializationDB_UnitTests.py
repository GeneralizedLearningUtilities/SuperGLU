import unittest

from SuperGLU.Util.Serialization import (
    SuperGlu_Serializable,
    untokenizeObject,
    tokenizeObject,
)

from SuperGLU.Util.SerializationDB import (
    SerializableDBWrapper,
    SerializableMongoWrapper,
    DBSerialized,
    ReadWriteChecking,
    _flushLazyWrappers
)

from SuperGLU.Util.Attr import get_prop

from AutoTutor_Interpreter.StudentModel.StudentKnowledge import (
    DialogSession,
    StudentSessionData,
    StudentStatement,
)


from pymongo import Connection

TEST_DB_URI = 'mongodb://127.0.0.1:27017/serial_test_db'

class TestClassSimple(SuperGlu_Serializable):

    def __init__(self, value=None):
        super(TestClassSimple, self).__init__()
        self._value = value;

    def initializeFromToken(self, token, context=None):
        super(TestClassSimple, self).initializeFromToken(token, context)
        self._value = token.__getitem__('value', True, None)

    def saveToToken(self):
        token = super(TestClassSimple, self).saveToToken()
        token['value'] = self._value
        return token

class TestClassComplex(SuperGlu_Serializable):

    def __init__(self, simpleList=[]):
        super(TestClassComplex, self).__init__()
        self._simples = list(simpleList);

    def initializeFromToken(self, token, context=None):
        super(TestClassComplex, self).initializeFromToken(token, context)
        self._simples = [untokenizeObject(i) for i in token.get('simples', [])]

    def saveToToken(self):
        token = super(TestClassComplex, self).saveToToken()
        token['simples'] = [tokenizeObject(i) for i in self._simples]
        return token

def _buildComplex(*names):
    return TestClassComplex([TestClassSimple(n) for n in names])

def makeMongo(collection=None):
    if collection:
        return SerializableMongoWrapper(collection)
    else:
        return SerializableMongoWrapper()

@ReadWriteChecking
class Serialization_Tests(unittest.TestCase):
    def setUp(self):
        Connection(TEST_DB_URI).drop_database('serial_test_db')
        SerializableMongoWrapper.configureConnection(TEST_DB_URI)
        SerializableDBWrapper.setWrapperFactory(makeMongo)

        #Pre-created wrapper for direct use
        self.wrapper = makeMongo()

    def tearDown(self):
        SerializableDBWrapper.setWrapperFactory(None)
        SerializableMongoWrapper.configureConnection(None)
        _flushLazyWrappers()

    def testReadWrite(self):
        orig = _buildComplex("Hello", "World")

        self.wrapper.save(orig)
        copy = self.wrapper.read(orig.getId())

        self.assertSerialEquals(orig, copy)

        copy._simples.append("Fozzy Bear")
        self.assertNotEquals(tokenizeObject(orig), tokenizeObject(copy))

        self.wrapper.save(copy)
        copy2 = self.wrapper.read(orig.getId())

        self.assertSerialEquals(copy, copy2)

    def testFindNothingAndSomething(self):
        self.assertIsNone(self.wrapper.read("12345"))

        something = _buildComplex("Here", "Now")
        something.updateId("12345")
        self.wrapper.save(something)
        found = self.wrapper.read("12345")

        self.assertSerialEquals(something, found)


    def testGetKeys(self):
        self.assertEquals(0, len(self.wrapper.getKeys()))

        allObjs = [
            _buildComplex("a", "b"),
            _buildComplex("x", "y"),
            _buildComplex("Kermit", "Frog"),
        ]

        for obj in allObjs:
            self.wrapper.save(obj)

        startKeys = set([o.getId() for o in allObjs])

        dbKeys = set(self.wrapper.getKeys())

        inter = startKeys.intersection(dbKeys)
        self.assertEquals(len(allObjs), len(inter))

        dbKeys = set(self.wrapper.getKeys(classId="TestClassComplex"))

        inter = startKeys.intersection(dbKeys)
        self.assertEquals(len(allObjs), len(inter))

    def testGetObjects(self):
        self.assertEquals(0, len(self.wrapper.getObjects()))

        allObjs = [
            _buildComplex("Ralph"),
            _buildComplex("Gonzo"),
            _buildComplex("Animal"),
        ]
        allObjsD = dict([ (o.getId(), o) for o in allObjs ])

        self.assertEquals(len(allObjs), len(allObjsD))

        for obj in allObjs:
            self.wrapper.save(obj)

        dbObjs = self.wrapper.getObjects()
        self.assertEquals(len(allObjs), len(dbObjs))
        for dbo in dbObjs:
            self.assertTrue(dbo.getId() in allObjsD)
            self.assertSerialEquals(dbo, allObjsD[dbo.getId()])

        dbObjs = self.wrapper.getObjects(classId="TestClassComplex")
        self.assertEquals(len(allObjs), len(dbObjs))
        for dbo in dbObjs:
            self.assertTrue(dbo.getId() in allObjsD)
            self.assertSerialEquals(dbo, allObjsD[dbo.getId()])

    def testRealWorldReadWrite(self):
        def makeDialogSession(prefix, nPrompts=0, nHints=0, goodClosing=True, sessionCompleted=False):
            ds = DialogSession(
                userName=prefix + 'UserName',
                userID=prefix + 'UserID',
                conceptID=prefix + 'ConceptID',
                nPrompts=nPrompts,
                nHints=nHints,
                closingType=DialogSession.BAD_CLOSING if goodClosing else DialogSession.GOOD_CLOSING,
                sessionCompleted=sessionCompleted,
            )
            ds.addStudentStatement(prefix + " msg", 1.0, 1.0)
            return ds

        source = StudentSessionData("TestUserID", "TestUserName")
        source.addSession("concept1", makeDialogSession("C1D1", 1, 1))
        source.addSession("concept1", makeDialogSession("C1D2", 2, 2))
        source.addSession("concept2", makeDialogSession("C2D1", 3, 3))
        source.addSession("concept2", makeDialogSession("C2D2", 4, 4))

        self.wrapper.save(source)
        copy = self.wrapper.read(source.getId())

        self.assertSerialEquals(source, copy)

        copy.addSession("concept3", makeDialogSession("C3D1", 5, 5))
        self.assertNotEquals(tokenizeObject(source), tokenizeObject(copy))

        self.wrapper.save(copy)
        copy2 = self.wrapper.read(source.getId())

        self.assertSerialEquals(copy, copy2)

        #Dialog sessions use session ID as their key, which allows us
        #to test custom key logic with our wrapper
        #ALSO - they use the decorator so we can test them separately
        ds = makeDialogSession("Standalone", 5, 5)
        ds.save()
        #Use our save/read/compare check on an already saved object
        self.assertReadWrite(ds)

        dsCopy = DialogSession.objects(_id=ds.getSessionID())[0]
        self.assertSerialEquals(ds, dsCopy)

        dsCopy = DialogSession.read(ds.getSessionID())
        self.assertSerialEquals(ds, dsCopy)

    def testDecorated(self):
        @DBSerialized("DecoratedCollection")
        class TestDecSimple(SuperGlu_Serializable):
            def __init__(self, value=None):
                super(TestDecSimple, self).__init__()
                self._value = value;

            def initializeFromToken(self, token, context=None):
                super(TestDecSimple, self).initializeFromToken(token, context)
                self._value = token.__getitem__('value', True, None)

            def saveToToken(self):
                token = super(TestDecSimple, self).saveToToken()
                token['value'] = self._value
                return token

        obj = TestDecSimple("MyValue")
        #Do a save/read/compare both before and after an explicit save
        self.assertReadWrite(obj)
        obj.save()
        self.assertReadWrite(obj)

        copy = TestDecSimple.read(obj.getId())
        self.assertSerialEquals(obj, copy)

        copy = TestDecSimple.objects()[0]
        self.assertSerialEquals(obj, copy)

        copy = TestDecSimple.objects(classId="TestDecSimple")[0]
        self.assertSerialEquals(obj, copy)

        copyKey = TestDecSimple.keys()[0]
        self.assertEquals(obj.getId(), copyKey)

        copyKey = TestDecSimple.keys(classId="TestDecSimple")[0]
        self.assertEquals(obj.getId(), copyKey)


@DBSerialized()
class IndexedSimple(SuperGlu_Serializable):
    INDEXES = ['fielda', 'fieldb']
    def __init__(self, a=None, b=None):
        super(IndexedSimple, self).__init__()
        self._fielda = a;
        self._fieldb = b;

    def initializeFromToken(self, token, context=None):
        super(IndexedSimple, self).initializeFromToken(token, context)
        self._fielda = token.__getitem__('fielda', True, None)
        self._fieldb = token.__getitem__('fieldb', True, None)

    def saveToToken(self):
        token = super(IndexedSimple, self).saveToToken()
        token['fielda'] = self._fielda
        token['fieldb'] = self._fieldb
        return token

@DBSerialized()
class IndexedComplex(SuperGlu_Serializable):
    @classmethod
    def INDEXES(cls):
        return ['fielda', 'fieldb']

    def __init__(self, a=None, b=None):
        super(IndexedComplex, self).__init__()
        self._mya = a;
        self._myb = b;

    def getFielda(self):
        return self._mya

    def getFieldb(self):
        return self._myb

    def initializeFromToken(self, token, context=None):
        super(IndexedComplex, self).initializeFromToken(token, context)
        self._mya = token.__getitem__('fielda', True, None)
        self._myb = token.__getitem__('fieldb', True, None)

    def saveToToken(self):
        token = super(IndexedComplex, self).saveToToken()
        token['fielda'] = self._mya
        token['fieldb'] = self._myb
        return token

@ReadWriteChecking
class Indexing_Tests(unittest.TestCase):
    def setUp(self):
        Connection(TEST_DB_URI).drop_database('serial_test_db')
        SerializableMongoWrapper.configureConnection(TEST_DB_URI)
        SerializableDBWrapper.setWrapperFactory(makeMongo)

    def tearDown(self):
        SerializableDBWrapper.setWrapperFactory(None)
        SerializableMongoWrapper.configureConnection(None)
        _flushLazyWrappers()

    def testIndexedValid(self):
        #Make sure our indexing test class actually works
        obj = IndexedSimple("fozzy", "kermit")
        self.assertEquals("fozzy", obj._fielda)
        self.assertEquals("kermit", obj._fieldb)
        self.assertReadWrite(obj)

        obj = IndexedComplex("fozzy", "kermit")
        self.assertEquals("fozzy", obj.getFielda())
        self.assertEquals("kermit", obj.getFieldb())
        self.assertReadWrite(obj)

    def testIndexedSimple(self):
        self._checkIndexedClass(IndexedSimple, ["fielda", "fieldb"])

        obj = IndexedSimple("first", "last")
        self.assertReadWrite(obj)

        self._checkIndexedVals(IndexedSimple, obj, {
            "fielda": "first",
            "fieldb": "last",
        })

    def testIndexedComplex(self):
        self._checkIndexedClass(IndexedComplex, ["fielda", "fieldb"])

        obj = IndexedComplex("mahna", "mahna2")
        self.assertReadWrite(obj)

        self._checkIndexedVals(IndexedComplex, obj, {
            "fielda": "mahna",
            "fieldb": "mahna2",
        })

    def _checkIndexedClass(self, cls, expected_indexes):
        #Pretty white-box, I know

        #Force a lazy init and grab the wrapper
        cls._lazyWrapper()
        wrapper = cls._dbWrapper

        #Insure we're getting the right indexes
        cls_indexes = sorted(get_prop(cls, "INDEXES"))
        self.assertEquals(expected_indexes, cls_indexes)

        #Indexes from class
        self.assertEquals(cls_indexes, sorted(wrapper._listIndexes(IndexedSimple)))

        #The actual DB should index _id, classId, and our indexes
        expected = sorted(cls_indexes + ['_id', 'classId'])

        #checkIndexes should have already been called - so we can check
        #the DB directly for the indexes
        db_indexes = []

        found = wrapper._collection.index_information()
        for name,index in found.iteritems():
            keys = [k for k,direct in index.get('key', [])]
            self.assertEquals(1, len(keys))
            db_indexes.append(keys[0])

        self.assertEquals(expected, sorted(db_indexes))

    def _checkIndexedVals(self, cls, obj, expected):
        raw = cls._dbWrapper._collection.find_one({'_id' : obj.getId()})
        print raw

        for expkey, expval in expected.iteritems():
            foundval = raw.get(expkey, "MISSING:"+expval)
            self.assertEquals(expval, foundval)


if __name__ == "__main__":
    unittest.main()
