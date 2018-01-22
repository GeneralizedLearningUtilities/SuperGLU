import types
import unittest
from SuperGLU.Util.TestGenerator import UnitTestTemplateGenerator, breakStringIntoLines, \
    getBestSeparatorIndex, getLeadingSpaces

class TestGenerator_FunctionsTest(unittest.TestCase):

    def testBreakStringIntoLines_tooSmallToBreak(self):
        maxColumnWidth = 80
        tabSize = 4
        smallString = "X"*80
        stringLines = breakStringIntoLines(smallString, maxColumnWidth)
        self.assertEqual(len(stringLines),1)
        self.assertEqual(stringLines[0], smallString)

    def testBreakStringIntoLines_unbreakable(self):
        maxColumnWidth = 80
        tabSize = 4
        unbreakableString = "X"*100
        stringLines = breakStringIntoLines(unbreakableString, maxColumnWidth)
        self.assertEqual(len(stringLines),1)
        self.assertEqual(stringLines[0], unbreakableString)

    def testBreakStringIntoLines_hasNewLine(self):
        maxColumnWidth = 80
        tabSize = 4
        smallString = "X"*80
        twoLineString = smallString + "\n" + smallString
        stringLines = breakStringIntoLines(twoLineString, maxColumnWidth)
        self.assertEqual(len(stringLines),2)
        self.assertEqual(stringLines[0], smallString)
        self.assertEqual(stringLines[1], smallString)

    def testBreakStringIntoLines_breakInTwo(self):
        maxColumnWidth = 80
        separatorDist = 40
        tabSize = 4
        separator = ','
        lineSeparator = " \\"
        splitmarker = ''
        unbreakableString = "X"*100
        breakableString = unbreakableString + separator + unbreakableString
        stringLines = breakStringIntoLines(breakableString, maxColumnWidth)
        self.assertEqual(len(stringLines), 2)
        self.assertEqual(stringLines[0], unbreakableString+separator+splitmarker)
        self.assertEqual(stringLines[1], " "*tabSize + unbreakableString)

    def testGetBestSeparatorIndex_inseparable(self):
        separator = ','
        seps = [separator,]
        phrase = "X"*10
        inseparableString = phrase + phrase
        self.assertEqual(getBestSeparatorIndex(inseparableString, seps), -1)

    def testGetBestSeparatorIndex_separable(self):
        separator = ','
        seps = [separator,]
        phrase = "X"*10
        separableString = phrase + separator + phrase
        self.assertEqual(getBestSeparatorIndex(separableString, seps), len(phrase + separator))
        self.assertEqual(getBestSeparatorIndex(separableString, seps, len(phrase + separator)), -1)
        self.assertEqual(getBestSeparatorIndex(separableString, seps, None, len(phrase + separator)-1), -1)

    def testGetBestSeparatorIndex_multiSeparable(self):
        separator = ','
        seps = [separator,]
        phrase = "X"*10
        separableString = separator.join([phrase]*3)
        self.assertEqual(getBestSeparatorIndex(separableString, seps), len((phrase + separator)*2))
        self.assertEqual(getBestSeparatorIndex(separableString, seps, getHighest=False), \
                         len((phrase + separator)))

    def testGetLeadingSpaces(self):
        noSpaces = "SOMETHING"
        leadingSpaces = "   \t\t\n"
        self.assertEquals(getLeadingSpaces(noSpaces), '')
        self.assertEquals(getLeadingSpaces(leadingSpaces), leadingSpaces)
        self.assertEquals(getLeadingSpaces(leadingSpaces+noSpaces), leadingSpaces)


class UnitTestTemplateGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.tabWidth = 4
        self.templateGenerator = UnitTestTemplateGenerator()

    def test__init__(self):
        generator = UnitTestTemplateGenerator()
        self.assertIsInstance(generator, UnitTestTemplateGenerator)
        generator2 = UnitTestTemplateGenerator(object, ["hateThisName",], [str, object], [types.ClassType], 100, 4, False)
        self.assertIsInstance(generator2, UnitTestTemplateGenerator)

    def testGenerateContainerTestTemplate_empty(self):
        generator = self.templateGenerator
        containerName = "SomeContainer"
        containerAttributes = []
        tabSpaces = ' '*generator.indentSpaces
        testClassName = generator.unitTestClass.__module__ + '.' + generator.unitTestClass.__name__
        targetCodeLines = ["class SomeContainerTest(%s):"%testClassName,
                           "%spass"%(tabSpaces,),
                           '']
        templateCodeLines = generator.generateContainerTestTemplate(containerName, containerAttributes)
        self.assertEqual(targetCodeLines, templateCodeLines)

    def testGenerateContainerTestTemplate_hasAttributes(self):
        generator = self.templateGenerator
        containerName = "SomeContainer"
        containerAttributes = ["Attr1", "Attr2"]
        tabSpaces = ' '*generator.indentSpaces
        testClassName = generator.unitTestClass.__module__ + '.' + generator.unitTestClass.__name__
        targetCodeLines = ["class SomeContainerTest(%s):"%testClassName,
                           '']
        for attr in containerAttributes:
            targetCodeLines.append(tabSpaces+"def test%s(self):"%(attr))
            targetCodeLines.append(tabSpaces*2+"pass")
            targetCodeLines.append("")
        targetCodeLines.append("")
        templateCodeLines = generator.generateContainerTestTemplate(containerName, containerAttributes)
        self.assertEqual(targetCodeLines, templateCodeLines)

    def testGenerateClassTestTemplate(self):
        class TestObject(object):
            def boundFunct(self):
                pass
            @classmethod
            def classFunct(cls):
                pass
            @staticmethod
            def staticFunct():
                pass
        generator = self.templateGenerator
        containerName = "TestObject"
        containerAttributes = ["BoundFunct", "ClassFunct","StaticFunct"]
        tabSpaces = ' '*generator.indentSpaces
        testClassName = generator.unitTestClass.__module__ + '.' + generator.unitTestClass.__name__
        targetCodeLines = ["class TestObjectTest(%s):"%testClassName,
                           '']
        for attr in containerAttributes:
            targetCodeLines.append(tabSpaces+"def test%s(self):"%(attr))
            targetCodeLines.append(tabSpaces*2+"pass")
            targetCodeLines.append("")
        targetCodeLines.append("")
        templateCodeLines = generator.generateClassTestTemplate(TestObject)
        self.assertEqual(targetCodeLines, templateCodeLines)

    def testGenerateUnitTestCode(self):
        import Util.Tests.TestGeneratorExampleModule as testModule
        testContainers = [('TestGeneratorExampleModule_Functions', ["Function1", "Function2"]), \
                          ('EmptyClass', []), \
                          ('ExampleClass',  ['SomeFunction'])]
        generator = self.templateGenerator
        tabSpaces = ' '*generator.indentSpaces
        maxColWidth = generator.maxColWidth
        testClassName = generator.unitTestClass.__module__ + '.' + generator.unitTestClass.__name__
        targetCodeLines = []
        targetCodeLines.append("import %s"%(generator.unitTestClass.__module__,))
        targetCodeLines.append("from %s import (EmptyClass, ExampleClass, function1, function2,)"%(testModule.__name__,))
        targetCodeLines.append('')
        for containerName, containerAttributes in testContainers:
            targetCodeLines.append("class %sTest(%s):"%(containerName,testClassName))
            targetCodeLines.append('')
            targetCodeLines.append(tabSpaces+"def setUp(self):")
            targetCodeLines.append(tabSpaces*2+"pass")
            targetCodeLines.append("")
            for attr in containerAttributes:
                targetCodeLines.append(tabSpaces+"def test%s(self):"%(attr))
                targetCodeLines.append(tabSpaces*2+"pass")
                targetCodeLines.append("")
            targetCodeLines.append("")
        targetCodeLines.append('if __name__ == "__main__":')
        targetCodeLines.append(tabSpaces + 'unittest.main()')
        #targetCodeLines.append('else:')
        #targetCodeLines.append(tabSpaces + 'import sys')
        #targetCodeLines.append(tabSpaces + 'TestSuite = unittest.TestLoader.loadTestsFromModule(sys.modules[__name__])')
        targetCodeLines = [codeLine for targetLine in targetCodeLines \
                           for codeLine in breakStringIntoLines(targetLine, maxColWidth)]
        targetSourceCode = '\n'.join(targetCodeLines)
        x= targetSourceCode
        y= generator.generateUnitTestCode(testModule)
        for i, v in enumerate(x):
            if y[i] != v:
                print i, y[i:]
        self.assertEqual(targetSourceCode, generator.generateUnitTestCode(testModule))

    def testGetAllowedNames_object(self):
        generator = self.templateGenerator
        self.assertItemsEqual(generator.getAllowedNames(object), [])

    def testGetAllowedNames_CustomObject(self):
        generator = self.templateGenerator
        class TestObject(object):
            VALUE = 1
            CONSTANT = "CONSTANT"
            BUILTIN_INST = object()
            EXTERNAL_INST = UnitTestTemplateGenerator()
            def boundFunct(self):
                pass
            @classmethod
            def classFunct(cls):
                pass
            @staticmethod
            def staticFunct():
                pass
            class OtherClass():
                pass
            class AnotherClass(object):
                pass
        allowedNames = ["boundFunct","classFunct","staticFunct", "OtherClass", "AnotherClass"]
        self.assertItemsEqual(generator.getAllowedNames(TestObject), allowedNames)


if __name__ == "__main__":
    unittest.main()
