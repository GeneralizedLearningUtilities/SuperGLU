import unittest.case
from SuperGLU.Core.ClassifierEngine import (ANDCondition, AllInSetCondition,
    AtomicClassifierCondition, ClassifierCondition, ClassifierEngine,
    ClassifierSpecification, CompositeClassifierCondition,
    DataClassifierCondition, DateClassifierCondition, DateRangeCondition,
    ExistsInSetCondition, InEnumeratedCondition, IsMemberClassifierCondition,
    IsValidURLCondition, ListIntersectionCondition, MapClassifierCondition,
    MapElementCondition, MapItemsCondition, MapKeysCondition,
    MapKeysIntersectionCondition, MapValuesCondition,
    MapValuesIntersectionCondition, NOTCondition, NoneInSetCondition,
    NumericClassifierCondition, NumericRangeCondition, ORCondition,
    ObjectClassifierCondition, RegExCondition, SequenceClassifierCondition,
    SequenceElementsCondition, SequenceLengthCondition,
    SetIntersectionCondition, StringCondition, XORCondition,)

class ClassifierEngineTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        pass

    def test_validateConditions(self):
        pass

    def testGetClassMemberships(self):
        pass

    def testReset(self):
        pass


class ClassifierSpecificationTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        pass

    def testGetConditions(self):
        pass

    def testGetName(self):
        pass

    def testIsMember(self):
        pass


# HIGH LEVEL CLASSIFIER CONDITIONS 
class ClassifierConditionTest(unittest.case.TestCase):
    TEST_CLASS = ClassifierCondition

    def setUp(self):
        self._x = self.TEST_CLASS()

    def test__call__(self):
        self.assertRaises(NotImplementedError, self._x, None)

    def testGetClasses(self):
        self.assertItemsEqual(self._x.getClasses(), [])

    def test__eq__(self):
        self.assertEqual(self._x, self._x)
        self.assertEqual(self._x, self.TEST_CLASS())
        self.assertNotEqual(self._x, 10)


class AtomicClassifierConditionTest(ClassifierConditionTest):
    TEST_CLASS = AtomicClassifierCondition

    def setUp(self):
        self._x = self.TEST_CLASS()
        self._y = self.TEST_CLASS("PROP NAME")

    def test__init__(self):
        x = self.TEST_CLASS()
        self.assertIsInstance(x, self.TEST_CLASS)
        y = self.TEST_CLASS("PROP NAME")
        self.assertIsInstance(y, self.TEST_CLASS)

    def test__eq__(self):
        self.assertEqual(self._x, self._x)
        self.assertEqual(self._x, self.TEST_CLASS())
        self.assertEqual(self._y, self._y)
        self.assertNotEqual(self._x, 10)
        self.assertNotEqual(self._x, self._y)


class DataClassifierConditionTest(AtomicClassifierConditionTest):
    TEST_CLASS = DataClassifierCondition


class ObjectClassifierConditionTest(AtomicClassifierConditionTest):
    TEST_CLASS = ObjectClassifierCondition

    def setUp(self):
        self._classes = [ClassifierSpecification("One"), ClassifierSpecification("Two")]
        self._x = self.TEST_CLASS()
        self._y = self.TEST_CLASS("PropName")
        self._z = self.TEST_CLASS("PropName", self._classes)

    def test__init__(self):
        x = self.TEST_CLASS()
        self.assertIsInstance(x, self.TEST_CLASS)
        y = self.TEST_CLASS("PROP NAME")
        self.assertIsInstance(y, self.TEST_CLASS)
        z = self.TEST_CLASS("PROP NAME", [ClassifierSpecification("One"), ClassifierSpecification("Two")])
        self.assertIsInstance(z, self.TEST_CLASS)

    def testGetClasses(self):
        self.assertItemsEqual(self._x.getClasses(), [])
        self.assertItemsEqual(self._y.getClasses(), [])
        self.assertItemsEqual(self._z.getClasses(), self._classes)

    def test__eq__(self):
        self.assertEqual(self._x, self._x)
        self.assertEqual(self._x, self.TEST_CLASS())
        self.assertEqual(self._y, self._y)
        self.assertEqual(self._z, self._z)
        self.assertNotEqual(self._x, 10)
        self.assertNotEqual(self._x, self._y)
        self.assertNotEqual(self._x, self._z)
        self.assertNotEqual(self._y, self._z)


