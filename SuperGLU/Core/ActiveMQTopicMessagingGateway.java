package Core;

import java.util.Collection;
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
	
	protected TopicConnection connection; 

	public ActiveMQTopicMessagingGateway() {
		super();
		ActiveMQTopicConfiguration defaultConfig = new ActiveMQTopicConfiguration();
		try {
			connection = new ActiveMQConnectionFactory(defaultConfig.getBrokerHost()).createTopicConnection();
			connection.start();
			session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			Destination dest = session.createTopic(defaultConfig.getTopic());
			producer = session.createProducer(dest);
			consumer = session.createConsumer(dest);
			consumer.setMessageListener(this);
		} catch (JMSException e) {
			e.printStackTrace();
			throw new RuntimeException("Failed to connect to ActiveMQ");
		}
	}

	public ActiveMQTopicMessagingGateway(String anId, MessagingGateway gateway, Map<String, Object> scope, Collection<BaseMessagingNode> nodes, Predicate<Message> conditions, ActiveMQTopicConfiguration activeMQConfiguration) {
		super(anId, gateway, scope, nodes, conditions);
		try
		{
			connection = new ActiveMQConnectionFactory(activeMQConfiguration.getBrokerHost()).createTopicConnection();
			session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			Destination dest = session.createTopic(activeMQConfiguration.getTopic());
			this.producer = session.createProducer(dest);
			this.consumer = session.createConsumer(dest);
			consumer.setMessageListener(this);
		}
		catch (JMSException e)
		{
			e.printStackTrace();
			log.log(Level.SEVERE, "Failed To connect to ActiveMQ", e);
			throw new RuntimeException("Failed to connect to ActiveMQ");
		}
	}
	
	
	@Override
	public void sendMessage(Message msg) {
		super.sendMessage(msg);
		try {
			TextMessage activeMQMessage = session.createTextMessage(SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
			producer.send(activeMQMessage);
		} catch (JMSException e) {
			e.printStackTrace();
			log.log(Level.WARNING, "Failed to Send Message to ActiveMQ:" + SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
		}
	}


	@Override
	public void onMessage(javax.jms.Message jmsMessage) {
		
		if(jmsMessage instanceof TextMessage)
		{
			try {
				String body = ((TextMessage) jmsMessage).getText();
				Message msg = (Message) SerializationConvenience.nativeizeObject(body, SerializationFormatEnum.JSON_FORMAT);
				super.receiveMessage(msg);
			} catch (JMSException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				log.log(Level.WARNING, "Failure while receiving JMS message.", e);
			}
		}
		
	}

}
