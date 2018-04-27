package edu.usc.ict.superglu.core;

import edu.usc.ict.superglu.core.config.GatewayConfiguration;
import edu.usc.ict.superglu.core.config.GatewayConfigurationCollection;
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
 * This class is responsible for launching gateways based on a
 * GatewayConfiguration Object. It should also be used to shut down gateways
 * once that functionality is implemented.
 * <p>
 * In order for a service to use this, it will need to implement a constructor
 * that takes a GatewayConfiguration object.
 *
 * @author auerbach
 */

public class ServiceLauncher {

    private Map<String, BaseMessagingGateway> gateways;

    public ServiceLauncher() {
        gateways = new HashMap<>();
    }

    public void launchAndConnectAllServices(GatewayConfigurationCollection configs) {

        for (String key : configs.getServiceConfigurationMap().keySet()) {
            if (configs.getServiceConfigurationMap().get(key) instanceof GatewayConfiguration) {
                GatewayConfiguration config = configs.getServiceConfigurationMap().get(key);

                launchService(config);
            }
        }

        for (String key : configs.getServiceConfigurationMap().keySet()) {
            if (configs.getServiceConfigurationMap().get(key) instanceof GatewayConfiguration) {
                GatewayConfiguration config = configs.getServiceConfigurationMap().get(key);
                connectService(config);
            }
        }

    }

    public void launchService(GatewayConfiguration config) {
        try {
            Constructor<?> constructor = config.getType().getConstructor(GatewayConfiguration.class);
            BaseMessagingGateway gateway = (BaseMessagingGateway) constructor.newInstance(config);
            gateways.put(config.getId(), gateway);
        } catch (NoSuchMethodException | SecurityException | InstantiationException | IllegalAccessException
                | IllegalArgumentException | InvocationTargetException e) {
            e.printStackTrace();
        }

    }

    public void addContextToService(BaseMessagingNode service, String key, Object context) {
        service.addToContext(key, context);
    }

    public void connectService(GatewayConfiguration config) {
        BaseMessagingGateway gateway = (BaseMessagingGateway) gateways.get(config.getId());

        if (gateway != null) {

            for (String connectionId : config.getNodes()) {
                BaseMessagingGateway connection = (BaseMessagingGateway) gateways.get(connectionId);

                if (connection != null)
                    gateway.addNode(connection);
            }
        }
    }

    public GatewayConfigurationCollection readConfigurationFromFile(String fileName, String defaultFileName) {
        String fileAsString = this.fileToString(fileName);

        if (fileAsString == null)
            fileAsString = this.fileToString(defaultFileName);

        GatewayConfigurationCollection result = (GatewayConfigurationCollection) SerializationConvenience.nativeizeObject(fileAsString,
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

    public Map<String, BaseMessagingGateway> getGateways() {
        return this.gateways;
    }

    public void stopService(String gatewayName) {
        if (this.gateways.containsKey(gatewayName)) {
            BaseMessagingGateway gatewayToStop = this.gateways.get(gatewayName);

            final List<BaseMessagingNode> connections = new ArrayList<BaseMessagingNode>(gatewayToStop.getNodes());

            for (BaseMessagingNode connection : connections) {
                gatewayToStop.onUnbindToNode(connection);
            }

            // If it's a gateway make sure to shut it down properly
            if (gatewayToStop instanceof BaseMessagingGateway) {
                BaseMessagingGateway gateway = (BaseMessagingGateway) gatewayToStop;

                gateway.disconnect();
            }

            // finally remove it from the list of gateways
            this.gateways.remove(gatewayName);
        }
    }


    public void stopAllGateways() {
        for (String serviceName : this.gateways.keySet()) {
            stopService(serviceName);
        }
    }

}
