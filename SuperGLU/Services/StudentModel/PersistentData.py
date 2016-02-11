import datetime
from gludb.simple import DBObject, Field, Index
from SuperGLU.Services.QueryService.Queries import getKCsForAGivenUserAndTask, getAllHintsForSingleUserAndTask, getAllFeedbackForSingleUserAndTask
"""
"""

@DBObject(table_name="Systems")
class System(object):
    uuid              = Field('00000000-0000-0000-0000-000000000000')
    ids               = Field(list)
    name              = Field('')
    contactEmails     = Field(list)
    description       = Field('')
    metadata          = Field(dict)
    tasks             = Field(list)
    baseURL           = Field('')
    authoringURL      = Field('')
    taskListURL       = Field('')
    deliveryURL       = Field('')
    authenticationURL = Field('')
    
    def __repr__(self):
        return self.uuid + "|" + str(self.ids) + "|" + self.name + "|" + str(self.contactEmails) + "|" + self.description + "|" + str(self.metadata) + "|" + str(self.tasks) + "|" + self.baseURL + "|" + self.authoringURL + "|" + self.taskListURL + "|" + self.deliveryURL + "|" + self.authenticationURL

    
@DBObject(table_name="Tasks")
class Task(object):
    ids  = Field(list)
    name = Field('')
    kcs  = Field(list)
    url  = Field('')
    
    def __repr__(self):
        return str(self.ids) + "|" + self.name + "|" + str(self.kcs) + "|" + self.url
        
        
        
@DBObject(table_name="Topics")
class Topic(object):
    kcList       = Field(list)
    resourceList = Field(list)
    
    def __repr__(self):
        return str(self.kcList) + "|" + str(self.resourceList)
        

@DBObject(table_name="Sessions")
class Session(object):
    students       = Field(list)
    system         = Field('')
    task           = Field('')
    startTime      = Field('')
    duration       = Field(-1.0)
    endCondition   = Field('')
    performance    = Field(dict)
    classId        = Field('')
    hints          = Field(list)
    feedback       = Field(list)
    messageIds     = Field(list)
    sourceDataN    = Field(-1)
    sourceDataHash = Field(-1)
    
    
    def setStartTime(self, sTime):
        self.startTime = sTime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
    def getStartTime(self):
        if(self.startTime != ''):
            return datetime.strptime(self.startTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            
        return None
        
    def getPerformance(self, useCachedValue = False):
        if useCachedValue:
            return self.performance
        
        self.performance = dict()
        
        if self.task is None or self.startTime is None:
            return self.performance
        
        for currentStudent in self.students:
            self.performance[currentStudent] = dict()
            kcList = getKCsForAGivenUserAndTask(currentStudent, self.task, self.startTime, False)
            for kcMessage in kcList:
                self.performance[currentStudent][kcMessage.object] = kcMessage.result
                if kcMessage.id not in self.messageIds:
                    self.messageIds.append(kcMessage.id)
        
        return self.performance
        
    def getHints(self, useCachedValue = False):
        if useCachedValue:
            return self.hints
        else:
            self.hints = list()
            
            if self.task is None or self.startTime is None:
                return self.hints
                
            for currentStudent in self.students:
                studentHints = getAllHintsForSingleUserAndTask(currentStudent, self.task, self.startTime, False)
                for currentHint in studentHints:         
                    self.hints.append(currentHint)
                    if currentHint.id not in self.messageIds:
                        self.messageIds.append(currentHint)
            return self.hints
            
    def getFeedback(self, useCachedValue = False):
        if useCachedValue:
            return self.feedback
        else:
            self.feedback = list()
            
            if self.task is None or self.startTime is None:
                return self.feedback
                
            for currentStudent in self.students:
                studentFeedback = getAllFeedbackForSingleUserAndTask(currentStudent, self.task, self.startTime, False)
                for currentFeedback in studentFeedback:         
                    self.feedback.append(currentFeedback)
                    if currentFeedback.id not in self.messageIds:
                        self.messageIds.append(currentFeedback)
            return self.feedback
            
            
    def getSourceDataN(self, useCachedValue = False):
        if useCachedValue:
            return self.sourceDataN
        else:
            self.sourceDataN = len(self.messageIds)
            return self.sourceDataN