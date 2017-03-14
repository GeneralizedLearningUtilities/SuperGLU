package Examples.VHuman;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;
import Core.BaseMessage;
import Core.MessagingGateway;
import Core.VHMessage;
import edu.usc.ict.vhmsg.VHMsg;

/**
 * This class is the internal service that will route received virtual human messages to vhmsg 
 * @author auerbach
 *
 */

public class GIFTVHumanBridge extends MessagingGateway
{
    protected VHMsg vhmsg;
    
    public GIFTVHumanBridge()
    {
	super("GIFT_VHUMAN_BRIDGE", null, null, null, null);
	this.vhmsg = new VHMsg();
	this.vhmsg.openConnection();
    }

    @Override
    public void receiveMessage(BaseMessage msg)
    {
	super.receiveMessage(msg);
	
	//attempt to convert the recieved message to a vhuman message.
	BaseMessage convertedMessage = super.convertMessages(msg, VHMessage.class);
	
	if(convertedMessage != null && convertedMessage instanceof VHMessage)
	{
	    VHMessage convertedVHMessage = (VHMessage) convertedMessage;
	    
	    //send out the message if it was successfully converted.
	    vhmsg.sendMessage(convertedVHMessage.getFirstWord(), convertedVHMessage.getBody());
	}
    }
    
    
    public static void main(String[] args) {
	
	ActiveMQTopicConfiguration config = new ActiveMQTopicConfiguration("config", null, "failover://tcp://localhost:61617");
	ActiveMQTopicMessagingGateway receiver = new ActiveMQTopicMessagingGateway("receiver", null, null, null, null, config);
	GIFTVHumanBridge bridge = new GIFTVHumanBridge();
	bridge.bindToGateway(receiver);
    }
    
    
}
