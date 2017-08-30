package Core.Config.Tests;

import org.junit.Assert;
import org.junit.Test;

import Core.Config.ServiceConfigurations;
import Core.Config.ServiceLauncher;

public class ServiceLauncherTest {

	@Test
	public void testLaunchAndConnectAllServices() {
		ServiceLauncher launcher = new ServiceLauncher();
		
		ServiceConfigurations configurations = launcher.readConfigurationFromFile("./SuperGLU/Core/Config/Tests/agentsConfig.json");
		
		launcher.launchAndConnectAllServices(configurations);
		
		
		Assert.assertEquals(2, launcher.getServices().size());
		
		launcher.stopService("socketIOGateway");
	}

	@Test
	public void testReadConfigurationFromFile() {
		ServiceLauncher launcher = new ServiceLauncher();
		
		ServiceConfigurations configurations = launcher.readConfigurationFromFile("./SuperGLU/Core/Config/Tests/agentsConfig.json");
		
		Assert.assertEquals(2, configurations.getServiceConfigurationMap().size());
		
		
	}
	
	
	@Test
	public void testShutdownActiveService()
	{
		ServiceLauncher launcher = new ServiceLauncher();
		
		ServiceConfigurations configurations = launcher.readConfigurationFromFile("./SuperGLU/Core/Config/Tests/agentsConfig.json");
		
		launcher.launchAndConnectAllServices(configurations);
		
		launcher.stopService("socketIOGateway");
	}

}
