package Core.Config;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Core.BaseMessagingNode;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 * This class is responsible for launching services based on a
 * ServiceConfiguration Object. It should also be used to shut down services
 * once that functionality is implemented.
 * 
 * In order for a service to use this, it will need to implement a constructor
 * that takes a ServiceConfiguration object.
 * 
 * @author auerbach
 *
 */

public class ServiceLauncher {

	private Map<String, BaseMessagingNode> services;

	public ServiceLauncher() {
		services = new HashMap<>();
	}

	public void launchAndConnectAllServices(ServiceConfigurations configs) {

		for (String key : configs.getServiceConfigurationMap().keySet()) {
			ServiceConfiguration config = configs.getServiceConfigurationMap().get(key);

			launchService(config);
		}

		for (String key : configs.getServiceConfigurationMap().keySet()) {
			ServiceConfiguration config = configs.getServiceConfigurationMap().get(key);
			connectService(config);
		}

	}

	public void launchService(ServiceConfiguration config) {
		try {
			Constructor<?> constructor = config.getType().getConstructor(ServiceConfiguration.class);
			BaseMessagingNode service = (BaseMessagingNode) constructor.newInstance(config);
			services.put(config.getId(), service);
		} catch (NoSuchMethodException | SecurityException | InstantiationException | IllegalAccessException
				| IllegalArgumentException | InvocationTargetException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void connectService(ServiceConfiguration config) {
		BaseMessagingNode service = services.get(config.getId());

		for (String connectionId : config.getNodes()) {
			BaseMessagingNode connection = services.get(connectionId);
			service.onBindToNode(connection);
		}
	}

	public ServiceConfigurations readConfigurationFromFile(String fileName) {
		String fileAsString = this.fileToString(fileName);

		ServiceConfigurations result = (ServiceConfigurations) SerializationConvenience.nativeizeObject(fileAsString,
				SerializationFormatEnum.JSON_FORMAT);

		return result;
	}

	private String fileToString(String fileName) {
		String result = null;

		try {
			FileReader fileIn = new FileReader(fileName);
			BufferedReader reader = new BufferedReader(fileIn);

			StringBuilder fileAsString = new StringBuilder();

			while (reader.ready()) {
				fileAsString.append(reader.readLine());
			}

			reader.close();

			result = fileAsString.toString();

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return result;
	}
	
	
	public Map<String, BaseMessagingNode> getServices()
	{
		return this.services;
	}

}
