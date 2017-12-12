package edu.usc.ict.superglu.ontology.mappings;

import static org.junit.Assert.*;

import java.util.ArrayList;

import org.junit.Assert;
import org.junit.Test;

import edu.usc.ict.superglu.core.GIFTMessage;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.util.StorageToken;

public class MessageTemplateFactoryTest {

	@Test
	public void testCreateMessageTemplate() {
			
		String messageAsJSON = "{\"classId\":\"GIFTMessage\",\"payload\":{\"SenderModuleType\":\"Domain_Module\",\"SenderQueueName\":\"Domain_Queue:172.16.41.120:Inbox\",\"Message_Type\":\"DisplayContentTutorRequest\",\"NeedsACK\":true,\"userName\":\"dan100110\",\"clientAddress\":\"172.16.41.120\",\"Guidance\":\"<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\" standalone=\\\"yes\\\"?>\\n<Guidance>\\n    <transitionName>Last<\\/transitionName>\\n    <message>\\n        <content>Enter your message here!<\\/content>\\n    <\\/message>\\n    <fullScreen>true<\\/fullScreen>\\n<\\/Guidance>\\n\",\"WhileTrainingAppLoads\":false,\"Display_Duration\":0,\"Time_Stamp\":1512071625887,\"UserId\":3,\"SequenceNumber\":350,\"Class\":\"mil.arl.gift.common.DisplayMessageTutorRequest\",\"SenderModuleName\":\"Domain_Module\",\"id\":\"9c665fb9-e134-40bc-bd5c-539697cd077f\",\"SessionId\":101,\"DestinationQueueName\":\"Tutor_Queue:172.16.41.120:Inbox\"},\"context\":{\"map\":{}},\"header\":\"DisplayContentTutorRequest\",\"id\":\"ae544e27-1b15-448e-befe-1af8a5af1d1f\"}";
		
		StorageToken token = SerializationConvenience.makeNative(messageAsJSON, SerializationFormatEnum.JSON_STANDARD_FORMAT);
		
		MessageTemplate template = MessageTemplateFactory.createMessageTemplate(token, new ArrayList<>(), new ArrayList<>());
		
		StorageToken copy = template.createTargetStorageToken("test", GIFTMessage.class.toString());
		
		System.out.println(copy);
		
		Assert.assertEquals(token, copy);
	}

}
