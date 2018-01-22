# -*- coding: utf-8 -*-
import types
import unittest

MAX_ITER = 10000000


class UnitTestTemplateGenerator(object):
    """
    A class for generating barebones unit tests (templates to fill in), given a module
    """
    
    DEFAULT_IGNORE_NAMES = ('__class__','__builtins__', '__doc__', '__file__', '__name__', '__package__')
    DEFAULT_IGNORE_TYPES = ()
    DEFAULT_ALLOWED_TYPES = (type, types.CodeType, types.FunctionType, types.GeneratorType, \
                             types.MethodType, type, types.UnboundMethodType)
    CONTAINER_TYPES = (type, type)
    
    def __init__(self, unitTestClass=unittest.TestCase, ignoreNames=DEFAULT_IGNORE_NAMES, ignoreTypes=DEFAULT_IGNORE_TYPES, \
                 allowedTypes=DEFAULT_ALLOWED_TYPES, maxColWidth=80, indentSpaces=4, capitalLetters=True):
        """
        Initialize the template generator.
        @param unitTestClass: Class of unit test to build.  Module must have a .main() for certain functionality.
        @type unitTestClass: class
        @param ignoreNames: Names to ignore, always
        @type ignoreNames: list of str
        @param ignoreTypes: Types to ignore, always
        @type ignoreTypes: list of types
        @param allowedTypes: Types of data to build tests for.  Generally, this will include only classes, functions, an generators
        @type allowedTypes: list of types
        @param maxColWidth: Number of characters allowed on a line for the generated file.  Lines longer than this will be broken.
        @type maxColWidth: int
        @param indentSpaces: Number of spaces for an indent
        @type indentSpaces: int
        @param capitalLetters: If True, capitalize the letters of attributes when building test functions for them.  Else, use verbatim.
        @type capitalLetters: bool
        """
        self.unitTestClass = unitTestClass
        self.ignoreNames = ignoreNames
        self.ignoreTypes = ignoreTypes
        self.allowedTypes = allowedTypes
        self.maxColWidth = maxColWidth
        self.indentSpaces = indentSpaces
        self.capitalizeFirstLetters = capitalLetters

    def getAllowedNames(self, anObject, ignoreTypes=None):
        """
        Get the allowed names from an object such as a module or class definition
        @param anObject: Object to get attribute names from
        @type anObject: Any container with a __dict__ function
        @param ignoreTypes: Types of values to ignore, in addition to the default set
        @type ignoreTypes: list of types
        @return: List of names of attributes of the object which are allowed to be tested
        @rtype: list of str
        """
        if ignoreTypes:
            allowedTypes = tuple([aType for aType in self.allowedTypes if aType not in ignoreTypes and aType not in self.ignoreTypes])
        else:
            allowedTypes = tuple([aType for aType in self.allowedTypes if aType not in self.ignoreTypes])
        dataDict = anObject.__dict__
        return [name for name in dataDict if name not in self.ignoreNames and isinstance(getattr(anObject,name), allowedTypes)]


    def generateUnitTestFile(self, sourceModule, destinationFileName, moduleFunctionsPostfix="_Functions", addSetUp=True, fromStyleImports=True):
        """
        Create a barebones unit test with one test class defined per class and one test case per function/method.
        Note: This raises an error if module level functions are defined and a class in the module has a name where
        name = module.__name__ + moduleFunctionsPostfix (two unit tests attempt to have the same name)
        @param sourceModule: The source module to build the test from
        @type sourceModule: Module
        @param destinationFileName: Where to save the unit test template once created
        @type destinationFileName: str
        @param moduleFunctionsPostfix: Postfix to use for the unit test class that captures any module-level functions
        @type moduleFunctionsPostfix: str
        @param addSetUp: If True, add an empty setUp function to each test class.  Else, don't.
        @type addSetUp: bool
        @param fromStyleImports: If True, tested attributes will be imported using "from .. import" statement.  Else, an "import" module statement is used.
        @type fromStyleImports: bool
        """
        testSource = self.generateUnitTestCode(sourceModule, moduleFunctionsPostfix, addSetUp, fromStyleImports)
        newFile = file(destinationFileName, 'w')
        newFile.write(testSource)
        newFile.close()
    
    def generateUnitTestCode(self, sourceModule, moduleFunctionsPostfix="_Functions", addSetUp=True, fromStyleImports=True):
        """
        Create a barebones unit test with one test class defined per class and one test case per function/method.
        Note: This raises an error if module level functions are defined and a class in the module has a name where
        name = module.__name__ + moduleFunctionsPostfix (two unit tests attempt to have the same name)
        @param sourceModule: The source module to build the test from
        @type sourceModule: Module
        @param moduleFunctionsPostfix: Postfix to use for the unit test class that captures any module-level functions
        @type moduleFunctionsPostfix: str
        @param addSetUp: If True, add an empty setUp function to each test class.  Else, don't.
        @type addSetUp: bool
        @param fromStyleImports: If True, tested attributes will be imported using "from .. import" statement.  Else, an "import" module statement is used.
        @type fromStyleImports: bool
        @return: Compilable source code for a set of empty unit tests
        @rtype: str
        """
        if not isinstance(sourceModule, types.ModuleType): raise TypeError("sourceModule was not a module type.")
        allowedNames = sorted([name for name in self.getAllowedNames(sourceModule) \
                               if getattr(sourceModule, name).__module__ == sourceModule.__name__])
        containerNames = [name for name in allowedNames if isinstance(getattr(sourceModule, name), self.CONTAINER_TYPES)]
        containerNames.sort()
        spacer = ' '*self.indentSpaces
        codeLines = []
        #Header
        codeLines.append("import %s"%self.unitTestClass.__module__)
        if fromStyleImports:
            importString = "from %s import (%s,)"%(sourceModule.__name__, ", ".join(allowedNames))
            codeLines.append(importString)
        else:
            codeLines.append("import %s"%sourceModule.__name__)
        codeLines.append("")
        # Miscellaneous Functions and Other Non Containers
        if len(allowedNames) > len(containerNames):
            moduleFunctionTestName = sourceModule.__name__.split('.')[-1] + moduleFunctionsPostfix
            if moduleFunctionTestName in containerNames:
                raise NameError("Module-level function container name %s is already in use"%moduleFunctionTestName)
            nonContainerNames = [name for name in allowedNames if name not in containerNames]
            codeLines.extend(self.generateContainerTestTemplate(moduleFunctionTestName, nonContainerNames, addSetUp))
        #Containers (Such as Classes) With Functions
        for containerName in containerNames:
            containerObject = getattr(sourceModule, containerName)
            codeLines.extend(self.generateClassTestTemplate(containerObject, addSetUp))
        #Footer
        codeLines.append('if __name__ == "__main__":')
        codeLines.append(spacer + 'unittest.main()')
        #codeLines.append('else:')
        #codeLines.append(spacer + 'import sys')
        #codeLines.append(spacer + 'TestSuite = unittest.TestLoader.loadTestsFromModule(sys.modules[__name__])')
        newCodeLines = []
        for codeLine in codeLines:
            newCodeLines.extend(breakStringIntoLines(codeLine, self.maxColWidth))
        return '\n'.join(newCodeLines)

    def generateClassTestTemplate(self, sourceClass, addSetUp=False, indentationDepth=0):
        """
        Create a template for a test class
        @param sourceClass: Class to make a test template for
        @type sourceClass: class
        @param addSetUp: If True, add an empty setUp function to each test class.  Else, don't.
        @type addSetUp: bool
        @param indentationDepth: How indented this test definition should be
        @type indentationDepth: int
        @return: list of lines of code that define tests for this class
        @rtype list of str
        """
        allowedNames = sorted(self.getAllowedNames(sourceClass))
        return self.generateContainerTestTemplate(sourceClass.__name__, allowedNames, addSetUp, indentationDepth)

    def generateContainerTestTemplate(self, containerName, attributeNames, addSetUp=False, indendationDepth=0):
        """
        Generate lines of code for a container
        @param containerName: Name of the container to make a test class for
        @type containerName: class
        @param attributeNames: Names of all the attributes to be tested on this class
        @type attributeNames: list of str
        @param addSetUp: If True, add an empty setUp function to each test class.  Else, don't.
        @type addSetUp: bool
        @param indentationDepth: How indented this test definition should be
        @type indentationDepth: int
        @return: list of lines of code that define tests for this container
        @rtype list of str
        """
        attributeNames.sort()
        testClassName = self.unitTestClass.__module__ + '.' + self.unitTestClass.__name__
        spacer = ' '*self.indentSpaces
        indent = ' '*(self.indentSpaces*indendationDepth)
        codeLines = [indent+'class %sTest(%s):'%(containerName, testClassName)]
        if addSetUp or len(attributeNames) > 0:
            codeLines.append('')
            if addSetUp:
                codeLines.append(indent+spacer + 'def setUp(self):')
                codeLines.append(indent+spacer*2 + 'pass')
                codeLines.append('')
            for name in attributeNames:
                if self.capitalizeFirstLetters:
                    name = name[0].upper() + name[1:]
                codeLines.append(indent+spacer + 'def test%s(self):'%(name))
                codeLines.append(indent+spacer*2 + 'pass')
                codeLines.append('')
        else:
            codeLines.append(indent+spacer + 'pass')
        codeLines.append('')
        return codeLines


