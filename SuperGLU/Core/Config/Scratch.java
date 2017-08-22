package Core.Config;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;
import Core.HTTPMessagingGateway;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;
import Util.StorageToken;

/**
 * this is just some scratch space I made to create a quick program to build a service configuration file
 * @author auerbach
 *
 */

public class Scratch {

	public static void main(String[] args) {
		
		ActiveMQTopicConfiguration topicConfiguration = new ActiveMQTopicConfiguration("ActiveMQ", new ArrayList<>(), "tcp://localhost:61617");
		
		Map<String, Object> amqParams = new HashMap<String, Object>();
		amqParams.put(ServiceConfiguration.ACTIVEMQ_PARAM_KEY, topicConfiguration);
		
		String amqGatewayName = "activeMQGateway";
		String socketioGatewayName = "socketIOGateway";
		
		List<String> amqNodes = new ArrayList<>();
		
		amqNodes.add(socketioGatewayName);
		
		ServiceConfiguration activeMQGateway = new ServiceConfiguration(amqGatewayName, ActiveMQTopicConfiguration.class, amqParams, amqNodes);
		
		
		Map<String, Object> socketIOParams = new HashMap<>();
		socketIOParams.put(ServiceConfiguration.SOCKETIO_PARAM_KEY, 5333);
		
		List<String> socketIONodes = new ArrayList<>();
		socketIONodes.add(amqGatewayName);
		
		
		ServiceConfiguration socketIOGateway = new ServiceConfiguration(socketioGatewayName, HTTPMessagingGateway.class, socketIOParams, socketIONodes);
		
		Map<String, ServiceConfiguration> result = new HashMap<>();
		result.put(activeMQGateway.getId(), activeMQGateway);
		result.put(socketIOGateway.getId(), socketIOGateway);
		
		
		Object map  = SerializationConvenience.tokenizeObject(result);
		StorageToken token = new StorageToken((Map<String, Object>) map, "storageToken", null);
		String json = SerializationConvenience.makeSerialized(token, SerializationFormatEnum.JSON_FORMAT);
		
		System.out.println(json);

	}

}
