# -*- coding: utf-8 -*-
from SKO_Architecture.xAPI.TinCanHelperClasses import TinCanBaseSerializable

class TinCanVerb(TinCanBaseSerializable):

    def __init__(self, verbId=None, display=None):
        if display is None: display = {}
        self._verbId = verbId
        self._display = display
        