def getLeadingSpaces(aString):
    """
    Get the leading spaces for the string given
    @param aString: String to get leading spaces for
    @type aString: str
    @return: The leading spaces as a string
    @rtype: str
    """
    leadingWhiteSpace = ''
    for char in aString:
        if char.isspace():
            leadingWhiteSpace += char
        else:
            break
    return leadingWhiteSpace

def getBestSeparatorIndex(aString, separators, minIndex=None, maxIndex=None, getHighest=True):
    """
    Get a good separation point for line breaks
    @param aString: String to find a separation point for
    @type aString: str
    @param separators: List of separators to look for when breaking up the string
    @type separators: list of str
    @param minIndex: Minimum index to look for separation points
    @type minIndex: int
    @param maxIndex: Maximum index to look for separation points.
    @type maxIndex: int
    @param getHighest: If true, get the highest separation point (max index).  Else, get the lowest.
    @type getHighest: bool
    @return: Index for the separation point.  -1 if no valid separation points could be found.
    @rtype: int
    """
    if minIndex is None:
        minIndex = 0
    if maxIndex is None:
        maxIndex = len(aString)
    closestSepIndex = -1
    separator = None
    for sep in separators:
        if len(sep) == 0:
            raise ValueError("Cannot have a null separator.  Got a sequence of zero length.")
        if getHighest:
            separatorPosition = aString.rfind(sep, minIndex-len(sep)+1, maxIndex+len(sep)-1)
            if separatorPosition > closestSepIndex:
                closestSepIndex = separatorPosition
                separator = sep
        else:
            separatorPosition = aString.find(sep, minIndex-len(sep)+1, maxIndex+len(sep)-1)
            if closestSepIndex < 0 or (separatorPosition >= 0 and separatorPosition < closestSepIndex):
                closestSepIndex = separatorPosition
                separator = sep
    if closestSepIndex < 0:
        return -1
    else:
        return closestSepIndex + len(separator)

