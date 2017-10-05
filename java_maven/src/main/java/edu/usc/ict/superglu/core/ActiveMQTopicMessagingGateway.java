package edu.usc.ict.superglu.core;

import java.net.InetAddress;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

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

import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.util.StorageToken;
import edu.usc.ict.superglu.util.tokenformat.JSONStandardRWFormat;

/**
 * this class will connect to an ActiveMQ Broker.
 * It will then pass on any messages it receives from the broker.
 * For GIFT messages it will determine what queue needs the message is
 * supposed to go to, and create a producer for that queue if it does not
 * already exist.
 *
 * @author auerbach
 */
public class ActiveMQTopicMessagingGateway extends MessagingGateway implements MessageListener {

    protected MessageConsumer consumer;
    protected MessageProducer producer;
    protected Session session;
    protected MessageProducer vhProducer;

    protected List<String> excludedTopics;

    protected Map<String, MessageProducer> queueProducers;

    protected TopicConnection connection;

    // This property defines to which system the activeMQ message belongs.
    public static final String MESSAGETYPE = "MESSAGE_TYPE";
    // this is the identifier for SUPERGLU messages
    public static final String SUPERGLU = "SUPERGLU_MSG";
    // Identifier for virtual human messages
    public static final String VHMSG = "VHMSG";
    // Identifier for GIFT messages
    public static final String GIFT = "GIFT_MSG";

    public static String pedagogicalQueueName;
    public static String localIpAddr;

    static {
        try {
            localIpAddr = InetAddress.getLocalHost().getHostAddress();
            pedagogicalQueueName = "Learner_Queue:" + localIpAddr + ":Inbox"; // Pedagogical_Queue:172.16.41.14
        } catch (Exception ex) {
            pedagogicalQueueName = null;
            ex.printStackTrace();
        }
    }

    public void init(ActiveMQTopicConfiguration config) {
        try {
            this.queueProducers = new HashMap<>();
            connection = new ActiveMQConnectionFactory(config.getBrokerHost()).createTopicConnection();
            connection.start();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            Destination consumerDestination = session.createTopic(ActiveMQTopicConfiguration.DEFAULT_TOPIC);
            Destination producerDestination = session.createTopic(ActiveMQTopicConfiguration.DEFAULT_TOPIC);
            producer = session.createProducer(producerDestination);
            consumer = session.createConsumer(consumerDestination);
            consumer.setMessageListener(this);

            Destination dest2 = session.createTopic("DEFAULT_SCOPE");
            this.vhProducer = session.createProducer(dest2);
            this.excludedTopics = new ArrayList<String>();
        } catch (JMSException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to connect to ActiveMQ");
        }
    }

    public ActiveMQTopicMessagingGateway() {
        super();
        ActiveMQTopicConfiguration defaultConfig = new ActiveMQTopicConfiguration();
        init(defaultConfig);
    }

    public ActiveMQTopicMessagingGateway(ServiceConfiguration config) {
        super(config.getId(), null, null, null, null);
        // Have a default configuration to fall back on.
        ActiveMQTopicConfiguration activeMQConfig = new ActiveMQTopicConfiguration();

        if (config.getParams().containsKey(ServiceConfiguration.ACTIVEMQ_PARAM_KEY))
            activeMQConfig = (ActiveMQTopicConfiguration) config.getParams()
                    .get(ServiceConfiguration.ACTIVEMQ_PARAM_KEY);

        init(activeMQConfig);
    }

    public ActiveMQTopicMessagingGateway(String anId, Map<String, Object> scope, Collection<BaseMessagingNode> nodes,
                                         Predicate<BaseMessage> conditions, List<ExternalMessagingHandler> handlers,
                                         ActiveMQTopicConfiguration activeMQConfiguration) {
        super(anId, scope, nodes, conditions, handlers);
        init(activeMQConfiguration);
    }

    @Override
    public void disconnect() {
        super.disconnect();
        try {
            this.connection.close();
        } catch (JMSException e) {
            log.error("Failed to disconnect.  Connection was already closed.");
            e.printStackTrace();
        }
    }
    

	public MessageProducer getOrCreateQueueProducer(String destination) {
		MessageProducer result = null;
		if (this.queueProducers.containsKey(destination)) {
			result = this.queueProducers.get(destination);
		} else {
			Destination producerDestination;
			try {
				producerDestination = session.createQueue(pedagogicalQueueName);
				result = session.createProducer(producerDestination);
				
				this.queueProducers.put(destination, result);
			} catch (JMSException e) {
				log.error("failed to connect to queue: " + destination, e);
				throw new RuntimeException(e);
			}
			
		}
		
		return result;
	}

