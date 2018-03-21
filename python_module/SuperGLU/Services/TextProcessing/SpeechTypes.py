import re
import random
from SuperGLU.Services.TextProcessing.Utilities.ASATSerialization import ASATSerializable
from SuperGLU.Util.Serialization import NamedSerializable, SuperGlu_Serializable, tokenizeObject, untokenizeObject


class BaseSpeechType(object):
    """ Representations of a certain verbal statement """

    TEXT_TYPE = "Text"
    SPOKEN_TYPE = "Spoken"
    REGEX_TYPE = "RegEx"
    TYPE_ORDERING = (TEXT_TYPE, SPOKEN_TYPE, REGEX_TYPE)

    def getText(self, language=None, errorOnMissing=True):
        return self.getUtteranceValue(language, self.TEXT_TYPE, errorOnMissing=errorOnMissing)

    def getSpeech(self, language=None, errorOnMissing=True):
        return self.getUtteranceValue(language, self.SPOKEN_TYPE, errorOnMissing=errorOnMissing)

    def getUtteranceValue(self, language=None, speechType=None, allowSubstitution=True,
                          errorOnMissing=True, allowBlank=True):
        raise NotImplementedError

    def setUtteranceValue(self, value, speechType=None, language=None):
        raise NotImplementedError


class UtteranceContainer(BaseSpeechType, SuperGlu_Serializable, ASATSerializable):
    """ Representations of a certain verbal statement """

    DEFAULT_LANGUAGE = "EN-US"

    # TESTME: added missing parameters in JS file constructor, test!
    def __init__(self, text=None, speech=None, regex=None,
                 language=DEFAULT_LANGUAGE, languageMap=None):
        """
        Initialize the utterance.  If text and speech values are given,
        these override their counterparts in the languageMap (if any)
        @param text: Default text display for the utterance
        @type text: str
        @param speech: Default speech markup associated with the utterance
        @type speech: str
        @param regex: Default regular expression to compare values against
        @type regex: str
        @param language: Default language for the system to use
        @type language: str
        @param languageMap: Map of languages to utterance outputs, in form
                            {language : {type : utterance}}
        @type languageMap: dict of dict
        """
        if languageMap is None: languageMap = {}
        super(UtteranceContainer, self).__init__()
        self._defaultLanguage = language
        self._languageMap = languageMap
        if self._defaultLanguage not in self._languageMap:
            self._languageMap[self._defaultLanguage] = {}
        if text is not None:
            self._languageMap[self._defaultLanguage][self.TEXT_TYPE] = text
        if speech is not None:
            self._languageMap[self._defaultLanguage][self.SPOKEN_TYPE] = speech
        if regex is not None:
            self._languageMap[self._defaultLanguage][self.REGEX_TYPE] = regex

    #@TODO: Should switch this across the code to have language be the second param
    def getUtteranceValue(self, language=None, speechType=None, allowSubstitution=True,
                          errorOnMissing=True, allowBlank=True):
        """
        Get the value of an utterance, for a particular language and speech type
        @param language: The language for the utterance (e.g., US English)
        @type language: str
        @param speechType: Type of output for the utterance (e.g., text, spoken)
        @type speechType: str
        @param allowSubstitution: If True and speechType non-None but not found,
                                  walk the TYPE_ORDERING to find next best output
        @type allowSubstitution: bool
        @return: The value of the utterance
        @rtype: str
        """
        if language is None:
            language = self._defaultLanguage
        # Check that language exists and has non-zero length here
        utterances = self._languageMap[language]
        if ((speechType is None) or (speechType not in utterances and allowSubstitution) or
            (not allowBlank and len(utterances[speechType].strip()) == 0)):
            for aType in self.TYPE_ORDERING:
                if aType in utterances and (allowBlank or len(utterances[aType].strip()) > 0):
                    return utterances[aType]
            # If we banned blank and came up empty, allow them
            if not allowBlank:
                for aType in self.TYPE_ORDERING:
                    if aType in utterances:
                        return utterances[aType]
            if errorOnMissing:
                raise KeyError("No utterance of type <%s> found for language <%s>"%(speechType, language))
            else:
                return None
        elif errorOnMissing or (speechType in utterances):
            return utterances[speechType]
        else:
            return None


    def setUtteranceValue(self, value, speechType=None, language=None):
        if language is None:
            language = self._defaultLanguage
        if speechType is None:
            speechType = self.TYPE_ORDERING[0]
        self._languageMap[language][speechType] = value

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._defaultLanguage == other._defaultLanguage and
                self._languageMap == other._languageMap)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getDefaultLanguage(self):
        return self._defaultLanguage

    def getLanguageMap(self):
        return self._languageMap

    def saveToToken(self):
        token = super(UtteranceContainer, self).saveToToken()
        token["language"] = self._defaultLanguage
        token["languageMap"] = tokenizeObject(self._languageMap)
        return token

    def initializeFromToken(self, token, context=None):
        super(UtteranceContainer, self).initializeFromToken(token, context)
        self._defaultLanguage = token["language"]
        self._languageMap = untokenizeObject(token["languageMap"])

    def getASATData(self, name="Item"):
        """
        Get ASAT XML Data for this utterance.
        NOTE: This is a lossy transformation, as it discards any regex
        information and also discards any languages other than the
        default language (and assumes the default language is English)
        """
        node = super(UtteranceContainer, self).getASATData(name)
        if self.getText() is not None:
            node.attrib['text'] = self.getText()
        if self.getSpeech() is not None:
            node.attrib['speech'] = self.getSpeech()
        return node

    def loadFromASATData(self, node):
        super(UtteranceContainer, self).loadFromASATData(node)
        self._languageMap = {}
        self._languageMap[self._defaultLanguage] = {}
        text = node.attrib.get('text', None)
        speech = node.attrib.get('speech', None)
        if text is not None:
            self._languageMap[self._defaultLanguage][self.TEXT_TYPE] = text
        if speech is not None:
            self._languageMap[self._defaultLanguage][self.SPOKEN_TYPE] = speech


