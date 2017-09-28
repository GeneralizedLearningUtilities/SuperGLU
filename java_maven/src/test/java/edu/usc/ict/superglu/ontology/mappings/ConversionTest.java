package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.GIFTMessage;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.ontology.OntologyBroker;
import org.junit.Test;


public class ConversionTest {

    @Test
    public void testConvertCompletedMessage() {

        OntologyBroker broker = new OntologyBroker(MessageMapFactory.buildMessageMaps(), MessageMapFactory.buildDefaultMessageTemplates());

        Message completedMessage = new Message();
        completedMessage.setVerb("Completed");

        MessageType inMsgType = broker.buildMessageType(Message.class.getSimpleName(), "Completed", 1.0f, 1.0f);
        MessageType outMsgType = broker.buildMessageType(GIFTMessage.class.getSimpleName(), "", 1.0f, 1.0f);

        BaseMessage result = broker.findPathAndConvertMessage(completedMessage, inMsgType, outMsgType, null, true);
        System.out.println();
    }

}
