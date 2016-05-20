'''
Created on May 18, 2016
This Module contains the service for handling the initial receipt of iCal strings from a client
The strings are converted to serializable objects and sent off to the GLUDB storage service to be stored.
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Core.FIPA.SpeechActs import INFORM_ACT
from SuperGLU.Core.MessagingDB import ELECTRONIX_TUTOR_UPLOAD_VERB
from SuperGLU.Util.ErrorHandling import logInfo


ICAL_READER_SERVICE_NAME = "iCalReader"

ICAL_OBJECT_TYPE = "iCalendar"

class ICalReader(BaseService):

    """
    message format for loading calendars: 
    actor = className
    verb = electronixTutorUploadVerb
    object = "calendar"
    result = iCal data
    """

    def receiveMessage(self, msg):
        if msg.getSpeechAct() == INFORM_ACT:
            if msg.getVerb() == ELECTRONIX_TUTOR_UPLOAD_VERB:
                logInfo('{0} is processing a {1},{2} message'.format(ICAL_READER_SERVICE_NAME, ELECTRONIX_TUTOR_UPLOAD_VERB, INFORM_ACT), 4)
                