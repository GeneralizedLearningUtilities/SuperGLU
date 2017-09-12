package Ontology.Mappings.Tests;

import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

import org.junit.Test;

import Core.BaseMessage;
import Core.GIFTMessage;
import Core.Message;
import Core.VHMessage;
import Ontology.OntologyBroker;
import Ontology.Mappings.MessageMapFactory;
import Ontology.Mappings.MessageType;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;
import Util.StorageToken;


public class ConversionTest {

	@Test
	public void testConvertCompletedMessage() {
	
		OntologyBroker broker = new OntologyBroker(MessageMapFactory.buildMessageMaps(), MessageMapFactory.buildDefaultMessageTemplates());
		
		Message completedMessage = new Message();
		completedMessage.setVerb("Completed");
	
		 MessageType inMsgType = broker.buildMessageType(Message.class.getSimpleName(), "Completed", 1.0f, 1.0f);
		 MessageType outMsgType = broker.buildMessageType(GIFTMessage.class.getSimpleName(), "", 1.0f, 1.0f);
		
		BaseMessage result = broker.findPathAndConvertMessage(completedMessage, inMsgType, outMsgType, null, true);
		
	}

}