    @Override
    public void sendMessage(BaseMessage msg) {
        super.sendMessage(msg);
        try {
            if (msg instanceof Message) {
                this.addContextDataToMsg(msg);
                TextMessage activeMQMessage = session.createTextMessage(
                        SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
                activeMQMessage.setStringProperty(MESSAGETYPE, SUPERGLU);
                producer.send(activeMQMessage);
            } else if (msg instanceof GIFTMessage) {
                String msgAsString = JSONStandardRWFormat.serialize(((GIFTMessage) msg).getPayload());
                TextMessage activeMQMessage = session.createTextMessage(msgAsString);
                activeMQMessage.setStringProperty(MESSAGETYPE, GIFT);
                activeMQMessage.setByteProperty("Encoding", (byte) 0);

                String destination = ((GIFTMessage) msg).getDestinationQueueName();
                MessageProducer queueProducer = getOrCreateQueueProducer(destination);

                queueProducer.send(activeMQMessage);
            } else if (msg instanceof VHMessage) {
                VHMessage vhMsg = (VHMessage) msg;
                TextMessage activeMQMessage = session.createTextMessage(vhMsg.getFirstWord() + " " + vhMsg.getBody());
                activeMQMessage.setStringProperty(VHMSG, VHMSG);
                activeMQMessage.setStringProperty("ELVISH_SCOPE", "DEFAULT_SCOPE");
                activeMQMessage.setStringProperty("MESSAGE_PREFIX", vhMsg.getFirstWord());
                activeMQMessage.setStringProperty("VHMSG_VERSION", "1.0.0.0");

                vhProducer.send(activeMQMessage);
            }
        } catch (JMSException e) {
            e.printStackTrace();
            log.warn("Failed to Send Message to ActiveMQ:"
                    + SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT));
        }
    }

    @Override
    public void receiveMessage(BaseMessage msg) {
        // We need to override this function so that we actually send messages
        // from other services over activeMQ.
        super.receiveMessage(msg);
        this.sendMessage(msg);
    }

    /**
     * message handler for receiving all activeMQ messages Will filter out
     * topics that this gateway doesn't care about.
     */
    @Override
    public void onMessage(javax.jms.Message jmsMessage) {
        try {
            if (jmsMessage instanceof TextMessage) {
                Destination dest = jmsMessage.getJMSDestination();
                if (dest instanceof ActiveMQTopic) {
                    ActiveMQTopic messageTopic = (ActiveMQTopic) dest;
                    if (this.excludedTopics.contains(messageTopic.getPhysicalName()))
                        return;
                }
            }

            String body = ((TextMessage) jmsMessage).getText();
            try {
                body = URLDecoder.decode(body, "UTF-8");
            } catch (IllegalArgumentException ex) {
                log.info("Eating URLDecoding Exception ");
            }
            BaseMessage msg;
            String msgType = jmsMessage.getStringProperty(ActiveMQTopicMessagingGateway.MESSAGETYPE);
            String isVhmsg = jmsMessage.getStringProperty(ActiveMQTopicMessagingGateway.VHMSG);
            if (msgType != null && msgType.equals(ActiveMQTopicMessagingGateway.SUPERGLU)) {
                msg = (Message) SerializationConvenience.nativeizeObject(body, SerializationFormatEnum.JSON_FORMAT);
            } else if (isVhmsg != null) {
                String[] tokenizedMsg = body.split(" ");
                if (tokenizedMsg.length > 1) {
                    // make sure that the VH message
                    // actually has a body
                    String justTheBody = "";

                    for (int ii = 1; ii < tokenizedMsg.length; ++ii) {
                        if (ii == 1)
                            justTheBody = tokenizedMsg[ii];
                        else
                            justTheBody = justTheBody + " " + tokenizedMsg[ii];
                    }

                    msg = new VHMessage(null, null, tokenizedMsg[0], 1.0f, justTheBody);
                } else {// otherwise just set the body to an empty string
                    msg = new VHMessage(null, null, tokenizedMsg[0], 1.0f, "");
                }
            } else if (msgType != null && msgType.equals(GIFT)) {
                // need to figure out how to get all of the header properties
                // (and if we actually need them).

                // Ignore ModuleStatus Messages. They crowd things out.
                if (body.contains("ModuleStatus")) {
                    return;
                }

                StorageToken bodyAsStorageToken = SerializationConvenience.makeNative(body,
                        SerializationFormatEnum.JSON_FORMAT);
                msg = new GIFTMessage(null, new HashMap<>(),
                        (String) bodyAsStorageToken.getItem(GIFTMessage.MESSAGE_TYPE_KEY), bodyAsStorageToken);
            } else {
                msg = (Message) SerializationConvenience.nativeizeObject(body, SerializationFormatEnum.JSON_FORMAT);
            }

            // we already distributed this message when we sent it. no need to
            // re-process it.
            if (!msg.getContextValue(ORIGINATING_SERVICE_ID_KEY, "").equals(this.id)) {
                super.receiveMessage(msg);
                super.distributeMessage(msg, this.id);
            }

        } catch (Exception e) {
            // Don't crash if the message fails to be processed
            e.printStackTrace();
            log.warn("Failure while receiving JMS message:" + jmsMessage.toString(), e);
        }

    }

}
