# -*- coding: utf-8 -*-
from SuperGLU.Core.xAPI.TinCanHelperClasses import TinCanBaseSerializable

class TinCanVerb(TinCanBaseSerializable):

    def __init__(self, verbId=None, display=None):
        if display is None: display = {}
        self._verbId = verbId
        self._display = display
        
