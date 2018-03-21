import unittest
import uuid
from SuperGLU.Util.Paths import getFileDir, getBasePath
from SuperGLU.Util.JSInterpreter import executeJS
from SuperGLU.Util.Serialization import (SuperGlu_Serializable, StorageToken,
    makeSerialized, makeNative, tokenizeObject, untokenizeObject,
    nativizeObject, serializeObject, VALID_SERIAL_FORMATS)

class Serialization_Tests(unittest.TestCase):
    TEST_CLASS = SuperGlu_Serializable

    def setUp(self):
        self.jsdir = getFileDir(__file__)

    def test__init__(self):
        anId = uuid.uuid4()
        strId = str(anId)
        self.assertIsInstance(SuperGlu_Serializable(), SuperGlu_Serializable)
        self.assertIsInstance(SuperGlu_Serializable(anId), SuperGlu_Serializable)
        self.assertIsInstance(SuperGlu_Serializable(strId), SuperGlu_Serializable)

    def makeSerializableObj(self):
        return self.TEST_CLASS()

    def testSerializationToToken(self):
        instance = self.makeSerializableObj()
        token = instance.saveToToken()

    def testCreationFromToken(self):
        token = StorageToken(None, self.TEST_CLASS.CLASS_ID)
        instance = SuperGlu_Serializable.createFromToken(token)

    def testDataTransforms(self):
        st_1 = StorageToken(10, "TestProp", {"Prop11": 1, "Prop12": "Hello!"})
        st_2 = StorageToken(11, "TestClass3", {"Prop21": 1, "Prop22": st_1})
        obj1 = TestProp({"Prop11": 1, "Prop12": "Hello!"})
        obj2 = TestClass3({"Prop21": 1, "Prop22": obj1})
        dataStructures = [None, 1, 5.0, range(5), {"S":1,"R":[1,3,4], "5": "S"}, obj1, obj2]
        x = nativizeObject(serializeObject(obj1))
        x = nativizeObject(serializeObject(obj2))
        for aFormat in VALID_SERIAL_FORMATS:
            for x in dataStructures:
                self.assertEqual(x, x)
                s = serializeObject(x, aFormat)
                y = nativizeObject(s, None, aFormat)
                if isinstance(x, dict):
                    self.assertItemsEqual(x, y)
                else:
                    self.assertEqual(x, y)


    def testJSTranlation_JS_To_Python_BasicSerializable(self):
        sObj = executeJS("SerializableTestClass0.js", self.jsdir, getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, SuperGlu_Serializable)
        self.assertEqual(type(x), SuperGlu_Serializable)

    def testJSTranlation_JS_To_Python_SerializableSubclass1(self):
        sObj = executeJS("SerializableTestClass1.js", self.jsdir, getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, TestClass)
        self.assertEqual(type(x), TestClass)
        self.assertEqual(x._value, 10)

    def testJSTranlation_JS_To_Python_SerializableSubclass2(self):
        sObj = executeJS("SerializableTestClass2.js", self.jsdir, getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, TestClass2)
        self.assertEqual(type(x), TestClass2)
        self.assertEqual(x._statement, "AAA")

    def testJSTranlation_JS_To_Python_Serializable_NullVal(self):
        sObj = executeJS("SerializableTestClassNull.js", self.jsdir, getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, TestClass)
        self.assertEqual(type(x), TestClass)
        self.assertIsNone(x._value)

    def testJSTranlation_JS_To_Python_Serializable_UndefVal(self):
        sObj = executeJS("SerializableTestClassUndef.js", self.jsdir, getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, TestClass)
        self.assertEqual(type(x), TestClass)
        self.assertIsNone(x._value)

# Test Classes
class TestClass(SuperGlu_Serializable):

    def __init__(self, value=None):
        super(TestClass, self).__init__()
        self._value = value;

    def initializeFromToken(self, token, context=None):
        super(TestClass, self).initializeFromToken(token, context)
        self._value = token.__getitem__('value', True, None)

    def saveToToken(self):
        token = super(TestClass, self).saveToToken()
        token['value'] = self._value
        return token

class TestClass2(SuperGlu_Serializable):

    def __init__(self, statement=None):
        super(TestClass2, self).__init__()
        self._statement = statement;

    def initializeFromToken(self, token, context=None):
        super(TestClass2, self).initializeFromToken(token, context)
        self._statement = token['statement']

    def saveToToken(self):
        token = super(TestClass2, self).saveToToken()
        token['statement'] = self._statement
        return token

class TestProp(SuperGlu_Serializable):
    def __init__(self, data=None):
        super(TestProp, self).__init__()
        if data is None:
            data = {}
        self._data = data

    def saveToToken(self):
        token = super(TestProp, self).saveToToken()
        for name, val in self._data.iteritems():
            token[name] = tokenizeObject(val)
        return token

    def initializeFromToken(self, token, context=None):
        super(TestProp, self).initializeFromToken(token, context)
        for name, val in token.iteritems():
            if name not in token.RESERVED_KEYS:
                if isinstance(val, StorageToken):
                    val = SuperGlu_Serializable.createFromToken(val, context)
                self._data[name] = val

    def __eq__(self, obj):
        return (type(self) == type(obj) and
                self._data == obj._data)

class TestClass3(SuperGlu_Serializable):

    def __init__(self, data=None):
        super(TestClass3, self).__init__()
        if data is None:
            data = {}
        self._data = data

    def saveToToken(self):
        token = super(TestClass3, self).saveToToken()
        for name, val in self._data.iteritems():
            token[name] = tokenizeObject(val)
        return token

    def initializeFromToken(self, token, context=None):
        super(TestClass3, self).initializeFromToken(token, context)
        for name, val in token.iteritems():
            if name not in token.RESERVED_KEYS:
                if isinstance(val, StorageToken):
                    val = SuperGlu_Serializable.createFromToken(val, context)
                self._data[name] = val

    def __eq__(self, obj):
        return (type(self) == type(obj) and
                self._data == obj._data)


if __name__ == "__main__":
    unittest.main()
