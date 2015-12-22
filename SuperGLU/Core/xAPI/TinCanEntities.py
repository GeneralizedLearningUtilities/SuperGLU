# -*- coding: utf-8 -*-
from SuperGLU.Core.xAPI.TinCanHelperClasses import TinCanBaseSerializable

class TinCanAccount(TinCanBaseSerializable):
    """ An account in Tin Can"""
    
    def __init__(self, name=None, homepage=None, anId=None):
        super(TinCanAccount, self).__init__(anId)
        self._name = name
        self._homepage = homepage

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    def getHomePage(self):
        return self._homepage

    def setHomePage(self, value):
        self._homepage = value

    def tinCanSerialize(self):
        return self._tinCanOutput([("homePage", self._homepage),
                                   ("name", self._name)])

    
class TinCanInverseFunctionalID(TinCanBaseSerializable):
    """ A unique ID for an agent in Tin Can API """
    CLASS_ID = "InverseFunctionalID"
    
    ACCOUNT_TYPE = "account"
    MBOX_TYPE = "mbox"
    MBOX_SHA1_TYPE = "mbox_sha1sum"
    OPEN_ID_TYPE = "openID"
    FID_TYPES = frozenset([ACCOUNT_TYPE, MBOX_TYPE, MBOX_SHA1_TYPE, OPEN_ID_TYPE])
    
    def __init__(self, value=None, idType=ACCOUNT_TYPE, anId=None):
        super(TinCanInverseFunctionalID, self).__init__(anId)
        self._idType = idType
        self._value = value

    def getType(self):
       return self._idType

    def getValue(self):
        return self._value

    def setFID(self, value, idType=ACCOUNT_TYPE):
        self._idType = idType
        self._value = value

    def tinCanSerialize(self):
        if self._idType == self.ACCOUNT_TYPE:
            return '"%s":"%s"'%(self._idType, self._value.tinCanSerialize())
        else:
            return '"%s":"%s"'%(self._idType, self._value)


class TinCanAgent(TinCanBaseSerializable):
    """ An Agent in the Tin Can API system """
    
    def __init__(self, inverseFID=None, name=None, objectType=None, anId=None):
        super(TinCanAgent, self).__init__(anId)
        self._fid = inverseFID
        self._objectType = objectType
        self._name = name

    def getFID(self):
        return self._fid

    def getFIDType(self):
        if self._fid is None:
            return None
        else:
            return self._fid.getType()        

    def getFIDValue(self):
        if self._fid is None:
            return None
        else:
            return self._fid.getValue()

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    def getObjectType(self):
        return self._objectType

    def setObjectType(self, value):
        self._objectType = value

    def tinCanSerialize(self):
        return self._tinCanOutput([self._fid,
                                   ("objectType", self._objectType),
                                   ("name", self._name)])
