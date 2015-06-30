# -*- coding: utf-8 -*-
import csv
import math
import operator
import re
import sys
import SuperGLU.Services.TextProcessing.inflect
from SuperGLU.Util.ErrorHandling import logError, logWarning
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group,
                       Keyword, CaselessKeyword, Empty, ParseException,
                       Optional, ZeroOrMore, Forward, nums, alphas,
                       oneOf, alphanums, printables, ParseException, StringEnd)


class PhraseMapping(object):
    Dictionary = {}

    def __init__(self, DictionaryLocation):
        self._dictionary = {}
        try:
            self._dictionary = self.loadDictionary(DictionaryLocation)
        except Exception, e:
            logError(e)

    def loadDictionary(self, fileName):
        dictionary = []
        csv.field_size_limit(sys.maxsize)
        with open(fileName, 'rU') as aFile:
            reader = csv.reader(aFile, dialect=csv.excel)
            for line in reader:
                dictionary.append((str(line[0]), str(line[1])))
        self._dictionary = dictionary
        return self._dictionary
        
    def __call__(self, text):
        # Second problem: Doesn't detect word followed by punctuation
        text = text.lower()
        splittersArr = [' ', '\'', ',', '(', ')', ]
        punctuation = ['.', '!', ';', '?']
        for original, replacement in self._dictionary:
            text = re.sub(r'\b('+ original + r')\b', replacement, text)
        return text
        
            
#test
# we may need to move char by char just to deal with no space numbers like 5X 
class NumbersMapping(object):
    def __init__(self):
        pass

    def __call__(self, Dialog):
        p = AWS_Core_Services.TextProcessing.inflect.engine()
        #Dialog = Dialog.lower()
        splitters = ' ; |,| |\ |\'|[a-zA-Z]'
        splittersArr = ['',' ','\'',',']
        D = re.split(splitters,Dialog)
        for word in D:
            if word.replace('.','',1).isdigit() and not word.isdigit():
                for s1 in splittersArr:
                    for s2 in splittersArr:
                        try:
                            sreachRegx = '(?<='+s1+')'+word+'(?='+s2+')'

                            Dialog = Dialog.replace(re.search(sreachRegx,Dialog).group(0),p.number_to_words(float(word), andword='and'))
                            
                        except:
                            pass
            if word.replace('.','',1).isdigit() and word.isdigit():
                for s1 in splittersArr:
                    for s2 in splittersArr:
                        try:
                            sreachRegx = '(?<='+s1+')'+word+'(?='+s2+')'

                            Dialog = Dialog.replace(re.search(sreachRegx,Dialog).group(0),p.number_to_words(int(word), andword='and'))
                            
                        except:
                            pass
        return Dialog
    
class FormulaStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example
    '''

    UNARY_OPS_START = (('-', 'negative'),)
    UNARY_OPS_END = (('%', 'percent'),)
    BINARY_OPS = (('+',  'plus'),
                  ('-',  'minus'),
                  ('*',  'times'),
                  ('/',  'divided by'),
                  ('=',  'is equal to'),
                  ('!=', 'is not equal to'),
                  ('<>', 'is not equal to'),
                  ('^',  'to the power of'),
                  ('>=', 'is greater than or equal to'),
                  ('<=', 'is less than or equal to'),
                  ('>',  'is greater than'),
                  ('<',  'is less than'))

    SPECIAL_KWDS = (('pi', 'pie'),)

    SPECIAL_FUNCT = (('sin', 'sine of'),
                     ('cos', 'cosine of'),
                     ('tan', 'tangent of'),
                     ('abs', 'absolute value of'),
                     ('round', 'Rounded'),
                     ('avg', 'average of'),
                     ('log', 'logarithm of'))

    START_DELIMS = (('(',' '),)
    END_DELIMS = ((')',' '),)
            
    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        self.unaryOpsStart = dict(self.UNARY_OPS_START)
        self.unaryOpsEnd = dict(self.UNARY_OPS_END)
        self.specialKwds = dict(self.SPECIAL_KWDS)
        self.ops = dict(self.BINARY_OPS)
        self.fn = dict(self.SPECIAL_FUNCT)
        self.numMap = NumbersMapping()
        self.bnf = self.makeBNFParser()

    def addToStack(self, val, theType="Default"):
        self.exprStack.append(val)

    def pushMultVars(self, strg, loc, toks):
        val = toks[0]
        val = ' '.join(val)
        self.addToStack(val, "Vars")
    
    def pushFirst(self, strg, loc, toks):
        self.addToStack(toks[0].strip(), "Standard")

    def pushNum(self, strg, loc, toks):
        val = self.numMap(toks[0])
        self.addToStack(val, "Number")

    def pushKeyword(self, strg, loc, toks):
        val = self.specialKwds.get(toks[0].strip().lower(), ' ')
        self.addToStack(val, "Keyword")

    def pushOperation(self, strg, loc, toks):
        val = self.ops.get(toks[0].strip().lower(), ' ')
        self.addToStack(val, "Operation")

    def pushFunct(self, strg, loc, toks):
        val = self.fn.get(toks[0].strip().lower(), ' ')
        self.addToStack(val, "Funct")
        
    def pushUnarySt(self, strg, loc, toks):
        val = self.unaryOpsStart.get(toks[0].strip().lower(), ' ')
        self.addToStack(val, "Unary(Start)")

    def pushUnaryEnd(self, strg, loc, toks):
        val = self.unaryOpsEnd.get(toks[0].strip().lower(), ' ')
        self.addToStack(val, "Unary(End)")

    def logOnly(self, strg, loc, toks):
        logWarning("LOG: ", toks)

    def makeCombo(self, vals, theType, supress=False):
        combo = None
        for x, aStr in vals:
            if combo is None:
                if supress:
                    combo = theType(x).suppress()
                else:
                    combo = theType(x)
            if supress:
                combo |= theType(x).suppress()
            else:
                combo |= theType(x)
        return combo

    def makeBNFParser(self):
        # Basic Components
        point = Literal(".")
        integer = Word(nums)
        fNumber = Combine(integer + point + integer)
        number = fNumber | integer
        unaryStarts = self.makeCombo(self.UNARY_OPS_START, Literal)
        unaryEnds = self.makeCombo(self.UNARY_OPS_END, Literal)
        ops = self.makeCombo(self.BINARY_OPS, Literal)
        kwds = self.makeCombo(self.SPECIAL_KWDS, CaselessKeyword)
        kwdLits = self.makeCombo(self.SPECIAL_KWDS, CaselessLiteral)
        functs = self.makeCombo(self.SPECIAL_FUNCT, CaselessKeyword)
        functLits = self.makeCombo(self.SPECIAL_FUNCT, CaselessLiteral)
        anyLits = Word(printables)
        variable = Word(alphas)
        startDelim = self.makeCombo(self.START_DELIMS, Literal, True)
        endDelim = self.makeCombo(self.END_DELIMS, Literal, True)

        # Expression
        group = Forward()
        factor = Forward()
        expr = Forward()
        val = (startDelim |
               #unaryStarts.setParseAction(self.pushUnarySt) |
               kwds.setParseAction(self.pushKeyword) |
               functs.setParseAction(self.pushFunct) |
               number.setParseAction(self.pushNum) |
               kwdLits.setParseAction(self.pushKeyword) |
               functLits.setParseAction(self.pushFunct) |
               unaryEnds.setParseAction(self.pushUnaryEnd) |
               endDelim |
               variable.setParseAction(self.pushMultVars)|
               ops.setParseAction(self.pushOperation) |
               anyLits.setParseAction(self.pushFirst))
        vals = val + ZeroOrMore(val)
        group << (Optional(unaryStarts.setParseAction(self.pushUnarySt)) +
                  Optional(functs.setParseAction(self.pushFunct)) +
                  Optional(startDelim) + factor + Optional(endDelim) +
                  Optional(unaryEnds.setParseAction(self.pushUnaryEnd)))
        factor << (vals | expr)
        expr << (group + ZeroOrMore(ops.setParseAction(self.pushOperation) + group))
        closedExpr = expr + StringEnd()
        return closedExpr

    def evaluateStack(self, s):
        return ' '.join(s)
            
    def eval(self, num_string, parseAll=True):
        #logWarning('here it is ', num_string)
        if isinstance(num_string, unicode):
            num_string = num_string.encode('ascii', 'ignore')
        if len(num_string) == 0:
            return ''
        poses = [m.start() for m in re.finditer('\(',num_string )]
        #logWarning(poses)
        newstring = ''
        n=0
        while n < len(num_string):
            if n not in poses:
                newstring = newstring+num_string[n]
            else:
                if n == 0:
                    newstring = newstring+num_string[n]
                elif (num_string[n-1].isdigit()) or (num_string[n-1] == ')'):
                    newstring = newstring + "*("
                else:
                    newstring = newstring + num_string[n]
            n = n+1
        num_string = newstring
        #logWarning('string after = ' , num_string)
        self.exprStack=[]
        try:
            results=self.bnf.parseString(num_string, parseAll)
            val=self.evaluateStack( self.exprStack[:] )
        except ParseException, err:
            logWarning(err.line, '\n', num_string, '\n', " "*(err.column-1) + "^", '\n', err)
            val = num_string
        return val

    def __call__(self, string):
        formulaArray = string.split("|||")
        nFormulas = int(len(formulaArray)/2)
        for i in xrange(nFormulas):
            val = formulaArray[i*2+1]
            if len(val) > 0:
                formulaArray[i*2+1] = self.eval(val)
        return ' '.join(formulaArray)
        

if __name__ == '__main__':
    print '======================================'        
    nsp=FormulaStringParser()
    try:
        result=nsp.eval('28pi% x + tan 5%')
        print result
        result=nsp.eval('-x= -tan (7.5+(5*-y))')
        print result
        result=nsp.eval('$ 105')
        print result
        result=nsp.eval('5y')
        print result
        result=nsp.eval(u'ÂÂ')
    except ParseException, err:
        print err.line
        print " "*(err.column-1) + "^"
        print err
        raise
    print result 
    print '======================================'

    p = PhraseMapping('Dictionary.csv')
    s = p('i am is, who is ,is is\'is')
    print s
    s = p('is am is, who is ,is is\'is')
    print s
    s = p('is')
    print s
    print '------------------------'
    print 'searching for \'large string\' from Dictionary to Dialog '
    s = ''
    s= p('this is a dialog contains a  large string and replace it with \'another phrase\'')
    print s
    N = NumbersMapping()
    s = N('515.53 X555.55 x 55X')
    print s
    print 'tests are included in test folder'

