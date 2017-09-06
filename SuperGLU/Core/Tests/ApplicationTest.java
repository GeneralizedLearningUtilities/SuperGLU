package Core.Tests;

import java.util.ArrayList;
import java.util.List;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;
import Core.BaseMessage;
import Core.BaseService;
import Core.Message;
import Core.SpeechActEnum;

public class ApplicationTest {

	public static final List<Message> messagesToSend = new ArrayList<>();
	
	
	static
	{
		Message m1 = new Message("mockActor", "GiveFeedback", "MockObj", "MockResult", SpeechActEnum.INFORM_ACT, null, null, "mockID");
		messagesToSend.add(m1);
	}
	
	
	public static void main(String[] args) {
		
		
		ActiveMQTopicConfiguration config = new ActiveMQTopicConfiguration("config", null, "failover://tcp://localhost:61617");
		List<String> excludedTopics = new ArrayList<>();
		//excludedTopics.add("DEFAULT_SCOPE");
		config.setTopic(excludedTopics);
		
		
		
		ActiveMQTopicMessagingGateway sender = new ActiveMQTopicMessagingGateway("sender", null, null, null, null, config);
		ActiveMQTopicMessagingGateway receiver = new ActiveMQTopicMessagingGateway("receiver", null, null, null, null, config);
		
		class TestService extends BaseService
		{
			@Override
			public void receiveMessage(BaseMessage msg)
			{
				super.receiveMessage(msg);
				System.out.println("message received");
			}
			
		}
		
		TestService service = new TestService();
		
		sender.addNode(service);
		
		
		
		
		for(Message msg : messagesToSend)
		{
			sender.sendMessage(msg);
		}
		
		
		System.out.println("sending through another service");
		
		for (Message msg : messagesToSend)
		{
			service.sendMessage(msg);
		}

	}

}
