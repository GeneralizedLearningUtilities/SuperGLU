# -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger

from SuperGLU.Util.Serialization import SuperGlu_Serializable, StorageToken, untokenizeObject
from SuperGLU.Util.SerializationDB import DBSerialized

LOGGER = getLogger(__name__)

@DBSerialized()
class UserContext(SuperGlu_Serializable):
    """ A UserContext for things like experiment design. A context has a
    name, a dictionary of preference values, and a list of UserData keys.
    Since the user keys are UUID's they aren't terribly useful.  However,
    you may load the UserData objects in one go with readDBUsers.  Of
    course, you're also free to call UserData.read with any single ID
    to read a user if necessary
    """

    INDEXES = ["name", "users"]

    # NOTE that we maintain the user list as a set internally, but
    # present it as a list to the external world (and when saving)

    def __init__(self, name=None, userIDList=None, prefs=None):
        super(UserContext, self).__init__()

        self._name = str(name) if name else ''
        self._users = set(userIDList) if userIDList else set()
        self._prefs = dict(prefs) if prefs else {}

    @classmethod
    def findContext(cls, ctxId):
        """ Special helper - look for a context given the ID.  If that
        doesn't work, look using the context as a name
        """
        ctx = cls.read(ctxId)
        if not ctx:
            lst = cls.objects(name = ctxId)
            if lst:
                ctx = lst[0]
        return ctx

    @classmethod
    def getContextIds(cls):
        return [x.getId() for x in cls.objects()]

    @classmethod
    def getContextNames(cls):
        return [x.getName() for x in cls.objects()]

    def getName(self):
        """Simple getter for UserContext Name"""
        return self._name

    def getUsers(self):
        """ Simple getter for UserContext User ID's. Note that a copy of the
        list is returned to prevent modifying the UserContext's state
        """
        return sorted(self._users)

    def addUser(self, userID):
        """ Add the specified user ID to the list of users. Duplicate
        keys are silently ignored.  Return True if user was added for
        first time, and return False if user was a duplicate
        """
        if userID in self._users:
            return False
        self._users.add(userID)
        return True

    def removeUser(self, userID):
        """Remove the specified user ID from the list of users. Missing
        keys are silently ignored"""
        if userID in self._users:
            self._users.remove(userID)

    def readDBUsers(self):
        """Return a list of UserData instances matches the user ID we
        currently. Note that this IS a database hit"""
        if not self._users:
            return []

        return UserData.objects(_id={'$in': list(self._users)})

    def getPrefKeys(self):
        """Return the keys in the prefs (in a sorted list)"""
        return sorted(self._prefs.keys())

    def getPrefValue(self, prefKey, defval=None):
        """Return the specified preference value by key. If the key is
        missing, the defval is returned"""
        return self._prefs.get(prefKey, defval)

    def setPrefValue(self, prefKey, prefValue):
        """Set the given preference key to the given value"""
        self._prefs[prefKey] = prefValue

    def popPrefValue(self, prefKey, defval=None):
        """Remove the specified key from the preference dictionary and
        return the delete value. If the key wasn't present then defval
        is returned."""
        return self._prefs.pop(prefKey, defval)

    def saveToToken(self):
        token = super(UserContext, self).saveToToken()
        token['name'] = self._name
        token['users'] = list(self._users)
        token['prefs'] = dict(self._prefs)
        return token

    def initializeFromToken(self, token, context=None):
        super(UserContext, self).initializeFromToken(token, context)
        self._name = token.get('name', '')
        self._users = set(token.get('users', []))
        self._prefs = dict(token.get('prefs', {}))


