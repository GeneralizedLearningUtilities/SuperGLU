package Core.Config;

import java.util.HashMap;
import java.util.Map;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This class represents a collection of service configurations.
 * 
 * @author auerbach
 *
 */

public class ServiceConfigurations extends Serializable {

	public static final String SERVICE_CONFIG_MAP_KEY = "serviceConfigurations";

	private Map<String, ServiceConfiguration> serviceConfigurationMap;

	public ServiceConfigurations() {
		this.serviceConfigurationMap = new HashMap<>();
	}

	public ServiceConfigurations(Map<String, ServiceConfiguration> serviceConfigurationMap) {
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
