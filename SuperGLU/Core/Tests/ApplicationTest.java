package Core.Tests;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;
import Core.BaseMessagingNode;
import Core.Message;
import Core.MessagingGateway;
import Core.SpeechActEnum;

public class ApplicationTest {

	public static List<Message> messagesToSend = new ArrayList<>();
	
	
	static
	{
		Message m1 = new Message("mockActor", "MockVerb", "MockObj", "MockResult", SpeechActEnum.INFORM_ACT, null, null, "mockID");
		messagesToSend.add(m1);
	}
	
	
	public static void main(String[] args) {
		
		
		ActiveMQTopicConfiguration config = new ActiveMQTopicConfiguration();
		List<String> excludedTopics = new ArrayList<>();
		excludedTopics.add("DEFAULT_SCOPE");
		config.setTopic(excludedTopics);
		
		
		
		ActiveMQTopicMessagingGateway sender = new ActiveMQTopicMessagingGateway("sender", null, null, null, null, config);
		ActiveMQTopicMessagingGateway receiver = new ActiveMQTopicMessagingGateway("receiver", null, null, null, null, config);
		
		
		for(Message msg : messagesToSend)
		{
			sender.sendMessage(msg);
		}

	}

}
