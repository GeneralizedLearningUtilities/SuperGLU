# -*- coding: utf-8 -*-
import unittest

from SuperGLU.Util.Serialization import (
    SuperGlu_Serializable,
    tokenizeObject)

from SuperGLU.Util.SerializationDB import (
    SerializableDBWrapper,
    SerializableMongoWrapper,
    ReadWriteChecking,
    _flushLazyWrappers)

from SuperGLU.Services.Authentication.UserData import (
    UserContext,
    UserData)

from pymongo import Connection


TEST_DB_URI = 'mongodb://127.0.0.1:27017/auth_test_db'


def makeMongo(collection=None):
    if collection:
        return SerializableMongoWrapper(collection)
    else:
        return SerializableMongoWrapper()


@ReadWriteChecking
class UserContext_Serialization_Tests(unittest.TestCase):
    def setUp(self):
        Connection(TEST_DB_URI).drop_database('auth_test_db')
        SerializableMongoWrapper.configureConnection(TEST_DB_URI)
        SerializableDBWrapper.setWrapperFactory(makeMongo)

    def tearDown(self):
        SerializableDBWrapper.setWrapperFactory(None)
        SerializableMongoWrapper.configureConnection(None)
        _flushLazyWrappers()

    def testReadWriteSuperBlank(self):
        ctx = UserContext("SuperBlank")
        self.assertEquals("SuperBlank", ctx.getName())
        self.assertReadWrite(ctx)

    def testReadWriteNoPrefs(self):
        ctx = UserContext("NoPrefs", ["user1"])
        self.assertEquals("NoPrefs", ctx.getName())
        self.assertReadWrite(ctx)

    def testReadWriteNoUsers(self):
        ctx = UserContext("NoUsers", [], {"Pref1": "Super"})
        self.assertEquals("NoUsers", ctx.getName())
        self.assertReadWrite(ctx)

    def testReadWriteFull(self):
        ctx = UserContext(
            "Full",
            ["user1", "user2"],
            {"Pref1": "Super", "Pref2": "Duper"}
        )
        self.assertEquals("Full", ctx.getName())
        self.assertEquals(["Pref1", "Pref2"], ctx.getPrefKeys())
        self.assertReadWrite(ctx)

        #Get
        self.assertEquals("Super", ctx.getPrefValue("Pref1"))

        #Get missing
        self.assertIsNone(ctx.getPrefValue("NOPE"))
        self.assertEquals("MISSING", ctx.getPrefValue("StillNope", "MISSING"))

        #Pop missing
        self.assertIsNone(ctx.popPrefValue("NOPE"))
        self.assertEquals("MISSING", ctx.popPrefValue("StillNope", "MISSING"))

        #Pop and then re-pop now missing
        self.assertEquals("Duper", ctx.popPrefValue("Pref2", "WHAT?"))
        self.assertIsNone(ctx.popPrefValue("Pref2"))
        self.assertEquals("MISSING", ctx.popPrefValue("Pref2", "MISSING"))

        #Invasive state check
        ctx.setPrefValue("Pref1", "NewSuper")
        self.assertEquals({"Pref1": "NewSuper"}, ctx._prefs)
        self.assertEquals(["Pref1"], ctx.getPrefKeys())

    def testReadWriteRetrieveUsers(self):
        u1 = UserData.onLogin("user1", "User One", "user1@nowhere.com", "testing")
        u2 = UserData.onLogin("user2", "User Two", "user2@nowhere.com", "testing")
        self.assertNotEquals(u1.getId(), u2.getId())

        ctx = UserContext(
            "WithUsers",
            [u1.getId(), u2.getId()],
            {"u1Name": u1.getUserName(), "u2Name": u2.getUserName()}
        )

        self.assertReadWrite(ctx)

        #If read/write succeeded, check the indexes
        self.assertEquals([ctx], UserContext.objects(users=u1.getId()))
        self.assertEquals([ctx], UserContext.objects(users=u2.getId()))
        self.assertEquals([],    UserContext.objects(users='notAPerson'))
        self.assertEquals([ctx], UserContext.objects(name='WithUsers'))
        self.assertEquals([],    UserContext.objects(name='notAContext'))

        idList = sorted([u1.getId(), u2.getId()])

        #Test users changes that shouldn't affect state
        copy = UserContext.read(ctx.getId())
        self.assertSerialEquals(ctx, copy)
        ctx.addUser(u1.getId())
        ctx.removeUser("user3")
        self.assertSerialEquals(ctx, copy)
        self.assertEquals(idList, copy.getUsers())

        #Check user DB read
        users = ctx.readDBUsers()
        self.assertEquals(idList, sorted([u.getId() for u in users]))

        #What about empty users (via removal and then when hitting the DB)
        ctx.removeUser(u1.getId())
        ctx.removeUser(u2.getId())
        self.assertEquals([], ctx.getUsers())
        self.assertEquals([], ctx.readDBUsers())


