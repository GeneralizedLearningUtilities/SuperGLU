import unittest
import uuid
from random import random
from Queue import Queue
from SKO_Architecture.Services.TaskManager import (RequirementMap, TaskDispatcher,
    TaskSpecification,)

class SumMethod(object):
    def __init__(self):
        self._x = None
    def __call__(self, **kwds):
        self._x = sum(kwds.values())

class DummyMessage(object):
    def __init__(self, req, result=0):
        self._req = req
        self._result = result
    def getRequest(self):
        return self._req
    def getResult(self):
        return self._result

class RequirementMapTest(unittest.TestCase):

    FACTORY = None

    def setUp(self):
        self._req1 = "Req1"
        self._req2 = "Req2"
        self._args = {"A" : 10, "B" : 20}
        self._reqs = {"C" : self._req1, "D" : self._req2}
        self._reqValues = {self._req1: -5, self._req2 : -10}
        self._emptyTask = TaskSpecification(SumMethod())
        self._taskWArgs = TaskSpecification(SumMethod(), self._args)
        self._taskWReqs = TaskSpecification(SumMethod(), reqs=self._reqs)
        self._taskWBoth = TaskSpecification(SumMethod(), self._args, self._reqs)
        self._tasks = [self._emptyTask, self._taskWArgs, self._taskWReqs, self._taskWBoth]
        self._factory = self.FACTORY
        self._emptyMap = RequirementMap()
        self._mapWithTasks = RequirementMap()
        for task in self._tasks:
            self._mapWithTasks.addTask(task.getId(), task.getRequirements())

    def test__init__(self):
        pass

    def test_makeMap(self):
        self.assertEqual(self._emptyMap._makeMap(), {})

    def test_makeSet(self):
        self.assertEqual(self._emptyMap._makeSet(), set())

    def testAddTask_Empty(self):
        task = self._emptyTask
        taskId = task.getId()
        reqMap = self._emptyMap
        self.assertEqual(len(reqMap._taskReqs), 0)
        self.assertEqual(len(reqMap._tasksByReq), 0)
        self.assertEqual(len(reqMap._reqValues), 0)
        self.assertItemsEqual(reqMap.addTask(task.getId(), task.getRequirements()), set())
        self.assertEqual(len(reqMap._taskReqs), 1)
        self.assertIn(taskId, reqMap._taskReqs)
        self.assertItemsEqual(set([]), reqMap._taskReqs[taskId])
        self.assertEqual(len(reqMap._tasksByReq), 0)
        self.assertEqual(len(reqMap._reqValues), 0)

    def testAddTask_WithReqs(self):
        task = self._taskWReqs
        taskId = task.getId()
        reqMap = self._emptyMap
        self.assertEqual(len(reqMap._taskReqs), 0)
        self.assertEqual(len(reqMap._tasksByReq), 0)
        self.assertEqual(len(reqMap._reqValues), 0)
        self.assertItemsEqual(reqMap.addTask(task.getId(), task.getRequirements()),
                              set(task.getRequirements()))
        self.assertEqual(len(reqMap._taskReqs), 1)
        self.assertIn(taskId, reqMap._taskReqs)
        self.assertItemsEqual(set(self._reqs.values()), reqMap._taskReqs[taskId])
        self.assertEqual(len(reqMap._tasksByReq), 2)
        for req in self._reqs.values():
            self.assertEqual(reqMap._tasksByReq[req], set([taskId]))
        self.assertEqual(len(reqMap._reqValues), 0)

    def testAddTask_Duplicate(self):
        task = self._emptyTask
        taskId = task.getId()
        reqMap = self._emptyMap
        reqMap.addTask(taskId, task.getRequirements())
        self.assertEqual(len(reqMap._taskReqs), 1)
        reqMap.addTask(taskId, task.getRequirements())
        self.assertEqual(len(reqMap._taskReqs), 1)
        self.assertRaises(KeyError, reqMap.addTask, taskId, task.getRequirements(),
                          errorOnDuplicate=True)
        self.assertEqual(len(reqMap._taskReqs), 1)

    def testClear(self):
        pass

    def testGetRequirementsForTask(self):
        task = self._taskWReqs
        self.assertRaises(KeyError, self._emptyMap.getRequirementsForTask, task.getId())
        self.assertItemsEqual(self._mapWithTasks.getRequirementsForTask(task.getId()),
                              self._taskWReqs.getRequirements())

    def testGetTaskRequirementValues(self):
        reqMap = self._mapWithTasks
        taskId = self._taskWReqs.getId()
        reqValues = self._reqValues
        self.assertRaises(KeyError, reqMap.getTaskRequirementValues, taskId)
        for req, val in reqValues.items():
            reqMap.setRequirementValue(req, val)
        self.assertItemsEqual(reqMap.getTaskRequirementValues(taskId), reqValues)

    def testSetRequirementValue(self):
        reqMap = self._mapWithTasks
        taskId = self._taskWReqs.getId()
        reqValues = self._reqValues
        for req, val in reqValues.items():
            self.assertNotIn(req, reqMap._reqValues)
            reqMap.setRequirementValue(req, val)
            self.assertEqual(reqMap._reqValues[req], val)

    def testGetTasksWithRequirement(self):
        reqMap = self._mapWithTasks
        reqValues = self._reqValues
        tasksWithReqs = [self._taskWReqs.getId(), self._taskWBoth.getId()]
        for req in reqValues:
            self.assertItemsEqual(reqMap.getTasksWithRequirement(req), tasksWithReqs)

    def testGetTasksWithRequirement_Empty(self):
        reqMap = self._emptyMap
        reqValues = self._reqValues
        for req in reqValues:
            self.assertItemsEqual(reqMap.getTasksWithRequirement(req), set())

    def testIsTaskReady(self):
        reqMap = self._mapWithTasks
        reqValues = self._reqValues
        tasksWithReqs = [self._taskWReqs.getId(), self._taskWBoth.getId()]
        for task in self._tasks:
            taskId = task.getId()
            if taskId in tasksWithReqs:
                self.assertFalse(reqMap.isTaskReady(taskId))
            else:
                self.assertTrue(reqMap.isTaskReady(taskId))

    def testRemoveTask(self):
        reqMap = self._mapWithTasks
        reqValues = self._reqValues
        reqMap.setRequirementValue(self._req1, reqValues[self._req1])
        reqMapValues = {self._req1: reqValues[self._req1]}
        task1Id = self._taskWReqs.getId()
        task2Id = self._taskWBoth.getId()
        tasksWithReqs = [task1Id, task2Id]
        for req in reqValues:
            self.assertItemsEqual(reqMap.getTasksWithRequirement(req), tasksWithReqs)
            self.assertItemsEqual(reqMap.fillRequirements(reqValues.keys()), reqMapValues)
        reqMap.removeTask(task1Id)
        for req in reqValues:
            self.assertItemsEqual(reqMap.getTasksWithRequirement(req), [task2Id])
            self.assertItemsEqual(reqMap.fillRequirements(reqValues.keys()), reqMapValues)
        reqMap.removeTask(task2Id)
        for req in reqValues:
            self.assertItemsEqual(reqMap.getTasksWithRequirement(req), set())
            self.assertItemsEqual(reqMap.fillRequirements(reqValues.keys()), {})

    def testFillRequirements(self):
        reqMap = self._mapWithTasks
        reqValues = self._reqValues
        self.assertItemsEqual(reqMap.fillRequirements(reqValues.keys()), {})
        for req, val in reqValues.items():
            reqMap.setRequirementValue(req, val)
        self.assertItemsEqual(reqMap.fillRequirements(reqValues.keys()), reqValues)


