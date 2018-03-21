# -*- coding: utf-8 -*-
from abc import abstractmethod
from SuperGLU.Util.Serialization import SuperGlu_Serializable

class TinCanBaseSerializable(SuperGlu_Serializable):
    """ Base class for tin can serializables """

    @abstractmethod
    def tinCanSerialize(self):
        raise NotImplementedError

    @classmethod
    def _tinCanOutput(cls, members):
        """ Generate Tin Can API output for members """
        tinCanSerialized = []
        for x in members:
            if isinstance(x, TinCanBaseSerializable):
                x = x.tinCanSerialize()
                tinCanSerialized.append(x)
            elif len(x) == 2 and x[1] is not None:
                if isinstance(x[1], TinCanBaseSerializable):
                    x = '"%s":%s'%(x[0], x[1].tinCanSerialize())
                else:
                    x = '"%s":"%s"'%(x[0], x[1])
                tinCanSerialized.append(x)
        return "{%s}"%",".join(tinCanSerialized)


class TinCanLanguageMap(TinCanBaseSerializable):

    def __init__(self, aMap=None, anId=None):
        super(TinCanLanguageMap, self).__init__(anId)
        if aMap is None: aMap = {}
        self._map = aMap

    def getValue(self, key):
        return self._map[key]

    def setValue(self, key, value):
        self._map[key] = value
