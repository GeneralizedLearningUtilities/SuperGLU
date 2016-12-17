package Core;

import org.apache.activemq.ActiveMQConnection;
import Util.Serializable;
import Util.StorageToken;
/**
 * This class contains all the information needed to set up an activeMQ connection.  
 * It can be written and read from a configuration file if necessary
 * @author auerbach
 *
 */
public class ActiveMQTopicConfiguration extends Serializable {

	private static String TOPIC_KEY = "topic";
	private static String BROKER_URL_KEY = "brokerURL";
	
	
	private String topic;
	private String brokerHost;
	
	private static String DEFAULT_TOPIC = "DEFAULT_SCOPE";
	
	//Constructors
	public ActiveMQTopicConfiguration(String id, String topic, String brokerHost) {
		super(id);
		
		if(topic == null)
			this.topic = DEFAULT_TOPIC;
		else
			this.topic = topic;
		
		if(brokerHost == null)
			this.brokerHost = ActiveMQConnection.DEFAULT_BROKER_URL;
		else
			this.brokerHost = brokerHost;
			
	}

	public ActiveMQTopicConfiguration() {
		super();
		this.topic = DEFAULT_TOPIC;
		this.topic = ActiveMQConnection.DEFAULT_BROKER_URL;
	}

	
	//Serialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.topic = (String) token.getItem(TOPIC_KEY, true, DEFAULT_TOPIC);
		this.brokerHost = (String) token.getItem(BROKER_URL_KEY, true, ActiveMQConnection.DEFAULT_BROKER_URL);
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken token = super.saveToToken();
		token.setItem(TOPIC_KEY, this.topic);
		token.setItem(BROKER_URL_KEY, this.brokerHost);
		return token;
		
	}

	
	//Accessors
	public String getTopic() {
		return topic;
	}

	public void setTopic(String topic) {
		this.topic = topic;
	}

	public String getBrokerHost() {
		return brokerHost;
	}

	public void setBrokerHost(String brokerHost) {
		this.brokerHost = brokerHost;
	}

	
	
}