class TaskDispatcherTest(unittest.TestCase):

    FACTORY = None

    def setUp(self):
        self._factory = self.FACTORY
        # Available Tasks
        self._req1 = "Req1"
        self._req2 = "Req2"
        self._req3 = "Req3"
        self._args = {"A" : 10, "B" : 20}
        self._reqs = {"C" : self._req1, "D" : self._req2}
        self._otherReqs = {"E" : self._req3}
        self._emptyTask = TaskSpecification(SumMethod())
        self._singleReqTask = TaskSpecification(SumMethod(), reqs=self._otherReqs)
        self._taskWReqs = TaskSpecification(SumMethod(), reqs=self._reqs)
        self._taskWBoth = TaskSpecification(SumMethod(), self._args, self._reqs)
        self._tasks = [self._emptyTask, self._singleReqTask, self._taskWReqs, self._taskWBoth]
        # Messages
        self._dummyMessage = DummyMessage(self._req3, 100)
        self._req1Message = DummyMessage(self._req1, -5)
        self._req2Message = DummyMessage(self._req2, 10)
        self._req3Message = self._dummyMessage
        # Task Managers
        self._emptyDispatcher = TaskDispatcher(None, self._factory)
        self._dispatcherWTasks = TaskDispatcher(self._tasks, self._factory)

    def test__init__(self):
        pass

    def testClear(self):
        pass

    def test_makeMap(self):
        self.assertEqual(self._emptyDispatcher._makeMap(), {})

    def test_makeQueue(self):
        self.assertIsInstance(self._emptyDispatcher._makeQueue(), Queue)

    def test_makeRequirementMap(self):
        self.assertIsInstance(self._emptyDispatcher._makeRequirementMap(), RequirementMap)

    def testGetTask(self):
        task = self._emptyTask
        taskId = task.getId()
        self.assertRaises(KeyError, self._emptyDispatcher.getTask, taskId)
        self.assertEqual(self._dispatcherWTasks.getTask(taskId), task)

    def testAddTask_NoReqs(self):
        task = self._emptyTask
        dispatcher = self._emptyDispatcher
        self.assertTrue(dispatcher._readyTasks.empty())
        self.assertTrue(dispatcher._newRequirements.empty())
        self.assertRaises(KeyError, dispatcher.getTask, task.getId())
        # Add a task
        dispatcher.addTask(task)
        self.assertFalse(dispatcher._readyTasks.empty())
        self.assertTrue(dispatcher._newRequirements.empty())
        self.assertEqual(dispatcher.getTask(task.getId()), task)
        # Add same task again
        dispatcher.addTask(task)
        self.assertRaises(KeyError, dispatcher.addTask, task, errorOnDuplicate=True)

    def testAddTask_WReqs(self):
        task = self._taskWReqs
        dispatcher = self._emptyDispatcher
        self.assertTrue(dispatcher._readyTasks.empty())
        self.assertTrue(dispatcher._newRequirements.empty())
        self.assertRaises(KeyError, dispatcher._requirementMap.getRequirementsForTask,
                          task.getId())
        self.assertRaises(KeyError, dispatcher.getTask, task.getId())
        # Add a task
        dispatcher.addTask(task)
        self.assertTrue(dispatcher._readyTasks.empty())
        self.assertFalse(dispatcher._newRequirements.empty())
        self.assertItemsEqual(dispatcher._requirementMap.getRequirementsForTask(task.getId()),
                              task.getRequirements())
        self.assertEqual(dispatcher.getTask(task.getId()), task)
        # Add same task again
        dispatcher.addTask(task)
        self.assertRaises(KeyError, dispatcher.addTask, task, errorOnDuplicate=True)
        # Pop Requirements to Check them
        newReqs = []
        while not dispatcher._newRequirements.empty():
            newReqs.append(dispatcher._newRequirements.get())
        self.assertItemsEqual(newReqs, self._reqs.values())

    def test_dispatchNextTask_NoTasks(self):
        dispatcher = self._emptyDispatcher
        dispatcher._dispatchNextTask()

    def test_dispatchNextTask_SingleTask(self):
        task = self._emptyTask
        dispatcher = self._emptyDispatcher
        dispatcher.addTask(task)
        self.assertIsNone(self._emptyTask._method._x, None)
        dispatcher._dispatchNextTask()
        self.assertEqual(task._method._x, 0)

    def test_dispatchNextTask_TwoTasks(self):
        dispatcher = self._emptyDispatcher
        dispatcher.addTask(self._singleReqTask)
        dispatcher.addTask(self._emptyTask)
        self.assertIsNone(self._emptyTask._method._x, None)
        self.assertIsNone(self._singleReqTask._method._x, None)
        # Dispatch empty-req task
        dispatcher._dispatchNextTask()
        self.assertEqual(self._emptyTask._method._x, 0)
        self.assertIsNone(self._singleReqTask._method._x, None)
        # No change since next task is not ready
        dispatcher._dispatchNextTask()
        self.assertEqual(self._emptyTask._method._x, 0)
        self.assertIsNone(self._singleReqTask._method._x, None)
        # Add a message
        dummyMessage = self._dummyMessage
        dispatcher.receiveRequirement(dummyMessage)
        dispatcher._processNextReceivedRequirement()
        dispatcher._dispatchNextTask()
        self.assertEqual(self._emptyTask._method._x, 0)
        self.assertEqual(self._singleReqTask._method._x, 100)

    # Messages
    def testMakeCanonicalMessage(self):
        # Not implemented yet
        pass

    def testIsValidRequirementMessage(self):
        # Not implemented yet
        pass

    def test_sendNextRequirement(self):
        # Not implemented yet
        pass

    def testReceiveRequirement(self):
        dispatcher = self._emptyDispatcher
        dispatcher.receiveRequirement(self._dummyMessage)
        self.assertTrue(dispatcher.doAction())
        self.assertFalse(dispatcher.doAction())

    def test_processNextReceivedRequirement_NoMatches(self):
        dispatcher = self._emptyDispatcher
        dispatcher.receiveRequirement(self._dummyMessage)
        dispatcher._processNextReceivedRequirement()

    def test_processNextReceivedRequirement_OneMatch(self):
        dispatcher = self._dispatcherWTasks
        dispatcher.receiveRequirement(self._dummyMessage)
        self.assertEqual(dispatcher._readyTasks.qsize(), 1)
        dispatcher._processNextReceivedRequirement()
        self.assertEqual(dispatcher._readyTasks.qsize(), 2)

    def test_processNextReceivedRequirement_TwoMatches(self):
        dispatcher = self._dispatcherWTasks
        dispatcher.receiveRequirement(self._req1Message)
        dispatcher.receiveRequirement(self._req2Message)
        self.assertEqual(dispatcher._readyTasks.qsize(), 1)
        dispatcher._processNextReceivedRequirement()
        self.assertEqual(dispatcher._readyTasks.qsize(), 1)
        dispatcher._processNextReceivedRequirement()
        self.assertEqual(dispatcher._readyTasks.qsize(), 3)

    # Execution
    def testDoAction(self):
        dispatcher = self._dispatcherWTasks
        # 4 Tasks: One with no reqs, one with Req3, and two with Req1 and Req2
        self.assertEquals(dispatcher.SEND_REQUIREMENT_ACTION, dispatcher.doAction())
        dispatcher.receiveRequirement(self._req1Message)
        self.assertEquals(dispatcher.SEND_REQUIREMENT_ACTION, dispatcher.doAction())
        self.assertEquals(dispatcher.SEND_REQUIREMENT_ACTION, dispatcher.doAction())
        self.assertEquals(dispatcher.DISPATCHED_TASK_ACTION, dispatcher.doAction())
        self.assertEquals(self._emptyTask._method._x, 0)
        self.assertEquals(dispatcher.PROCESSED_REQ_ACTION, dispatcher.doAction())
        self.assertIsNone(dispatcher.doAction())
        self.assertIsNone(dispatcher.doAction())
        self.assertIsNone(dispatcher.doAction())
        dispatcher.receiveRequirement(self._req3Message)
        self.assertEquals(dispatcher.PROCESSED_REQ_ACTION, dispatcher.doAction())
        self.assertEquals(dispatcher.DISPATCHED_TASK_ACTION, dispatcher.doAction())
        self.assertEquals(self._singleReqTask._method._x, 100)
        self.assertIsNone(dispatcher.doAction())
        dispatcher.receiveRequirement(self._req2Message)
        self.assertEquals(dispatcher.PROCESSED_REQ_ACTION, dispatcher.doAction())
        self.assertEquals(dispatcher.DISPATCHED_TASK_ACTION, dispatcher.doAction())
        self.assertEquals(dispatcher.DISPATCHED_TASK_ACTION, dispatcher.doAction())
        # No guarrantee of order: Depends on when reqs arrive
        self.assertEquals(self._taskWReqs._method._x, 5)
        self.assertEquals(self._taskWBoth._method._x, 35)
        self.assertIsNone(dispatcher.doAction())

    def testRun(self):
        dispatcher = self._dispatcherWTasks
        dispatcher.run()
        self.assertEquals(self._emptyTask._method._x, 0)
        self.assertIsNone(self._singleReqTask._method._x)
        self.assertIsNone(self._taskWReqs._method._x)
        self.assertIsNone(self._taskWBoth._method._x)
        # Fill Req1
        dispatcher.receiveRequirement(self._req1Message)
        dispatcher.run()
        self.assertEquals(self._emptyTask._method._x, 0)
        self.assertIsNone(self._singleReqTask._method._x)
        self.assertIsNone(self._taskWReqs._method._x)
        self.assertIsNone(self._taskWBoth._method._x)
        # Fill Req1 (Again) and Req2
        dispatcher.receiveRequirement(self._req1Message)
        dispatcher.receiveRequirement(self._req2Message)
        dispatcher.run()
        self.assertEquals(self._emptyTask._method._x, 0)
        self.assertIsNone(self._singleReqTask._method._x)
        self.assertEquals(self._taskWReqs._method._x, 5)
        self.assertEquals(self._taskWBoth._method._x, 35)
        # Fill Req3
        dispatcher.receiveRequirement(self._req3Message)
        dispatcher.run()
        self.assertEquals(self._emptyTask._method._x, 0)
        self.assertEquals(self._singleReqTask._method._x, 100)
        self.assertEquals(self._taskWReqs._method._x, 5)
        self.assertEquals(self._taskWBoth._method._x, 35)
        # Add Task 3 Again (Should no longer be in system)
        dispatcher.addTask(self._singleReqTask)
        self._singleReqTask._method(**{"Z":19})
        self._singleReqTask.resetStatus()
        dispatcher.run()
        self.assertEquals(self._singleReqTask._method._x, 19)
        dispatcher.receiveRequirement(self._req3Message)
        dispatcher.run()
        self.assertEquals(self._singleReqTask._method._x, 100)