class UtteranceType(UtteranceContainer):
    """ An atomic verbal statement, for outputing """
    TYPE_ORDERING = (UtteranceContainer.TEXT_TYPE, UtteranceContainer.SPOKEN_TYPE)

    def __init__(self, text=None, speech=None, language=UtteranceContainer.DEFAULT_LANGUAGE, languageMap=None):
        """
        Initialize the utterance.  If text and speech values are given,
        these override their counterparts in the languageMap (if any).
        This class ignores any regex values and will not retrieve them.
        @param text: Default text display for the utterance
        @type text: str
        @param speech: Default speech markup associated with the utterance
        @type speech: str
        @param language: Default language for the system to use
        @type language: str
        @param languageMap: Map of languages to utterance outputs, in form {language : {type : utterance}}
        @type languageMap: dict of dict
        """
        super(UtteranceType, self).__init__(text=text, speech=speech, language=language, languageMap=languageMap)
        # CHECKME: add __eq__ or use UtteranceContainer's?

    def __str__(self):
        return '<text: ' + str(self._languageMap) + '>'

# TESTME: Added implementation to JS file, test!
# TODO: add serialization tests
class KeywordType(UtteranceContainer):
    """ A keyword or regular expression for matching purposes """
    TYPE_ORDERING = (UtteranceContainer.REGEX_TYPE, UtteranceContainer.TEXT_TYPE)

    def __init__(self, text=None, regex=None, language=UtteranceContainer.DEFAULT_LANGUAGE, languageMap=None):
        """
        Initialize the keyword.  If text and regex values are given,
        these override their counterparts in the languageMap (if any).
        This class ignores any speech values and will not retrieve them.
        @param text: Default text display for the utterance
        @type text: str
        @param regex: Default regular expression to compare values against
        @type regex: str
        @param language: Default language for the system to use
        @type language: str
        @param languageMap: Map of languages to utterance outputs, in form {language : {type : utterance}}
        @type languageMap: dict of dict
        """
        super(KeywordType, self).__init__(text=text, regex=regex, language=language, languageMap=languageMap)
        self._compiledRegex = {}

    def isMatch(self, aStr, language=None):
        """ Check if the given string matches this keyword """
        if language is None:
            language = self._defaultLanguage
        if language not in self._compiledRegex:
            val = self.getUtteranceValue(language)
            if language in self._languageMap and self.REGEX_TYPE not in self._languageMap[language]:
                val = r"\b" + val.strip().lower() + r"\b"
            pattern = re.compile(val)
            self._compiledRegex[language] = pattern
        return self._compiledRegex[language].search(aStr) is not None

    def initializeFromToken(self, token, context=None):
        super(KeywordType, self).initializeFromToken(token, context)
        self._compiledRegex = {}

    def loadFromASATData(self, node):
        super(KeywordType, self).loadFromASATData(node)
        self._compiledRegex = {}


