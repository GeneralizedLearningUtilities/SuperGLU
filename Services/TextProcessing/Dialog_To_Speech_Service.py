import cgi
import os
import sys
import re
import traceback
from random import randint
from unidecode import unidecode

from SuperGLU.Services.TextProcessing.Speech_Processing import (FormulaStringParser,
    PhraseMapping, NumbersMapping)
from SuperGLU.Services.StorageService.Storage_Service_Interface import STORAGE_SERVICE_NAME, BaseStorageService
from SuperGLU.Core.FIPA.SpeechActs import REQUEST_ACT, INFORM_ACT, DISCONFIRM_ACT
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Util.ErrorHandling import logError, logWarning
from SuperGLU.Util.Paths import getBasePath

TEXT_KEY = 'text'
VOICE_KEY = 'voice'
SEGMENTERS = r'\.!\?'
SEGMENTING_REGEX = r'['+SEGMENTERS+']\s+(?=\S)'

TRANSFORM_DIALOG_PACK_CONTEXT_TAG = 'Transform Dialog Pack'
SEGMENT_CONTEXT_TAG = 'Segment_Dialog'
AGENT_CONTEXT_TAG = 'Agent Name'
MS_XML_CONTEXT_TAG = 'Make Media Semantics XML'
MS_XML_TYPE_CONTEXT_TAG = 'Media Semantics Speech Type'

TALKING_HEADS_TAG = 'TalkingHeads'
BUBBLE_HEADS_TAG = 'BubbleHeads'

def safeUnidecode(string):
    if isinstance(string, unicode):
        return unidecode(string)
    else:
        return string

def makeSpeechObject(text=None, voice=None):
    speechObj = {}
    if text is not None:
        speechObj[TEXT_KEY] = text
    if voice is not None:
        speechObj[VOICE_KEY] = voice
    if len(speechObj) > 0:
        return speechObj
    else:
        return None

def preprocessText(text):
    return text.replace('|||','')

