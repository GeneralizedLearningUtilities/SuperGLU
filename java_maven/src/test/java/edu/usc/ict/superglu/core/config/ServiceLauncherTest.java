package edu.usc.ict.superglu.core.config;

import edu.usc.ict.superglu.core.ServiceLauncher;
import org.junit.Assert;
import org.junit.Test;

public class ServiceLauncherTest {

    private static String CONFIG_FILE = "agentsConfig.json";

    private String testResourceFullPath(String fileName) {
        String fullFilePath = getClass().getClassLoader().getResource(fileName).getFile();
        return fullFilePath;
    }

    @Test
    public void testLaunchAndConnectAllServices() {
        ServiceLauncher launcher = new ServiceLauncher();
        ServiceConfigurationCollection configurations = launcher.readConfigurationFromFile(testResourceFullPath(CONFIG_FILE));
        launcher.launchAndConnectAllServices(configurations);
        Assert.assertEquals(2, launcher.getServices().size());
        launcher.stopService("socketIOGateway");
    }

    @Test
    public void testReadConfigurationFromFile() {
        ServiceLauncher launcher = new ServiceLauncher();
        ServiceConfigurationCollection configurations = launcher.readConfigurationFromFile(testResourceFullPath(CONFIG_FILE));
        Assert.assertEquals(2, configurations.getServiceConfigurationMap().size());
    }

    @Test
    public void testShutdownActiveService() {
        ServiceLauncher launcher = new ServiceLauncher();
        ServiceConfigurationCollection configurations = launcher.readConfigurationFromFile(testResourceFullPath(CONFIG_FILE));
        launcher.launchAndConnectAllServices(configurations);
        launcher.stopService("socketIOGateway");
    }
}