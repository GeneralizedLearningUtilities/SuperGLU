package Core.Tests;

import java.util.ArrayList;
import java.util.List;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;

public class ApplicationTest {

	public static void main(String[] args) {
		ActiveMQTopicConfiguration config = new ActiveMQTopicConfiguration();
		List<String> excludedTopics = new ArrayList<>();
		excludedTopics.add("DEFAULT_SCOPE");
		config.setTopic(excludedTopics);
		ActiveMQTopicMessagingGateway gateway = new ActiveMQTopicMessagingGateway("ID", null, null, null, null, config);

	}

}