@DBSerialized()
class UserData(SuperGlu_Serializable):
    """User Data as a serializable object.  Each object is keyed by
    a "standard" UUID, has a "regular" user ID, and contains the roles
    for the user (so this represents both authN and authZ data).  Note
    that we assume the user is authenticated via someone else's OAuth2
    service.

    When someone logs in via some authsource, we get the user ID, user
    name, and email from that authsource.  We save (or update) that info
    per source.  We also index the user ID and email.

    If we can't find the user, we create a new user and set that user's
    "real" or "top-level" user ID, user name, and email to the one we
    just got.

    Note that authN sources and preferences are dictionaries of
    dictionaries.  For instance, if we only had prefs for service1 and
    service2, it might look something like:

        {
            'service1': {'opt1': 'Hello', 'opt2': 'World'},
            'service2': {'optA': 'Goodbye', 'optb': 'Cruel', 'optc': 'World'},
        }
    """

    #This is for automatic indexing for us
    INDEXES = ["AllEmails", "AllUserIDs"]

    USER_ANONYMOUS = 'anonymous'
    PREFS_AUTH = 'authsources'
    PREFS_STATS = 'loginstats'
    UNKNOWN_AUTH = 'UNKNOWN'
    ALEKS_AUTH = 'ALEKS'
    ALEKS_GUID = '3df19190-a8b7-11e3-a5e2-0800200c9a66'

    def __init__(self, userID=None, userName=None, email=None, roles=None, prefs=None):
        super(UserData, self).__init__()
        #No user ID = anonymous user
        if not userID:
            self.becomeAnon()
        else:
            self._userID = userID
            self._userName = str(userName) if userName else ''
            self._email = str(email) if email else ''
            self._roles = set(roles) if roles else set()
            self._prefs = dict(prefs) if prefs else {}

    def getUserID(self):
        """ Simple getter for user ID"""
        return self._userID

    def getUserName(self):
        """Simple getter for user name"""
        return self._userName

    def setUserName(self, userName):
        """Simple setter for user name"""
        self._userName = str(userName) if userName else ''

    def getEmail(self):
        """Simple getter for user email"""
        return self._email

    def setEmail(self, email):
        """Simple setter for user email"""
        self._email = str(email) if email else ''

    def getRoles(self):
        """Simple getter for roles: note that a copy of the internal
        list is made so that changes to the returned list aren't reflected
        in the object"""
        return sorted(self._roles)

    def addRole(self, role):
        """Add the given role.  Duplicates are silently ignored"""
        self._roles.add(role)

    def needRole(self, role):
        """Identical to addRole, but returns True if and only if the
        role wasn't already present."""
        found = role not in self._roles
        self.addRole(role)
        return found

    def getAllPrefs(self):
        """Simple getter for all prefs: note that a copy of the internal
        dict is made so that changes to the returned dict aren't reflected
        in the object"""
        return dict(self._prefs)

    def getPrefs(self, prefName):
        """Return the prefs for the given prefs name.  If the prefs name
        hasn't been seen before, an empty dictionary is returned.  Note
        that the dict is copied to prevent internal modification."""
        return dict(self._prefs.get(prefName, {}))

    def setPrefValue(self, prefName, key, value):
        """Set pref key-value pair under the preference name"""
        if prefName not in self._prefs:
            self._prefs[prefName] = {}
        self._prefs[prefName][key] = value

    def getPrefValue(self, prefName, key, defval=None):
        """Return the value for the given prefName and key.  If either
        the prefName or the key are missing, then defval is returned"""
        return self._prefs.get(prefName, {}).get(key, defval)

    def popPrefValue(self, prefName, key, defVal=None):
        """Remove and return the prefs entry under the prefName for the
        given key.  If either the prefName or the key are missing, then
        defVal is returned."""
        return self._prefs.get(prefName, {}).pop(key, defVal)

    def becomeAnon(self):
        """ Simple helper method to force current instance to be the
        anonymous user.  Note that there is an assumption that there will
        not be a user ID associated with anonymous login, BUT we don't want
        to accidentally create multiple copies of the anonymous user with
        different UUID keys.  As a result, we force userID to '' but specify
        that the Serializable ID (and thus _id in MongoDB) is 'anonymous'."""
        self._userID = ''
        self._userName = UserData.USER_ANONYMOUS
        self._email = ''
        self._roles = set()
        self._prefs = {}
        self.updateId(UserData.USER_ANONYMOUS)

    def _getPrefsAuthSet(self, keyname):
        """Helper to extract a set of attributes for all authsources in
        PREFS_AUTH.  Note that the attribute is assumed to be iterable
        (so probably a list).  The returned set is a collection tuples
        of the form (value, authsource)
        """
        vals = set()

        allPrefs = self.getPrefs(UserData.PREFS_AUTH)
        for authsource, authPrefs in allPrefs.iteritems():
            for val in authPrefs.get(keyname, []):
                vals.add((val, authsource))

        return vals

    def getAllEmails(self):
        """Return a list of all emails currently associated with this
        user.  Note that this is also indexed."""
        #Drop the auth stuff for emails
        emails = set([e for e,auth in self._getPrefsAuthSet("Emails")])
        emails.add(self.getEmail())
        return [e for e in sorted(emails) if e]

    def getAllUserIDs(self):
        """Return a list of all user ID's currently associated with this
        user.  Note that this is also indexed."""
        userIDs = self._getPrefsAuthSet("UserIDs")
        if self.getUserID():
            #top-level user ID has blank auth source prefix
            userIDs.add((self.getUserID(), ''))
        return [':'.join([auth,u]) for u,auth in sorted(userIDs) if u]

    def __str__(self):
        return "%s[_id=%s] (%s <%s>) roles=%s" % (
            self._userID,
            self.getId(),
            self._userName,
            self._email or 'NO EMAIL',
            sorted(self._roles) or '[]',
        )

    @classmethod
    def isAleksGuid(cls, testGuid):
        """Return True if testGuid is indeed the GUID representing an
        ALEKS login attempt
        """
        if not testGuid:
            return False

        def filt(s):
            return str(s).lower().replace('-', '').strip()
        return filt(testGuid) == filt(cls.ALEKS_GUID)

    @classmethod
    def readByLogin(cls, userID=None, email='', authSource=None):
        if email is None: email = ''
        userData = None
        if not authSource:
            authSource = UserData.UNKNOWN_AUTH
        elif authSource.upper() == cls.ALEKS_AUTH:
            authSource = cls.ALEKS_AUTH + ':' + cls.ALEKS_GUID
        elif authSource == cls.ALEKS_GUID:
            authSource = cls.ALEKS_AUTH + ':' + authSource
        cls.objects()
        if userID:
            userData = cls.objects(AllUserIDs = ':'.join([authSource, userID]))
        if not userData and email:
            userData = cls.objects(AllEmails = email)
        if userData:
            return userData[0]
        else:
            return None

    @classmethod
    def onLogin(cls, userID, userName, email, authSource):
        """ Designed to be called when login occurs, this function
        insures the presence of a UserData record, handles any updates
        required on login, and returns a fully populated UserData
        instance (including roles for the current user) """

        if not userID:
            return UserData(None) #Will become anonymous

        #Find previous user - and create if necessary. We check for user
        #ID first and then by email if that isn't found.  Note that we
        #store user ID's as auth:ID, but emails are stored "plain".
        #ALSO NOTE that if the auth source is None we try and proceed
        #with the "unknown" auth source.  This really only lets broken
        #implementations proceed authN - the user won't have any roles
        #and is little better than an anonymous user
        if not authSource:
            authSource = UserData.UNKNOWN_AUTH
        userData = cls.objects(AllUserIDs = ':'.join([authSource, userID]))
        if not userData and email:
            userData = cls.objects(AllEmails = email)

        if not userData:
            LOGGER.debug("First login for %s" % userID)
            userData = UserData(userID, userName, email)
        else:
            #Found something - we'll take the first item
            userData = userData[0]
            #Fill in any missing data
            if userName and not userData.getUserName():
                userData.setUserName(userName)
            if email and not userData.getEmail():
                userData.setEmail(email)

        #Update stats for the user
        dt = datetime.now().isoformat()
        userData.setPrefValue(UserData.PREFS_STATS, "LastLoginTime", dt)
        userData.setPrefValue(UserData.PREFS_STATS, "LastLoginAuth", authSource)
        userData.setPrefValue(UserData.PREFS_STATS, "LastLoginID", userID)
        userData.setPrefValue(UserData.PREFS_STATS, "LastLoginEmail", email)

        #Update all authsource information for this authsource on this
        #user. Remember that a single authsource's data is stored in a
        #dictionary stored under the pref key name PREFS_AUTH)
        authPrefs = userData.getPrefValue(UserData.PREFS_AUTH, authSource, {})

        authPrefs["LastLogin"] = dt
        authPrefs["LastID"] = userID
        authPrefs["LastEmail"] = email
        authPrefs["UserName"] = userName

        emails = set(authPrefs.get("Emails", []))
        emails.add(email)
        authPrefs["Emails"] = sorted(emails)

        userids = set(authPrefs.get("UserIDs", []))
        userids.add(userID)
        authPrefs["UserIDs"] = sorted(userids)

        userData.setPrefValue(UserData.PREFS_AUTH, authSource, authPrefs)

        #Save updated data
        userData.save()

        #Now they can have the user data
        return userData

    def saveToToken(self):
        token = super(UserData, self).saveToToken()

        if not self._userID:
            token.setId(UserData.USER_ANONYMOUS)
        else:
            token.setId(self.getId())

        token['userID'] = self._userID
        token['userName'] = self._userName
        token['email'] = self._email
        token['roles'] = sorted(self._roles)
        token['prefs'] = dict(self._prefs)

        return token

    def initializeFromToken(self, token, context=None):
        super(UserData, self).initializeFromToken(token, context)

        self.updateId(token.getId())

        self._userID = token.get('userID', '')

        #Anonymous users actually have a blank user ID, but USER_ANONYMOUS
        #for their Serializable and MongoDB id's
        if self._userID == UserData.USER_ANONYMOUS:
            self._userID = ''

        self._userName = token.get('userName', '')
        self._email = token.get('email', '')
        self._roles = set(token.get('roles', []))
        self._prefs = dict(token.get('prefs', {}))
