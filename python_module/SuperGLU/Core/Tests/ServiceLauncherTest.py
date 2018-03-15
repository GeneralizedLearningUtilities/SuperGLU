'''
Created on Mar 13, 2018

@author: auerbach
'''
import unittest
from SuperGLU.Core.MessagingGateway import BaseMessagingNode
from SuperGLU.Core.ServiceConfiguration import ServiceConfiguration
from SuperGLU.Core.ServiceLauncher import ServiceLauncher
from SuperGLU.Util.Serialization import makeSerialized, serializeObject
from SuperGLU.Util.Serialization import JSON_STANDARD_FORMAT


class MockService1(BaseMessagingNode):
    
    def __init__(self, serviceConfiguration):
        super(MockService1, self).__init__(serviceConfiguration.getId(), None, None, None, serviceConfiguration.getBlackList(), serviceConfiguration.getWhiteList())
        

class ServiceLauncherTest(unittest.TestCase):


    def testReadFile(self):
        launcher = ServiceLauncher()
        config = launcher.readConfigurationFromFile("tests/agentsConfig.json", None)
        print (serializeObject(config, JSON_STANDARD_FORMAT))
        
    def testLaunchServices(self):
        launcher = ServiceLauncher()
        config = launcher.readConfigurationFromFile("tests/agentsConfig.json", None)
        launcher.launchAndConnectAllServices(config)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()