package Core.Config;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Core.BaseMessagingNode;

/**
 * This class is responsible for launching services based on a ServiceConfiguration Object.  It should also be used to shut down services once that
 * functionality is implemented.
 * 
 * In order for a service to use this, it will need to implement a constructor that takes a ServiceConfiguration object.
 * 
 * @author auerbach
 *
 */

public class ServiceLauncher {

	private Map<String, BaseMessagingNode> services;
	
	
	public ServiceLauncher()
	{
		services = new HashMap<>();
	}
	
	
	//public void launchAllServices
	
	public void launchService(ServiceConfiguration config)
	{
		
	}
	
	
	public Map<String, ServiceConfiguration> readConfigurationFromFile(String fileName)
	{
		
		return null;
	}
	
}