class TaskSpecificationTest(unittest.TestCase):

    class DummyException(Exception): pass

    def setUp(self):
        self._taskId = uuid.uuid4()
        self._req1 = "Req1"
        self._req2 = "Req2"
        self._args = {"A" : 10, "B" : 20}
        self._reqs = {"C" : self._req1, "D" : self._req2}
        self._reqValues = {self._req1: -5, self._req2 : -10}
        self._emptyTask = TaskSpecification(SumMethod())
        self._taskWithId = TaskSpecification(SumMethod(), taskId=self._taskId)
        self._taskWithArgs = TaskSpecification(SumMethod(), self._args,
                                               taskId=self._taskId)
        self._taskWithReqs = TaskSpecification(SumMethod(), reqs=self._reqs,
                                               taskId=self._taskId)
        self._taskWithBoth = TaskSpecification(SumMethod(), self._args,
                                               self._reqs, self._taskId)
        self._tasks = [self._emptyTask, self._taskWithId, self._taskWithArgs,
                       self._taskWithReqs, self._taskWithBoth]

    def test__init__(self):
        self.assertIsInstance(TaskSpecification(SumMethod()), TaskSpecification)

    def test__call__Empty(self):
        task = self._emptyTask
        task()
        actualValue = task._method._x
        self.assertEqual(actualValue, 0)

    def test__call__WithId(self):
        task = self._taskWithId
        task()
        actualValue = task._method._x
        self.assertEqual(actualValue, 0)

    def test__call__WithArgs(self):
        task = self._taskWithArgs
        expectedVal = sum(self._args.values())
        task()
        actualValue = task._method._x
        self.assertEqual(actualValue, expectedVal)

    def test__call__WithArgsDuplicated(self):
        task = self._taskWithArgs
        expectedVal = sum(self._args.values())
        dummyReqs = dict([(key, random()) for key in self._args])
        task(dummyReqs)
        actualValue = task._method._x
        self.assertEqual(actualValue, expectedVal)

    def test__call__WithReqs(self):
        task = self._taskWithReqs
        expectedVal = sum(self._reqValues.values())
        task(self._reqValues)
        actualValue = task._method._x
        self.assertEqual(actualValue, expectedVal)

    def test__call__MissingReqs(self):
        task = self._taskWithReqs
        expectedVal = sum(self._reqValues.values())
        self.assertRaises(KeyError, task)
        self.assertRaises(KeyError, task, {"GARBAGE_REQ" : 1})

    def test__call__WithBoth(self):
        task = self._taskWithBoth
        expectedVal = sum(self._args.values()) + sum(self._reqValues.values())
        task(self._reqValues)
        actualValue = task._method._x
        self.assertEqual(actualValue, expectedVal)

    def testGetId(self):
        for task in self._tasks:
            self.assertIsInstance(task.getId(), uuid.UUID)
            if task is not self._emptyTask:
                self.assertEqual(task.getId(), self._taskId)

    def testGetRequirements(self):
        noReqsTasks = [self._emptyTask, self._taskWithId, self._taskWithArgs]
        reqsTasks = [self._taskWithReqs, self._taskWithBoth]
        for task in noReqsTasks:
            self.assertItemsEqual(task.getRequirements(), set())
        for task in reqsTasks:
            self.assertItemsEqual(task.getRequirements(), set(self._reqs.values()))

    def testGetStatus(self):
        for task in self._tasks:
            self.assertEqual(task.getStatus(), task.WAITING_STATUS)
            task(self._reqValues)
            self.assertEqual(task.getStatus(), task.DISPATCHED_STATUS)

    def testGetStatus_ErrorInEval(self):
        def brokenFunction(**kwds):
            raise self.DummyException
        for task in self._tasks:
            task._method = brokenFunction
            self.assertEqual(task.getStatus(), task.WAITING_STATUS)
            self.assertRaises(self.DummyException, task, self._reqValues)
            self.assertEqual(task.getStatus(), task.ERROR_STATUS)

    def testResetStatus(self):
        for task in self._tasks:
            self.assertEqual(task.getStatus(), task.WAITING_STATUS)
            task(self._reqValues)
            self.assertEqual(task.getStatus(), task.DISPATCHED_STATUS)
            task.resetStatus()
            self.assertEqual(task.getStatus(), task.WAITING_STATUS)

if __name__ == "__main__":
    unittest.main()