# TODO: Finish this by using Python keyword substitution
class ParameterizedUtteranceType(UtteranceType): # TODO add serialization tests?
    """
    A parameterized utterance attempts to substitute some context values
    for parameters in the string representation.
    NOTE: This loses data and becomes a weird string if serialized to ASAT form
    """
    NATIVE_START_DELIMETER = '{'
    NATIVE_END_DELIMETER = '}'
    STORAGE_START_DELIMETER = NATIVE_START_DELIMETER
    STORAGE_END_DELIMETER = NATIVE_END_DELIMETER

    def __init__(self, text=None, speech=None, language=UtteranceContainer.DEFAULT_LANGUAGE,
                 languageMap=None, parameterNames=None):
        """
        Initialize the parameterized utterance.  This is the same
        as a regular utterance, but can have values substituted into the text.
        Parameters are implanted in the text between NATIVE_START_DELIMETER and NATIVE_END_DELIMETER.
        @param text: Default text display for the utterance
        @type text: str
        @param speech: Default speech when spoken
        @type speech: str
        @param language: Default language for the system to use
        @type language: str
        @param languageMap: Map of languages to utterance outputs, in form {language : {type : utterance}}
        @type languageMap: dict of dict
        @param parameterNames: The names of parameters found in this utterance.
        @type parameterNames: list of str
        """
        super(ParameterizedUtteranceType, self).__init__(text=text, speech=speech, language=language,
                                                         languageMap=languageMap)
        self._parameterNames = parameterNames

    def getUtteranceValue(self, params, language=None, speechType=None, allowSubstitution=True,
                          errorOnMissing=True, allowBlank=True):
        utterance = super(ParameterizedUtteranceType, self).getUtteranceValue(language, speechType,
                                                                              allowSubstitution, errorOnMissing,
                                                                              allowBlank)
        return utterance.format(**params)

    def saveToToken(self):
        token = super(ParameterizedUtteranceType, self).saveToToken()
        token["parameterNames"] = tokenizeObject(self._parameterNames)
        return token

    def initializeFromToken(self, token, context=None):
        super(ParameterizedUtteranceType, self).initializeFromToken(token, context)
        self._parameterNames = untokenizeObject(token["parameterNames"])


class SpeechActType(SuperGlu_Serializable, ASATSerializable):
    """
    A speech act classifier using a set of keywords/regex
    Note: Complies with ASAT XSD
    """

    def __init__(self, name=None, keywords=None):
        """
        Initialize the speech act.
        @param name: Name for the speech act
        @type name: str
        @param keywords: Keywords used to detect the speech act.  Matches if any hit.
        @type keywords: list of AutoTutorInterpreter.Speech.SpeechTypes.KeywordType
        """
        super(SpeechActType, self).__init__()
        if keywords is None:
            keywords = tuple()
        self._name = name
        self._keywords = keywords

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._name == other._name and
                self._keywords == other._keywords)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getName(self):
        return self._name

    def getKeywords(self):
        return self._keywords

    def isMatch(self, aStr, language=None):
        return all(regex.isMatch(aStr, language) for regex in self._keywords)

    def saveToToken(self):
        token = super(SpeechActType, self).saveToToken()
        token["name"] = self._name
        token["keywords"] = tokenizeObject(self._keywords)
        return token

    def initializeFromToken(self, token, context=None):
        super(SpeechActType, self).initializeFromToken(token, context)
        self._name = token["name"]
        self._keywords = tuple(untokenizeObject(token["keywords"]))

    def getASATData(self, name="SpeechAct"):
        node = super(SpeechActType, self).getASATData(name)
        if self._name is not None:
            node.attrib['name'] = self._name
        regexList = [x.getUtteranceValue(speechType=BaseSpeechType.REGEX_TYPE) for x in self._keywords]
        if False:
            for regex in regexList:
                regexNode = self._saveToXMLElement("RegEx")
                regexNode.text = regex
                node.append(regexNode)
        node.text = '|'.join(regexList)
        return node

    def loadFromASATData(self, node):
        super(SpeechActType, self).loadFromASATData(node)
        self._name = node.attrib.get('name', None)
        keywords = node.text
        if keywords is not None:
            self._keywords = tuple([KeywordType(None, keywords)])
        else:
            self._keywords = tuple()