class CompositeClassifierConditionTest(ClassifierConditionTest):
    TEST_CLASS = CompositeClassifierCondition

    def setUp(self):
        self._class1 = ClassifierSpecification("One")
        self._class2 = ClassifierSpecification("Two")
        self._cond1 = ObjectClassifierCondition("A", [self._class1])
        self._cond2 = ObjectClassifierCondition("B", [self._class1, self._class2])
        self._cond3 = NumericClassifierCondition("Number")
        self._conditions = [self._cond1, self._cond2, self._cond3]
        self._x = self.TEST_CLASS([self._cond1])
        self._y = self.TEST_CLASS([self._cond1, self._cond2, self._cond3])
        self._z = self.TEST_CLASS([self._cond3])

    def test__init__(self):
        class1 = ClassifierSpecification("One")
        class2 = ClassifierSpecification("Two")
        cond1 = ObjectClassifierCondition("A", [class1])
        cond2 = ObjectClassifierCondition("B", [class1, class2])
        cond3 = NumericClassifierCondition("Number")
        conditions = [cond1, cond2, cond3]
        x = self.TEST_CLASS([self._cond1])
        y = self.TEST_CLASS([self._cond1, self._cond2, self._cond3])
        z = self.TEST_CLASS([self._cond3])
        self.assertIsInstance(x, self.TEST_CLASS)
        self.assertIsInstance(y, self.TEST_CLASS)
        self.assertIsInstance(z, self.TEST_CLASS)

    def testGetClasses(self):
        self.assertItemsEqual(self._x.getClasses(), [self._class1])
        self.assertItemsEqual(self._y.getClasses(), [self._class1, self._class2])
        self.assertItemsEqual(self._z.getClasses(), [])

    def test__eq__(self):
        self.assertEqual(self._x, self._x)
        self.assertEqual(self._y, self._y)
        self.assertNotEqual(self._x, 10)
        self.assertNotEqual(self._x, self._y)

# DATA PROPERTY CLASSIFIER CONDITIONS
class NumericClassifierConditionTest(DataClassifierConditionTest):
    TEST_CLASS = NumericClassifierCondition

    def test__call__(self):
        self.assertTrue(self._x(10))
        self.assertTrue(self._x(10.1232))
        self.assertTrue(self._x(-10.1232))
        self.assertFalse(self._x("A"))
        self.assertFalse(self._x([]))
        self.assertFalse(self._x({}))


class NumericRangeConditionTest(NumericClassifierConditionTest):
    TEST_CLASS = NumericRangeCondition

    def setUp(self):
        self._x = self.TEST_CLASS(minVal=0)
        self._x2 = self.TEST_CLASS("A", minVal=0)
        self._y = self.TEST_CLASS(maxVal=0)
        self._z = self.TEST_CLASS(minVal=10.1, maxVal=11)

    def test__init__(self):
        x = self.TEST_CLASS(None, 1, 2)
        self.assertIsInstance(x, self.TEST_CLASS)
        self.assertRaises(ValueError, self.TEST_CLASS)
        self.assertRaises(TypeError, self.TEST_CLASS, None, "A")
        self.assertRaises(TypeError, self.TEST_CLASS, None, None, "B")
        self.assertRaises(ValueError, self.TEST_CLASS, None, 1, 1)
        

    def test__call__(self):
        self.assertTrue(self._x(10))
        self.assertTrue(self._x(10.1232))
        self.assertFalse(self._x(-10.1232))
        self.assertFalse(self._y(10))
        self.assertFalse(self._y(10.1232))
        self.assertTrue(self._y(-10.1232))
        self.assertFalse(self._z(10))
        self.assertTrue(self._z(10.1232))
        self.assertFalse(self._z(-10.1232))
        self.assertFalse(self._x("A"))
        self.assertFalse(self._x([]))
        self.assertFalse(self._x({}))

    def test__eq__(self):
        self.assertEqual(self._x, self._x)
        self.assertEqual(self._y, self._y)
        self.assertNotEqual(self._x, 10)
        self.assertNotEqual(self._x, self._y)


class DateClassifierConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass


class DateRangeConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass

    def testValidate(self):
        pass


class SequenceClassifierConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass


class SequenceElementsConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class SequenceLengthConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class InEnumeratedConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class AllInSetConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class ExistsInSetConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass

class NoneInSetConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass

class SetIntersectionConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def testSet(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class ListIntersectionConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass

class StringConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class RegExConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class IsValidURLConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__ini__(self):
        pass

    def testUrlparse(self):
        pass
    

class MapClassifierConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapElementConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapItemsConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapKeysConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapKeysIntersectionConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def testSet(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapValuesConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


class MapValuesIntersectionConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def testSet(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass


# Object Property Conditions
class IsMemberClassifierConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass



class NOTConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass

    def test__init__(self):
        pass
    

class ANDConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass


class ORConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass


class XORConditionTest(unittest.case.TestCase):

    def setUp(self):
        pass

    def test__call__(self):
        pass


if __name__ == "__main__":
    unittest.main()
