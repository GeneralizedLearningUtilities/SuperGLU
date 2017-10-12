package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.core.config.ServiceConfigurationCollection;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.*;

/**
 * This class is responsible for launching services based on a
 * ServiceConfiguration Object. It should also be used to shut down services
 * once that functionality is implemented.
 * <p>
 * In order for a service to use this, it will need to implement a constructor
 * that takes a ServiceConfiguration object.
 *
 * @author auerbach
 */

public class ServiceLauncher {

    private Map<String, BaseMessagingNode> services;

    public ServiceLauncher() {
        services = new HashMap<>();
    }

    public void launchAndConnectAllServices(ServiceConfigurationCollection configs) {

        for (String key : configs.getServiceConfigurationMap().keySet()) {
            if (configs.getServiceConfigurationMap().get(key) instanceof ServiceConfiguration) {
                ServiceConfiguration config = configs.getServiceConfigurationMap().get(key);

                launchService(config);
            }
        }

        for (String key : configs.getServiceConfigurationMap().keySet()) {
            if (configs.getServiceConfigurationMap().get(key) instanceof ServiceConfiguration) {
                ServiceConfiguration config = configs.getServiceConfigurationMap().get(key);
                connectService(config);
            }
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

    public void addContextToService(BaseMessagingNode service, String key, Object context) {
        service.addToContext(key, context);
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

    public ServiceConfigurationCollection readConfigurationFromFile(String fileName) {
        String fileAsString = this.fileToString(fileName);

        ServiceConfigurationCollection result = (ServiceConfigurationCollection) SerializationConvenience.nativeizeObject(fileAsString,
                SerializationFormatEnum.JSON_STANDARD_FORMAT);

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
            e.printStackTrace();
        } catch (IOException e) {
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

            final List<BaseMessagingNode> connections = new ArrayList<>(serviceToStop.getNodes());

            for (BaseMessagingNode connection : connections) {
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