class SpeechCan(BaseSpeechType, NamedSerializable, ASATSerializable):
    """
    A speech can which selects an utterance from a set of options
    Note: Complies with ASAT XSD
    """

    def __init__(self, utterances=None, name=None, description=None):
        """
        Initialize the speech can.
        @param utterances: List of utterances that can be said using this can
        @type utterances: list of AutoTutorInterpreter.Speech.SpeechTypes.UtteranceType
        @param name: Name for the speech can
        @type name: str
        @param description: Description of the speech can purpose
        @type description: str
        """
        super(SpeechCan, self).__init__(name=name)
        if utterances is None: utterances = tuple()
        self._name = name
        self._description = description
        self._utterances = tuple(utterances)
        self._orderedUtterances = tuple(self._utterances)
        self.update()

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._name == other._name and
                self._description == other._description and
                self._utterances == other._utterances)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '<name: ' + self._name + ', description: ' + self._description + ', utterances: ' + str(self._utterances) + '>'

    def update(self):
        """ Shuffle the speech acts so they occur in a random order """
        x = list(self._utterances)
        random.shuffle(x)
        self._orderedUtterances = tuple(x)

    def getUtteranceValue(self, language=None, speechType=None, allowSubstitution=True,
                          errorOnMissing=True, allowBlank=True):
        currentUtterance = self._orderedUtterances[0]
        return currentUtterance.getUtteranceValue(language, speechType, allowSubstitution, errorOnMissing, allowBlank)

    def getUtteranceList(self, speechType=BaseSpeechType.SPOKEN_TYPE, allowBlank=False, role=None):
        if role is not None:
            return []
        return [x.getUtteranceValue(speechType=speechType, allowBlank=allowBlank) for x in self._utterances]

    def saveToToken(self):
        token = super(SpeechCan, self).saveToToken()
        token["description"] = self._description
        token["utterances"] = tokenizeObject(self._utterances)
        return token

    def initializeFromToken(self, token, context=None):
        super(SpeechCan, self).initializeFromToken(token, context)
        self._description = token["description"]
        self._utterances = tuple(untokenizeObject(token["utterances"]))

    def getASATData(self, name="SpeechCan"):
        """
        ASAT Data forms:
        1. Complex: (attributes {}, elements [])
        2. Simple: str, number, etc
        3. Elements: [(name, Simple/Complex), ...]
        """
        node = super(SpeechCan, self).getASATData(name)
        if self._name is not None:
            node.attrib['name'] = self._name
        if self._description is not None:
            node.attrib['description'] = self._description
        node.extend(self._makeASATDataSeq(None, "Item", self._utterances))
        return node

    def loadFromASATData(self, node):
        super(SpeechCan, self).loadFromASATData(node)
        self._name = node.attrib.get('name', None)
        self._description = node.attrib.get('description', None)
        self._utterances = tuple(self._loadASATDataSeq(UtteranceType, node))
        return node

if __name__ == '__main__':
    x = UtteranceContainer("My Text", "My Speech")
    dat = x.getASATData("UtteranceType")
    x.loadFromASATData(dat)
    y1 = UtteranceContainer.createFromASATData(dat)

    xmlStr = x.outputASATDataStr("UtteranceType")
    x.loadFromASATDataStr(xmlStr)
    y2 = UtteranceContainer.createFromASATDataStr(xmlStr)

    print xmlStr