def breakStringIntoLines(aString, maxColumnWidth=80, separatorDist=40, separators=(',','import'), tabSize=4, splitMarker=""):
    """
    Break a string into multiple strings if it exceeds the max column width.
    Add '\' separators when doing so and return back a list of strings.
    @param aString: String to break up into a list of substrings
    @type aString: str
    @param maxColumnWidth: Maximum width of a column (not including any end-line characters added by this)
    @type maxColumnWidth: int
    @param separatorDist: Distance to look for separators (won't make sublines unless they are at least this long)
    @type separatorDist: int
    @param separators: Separators to look for when breaking up lines
    @type separators: list of char
    @param tabSize: When expanding tabs, make them this size
    @type tabSize: int
    @return: list of substrings that are broken up to fit the line restrictions
    @rtype: list of str
    """
    if maxColumnWidth < 1: raise ValueError("Columns must be at least 1 element wide.")
    aString = aString.expandtabs(tabSize)
    indentSpaces = ' '*tabSize
    separatorDist = min(separatorDist, maxColumnWidth)
    if '\n' in aString or '\r' in aString:
        substrings = aString.splitlines()
        return [aStr for subStr in substrings for aStr in breakStringIntoLines(subStr, maxColumnWidth, separatorDist, separators)]
    elif len(aString) <= maxColumnWidth:
        return [aString]
    else:
        leadingWhiteSpace = getLeadingSpaces(aString)
        #Break Up String
        strings = []
        count = 0
        while len(aString) > maxColumnWidth and count < MAX_ITER:
            count +=1
            #If only whitespace left, append an empty line and break loop
            if aString.isspace():
                strings.append(' ')
                aString = ''
                break
            minSeparationIndex = max(maxColumnWidth-separatorDist, len(leadingWhiteSpace)+1)
            #Try to break at a separator in ideal range, if possible
            breakIndex = getBestSeparatorIndex(aString, separators, minSeparationIndex, maxColumnWidth)
            #Else try to break at first whitespace in ideal range
            if breakIndex < 0:
                breakIndex = getBestSeparatorIndex(aString, (' ',), minSeparationIndex, maxColumnWidth)
            #Try to break at first separator or whitespace after max, if nothing else
            if breakIndex < 0:
                breakIndex = getBestSeparatorIndex(aString, (' ',)+tuple(separators), minSeparationIndex, len(aString), False)
            #If no breaks found, put everything on this line
            if breakIndex < 0:
                strings.append(aString)
                aString = ''
                break
            #Else, break string at the appropriate point and continue
            else:
                substring, aString = aString[:breakIndex], indentSpaces+leadingWhiteSpace + aString[breakIndex:].lstrip()
                strings.append(substring + splitMarker)
        if count > MAX_ITER:
            raise RuntimeError("Failure in breakStringIntoLine due to inability to complete splitting loop.")
        #Add any remaining string to the end
        if len(aString) > 0:
            strings.append(aString)
        return strings
            
