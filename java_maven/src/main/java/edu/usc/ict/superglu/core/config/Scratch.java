package edu.usc.ict.superglu.core.config;

import edu.usc.ict.superglu.core.ActiveMQTopicConfiguration;
import edu.usc.ict.superglu.core.HTTPMessagingGateway;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.vhuman.GIFTVHumanBridge;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
		String bridgeGatewayName = "VHMSGBridgeGateway";
		
		List<String> amqNodes = new ArrayList<>();
		
		amqNodes.add(socketioGatewayName);
		amqNodes.add(bridgeGatewayName);
		
		ServiceConfiguration activeMQGateway = new ServiceConfiguration(amqGatewayName, ActiveMQTopicConfiguration.class, amqParams, amqNodes, null,null);
		
		
		Map<String, Object> socketIOParams = new HashMap<>();
		socketIOParams.put(ServiceConfiguration.SOCKETIO_PARAM_KEY, 5333);
		
		List<String> socketIONodes = new ArrayList<>();
		socketIONodes.add(amqGatewayName);
		socketIONodes.add(bridgeGatewayName);
		
		ServiceConfiguration socketIOGateway = new ServiceConfiguration(socketioGatewayName, HTTPMessagingGateway.class, socketIOParams, socketIONodes,null,null);
		
		
		Map<String, Object> defaultBridgeParams = new HashMap<>();
		defaultBridgeParams.put(GIFTVHumanBridge.BROKER_HOST_PARAM_KEY, "localhost");
		defaultBridgeParams.put(GIFTVHumanBridge.BROKER_PORT_PARAM_KEY, 61617);
		
		List<String> bridgeNodes = new ArrayList<>();
		bridgeNodes.add(amqGatewayName);
		bridgeNodes.add(socketioGatewayName);
		
		ServiceConfiguration GiftVHumanBridge = new ServiceConfiguration("defaultBridge", GIFTVHumanBridge.class, defaultBridgeParams, bridgeNodes,null,null);
		
		
		Map<String, ServiceConfiguration> result = new HashMap<>();
		result.put(activeMQGateway.getId(), activeMQGateway);
		result.put(socketIOGateway.getId(), socketIOGateway);
		result.put(GiftVHumanBridge.getId(), GiftVHumanBridge);

		ServiceConfigurationCollection serviceConfigs = new ServiceConfigurationCollection(result);
		String json = SerializationConvenience.serializeObject(serviceConfigs, SerializationFormatEnum.JSON_STANDARD_FORMAT);
		
		System.out.println(json);

	}

}
