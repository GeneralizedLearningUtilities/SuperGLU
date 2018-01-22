import os
from SuperGLU.Util.Paths import getBasePath

class RegexProcessing(object):
    DELIM = '|'
    
    def __init__(self):
        self._regexBank = []
        SynFile = os.path.join(getBasePath(),'AWS_Core_Services',
                               'TextProcessing','syn.txt')
        with open(SynFile, 'rb') as aFile:
            for line in aFile.readlines():
                aSet = line.strip().lower()
                aSet = set(aSet.split(self.DELIM))
                aSet.remove('')
                self._regexBank.append(aSet)

    def KeyRegexMatch(self, Keyword):
        if Keyword == '':
            return Keyword
        else:
            Keyword = Keyword.strip().lower()
            FinalRegex = Keyword
            for item in self._regexBank:
                if Keyword in item:
                    FinalRegex = self.DELIM.join(item)
                    return FinalRegex
            return FinalRegex

if __name__ == '__main__':
    rp = RegexProcessing()
    print rp.KeyRegexMatch('sum')
    print rp.KeyRegexMatch('add')
    print rp.KeyRegexMatch('subtract ')
    print rp.KeyRegexMatch('some of ')
    print rp.KeyRegexMatch('some'),'==some'
    print rp.KeyRegexMatch('som'),'==som'
    print rp.KeyRegexMatch('some text'),'==some text'

