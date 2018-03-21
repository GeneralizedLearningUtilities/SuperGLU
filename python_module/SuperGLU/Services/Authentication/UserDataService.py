# -*- coding: utf-8 -*-
from datetime import datetime

from SuperGLU.Util.Serialization import SuperGlu_Serializable, StorageToken, untokenizeObject
from SuperGLU.Util.SerializationDB import DBSerialized
from SuperGLU.Core.FIPA.SpeechActs import (INFORM_ACT, REQUEST_ACT,
    NOT_UNDERSTOOD_ACT, CONFIRM_ACT, DISCONFIRM_ACT)
from SuperGLU.Core.Messaging import Message
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.Authentication.UserData import UserData, UserContext

HAS_USER_VERB = "HasUser"
HAS_CONTEXT_VERB = "HasContext"
CONTAINS_VERB = "Contains"
VALUE_VERB = "Value"
VOID_VERB = "Void"

CONTEXT_USER_CONTEXT = "UserContext"
CONTEXT_USER_ID = "UserId"
CONTEXT_USER_AUTH_FALLBACK = "UserAuthFallback";
CONTEXT_USER_NAME = "UserName"
CONTEXT_ERROR = "ErrorMessage"

class ProcessingExcept(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#TODO: Note that we don't have a way to add create a context and add
#      users to it.  See the echo function where we create a demo context

class UserDataService(BaseService):
    USER_SERVICE_NAME = "UserDataService"

    # Message format: ServiceName, Verb, (Key), (ReturnVal), Inform/Req,
    #                 Context: UserContext, (UserId/UserName)

    def receiveMessage(self, msg):
        if msg.getActor() != UserDataService.USER_SERVICE_NAME:
            return
        #Find and call the action, w/ exceptions as error messages
        action = self.mapMsg(msg)
        try:
            response = action(msg)
            if response:
                self.sendMessage(response)
        except ProcessingExcept as err:
            self.sendMessage(self.makeErrorResponse(msg, str(err)))

    def mapMsg(self, msg):
        speechAct = msg.getSpeechAct()
        verb = msg.getVerb()
        if verb == HAS_CONTEXT_VERB and  speechAct == REQUEST_ACT:
            return self.hasContext
        elif verb == HAS_CONTEXT_VERB and  speechAct == INFORM_ACT:
            return self.makeContext
        elif verb == CONTAINS_VERB and speechAct == REQUEST_ACT:
            return self.readContextKeys
        elif verb == HAS_USER_VERB and speechAct == REQUEST_ACT:
            return self.hasUserInContext
        elif verb == VALUE_VERB and speechAct == REQUEST_ACT:
            return self.readContextValue
        elif verb == VALUE_VERB and speechAct == INFORM_ACT:
            return self.writeContextValue
        #@TODO: Should clear out values, until then, set to None
        #elif verb == VOID_VERB and speechAct == REQUEST_ACT:
        #    return self.delContextValue
        elif verb == "ECHO":
            return self.echo
        else:
            return self.defaultAction

    def defaultAction(self, msg):
        return None

    def _findContext(self, msg, errorOnMissing=True):
        """Find and return the context matching the msg - throw an exception on error"""
        ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
        ctx = None
        if ctxId:
            #Note that the helper we call looks for ID *and* name
            ctx = UserContext.findContext(ctxId)
        if not ctx and errorOnMissing:
            raise ProcessingExcept("Error: No context with id/name = %s"%(ctxId,))
        else:
            return ctx

    def hasContext(self, msg):
        ctx = self._findContext(msg, False)
        hasContext = ctx is not None
        return self.makeResponse(msg, hasContext, INFORM_ACT)

    def makeContext(self, msg):
        ctxName = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
        ctx = UserContext.findContext(ctxName)
        hasContext = msg.getResult()
        if hasContext and ctx:
            return self.makeResponse(msg, True, CONFIRM_ACT)
        elif hasContext and not ctx:
            #Look by ID and name (we're expecting name)
            dt = datetime.now().isoformat()
            ctx = UserContext(name=ctxName)
            ctx.setPrefValue("ContextCreated", dt)
            ctx.setPrefValue("ContextUpdated", dt)
            ctx.save()
            return self.makeResponse(msg, True, CONFIRM_ACT)
        elif not hasContext and ctx:
            # Disallow deleting contexts from here
            return self.makeResponse(msg, False, DISCONFIRM_ACT)
        else:
            return self.makeResponse(msg, False, CONFIRM_ACT)

    def readContext(self, msg):
        ctx = self._findContext(msg)
        #NOTE that we ONLY get the prefs that go with the context name
        users = []
        for user in ctx.readDBUsers():
            users.append({
                'id': user.getId(),
                'userId': user.getUserID(),
                'userName': user.getUserName(),
                'userEmail': user.getEmail(),
                'prefs': user.getPrefs(ctx.getName())
            })
        prefs = dict([(ky, ctx.getPrefValue(ky))
                      for ky in ctx.getPrefKeys()])
        outData = {'name': ctx.getName(),
                   'users': users,
                   'prefs': prefs}
        return self.makeResponse(msg, outData, INFORM_ACT)

    def readContextKeys(self, msg):
        ctx = self._findContext(msg)
        userId = self.extractUserId(msg, False)
        if userId is None:
            return self.makeResponse(msg, ctx.getPrefKeys(), INFORM_ACT)
        else:
            return self.readContextUserKeys(msg)

    def readContextValue(self, msg):
        ctx = self._findContext(msg)
        userId = self.extractUserId(msg, False)
        key = msg.getObject()
        if key is None and userId is None:
            return self.readContext(msg)
        elif not key:
            return self.readContextUser(msg)
        elif userId is None:
            return self.makeResponse(msg, ctx.getPrefValue(key, ""), INFORM_ACT)
        else:
            return self.readContextUserVal(msg)

    def writeContextValue(self, msg):
        ctx = self._findContext(msg)
        userId = self.extractUserId(msg, False)
        key = msg.getObject()
        if not key:
            raise ProcessingExcept("No context pref key found")
        value = msg.getResult()
        if userId is None:
            ctx.setPrefValue(key, value)
            ctx.save()
            return self.makeResponse(msg, True, CONFIRM_ACT)
        else:
            return self.writeContextUserVal(msg)

    def readContextUser(self, msg):
        ctx = self._findContext(msg)
        userId = self.extractUserId(msg)
        if userId == '':
            userData = {'id': '',
                        'userId': '',
                        'userName': '',
                        'userEmail': '',
                        'prefs': {}}
        else:
            user = UserData.read(userId)
            if not user:
                ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
                user = UserData.readByLogin(userId, None, ctxId)
            if user is None:
                raise ProcessingExcept("No user found found in context")
            userData = {'id': user.getId(),
                        'userId': user.getUserID(),
                        'userName': user.getUserName(),
                        'userEmail': user.getEmail(),
                        'prefs': user.getPrefs(ctx.getName())}
        return self.makeResponse(msg, userData, INFORM_ACT)

    def hasUserInContext(self, msg):
        ctx = self._findContext(msg, False)
        userId = self.extractUserId(msg)
        user = UserData.read(userId)
        if not user:
            ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
            user = UserData.readByLogin(userId, None, ctxId)
        if user is None:
            return False
        elif ctx is not None and (user.getId() not in ctx.getUsers()):
            return False
        else:
            return True

    def readContextUserKeys(self, msg):
        ctx = self._findContext(msg)
        userId = self.extractUserId(msg)
        if userId == '':
            return self.makeResponse(msg, [], INFORM_ACT) #Anonymous
        else:
            usr = UserData.read(userId)
            if not usr:
                ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
                usr = UserData.readByLogin(userId, None, ctxId)
            if not usr:
                raise ProcessingExcept("Could not find user " + userId)
            return self.makeResponse(msg, usr.getPrefs(ctx.getName()), INFORM_ACT)

    def readContextUserVal(self, msg):
        ctx = self._findContext(msg)
        key = msg.getObject()
        if not key:
            raise ProcessingExcept("No user context pref key found")
        userId = self.extractUserId(msg)
        if userId == '':
            return self.makeResponse(msg, '', INFORM_ACT) #Anonymous
        usr = UserData.read(userId)
        if not usr:
            ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
            usr = UserData.readByLogin(userId, None, ctxId)
        if not usr:
            raise ProcessingExcept("Could not find user " + userId)
        value = usr.getPrefValue(ctx.getName(), key)
        return self.makeResponse(msg, value, INFORM_ACT)

    def writeContextUserVal(self, msg):
        ctx = self._findContext(msg)
        key = msg.getObject()
        if not key:
            raise ProcessingExcept("No user context pref key found")
        userId = self.extractUserId(msg)
        #NOPE - writing for an anonymous user is an error
        if not userId or len(userId) == 0:
            raise ProcessingExcept("No user ID specified")
        usr = UserData.read(userId)
        if not usr:
            ctxId = msg.getContextValue(CONTEXT_USER_CONTEXT, None)
            usr = UserData.readByLogin(userId, None, ctxId)
        if not usr:
            raise ProcessingExcept("Could not find user " + userId)
            #usr = UserData.onLogin(userId)
            #ctx.addUser(userId)
            #ctx.save()
        value = msg.getResult()
        usr.setPrefValue(ctx.getName(), key, value)
        usr.save()
        return self.makeResponse(msg, True, CONFIRM_ACT)

    #TODO: this extra-hacky method should go away at some point
    def echo(self, msg):
        if msg.getSpeechAct() != "experiment":
            #Not our hack - just echo back
            resp = self.makeResponse(msg, None, INFORM_ACT)
            resp.setVerb("HOLLA BACK")
            return resp

        #Special, hacky case: create an experiment context
        dt = datetime.now().isoformat()

        #Look by ID and name (we're expecting name)
        ctx = UserContext.findContext("DemoExperiment")
        if not ctx:
            ctx = UserContext(name="DemoExperiment")
            ctx.setPrefValue("ContextCreated", dt)

        ctx.setPrefValue("ContextUpdated", dt)

        #Add all users (and set an experimental context variable for them)
        for user in UserData.objects():
            user.setPrefValue(ctx.getName(), "UserAdded", dt)
            user.save()
            ctx.addUser(user.getId())
        ctx.save()

        resp = self.makeResponse(msg, None, INFORM_ACT)
        resp.setVerb("HOLLA BACK")
        resp.setSpeechAct(resp.getSpeechAct() + " => Created context " + ctx.getId())
        return resp

    def extractUserId(self, msg, errorOnMissing=True):
        userId = msg.getContextValue(CONTEXT_USER_ID, None)
        useAuth = msg.getContextValue(CONTEXT_USER_AUTH_FALLBACK, True)

        # Remember our Core Server decorates messages with the current user
        # Note that we default to '' (not None) for the anonymous user
        if not userId and useAuth:
            userId = msg.getContextValue(Message.AUTHENTICATION_KEY, '')

        # Note that we allow empty string (anon current user)
        if userId is None and errorOnMissing:
            raise ProcessingExcept("No user ID specified")
        return userId

    def makeResponse(self, request, value=None, speechAct=INFORM_ACT):
        oldId = request.getId()
        response = request.clone()
        response.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId)
        response.setSpeechAct(speechAct)
        if value is not None:
            response.setResult(value)
        response.updateTimestamp()
        return response

    def makeErrorResponse(self, request, errMsg):
        response = self.makeResponse(request, None, NOT_UNDERSTOOD_ACT)
        response.setContextValue(CONTEXT_ERROR, errMsg)
        return response