@ReadWriteChecking
class UserData_Serialization_Tests(unittest.TestCase):
    def setUp(self):
        Connection(TEST_DB_URI).drop_database('auth_test_db')
        SerializableMongoWrapper.configureConnection(TEST_DB_URI)
        SerializableDBWrapper.setWrapperFactory(makeMongo)

    def tearDown(self):
        SerializableDBWrapper.setWrapperFactory(None)
        SerializableMongoWrapper.configureConnection(None)

    def testAnon(self):
        anon1 = UserData.onLogin(None, None, None, None)

        anon2 = UserData()

        anon3 = UserData("bob")
        anon3.becomeAnon()

        self.assertSerialEquals(anon1, anon2)
        self.assertSerialEquals(anon2, anon3)
        self.assertSerialEquals(anon1, anon3)

        print anon1.getId(), anon1
        anon1.save()
        print UserData.read(anon1.getId())

        self.assertReadWrite(anon1)
        self.assertReadWrite(anon2)
        self.assertReadWrite(anon3)

    def testAleksCheck(self):
        self.assertFalse(UserData.isAleksGuid(None))
        self.assertFalse(UserData.isAleksGuid(''))
        self.assertFalse(UserData.isAleksGuid(' '))

        guid = UserData.ALEKS_GUID
        self.assertTrue(UserData.isAleksGuid(guid))

        guid = ' ' + guid.upper() + ' '
        self.assertTrue(UserData.isAleksGuid(guid))

    def testLoginNew(self):
        orig = UserData.onLogin("uid", "user name", "me@there.com", "test")
        self.assertSerialEquals(orig, UserData.read(orig.getId()))

        self.assertEquals("uid", orig.getUserID())
        self.assertEquals("user name", orig.getUserName())
        self.assertEquals("me@there.com", orig.getEmail())
        self.assertEquals([], orig.getRoles())

        self.assertEquals(["me@there.com"], orig.getAllEmails())
        self.assertEquals([":uid", "test:uid"], orig.getAllUserIDs())

        #Check stats

        def stat(name):
            return orig.getPrefValue(UserData.PREFS_STATS, name, "")

        self.assertTrue(len(stat("LastLoginTime")) > 1)
        self.assertEquals("test", stat("LastLoginAuth"))
        self.assertEquals("uid", stat("LastLoginID"))
        self.assertEquals("me@there.com", stat("LastLoginEmail"))

        #Check auth prefs

        #Only one auth section - our "test" from above
        self.assertEquals(1, len(orig.getPrefs(UserData.PREFS_AUTH)))

        def auth(name):
            prefs = orig.getPrefValue(UserData.PREFS_AUTH, "test", {})
            return prefs.get(name, "")

        self.assertTrue(len(auth("LastLogin")) > 1)
        self.assertEquals("uid", auth("LastID"))
        self.assertEquals("me@there.com", auth("LastEmail"))
        self.assertEquals("user name", auth("UserName"))

        self.assertEquals(["me@there.com"], auth("Emails"))
        self.assertEquals(["uid"], auth("UserIDs"))

    def testLoginExisting(self):
        first = UserData.onLogin("uid", "user name", "me@there.com", "test")
        self.assertSerialEquals(first, UserData.read(first.getId()))

        first.addRole("role1")
        first.save()
        self.assertSerialEquals(first, UserData.read(first.getId()))

        self.assertEquals(['role1'], first.getRoles())

        self.assertEquals(["me@there.com"], first.getAllEmails())

        import time
        time.sleep(1)

        last = UserData.onLogin("uid", "user name", "me@there.com", "test")
        self.assertEquals(first.getUserID(), last.getUserID())
        self.assertEquals(first.getUserName(), last.getUserName())
        self.assertEquals(first.getEmail(), last.getEmail())
        self.assertEquals(first.getRoles(), last.getRoles())

        self.assertEquals(["me@there.com"], last.getAllEmails())
        self.assertEquals([":uid", "test:uid"], last.getAllUserIDs())

        #Check stats

        def stat(name):
            return last.getPrefValue(UserData.PREFS_STATS, name, "")

        self.assertTrue(len(stat("LastLoginTime")) > 1)
        self.assertEquals("test", stat("LastLoginAuth"))
        self.assertEquals("uid", stat("LastLoginID"))
        self.assertEquals("me@there.com", stat("LastLoginEmail"))

        #Check auth prefs

        #Only one auth section - our "test" from above
        self.assertEquals(1, len(last.getPrefs(UserData.PREFS_AUTH)))

        def auth(name):
            prefs = last.getPrefValue(UserData.PREFS_AUTH, "test", {})
            return prefs.get(name, "")

        self.assertTrue(len(auth("LastLogin")) > 1)
        self.assertEquals("uid", auth("LastID"))
        self.assertEquals("me@there.com", auth("LastEmail"))
        self.assertEquals("user name", auth("UserName"))

        self.assertEquals(["me@there.com"], auth("Emails"))
        self.assertEquals(["uid"], auth("UserIDs"))

    def testLoginSameUserMultEmail(self):
        UserData.onLogin("uid", "user name", "me@there.com", "test")
        user = UserData.onLogin("uid", "user name", "me2@there.com", "test")

        self.assertSerialEquals(user, UserData.read(user.getId()))

        self.assertEquals(["me2@there.com", "me@there.com"], user.getAllEmails())
        self.assertEquals([":uid", "test:uid"], user.getAllUserIDs())

        #Check stats

        def stat(name):
            return user.getPrefValue(UserData.PREFS_STATS, name, "")

        self.assertEquals("test", stat("LastLoginAuth"))
        self.assertEquals("uid", stat("LastLoginID"))
        self.assertEquals("me2@there.com", stat("LastLoginEmail"))

        #Check auth prefs

        def auth(name):
            prefs = user.getPrefValue(UserData.PREFS_AUTH, "test", {})
            return prefs.get(name, "")

        self.assertEquals("uid", auth("LastID"))
        self.assertEquals("me2@there.com", auth("LastEmail"))
        self.assertEquals("user name", auth("UserName"))

        self.assertEquals(["me2@there.com", "me@there.com"], auth("Emails"))
        self.assertEquals(["uid"], auth("UserIDs"))

    def testLoginMultiple(self):
        logins = [
            ("uidA1", "user name 1", "email1@testA.com", "testA"),
            ("uidA2", "user name 2", "email1@testA.com", "testA"), #Same email, different user
            ("uidA1", "user name 3", "email2@testA.com", "testA"), #Same UID, different email
            ("uidB1", "user name 4", "email2@testA.com", "testB"), #New auth provider - but should match with previous email
            ("uidB1", "user name 5", "email1@testB.com", "testB"), #Same UID, different email (from other auth)
            ("uidB2", "user name 6", "email1@testB.com", "testB"), #Same email, different UID
            ("uidB2", "user name 7", "email2@testB.com", "testB"), #Same UID, different email
        ]

        all_emails = []
        all_uids = []

        user = None
        for uid, uname, email, auth in logins:
            all_emails.append(email)
            all_uids.append(auth + ':' + uid)
            user = UserData.onLogin(uid, uname, email, auth)

        self.assertIsNotNone(user)

        #First login created the user - so that's the "main" ID
        self.assertSerialEquals(user, UserData.read(user.getId()))

        all_emails = sorted(set(all_emails))
        print "ALL EMAILS: %s" % str(all_emails)
        self.assertEquals(4, len(all_emails))
        self.assertEquals(all_emails, user.getAllEmails())

        all_uids.append(":uidA1")
        all_uids = sorted(set(all_uids))
        print "ALL UIDS: %s" % str(all_uids)
        self.assertEquals(5, len(all_uids)) #4 + top-level ID
        self.assertEquals(all_uids, user.getAllUserIDs())

        #Check stats

        def stat(name):
            return user.getPrefValue(UserData.PREFS_STATS, name, "")

        self.assertEquals("testB", stat("LastLoginAuth"))
        self.assertEquals("uidB2", stat("LastLoginID"))
        self.assertEquals("email2@testB.com", stat("LastLoginEmail"))

        #Check auth prefs

        def auth(auth, name):
            prefs = user.getPrefValue(UserData.PREFS_AUTH, auth, {})
            return prefs.get(name, "")

        self.assertEquals("uidA1", auth("testA", "LastID"))
        self.assertEquals("email2@testA.com", auth("testA", "LastEmail"))
        self.assertEquals("user name 3", auth("testA", "UserName"))
        self.assertEquals(["email1@testA.com", "email2@testA.com"], auth("testA", "Emails"))
        self.assertEquals(["uidA1", "uidA2"], auth("testA", "UserIDs"))

        self.assertEquals("uidB2", auth("testB", "LastID"))
        self.assertEquals("email2@testB.com", auth("testB", "LastEmail"))
        self.assertEquals("user name 7", auth("testB", "UserName"))
        self.assertEquals(["email1@testB.com", "email2@testA.com", "email2@testB.com"], auth("testB", "Emails"))
        self.assertEquals(["uidB1", "uidB2"], auth("testB", "UserIDs"))

    def testSnarfMissingUserData(self):
        #Login/create user, then update with no name or email
        user = UserData.onLogin("uid", "user name 1", "me@there.com", "test")
        user.setUserName("")
        user.setEmail("")
        user.save()

        #Should grab the new stuff on login
        user = UserData.onLogin("uid", "user name 2", "me2@there.com", "test")
        self.assertSerialEquals(user, UserData.read(user.getId()))

        self.assertEquals("user name 2", user.getUserName())
        self.assertEquals("me2@there.com", user.getEmail())

    def testUpdateMissingAuth(self):
        orig = UserData.onLogin("uid", "user name", "me@there.com", None)
        self.assertSerialEquals(orig, UserData.read(orig.getId()))

        UA = UserData.UNKNOWN_AUTH #Make the code a little more concise

        self.assertEquals("uid", orig.getUserID())
        self.assertEquals("user name", orig.getUserName())
        self.assertEquals("me@there.com", orig.getEmail())
        self.assertEquals([], orig.getRoles())

        self.assertEquals(["me@there.com"], orig.getAllEmails())
        self.assertEquals([":uid", UA+":uid"], orig.getAllUserIDs())

        #Check stats

        def stat(name):
            return orig.getPrefValue(UserData.PREFS_STATS, name, "")

        self.assertTrue(len(stat("LastLoginTime")) > 1)
        self.assertEquals(UA, stat("LastLoginAuth"))
        self.assertEquals("uid", stat("LastLoginID"))
        self.assertEquals("me@there.com", stat("LastLoginEmail"))

        #Check auth prefs

        #Only one auth section - our "test" from above
        self.assertEquals(1, len(orig.getPrefs(UserData.PREFS_AUTH)))

        def auth(name):
            prefs = orig.getPrefValue(UserData.PREFS_AUTH, UA, {})
            return prefs.get(name, "")

        self.assertTrue(len(auth("LastLogin")) > 1)
        self.assertEquals("uid", auth("LastID"))
        self.assertEquals("me@there.com", auth("LastEmail"))
        self.assertEquals("user name", auth("UserName"))

        self.assertEquals(["me@there.com"], auth("Emails"))
        self.assertEquals(["uid"], auth("UserIDs"))

    def testRoles(self):
        user = UserData.onLogin("uid", "user name", "me@there.com", "test")
        self.assertSerialEquals(user, UserData.read(user.getId()))

        #Add role
        user.addRole("role1")
        self.assertEquals(["role1"], user.getRoles())

        #Maintain alphabetical order
        user.addRole("role0")
        self.assertEquals(["role0", "role1"], user.getRoles())

        #Save/read with multiple roles
        self.assertReadWrite(user)

        #Ignore dups
        user.addRole("role0")
        user.addRole("role1")
        self.assertEquals(["role0", "role1"], user.getRoles())

        self.assertFalse(user.needRole("role0"))
        self.assertFalse(user.needRole("role1"))
        self.assertTrue(user.needRole("role2"))
        self.assertEquals(["role0", "role1", "role2"], user.getRoles())


    def testPrefChanges(self):
        user = UserData.onLogin("uid", "user name", "me@there.com", "test")

        #Empty prefs
        self.assertEquals(user.getPrefs("NOPE"), {})
        self.assertEquals(user.getPrefs(""), {})

        #Simple optional preferences
        user.setPrefValue("opt", "K1", "V2")
        self.assertEquals("V2", user.getPrefValue("opt", "K1"))
        user.setPrefValue("opt", "K1", "V1")
        self.assertEquals("V1", user.getPrefValue("opt", "K1"))

        #Missing pref value
        self.assertEquals("MISS", user.getPrefValue("opt", "KX", "MISS"))
        self.assertEquals("MISS", user.getPrefValue("optNo", "K1", "MISS"))

        #pop value (including bad pref and key)
        user.setPrefValue("opt", "K2", "V2")
        self.assertEquals("V2", user.getPrefValue("opt", "K2"))
        self.assertEquals("MISS", user.popPrefValue("optNo", "K2", "MISS"))
        self.assertEquals("V2", user.popPrefValue("opt", "K2", "MISS"))
        self.assertEquals("MISS", user.popPrefValue("opt", "K2", "MISS"))
        self.assertEquals("MISS", user.popPrefValue("optNo", "K2", "MISS"))

        self.assertEquals(["me@there.com"], user.getAllEmails())
        self.assertEquals([":uid", "test:uid"], user.getAllUserIDs())

        #Cheat a little on the timestamp
        ts = user.getPrefValue(UserData.PREFS_STATS, "LastLoginTime")

        self.assertEquals(user.getAllPrefs(), {
            UserData.PREFS_STATS: {
                "LastLoginTime": ts,
                "LastLoginAuth": "test",
                "LastLoginID": "uid",
                "LastLoginEmail": "me@there.com",
            },
            UserData.PREFS_AUTH: {
                "test": {
                    "LastLogin": ts,
                    "LastID": "uid",
                    "LastEmail": "me@there.com",
                    "UserName": "user name",
                    "Emails": ["me@there.com"],
                    "UserIDs": ["uid"],
                }
            },
            "opt" : {
                "K1": "V1"
            }
        })

        #Check other prefs

        self.assertEquals(user.getPrefs("opt"), {"K1": "V1"})

        #Check stats

        self.assertEquals(user.getPrefs(UserData.PREFS_STATS), {
            "LastLoginTime": ts,
            "LastLoginAuth": "test",
            "LastLoginID": "uid",
            "LastLoginEmail": "me@there.com",
        })

        #Check auths

        self.assertEquals(user.getPrefs(UserData.PREFS_AUTH), {
            "test": {
                "LastLogin": ts,
                "LastID": "uid",
                "LastEmail": "me@there.com",
                "UserName": "user name",
                "Emails": ["me@there.com"],
                "UserIDs": ["uid"],
            }
        })

if __name__ == '__main__':
    unittest.main()
