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
import Core.MessagingGateway;
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
			e.printStackTrace();
		}

	}

	public void connectService(ServiceConfiguration config) {
		BaseMessagingNode service = services.get(config.getId());

		if (service != null) {

			for (String connectionId : config.getNodes()) {
				BaseMessagingNode connection = services.get(connectionId);

				if (connection != null)
					service.addNode(connection);
			}
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

	public Map<String, BaseMessagingNode> getServices() {
		return this.services;
	}

	public void stopService(String serviceName) {
		if (this.services.containsKey(serviceName)) {
			BaseMessagingNode serviceToStop = this.services.get(serviceName);

			for (BaseMessagingNode connection : serviceToStop.getNodes()) {
				// Remove connections to other services.
				serviceToStop.onUnbindToNode(connection);
				connection.onUnbindToNode(serviceToStop);
			}

			// If it's a gateway make sure to shut it down properly
			if (serviceToStop instanceof MessagingGateway) {
				MessagingGateway gateway = (MessagingGateway) serviceToStop;

				gateway.disconnect();
			}

			// finally remove it from the list of services
			this.services.remove(serviceName);
		}
	}

}
