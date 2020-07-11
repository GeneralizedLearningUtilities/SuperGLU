'''
Created on May 31, 2018
This service will forward logging messages to LearnLocker (if url and key are not None) as well as log them to a file.
@author: Daniel Auerbach, Alicia Tsai
'''
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.LoggingService.Constants import XAPI_LOG_VERB
import requests
import uuid
import json
from tincan import statement_list
from tincan.statement import Statement
from tincan.statement_list import StatementList
#import statement


class LearnLockerConnection(BaseService):

    def __init__(self, gateway, url, key):
        super(LearnLockerConnection, self).__init__(gateway=gateway)
        self._url = url
        self._key = key
        self.logFile = open(r"log.txt", 'w')
        self.errorLog = open(r"errorLog.txt", "w")
        self.statements = StatementList()

    def receiveMessage(self, msg):
        super(LearnLockerConnection, self).receiveMessage(msg)

        if msg.getVerb() == XAPI_LOG_VERB:
            statementAsJson = msg.getResult()
            self.statements.append(Statement.from_json(statementAsJson))
            headerDict = {'Authorization' : self._key,
                          'X-Experience-API-Version': '1.0.3',
                          'Content-Type' : 'application/json'
                          }
            
            if self.statements.__len__() == 1000:
                if self._url != None:
                    response = requests.post(url=self._url + '/data/xAPI/statements', data=self.statements.to_json(), headers=headerDict)
                    
                    #pass

                    # log bad request message into errorLog file
                    if str(response) == "<Response [400]>":
                        print('Warning: ', str(response), response.text)
                        self.errorLog.write(response.text)
                        self.errorLog.write("\n")
                        
                    self.statements = StatementList()

                # write xAPI statement to log file
            self.logFile.write(statementAsJson)
            self.logFile.write("\n")
