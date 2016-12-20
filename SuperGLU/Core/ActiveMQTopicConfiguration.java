package Core;

import java.util.ArrayList;
import java.util.List;

import org.apache.activemq.ActiveMQConnection;
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;
/**
 * This class contains all the information needed to set up an activeMQ connection.  
 * It can be written and read from a configuration file if necessary
 * @author auerbach
 *
 */
public class ActiveMQTopicConfiguration extends Serializable {

	private static String EXCLUDED_TOPICS_KEY = "topic";
	private static String BROKER_URL_KEY = "brokerURL";
	
	
	private List<String> excludedTopics;
	private String brokerHost;
	
	public static String DEFAULT_TOPIC = "*";
	
	//Constructors
	public ActiveMQTopicConfiguration(String id, List<String> excludedTopics, String brokerHost) {
		super(id);
		
		if(excludedTopics == null)
			this.excludedTopics = new ArrayList<>();
		else
			this.excludedTopics = excludedTopics;
		
		if(brokerHost == null)
			this.brokerHost = ActiveMQConnection.DEFAULT_BROKER_URL;
		else
			this.brokerHost = brokerHost;
			
	}

	public ActiveMQTopicConfiguration() {
		super();
		this.excludedTopics = new ArrayList<>();
		this.brokerHost = ActiveMQConnection.DEFAULT_BROKER_URL;
	}

	
	//Serialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.excludedTopics = (List<String>) token.getItem(EXCLUDED_TOPICS_KEY, true, new ArrayList<>());
		this.brokerHost = (String) token.getItem(BROKER_URL_KEY, true, ActiveMQConnection.DEFAULT_BROKER_URL);
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken token = super.saveToToken();
		token.setItem(EXCLUDED_TOPICS_KEY, SerializationConvenience.tokenizeObject(this.excludedTopics));
		token.setItem(BROKER_URL_KEY, this.brokerHost);
		return token;
		
	}

	
	//Accessors
	public List<String> getExcludedTopic() {
		return this.excludedTopics;
	}

	public void setTopic(List<String> excludedTopics) {
		this.excludedTopics = excludedTopics;
	}

	public String getBrokerHost() {
		return brokerHost;
	}

	public void setBrokerHost(String brokerHost) {
		this.brokerHost = brokerHost;
	}

	
	
}
