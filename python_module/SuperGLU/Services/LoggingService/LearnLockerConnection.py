'''
Created on May 31, 2018
This service will forward logging messages to LearnLocker as well as log them to a file.
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Constants import XAPI_LOG_VERB
import requests
import uuid


class LearnLockerConnection(BaseService):

    def __init__(self, gateway, url, key):
        super(LearnLockerConnection, self).__init__(gateway=gateway)
        self._url = url
        self._key = key

        self.logFile = open("log.txt", 'w')



    def receiveMessage(self, msg):
        super(LearnLockerConnection, self).receiveMessage(msg)

        if msg.getVerb() == XAPI_LOG_VERB:
            statementAsJson = msg.getResult()
            headerDict = {'Authorization' : self._key,\
                       'X-Experience-API-Version': '1.0.3',\
                       'Content-Type' : 'application/json',\
                      }
            response = requests.put(url=self._url + '/data/xAPI/statements?statementId=' + str(uuid.uuid4()), data=statementAsJson, headers=headerDict )
            print(str(response))

            self.logFile.write(statementAsJson)
