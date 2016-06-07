'''
Created on Jun 2, 2016

@author: auerbach
'''
import unittest
from SuperGLU.Services.StudentModel.PersistentData import DBCalendarData, STUDENT_OWNER_TYPE, PUBLIC_PERMISSION, DBTask
from SuperGLU.Services.iCalReader.iCalReader import ICalReader
from icalendar.cal import Calendar


class CalendarTest(unittest.TestCase):

    calendarData = None
    icalReader = None
    dummyTask = None

    def setUp(self):
        self.icalReader = ICalReader()
        
        self.calendarData = DBCalendarData()
        self.calendarData.ownerId = 'dummyOwner'
        self.calendarData.ownerType = STUDENT_OWNER_TYPE
        self.calendarData.accessPermissions = PUBLIC_PERMISSION
        self.calendarData.calendarData = Calendar().to_ical()
        
        self.dummyTask = DBTask()
        self.dummyTask.displayName = "dummyTaskDisplayName"
        self.dummyTask.name = "dummyTaskName"
        self.dummyTask.taskId = "dummyTaskId"
        
       


    def tearDown(self):
        pass


    def testAddTaskToCalendar(self):
        startTime = "2016-06-02T12:00:00.0000Z"
        self.icalReader.addTaskToCalendar(self.dummyTask, self.calendarData, startTime)
        print(self.calendarData.calendarData)
        self.assertEqual(b'BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nSUMMARY:dummyTaskDisplayName\r\nDTSTART;VALUE=DATE-TIME:20160602T120000\r\nCOMMENT:taskId = dummyTaskId\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n', self.calendarData.calendarData)

    def testAddTaskWithEndTime(self):
        startTime = "2016-06-02T12:00:00.0000Z"
        endTime = "2016-06-02T14:00:00.0000Z"
        self.icalReader.addTaskToCalendar(self.dummyTask, self.calendarData, startTime, endTime)
        print(self.calendarData.calendarData)
        self.assertEqual(b'BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nSUMMARY:dummyTaskDisplayName\r\nDTSTART;VALUE=DATE-TIME:20160602T120000\r\nDTEND;VALUE=DATE-TIME:20160602T140000\r\nCOMMENT:taskId = dummyTaskId\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n', self.calendarData.calendarData)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'CalendarTest.testAddTaskToCalendar']
    unittest.main()