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

public class ServiceConfigurationCollection extends SuperGlu_Serializable {

    public static final String SERVICE_CONFIG_MAP_KEY = "serviceConfigurations";

    private Map<String, ServiceConfiguration> serviceConfigurationMap;

    public ServiceConfigurationCollection() {
        this.serviceConfigurationMap = new HashMap<>();
    }

    public ServiceConfigurationCollection(Map<String, ServiceConfiguration> serviceConfigurationMap) {
        this.serviceConfigurationMap = serviceConfigurationMap;
    }

    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);

        this.serviceConfigurationMap = (Map<String, ServiceConfiguration>) SerializationConvenience.untokenizeObject(token.getItem(SERVICE_CONFIG_MAP_KEY, true, new HashMap<>()));
    }

    @Override
    public StorageToken saveToToken() {
        StorageToken token = super.saveToToken();

        token.setItem(SERVICE_CONFIG_MAP_KEY, SerializationConvenience.tokenizeObject(this.serviceConfigurationMap));

        return token;

    }

    public Map<String, ServiceConfiguration> getServiceConfigurationMap() {
        return serviceConfigurationMap;
    }

    public void setServiceConfigurationMap(Map<String, ServiceConfiguration> serviceConfigurationMap) {
        this.serviceConfigurationMap = serviceConfigurationMap;
    }

}
