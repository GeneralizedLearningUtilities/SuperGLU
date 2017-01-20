package Core;

import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.logging.Level;

import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.MessageListener;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.TopicConnection;

import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.command.ActiveMQTopic;

import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 * this class will connect to an ActiveMQ Broker and subscribe to a single topic.
 * It will then pass on any messages it receives from the broker. 
 * @author auerbach
 *
 */
public class ActiveMQTopicMessagingGateway extends MessagingGateway implements MessageListener{


	protected MessageConsumer consumer;
	protected MessageProducer producer;
	protected Session session;
	
	protected List<String> excludedTopics;
	
	protected TopicConnection connection; 
	
	//This property defines to which system the activeMQ message belongs.
	public static final String SYSTEM_NAME = "SYSTEM_NAME";
	//this is the identifier for SUPERGLU messages
	public static final String SUPERGLU = "SUPERGLU_MSG";
	public static final String VHMSG = "VHMSG_MSG"; //Identifier for virtual human messages
	public static final String GIFT = "GIFT_MSG";

	public ActiveMQTopicMessagingGateway() {
		super();
		ActiveMQTopicConfiguration defaultConfig = new ActiveMQTopicConfiguration();
		try {
			connection = new ActiveMQConnectionFactory(defaultConfig.getBrokerHost()).createTopicConnection();
			connection.start();
			session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			Destination dest = session.createTopic(ActiveMQTopicConfiguration.DEFAULT_TOPIC);
			producer = session.createProducer(dest);
			consumer = session.createConsumer(dest);
			consumer.setMessageListener(this);
			this.excludedTopics = new ArrayList<String>();
		} catch (JMSException e) {
			e.printStackTrace();
			throw new RuntimeException("Failed to connect to ActiveMQ");
		}
	}

	public ActiveMQTopicMessagingGateway(String anId, MessagingGateway gateway, Map<String, Object> scope, Collection<BaseMessagingNode> nodes, Predicate<BaseMessage> conditions, ActiveMQTopicConfiguration activeMQConfiguration) {
		super(anId, gateway, scope, nodes, conditions);
		try
		{
			connection = new ActiveMQConnectionFactory(activeMQConfiguration.getBrokerHost()).createTopicConnection();
			connection.start();
			session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			
			Destination dest = session.createTopic(ActiveMQTopicConfiguration.DEFAULT_TOPIC);
			this.producer = session.createProducer(dest);
			this.consumer = session.createConsumer(dest);
			consumer.setMessageListener(this);
			this.excludedTopics = activeMQConfiguration.getExcludedTopic();
		}
		catch (JMSException e)
		{
			e.printStackTrace();
			log.log(Level.SEVERE, "Failed To connect to ActiveMQ", e);
			throw new RuntimeException("Failed to connect to ActiveMQ");
		}
	}
	
	
	@Override
	public void sendMessage(BaseMessage msg) {
		super.sendMessage(msg);
		try {
			this.addContextDataToMsg(msg);
			TextMessage activeMQMessage = session.createTextMessage(SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
			activeMQMessage.setStringProperty(SYSTEM_NAME, SUPERGLU);
			producer.send(activeMQMessage);
		} catch (JMSException e) {
			e.printStackTrace();
			log.log(Level.WARNING, "Failed to Send Message to ActiveMQ:" + SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
		}
	}


	@Override
	/**
	 * message handler for receiving all activeMQ messages
	 * Will filter out topics that this gateway doesn't care about.
	 */
	public void onMessage(javax.jms.Message jmsMessage) {
				
		try {
			
			//TODO:check the header to make sure this is a superGLU message.
			if(jmsMessage instanceof TextMessage)
			{
				Destination dest = jmsMessage.getJMSDestination();
				if(dest instanceof ActiveMQTopic)
				{
					ActiveMQTopic messageTopic = (ActiveMQTopic)dest;
					if(this.excludedTopics.contains(messageTopic.getPhysicalName()))
						return;
				}
			}
			
			
			String body = ((TextMessage) jmsMessage).getText();
			body = URLDecoder.decode(body, "UTF-8");
			Message msg = (Message) SerializationConvenience.nativeizeObject(body, SerializationFormatEnum.JSON_FORMAT);
			
			//we already distributed this message when we sent it.  no need to re-process it.
			if(!msg.getContextValue(ORIGINATING_SERVICE_ID_KEY, "").equals(this.id))
				super.receiveMessage(msg);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			log.log(Level.WARNING, "Failure while receiving JMS message.", e);
		}
		
		
	}

}
