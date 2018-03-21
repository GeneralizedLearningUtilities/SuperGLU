'''
Created on Aug 22, 2016

@author: skarumbaiah
'''
from SuperGLU.Util.Serialization import SuperGlu_Serializable, tokenizeObject,\
    untokenizeObject
from xml.etree import ElementTree



class Speech(SuperGlu_Serializable):

    REF_KEY = "ref"
    TYPE_KEY = "typ"
    UTTERANCE_KEY = "utterance"

    ref = None
    typ = None
    utterance = ""
    

    @classmethod
    def parse(cls, clazzAsXMLString = None):
        result = Speech()

        if clazzAsXMLString is None:
            return result

        speechXMLElement = ElementTree.fromstring(clazzAsXMLString)
        result.ref = speechXMLElement.attrib["ref"]
        result.typ = speechXMLElement.attrib["type"]
        result.utterance = speechXMLElement.text

        return result


    def __init__(self, ref = None, typ = None, utterance=""):
        super(Speech, self).__init__()
        self.ref = ref
        self.typ = typ
        self.utterance = utterance


    def saveToToken(self):
        token = super(Speech, self).saveToToken()
        if self.ref is not None:
            token[self.REF_KEY] = tokenizeObject(self.ref)
        if self.typ is not None:
            token[self.TYPE_KEY] = tokenizeObject(self.typ)
        if self.utterance is not "":
            token[self.UTTERANCE_KEY] = tokenizeObject(self.utterance)

        return token

    def initializeFromToken(self, token, context=None):
        super(Speech, self).initializeFromToken(token, context)
        self.ref = untokenizeObject(token.get(self.REF_KEY, None))
        self.typ = untokenizeObject(token.get(self.TYPE_KEY, None))
        self.utterance = untokenizeObject(token.get(self.UTTERANCE_KEY, ""))
