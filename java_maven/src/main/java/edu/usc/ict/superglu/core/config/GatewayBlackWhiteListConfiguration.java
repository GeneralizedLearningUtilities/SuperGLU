package edu.usc.ict.superglu.core.config;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;

/**
 * This class represents the messages that a gateway is allowed to send and to
 * whom it is allowed to send them.
 * 
 * @author auerbach
 *
 */
public class GatewayBlackWhiteListConfiguration extends SuperGlu_Serializable {

	public static final String ALL_DESTINATIONS = "all";
	public static final String EXTERNAL_DESTINATIONS = "external";

	public static final String CONFIG_KEY = "config";

	private Map<String, List<String>> config;

	public GatewayBlackWhiteListConfiguration() {
		this.config = new HashMap<>();
	}

	public GatewayBlackWhiteListConfiguration(Map<String, List<String>> config) {
		this.config = config;
	}

	public void addMessage(String destination, String message) {
		if (!config.containsKey(destination))
			config.put(destination, new ArrayList<>());

		List<String> messages = config.get(destination);
		messages.add(message);

	}

	public List<String> getMessageList(String destination) {
		return config.get(destination);
	}
	
	
	public Set<String> getKeys()
	{
		return this.config.keySet();
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);

		this.config = (Map<String, List<String>>) SerializationConvenience.untokenizeObject(token.getItem(CONFIG_KEY, true, new HashMap<>()));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();

		result.setItem(CONFIG_KEY, SerializationConvenience.tokenizeObject(this.config));

		return result;
	}

}
