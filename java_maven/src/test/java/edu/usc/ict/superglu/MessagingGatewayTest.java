package edu.usc.ict.superglu;

import edu.usc.ict.superglu.core.*;
import edu.usc.ict.superglu.core.blackwhitelist.BlackWhiteListEntry;
import edu.usc.ict.superglu.core.config.GatewayBlackWhiteListConfiguration;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.fasterxml.jackson.databind.deser.Deserializers.Base;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

public class MessagingGatewayTest {

	class TestService extends BaseService
	{
		
		public TestService(String id) {
			super(id, null);
		}
		
		@Override
		public boolean receiveMessage(BaseMessage msg)
		{
			super.receiveMessage(msg);
			System.out.println("message received");
			return true;
		}
		
	}
	
	private MessagingGateway gateway;
	private MessagingGateway receiver;
	
	private List<BaseMessage> testMessages;
	
	private static boolean messageConditions(BaseMessage msg)
	{
		if(msg instanceof Message)
		{
			if(((Message)msg).getActor().equals("penguin"))
				return false;
			return true;
		}
		return false;
	}
	
	
	@Before
	public void setUp() throws Exception {
		Predicate<BaseMessage> condition = MessagingGatewayTest::messageConditions;
		List<BaseMessagingNode> nodes = new ArrayList<>();
		Map<String, Object> scope = new HashMap<>();
		scope.put("scope1","value1");
		scope.put("key2", "penguins");
		TestService mockService = new TestService("service1");
		nodes.add(mockService);
		
		List<BlackWhiteListEntry> blackList = new ArrayList<>();
		blackList.add(new BlackWhiteListEntry("VHuman.*.*"));
		
		receiver = new MessagingGateway("Receiver", null, new ArrayList<>(), null, null, blackList, null, null);
		gateway = new MessagingGateway("Sender", scope, nodes, condition, null, blackList, null, null);
		
		mockService.addNode(gateway);
		
		this.testMessages = buildMessages();
	}
	
	
	private List<BaseMessage> buildMessages()
	{
		List<BaseMessage> result = new ArrayList<>();
		
		Message msg1 = new Message("penguin", "eats", "fish", "gets fat", SpeechActEnum.INFORM_ACT, null, new HashMap<>(), "msg1");
		result.add(msg1);
		Message msg2 = new Message("TestService", "Sends Message", "to somebody", "this message should go through", SpeechActEnum.INFORM_ACT, null, new HashMap<>(), "msg2");
		result.add(msg2);
		VHMessage msg3 = new VHMessage("vhMessage", null, "vrSpeak", 1.2f, "speaking");
		result.add(msg3);
		
		return result;
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testReceiveMessage() {
		for(BaseMessage msg : this.testMessages)
			gateway.receiveMessage(msg);
	}
	
	
	@Test
	public void testSendMessage()
	{
		for(BaseMessage msg : this.testMessages)
			gateway.sendMessage(msg);
	}
	

	@Test
	public void testAddContextDataToMsg() {
		BaseMessage msg1 = testMessages.get(0);
		gateway.addContextDataToMsg(msg1);
		
		Assert.assertEquals(msg1.getContextValue("key2"), "penguins");
		
		System.out.println(msg1.toString());
	}

	@Test
	public void testGetMessageConditions() {
		boolean result = gateway.getMessageConditions().test(testMessages.get(0));
		Assert.assertEquals(false, result);
		
		result = gateway.getMessageConditions().test(testMessages.get(1));
		Assert.assertEquals(true, result);
		
	}
	

	@Test
	public void testMessagesToStringListAndBack() {
		List<String> msgsAsStrings = gateway.messagesToStringList(testMessages);
		System.out.print(msgsAsStrings.toString());
		List<BaseMessage> copy = gateway.stringListToMessages(msgsAsStrings);
		
		Assert.assertEquals(testMessages, copy);
	}

	
	@Test
	public void testGatewayBlackList()
	{
		System.out.println("testGatewayBlackList");
		Map<String, List<String>> config = new HashMap<>();
		List<String> messages = new ArrayList<>();
		messages.add("VHuman.*.*");
		config.put("service1", messages);
		GatewayBlackWhiteListConfiguration gateway1BlackList = new GatewayBlackWhiteListConfiguration(config);
		
		MessagingGateway gateway1 = new MessagingGateway("gateway1", null, null, null, null, null, null, gateway1BlackList);
		
		TestService service = new TestService("service1");
		TestService service2 = new TestService("service2");
		
		service.addNode(gateway1);
		service2.addNode(gateway1);
		
		for(BaseMessage msg : testMessages)
		{
			gateway1.sendMessage(msg);
		}
	}
}