def escapeXML(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def escapeVoice(text):
    text = text.replace('<', '')
    text = text.replace('>', '')
    return text

def makeBubbleText(text, voice=None, bubbleOnly=False):
    text = preprocessText(text)
    if bubbleOnly or voice is None:
        return '<bubble text="'+ escapeXML(text, "&quot;") +'"/>.'
    else:
        return '<bubble text="'+ escapeXML(text, "&quot;") +'"/> ' + escapeXML(voice, "&quot;");

def segmentUtterance(text):
    x = []
    last = None
    for match in re.finditer(SEGMENTING_REGEX, text):
        x.append(text[last:match.end(0)])
        last = match.end(0)
    if len(text[last:]) > 0 or len(x) == 0:
        x.append(text[last:])
    return x

def makeMediaSemanticsId(n=None, isBubble=False):
    if n is None: n = randint(0, 99999)
    if isBubble:
        return "B%05d"%n
    else:
        return "S%05d"%n
    

def makeMediaSemanticsLabel(s, length=64, isBubble=False):
    s = re.sub('[^0-9a-zA-Z]+', '_', s)
    sLen = str(len(s))
    if isBubble:
        prefix = "B"
    else:
        prefix = "S"
    length = length-(len(sLen)+2)
    if len(s) > length:
        s = s[:int(length/2)] + s[-int(length/2):]
    s = "%s%s_%s"%(prefix, sLen, s)
    return s

def makeMediaSemanticsMsgXML(text, voice, n=None, msType=None):
    if n is None: n = randint(0, 99999)
    text = escapeXML(text)
    voice = escapeVoice(voice)
    bubbleText = """<bubble text="%s"/>"""%(text,)
    textId = makeMediaSemanticsId(n)
    bubbleId = makeMediaSemanticsId(n, True)
    textLabel = makeMediaSemanticsLabel(text)
    bubbleLabel = makeMediaSemanticsLabel(text, isBubble=True)
    outStrs = []
    if msType is None or msType == TALKING_HEADS_TAG:
        outStrs.append('<message id="%s" name="%s">\n   <say>%s</say>\n</message>'%(textId, textLabel, bubbleText+voice))
    if msType is None or msType == BUBBLE_HEADS_TAG:
        outStrs.append('<message id="%s" name="%s">\n   <say>%s.</say>\n</message>'%(bubbleId, bubbleLabel, bubbleText))
    return '\n'.join(outStrs)

def makeMediaSemanticsMsgXMLList(utterances, msType=None):
    return '\n'.join([makeMediaSemanticsMsgXML(u[TEXT_KEY], u[VOICE_KEY], i, msType) for i, u in enumerate(utterances)])


class DialogToSpeechEngine(object):
    DEFAULT_PATH = ('AWS_Core_Services', 'TextProcessing')

    def __init__(self, mappings=None, filePath=None, fileName='Dictionary.csv'):
        if filePath is None:
            filePath = os.path.join(getBasePath(), *self.DEFAULT_PATH)
        fileName = os.path.join(filePath, fileName)
        if mappings is None:
            mappings = (FormulaStringParser(),
                        PhraseMapping(fileName),
                        NumbersMapping())
        self._mappings = mappings

    def __call__(self, string):
        return self.translateToSpeech(string)

    def translateToSpeech(self, string):
        for m in self._mappings:
            try:
                string = m(string)
            except Exception, err:
                logException(err)
        if isinstance(string, unicode):
            string = unidecode(string)
        return string


class DialogToSpeechService(BaseService, DialogToSpeechEngine):
    """ Converts Text into Speakable Dialog """
    LIST_UTTERANCES_VERB = "List Utterances"
    CONVERT_TEXT_VERB = "Convert Text"

    def __init__(self, anId=None, mappings=None, filePath=None, fileName='Dictionary.csv', converter=None):
        if converter is None: converter = AutoTutor_Interpreter.Speech.ASATScriptTransforms.FormScriptToASATConverter()
        BaseService.__init__(self, anId)
        DialogToSpeechEngine.__init__(self, mappings, filePath, fileName)
        self._converter = converter

    def receiveMessage(self, msg):
        super(DialogToSpeechService, self).receiveMessage(msg)
        # Signature: InputText, CONVERT_TEXT_VERB, VOICE_KEY, None, REQUEST_ACT
        if (msg.getVerb() == self.CONVERT_TEXT_VERB and
            msg.getSpeechAct() == REQUEST_ACT and
            msg.getObject() == VOICE_KEY):
            self.handleConvertMsg(msg)
        # Signature: ASATDialogPack, LIST_UTTERANCES_VERB, None, None, REQUEST_ACT
        # Context: BucketName, Segment, MS_XML
        elif (msg.getVerb() == self.LIST_UTTERANCES_VERB and
              msg.getSpeechAct() == REQUEST_ACT):
            self.handleListUtterancesMsg(msg)

    def handleConvertMsg(self, msg):
        text = msg.getActor()
        if text is None:
            text = ''
        try:
            text = self.translateToSpeech(text)
        except Exception, err:
            text = None
            logWarning("COULD NOT TRANSLATE: ", msg.getActor())
            raise err
        msg = self.makeDuplicateMsg(msg)
        msg.setResult(text)
        self.sendMessage(msg)

    def handleListUtterancesMsg(self, msg):
        scriptData = msg.getActor()
        segment = msg.getContextValue(SEGMENT_CONTEXT_TAG, False)
        msTag = msg.getContextValue(MS_XML_CONTEXT_TAG, False)
        msTypeTag = msg.getContextValue(MS_XML_TYPE_CONTEXT_TAG, None)
        transformDialog = msg.getContextValue(TRANSFORM_DIALOG_PACK_CONTEXT_TAG, False)
        agentName = msg.getContextValue(AGENT_CONTEXT_TAG, None)
        try:
            if isinstance(scriptData, (ASATDialogPack, ASATTutoringScript)):
                utterances = self.getUtterancesFromPack(scriptData, segment,
                                                        transformDialog, agentName)
                utterances = self.cleanUtterances(utterances)
                if msTag:
                    utterances = makeMediaSemanticsMsgXMLList(utterances, msTypeTag)
                msg = self.makeDuplicateMsg(msg, INFORM_ACT)
                msg.setResult(utterances)
                self.sendMessage(msg)
            elif isinstance(scriptData, TutoringPageView):
                self.getUtterancesFromTutoringPage(msg, scriptData, segment, msTag, msTypeTag,
                                                   transformDialog, agentName)
            else:
                msg = self.makeDuplicateMsg(msg, DISCONFIRM_ACT)
                msg.setResult(None)
                self.sendMessage(msg)
        except ValueError, err:
        #except ValueException, err:
            logError(err)
            utterances = None
            msg = self.makeDuplicateMsg(msg, DISCONFIRM_ACT)
            msg.setResult(None)
            self.sendMessage(msg)

    def getUtterancesFromPack(self, pack, segment=False, transformDialog=False, agentName=None):
        if transformDialog and not isinstance(pack, ASATTutoringScript):
            pack = self._converter.transformObject(pack)
            tutorScript = ASATTutoringScript()
            tutorScript.loadFromASATData(pack)
            pack = tutorScript
        utterances = pack.getUtteranceList(speechType=BaseSpeechType.SPOKEN_TYPE, allowBlank=False, role=agentName)
        utterances = [makeSpeechObject(preprocessText(safeUnidecode(u)),
                                       preprocessText(self.translateToSpeech(u)))
                          for u in utterances if isinstance(u, basestring)]
        if segment:
            utterances = self.segmentUtterances(utterances)
        return utterances

    def getUtterancesFromTutoringPage(self, msg, page, segment=False, msTag=False, msTypeTag=None,
                                      transformDialog=False, agentName=None):
        bucketName = msg.getContextValue(BaseStorageService.BUCKET_KEY, 'ONR')
        dialogs = page.getDialogs()
        reqMsg = self.makeStorageServiceReq(bucketName, dialogs)
        callback = self.makeOnDialogCallback(msg, segment, msTag, msTypeTag, transformDialog, agentName)
        self._makeRequest(reqMsg, callback)

    def makeStorageServiceReq(self, bucketName, dialogs):
        msg = Message(STORAGE_SERVICE_NAME,
                      BaseStorageService.VALUE_VERB,
                      None, None, REQUEST_ACT)
        msg.setContextValue(BaseStorageService.NAME_KEY, list(dialogs))
        msg.setContextValue(BaseStorageService.BUCKET_KEY, bucketName)
        return msg

    def makeOnDialogCallback(self, msg, segment=False, msTag=False, msTypeTag=None,
                             transformDialog=False, agentName=None):
        def onReceiveDialogs(msg, sentMsg, orig=msg, segment=segment, msTag=msTag, msTypeTag=msTypeTag,
                             transformDialog=transformDialog, agentName=agentName, self=self):
            dialogs = msg.getResult()
            if dialogs is None:
                dialogs = []
            dialogs = [d for d in dialogs if isinstance(d, (ASATDialogPack, ASATTutoringScript))]
            utterances = []
            for d in dialogs:
                utterances.extend(self.getUtterancesFromPack(d, segment, transformDialog, agentName))
            utterances = self.cleanUtterances(utterances)
            if msTag:
                utterances = makeMediaSemanticsMsgXMLList(utterances, msTypeTag)
            msg = self.makeDuplicateMsg(orig, INFORM_ACT)
            msg.setResult(utterances)
            self.sendMessage(msg)
        return onReceiveDialogs

    def segmentUtterances(self, utterances, keepFullOnSegment=True):
        segmentedUtterances = []
        for u in utterances:
            textSeqs = segmentUtterance(u[TEXT_KEY])
            voiceSeqs = segmentUtterance(u[VOICE_KEY])
            if len(textSeqs) == len(voiceSeqs):
                if keepFullOnSegment and len(textSeqs) != 1:
                    segmentedUtterances.append(u)
                for i, text in enumerate(textSeqs):
                    segmentedUtterances.append(makeSpeechObject(text, voiceSeqs[i]))
            else:
                segmentedUtterances.append(u)
        utterances = segmentedUtterances
        return utterances

    def cleanUtterances(self, utts, removeBlanks=True):
        newUtts = {}
        for u in utts:
            text = u[TEXT_KEY].strip()
            voice = u[VOICE_KEY].strip()
            if len(text) == 0 and removeBlanks:
                continue
            elif text in newUtts and newUtts[text] != voice:
                raise ValueError("Collision for utterance (%s): (%s) vs. (%s)"%(text, voice, newUtts[text]))
            else:
                newUtts[text] = voice
        return [makeSpeechObject(t, newUtts[t]) for t in sorted(newUtts.keys())]
            
    def makeDuplicateMsg(self, msg, speechAct=INFORM_ACT):
        msgId = msg.getId()
        msg = msg.clone()
        msg.setContextValue(msg.CONTEXT_CONVERSATION_ID_KEY, msgId)
        msg.updateId()
        if speechAct is not None:
            msg.setSpeechAct(speechAct)
        return msg

if __name__ == "__main__":
    parser = DialogToSpeechService()
    aText = 'this  is a text containing a number 8 and equation  |||-x= -tan (7.5+(5*-y))||| as compared to the original'
    print "Processed: "
    print parser(aText)
    print "Original: "
    print aText
    print parser('this is a test, hmm. Hmm! hmmm |||equ + 1|||')
    print parser('this is a test |||equ||| and another |||PIee|||')
    print segmentUtterance("")
    print segmentUtterance("aaaa")
    print segmentUtterance("aaa.aaa")
    print segmentUtterance("aaa. aaa!!  aaa")
    print segmentUtterance("!aaa. aaa! aaa")
    print segmentUtterance("!aaa. aaa!! aaa")
    print segmentUtterance("A text.Aaaa.  AAA.")
    print makeMediaSemanticsLabel("At which points of time is Tommy's height above the pool the highest?")
