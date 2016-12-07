package Util.Tests;

import static org.junit.Assert.*;

import java.util.Date;
import java.util.HashMap;

import org.junit.Assert;
import org.junit.Test;

import Core.Message;
import Core.SpeechActEnum;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

public class MessageTest {

	@Test
	public void testToJSON() {
		
		MockSerializables.MockSerializable m = new MockSerializables.MockSerializable(32, "penguins");
		
		Message message = new Message("testActor", "TestVerb", "TestObj", m, SpeechActEnum.Inform, new Date(), new HashMap<String, Object>(), "testID");
		
		message.setContextValue(Message.SESSION_ID_CONTEXT_KEY, "mockSessionID");
		
		String json = SerializationConvenience.serializeObject(message, SerializationFormatEnum.JSON_FORMAT);
		
		System.out.println(json);
	}
	
	
	@Test
	public void testFromJSON()
	{
		MockSerializables.MockSerializable m = new MockSerializables.MockSerializable(32, "penguins");
		
		Message message = new Message("testActor", "TestVerb", "TestObj", m, SpeechActEnum.Inform, new Date(), new HashMap<String, Object>(), "testID");
		
		message.setContextValue(Message.SESSION_ID_CONTEXT_KEY, "mockSessionID");
		
		String json = SerializationConvenience.serializeObject(message, SerializationFormatEnum.JSON_FORMAT);
		
		Message copy = (Message) SerializationConvenience.nativeizeObject(json, SerializationFormatEnum.JSON_FORMAT);
		
		Assert.assertEquals(message, copy);
	}

}
