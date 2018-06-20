'''
Created on May 31, 2018
This service will forward logging messages to LearnLocker as well as log them to a file.
@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Constants import XAPI_LOG_VERB
import requests
import uuid
import json


class LearnLockerConnection(BaseService):

    def __init__(self, gateway, url, key):
        super(LearnLockerConnection, self).__init__(gateway=gateway)
        self._url = url
        self._key = key
        self.logFile = open("log.txt", 'w')
        self.errorLog = open("errorLog.txt", "w")

    def receiveMessage(self, msg):
        super(LearnLockerConnection, self).receiveMessage(msg)

        if msg.getVerb() == XAPI_LOG_VERB:
            statementAsJson = msg.getResult()
            headerDict = {'Authorization' : self._key,
                          'X-Experience-API-Version': '1.0.3',
                          'Content-Type' : 'application/json'
                          }
            statement = json.loads(statementAsJson)
            statement['context']['extensions'] = {}
            statement['object']['id'] = "http://example.com/activities/solo-hang-gliding"
            statement['actor'].pop('openid', None)
            response = requests.put(url=self._url + '/data/xAPI/statements?statementId=' + str(uuid.uuid4()), data=json.dumps(statement), headers=headerDict)
            if str(response) == "<Response [400]>":
                print(str(response), response.text)
                self.errorLog.write(response.text)
                self.errorLog.write("\n")
            #response.raise_for_status()

            # write to log file
            self.logFile.write(statementAsJson)
            self.logFile.write("\n")
