'''
Created on Mar 12, 2018

 * This class is responsible for launching services based on a
 * ServiceConfiguration Object. It should also be used to shut down services
 * once that functionality is implemented.
 * <p>
 * In order for a service to use this, it will need to implement a constructor
 * that takes a ServiceConfiguration object.
 *

@author: auerbach
'''
import importlib
from SuperGLU.Util.Serialization import nativizeObject
from SuperGLU.Util import Serialization



class ServiceLauncher():
    
    services = {}
    
    def launchAndConnectAllServices(self, serviceConfigurations):
        for key in serviceConfigurations.getServiceConfigurationKeys():
            if key != "id":
                serviceConfiguration = serviceConfigurations.getServiceConfiguration(key)
                self.launchService(serviceConfiguration)
            
        for key in serviceConfigurations.getServiceConfigurationKeys():
            if key != "id":
                serviceConfiguration = serviceConfigurations.getServiceConfiguration(key)
                self.connectService(serviceConfiguration)
        
    
    def launchService(self, serviceConfiguration):
        classAndModule = serviceConfiguration.getType()
        splitName = classAndModule.split(sep=".", maxsplit=100)
        
        
        #small bit of annoyance:  the module name and class name are concatenated in the config file.
        #we'll have to split it up here
        ii=0
        moduleName=""
        while ii < len(splitName) - 1:
            moduleName = moduleName + splitName[ii]
            if ii < len(splitName) -2:
                moduleName = moduleName + "."
            ii = ii + 1
        
        className = splitName[len(splitName) - 1]
        module = importlib.import_module(moduleName)
        serviceClass = getattr(module, className)
        service = serviceClass(serviceConfiguration)
        self.services[serviceConfiguration.getId()] = service
        
        
    def connectService(self, serviceConfiguration):
        if serviceConfiguration.getId() in self.services:
            service = self.services[serviceConfiguration.getId()]
        
            if service is not None:
                for connectionId in serviceConfiguration.getNodes():
                    connection = self.services[connectionId]
                    if connection is not None:
                        service.addNodes([connection])
                    
                    
    def fileToString(self, fileName):
        result = ""
        file = open(fileName)
        
        if file is None:
            return None
        
        for line in file:
            result = result + line
        
        return result

    
    def readConfigurationFromFile(self, fileName, defaultFileName):
        fileAsString = self.fileToString(fileName)
        
        if fileAsString is None:
            fileAsString = self.fileToString(defaultFileName)
            
        
        result = nativizeObject(fileAsString, None, Serialization.JSON_STANDARD_FORMAT)
        return result
    
    def stopService(self, serviceName):
        if serviceName in self:
            serviceToStop = self[serviceName]
            connections = serviceToStop.getNodes()
            for connection in connections:
                serviceToStop.unregister(connection)
                connection.unregister(serviceToStop)
            
            del self.services[serviceName] 
    
    def stopAllServices(self):
        for serviceName in self.keys():
            self.stopService(serviceName)    