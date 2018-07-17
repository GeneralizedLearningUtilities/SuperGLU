# -*- coding: utf-8 -*-
import unittest
from uuid import uuid4
from time import time, sleep

from SuperGLU.Core.FIPA.SpeechActs import CONFIRM_ACT
from SuperGLU.Core.Messaging import (Message, INFORM_ACT)

class MessageTest(unittest.TestCase):

    def setUp(self):
        self.actor = "AnActor"
        self.object = "AnObject"
        self.verb = "AVerb"
        self.result = "Result"
        self.speechAct = CONFIRM_ACT
        self.contextKey = "SimpleContext"
        self.contextVal = 0
        self.context = {self.contextKey : self.contextVal}
        self.timestamp = time()
        self.theId = uuid4()
        self.blankMessage = Message()
        self.message = Message(self.actor, self.verb, self.object,
                               self.result, self.speechAct, self.context,
                               self.timestamp, self.theId)

    def test__init__(self):
        blankMessage = Message()
        fullMessage = Message(self.actor, self.verb, self.object,
                               self.result, self.speechAct, self.context,
                               self.timestamp, self.theId)
        self.assertIsInstance(blankMessage, Message)
        self.assertIsInstance(fullMessage, Message)

    def testGetActor(self):
        self.assertIsNone(self.blankMessage.getActor())
        self.assertEqual(self.message.getActor(), self.actor)

    def testSetActor(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getActor(), self.actor)
        self.message.setActor(newValue)
        self.assertEqual(self.message.getActor(), newValue)

    def testGetVerb(self):
        self.assertIsNone(self.blankMessage.getVerb())
        self.assertEqual(self.message.getVerb(), self.verb)

    def testSetVerb(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getVerb(), self.verb)
        self.message.setVerb(newValue)
        self.assertEqual(self.message.getVerb(), newValue)

    def testGetObject(self):
        self.assertIsNone(self.blankMessage.getObject())
        self.assertEqual(self.message.getObject(), self.object)

    def testSetObject(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getObject(), self.object)
        self.message.setObject(newValue)
        self.assertEqual(self.message.getObject(), newValue)

    def testGetResult(self):
        self.assertIsNone(self.blankMessage.getResult())
        self.assertEqual(self.message.getResult(), self.result)

    def testSetResult(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getResult(), self.result)
        self.message.setResult(newValue)
        self.assertEqual(self.message.getResult(), newValue)

    def testGetSpeechAct(self):
        self.assertEqual(self.blankMessage.getSpeechAct(), INFORM_ACT)
        self.assertEqual(self.message.getSpeechAct(), self.speechAct)

    def testSetSpeechAct(self):
        newValue = INFORM_ACT
        self.assertEqual(self.message.getSpeechAct(), self.speechAct)
        self.message.setSpeechAct(newValue)
        self.assertEqual(self.message.getSpeechAct(), newValue)

    def testGetTimestamp(self):
        self.assertIsNone(self.blankMessage.getTimestamp())
        self.assertEqual(self.message.getTimestamp(), self.timestamp)

    def testSetTimestamp(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getTimestamp(), self.timestamp)
        self.message.setTimestamp(newValue)
        self.assertEqual(self.message.getTimestamp(), newValue)

    def testUpdateTimestamp(self):
        self.assertEqual(self.message.getTimestamp(), self.timestamp)
        sleep(0.001)
        self.message.updateTimestamp()
        #Now a str in isoformat format
        self.assertIsInstance(self.message.getTimestamp(), str)
        self.assertTrue(self.message.getTimestamp() > str(self.timestamp))

    def testHasContextValue(self):
        self.assertFalse(self.blankMessage.hasContextValue(self.contextKey))
        self.assertTrue(self.message.hasContextValue(self.contextKey))
        self.assertFalse(self.message.hasContextValue("NonexistentKey"))

    def testGetContextValue(self):
        self.assertIsNone(self.blankMessage.getContextValue(self.contextKey))
        self.assertEqual(self.message.getContextValue(self.contextKey), self.contextVal)
        self.assertIsNone(self.message.getContextValue("NonexistentKey"))

    def testGetContextKeys(self):
        self.assertEqual(list(self.blankMessage.getContextKeys()), [])
        self.assertEqual(list(self.message.getContextKeys()), [self.contextKey])

    def testSetContextValue_NoKey(self):
        newKey = "NewKey"
        newValue = "NewValue"
        self.assertFalse(self.blankMessage.hasContextValue(newKey))
        self.blankMessage.setContextValue(newKey, newValue)
        self.assertTrue(self.blankMessage.hasContextValue(newKey))
        self.assertEqual(self.blankMessage.getContextValue(newKey), newValue)

    def testSetContextValue_KeyExists(self):
        newValue = "NewValue"
        self.assertEqual(self.message.getContextValue(self.contextKey), self.contextVal)
        self.message.setContextValue(self.contextKey, newValue)
        self.assertEqual(self.message.getContextValue(self.contextKey), newValue)

    def testDelContextValue(self):
        self.assertTrue(self.message.hasContextValue(self.contextKey))
        self.message.delContextValue(self.contextKey)
        self.assertFalse(self.message.hasContextValue(self.contextKey))

    def test__hash__(self):
        self.assertNotEqual(hash(self.blankMessage), hash(Message()))
        self.assertEqual(hash(self.blankMessage), hash(self.blankMessage.clone(newId=False)))
        self.assertEqual(hash(self.message), hash(self.message.clone(newId=False)))
        self.assertNotEqual(hash(self.blankMessage), hash(self.message))
        clone1ActorDiff = self.message.clone(newId=False)
        clone1ActorDiff.setActor("Nobody")
        clone2ContextDiff = self.message.clone(newId=False)
        clone2ContextDiff.setContextValue("ImaginaryKey", 0)
        self.assertNotEqual(hash(self.message), hash(clone1ActorDiff))
        self.assertEqual(hash(self.message), hash(clone2ContextDiff))

    def test__eq__(self):
        clone1ActorDiff = self.message.clone(newId=False)
        clone1ActorDiff.setActor("Nobody")
        clone2ContextDiff = self.message.clone(newId=False)
        clone2ContextDiff.setContextValue("ImaginaryKey", 0)
        
        self.assertFalse(self.blankMessage == Message())
        self.assertTrue(self.message == self.message.clone(newId=False))
        self.assertFalse((self.blankMessage) == (self.message))
        self.assertFalse((self.message) == (clone1ActorDiff))
        self.assertFalse((self.message) == (clone2ContextDiff))

    def test__ne__(self):
        clone1ActorDiff = self.message.clone(newId=False)
        clone1ActorDiff.setActor("Nobody")
        clone2ContextDiff = self.message.clone(newId=False)
        clone2ContextDiff.setContextValue("ImaginaryKey", 0)
        
        self.assertTrue(self.blankMessage != Message())
        self.assertFalse(self.message != self.message.clone(newId=False))
        self.assertTrue((self.blankMessage) !=(self.message))
        self.assertTrue((self.message) !=(clone1ActorDiff))
        self.assertTrue((self.message)!=(clone2ContextDiff))

    def testIsEquivalent(self):
        # Identity Tests
        self.assertFalse(self.blankMessage.isEquivalent(self.message))
        self.assertFalse(self.message.isEquivalent(self.blankMessage))
        self.assertTrue(self.blankMessage.isEquivalent(self.blankMessage))
        self.assertTrue(self.message.isEquivalent(self.message))
        # Equivalency Tests
        messageClone = self.message.clone(newId=False)
        messageClone._id = uuid4()
        self.assertTrue(self.blankMessage.isEquivalent(Message()))
        self.assertTrue(self.message.isEquivalent(messageClone))
        # Different Id
        messageClone = self.message.clone()
        messageClone._id = uuid4()
        self.assertTrue(self.blankMessage.isEquivalent(Message()))
        self.assertTrue(self.message.isEquivalent(messageClone))

    def testSerialize(self):
        token = self.message.saveToToken()
        newMessage = Message()
        newMessage.initializeFromToken(token)
        self.assertEqual(self.message, newMessage)

    def testClone(self):
        x = self.message.clone(newId=False)
        self.assertEqual(self.message, x)

    def testAuthContext(self):
        self.message.setContextValue(Message.AUTHORIZATION_KEY, "role1,role2")
        self.message.setContextValue(Message.AUTHENTICATION_KEY, "userid")
        
        self.testClone()
        
        #silly but thorough
        self.assertEquals("role1,role2", self.message.getContextValue(Message.AUTHORIZATION_KEY))
        self.assertEquals("userid", self.message.getContextValue(Message.AUTHENTICATION_KEY))

    def testMakeFIPAMessage(self):
        self.assertRaises(NotImplementedError, self.blankMessage.makeFIPAMessage)

    def testMakeTinCanMessage(self):
        self.assertRaises(NotImplementedError, self.blankMessage.makeTinCanMessage)



if __name__ == "__main__":
    #Please invoke with `python -m SKO_Architecture.Tests.Messaging_UnitTests`
    unittest.main()
