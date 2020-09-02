'''
Created on Jul 27, 2020

@author: auerbach
'''
from SuperGLU.Core.MessagingGateway import BaseService
from tincan.statement_list import StatementList
from SuperGLU.Services.LoggingService.Constants import XAPI_FLUSH_LOGGER_VERB,\
    XAPI_LOG_VERB, XAPI_FILE_FINISHED_VERB
from tincan.statement import Statement

class XAPIFileWriter(BaseService):

    def __init__(self, gateway):
        super(XAPIFileWriter, self).__init__(gateway=gateway)
        self.currentFile = None
        self.logFile = open(r"log.txt", 'w')
        self.errorLog = open(r"errorLog.txt", "w")
        self.statements = StatementList()

    def receiveMessage(self, msg):
        super(XAPIFileWriter, self).receiveMessage(msg)

        if msg.getVerb() == XAPI_FILE_FINISHED_VERB:
            fileName = msg.getObject()
            f = open("D:/Data/TF2XAPILogs/" + fileName, "w")
            f.write(self.statements.to_json())
            f.close()                
            self.statements = StatementList()

        if msg.getVerb() == XAPI_LOG_VERB:
            statementAsJson = msg.getResult()
            self.statements.append(Statement.from_json(statementAsJson))
            