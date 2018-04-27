package edu.usc.ict.superglu.core.config;

import edu.usc.ict.superglu.util.SuperGlu_Serializable;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

import java.util.HashMap;
import java.util.Map;

/**
 * This class represents a collection of service configurations.
 *
 * @author auerbach
 */

public class GatewayConfigurationCollection extends SuperGlu_Serializable {

    public static final String SERVICE_CONFIG_MAP_KEY = "gatewayConfigurations";

    private Map<String, GatewayConfiguration> serviceConfigurationMap;

    public GatewayConfigurationCollection() {
        this.serviceConfigurationMap = new HashMap<>();
    }

    public GatewayConfigurationCollection(Map<String, GatewayConfiguration> serviceConfigurationMap) {
        this.serviceConfigurationMap = serviceConfigurationMap;
    }

    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.serviceConfigurationMap = (Map<String, GatewayConfiguration>) SerializationConvenience.untokenizeObject(token.getItem(SERVICE_CONFIG_MAP_KEY, true, new HashMap<>()));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken token = super.saveToToken();

        token.setItem(SERVICE_CONFIG_MAP_KEY, SerializationConvenience.tokenizeObject(this.serviceConfigurationMap));

        return token;

    }

    public Map<String, GatewayConfiguration> getServiceConfigurationMap() {
        return serviceConfigurationMap;
    }

    public void setServiceConfigurationMap(Map<String, GatewayConfiguration> serviceConfigurationMap) {
        this.serviceConfigurationMap = serviceConfigurationMap;
    }

}
