"""
A class for dumping data about a student into an object,
which can then be merged across multiple copies of the same
student, assuming that the same data does not already exist
in both copies.
"""
import csv
import re
import sys
from datetime import datetime, timedelta

from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT, SPEECH_ACT_SET
from SuperGLU.Messaging import Message
from SuperGLU.MessagingGateway import BaseService
from SuperGLU.Util.Serialization import nativizeObject, makeNative


class StudentData(object):
    def __init__(self, anId, properties=None, events=None):
        """
        @param properties: Properties is a generic key-value pair
        @param events: A list of SKO Message instances
        """
        if properties is None: properties = {}
        if events is None: events = []
        self._id = anId
        self._properties = dict([(k, v) for k, v in properties.items() if k !=''])
        self._events = events

    def getId(self):
        return self._id

    def addCalculatedProperty(self, name, function, allowReplace=False):
        if allowReplace or name not in self._properties:
            value = function(self._properties, self._events)
            self._properties[name] = value

    def getProperty(self, name):
        return self._properties[name]

    def getPropertyNames(self):
        return self._properties.keys()

    def merge(self, other, errorOnConflict=True):
        #print 'merge called for ' +str(self._id)+ ' and ' + str(other._id)
        if type(self) != type(other):
            raise TypeError("Cannot merge student data with raw data")
        if self._id != other._id:
            raise KeyError("Data was for different students, could not merge")
        x = StudentData(self._id, dict(self._properties), list(self._events))
        for k, v in other._properties.items():
            if k in x._properties and v != x._properties[k] and errorOnConflict:
                raise ValueError("Duplicate value for key: %s\nGot: %s\nvs.: %s"%(k, v, x._properties[k]))
            x._properties[k] = v
        allEvents = [] + x._events + other._events
        allEvents = [(e.getTimestamp(), e) for e in allEvents]
        allEvents.sort()
        allEvents = [e for (t, e) in allEvents]
        x._events = allEvents
        return x

    def dumpPropertyRow(self, cols=None, idCol='id'):
        if cols is None:
            cols = [idCol] + sorted([k for k in self._properties.keys() if k != idCol])
        return [self.getId()] + [self._properties.get(k, None) for k in cols[1:]]

    def getEvents(self, aFilter=None):
        return [evt for evt in self._events if aFilter is None or aFilter(evt)]
