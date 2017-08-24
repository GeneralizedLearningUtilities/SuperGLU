package Examples.VHuman;

import Core.BaseMessage;
import Core.MessagingGateway;
import Core.VHMessage;
import Core.Config.ServiceConfiguration;
import edu.usc.ict.vhmsg.VHMsg;

/**
 * This class is the internal service that will route received virtual human
 * messages to vhmsg.  It will also attempt to convert non-VHuman messages  into VHuman messages.
 * 
 * @author auerbach
 *
 */

public class GIFTVHumanBridge extends MessagingGateway {
	
	public static final String BROKER_HOST_PARAM_KEY = "brokerHost";
	public static final String BROKER_PORT_PARAM_KEY = "brokerPort";
	
	
	protected VHMsg vhmsg;
	
	public GIFTVHumanBridge(ServiceConfiguration config)
	{
		super(config.getId(), null, null, null, null);
		
		
		String brokerHost = (String)config.getParams().get(BROKER_HOST_PARAM_KEY);
		int brokerPort = (int)config.getParams().get(BROKER_PORT_PARAM_KEY);
		
		
		this.vhmsg = new VHMsg(brokerHost, Integer.toString(brokerPort), "DEFAULT_SCOPE");
		this.vhmsg.openConnection();


		
	}
	
	
	public GIFTVHumanBridge(String brokerURL) {
		super("GIFT_VHUMAN_BRIDGE", null, null, null, null);

		String[] split = brokerURL.split(":");

		String brokerHost = brokerURL.split(":")[1].split("//")[1];
		String brokerPort = brokerURL.split(":")[2];

		this.vhmsg = new VHMsg(brokerHost, brokerPort, "DEFAULT_SCOPE");
		this.vhmsg.openConnection();
	}

	@Override
	public void receiveMessage(BaseMessage msg) {
		super.receiveMessage(msg);

		// attempt to convert the recieved message to a vhuman message.
		BaseMessage convertedMessage = super.convertMessages(msg, VHMessage.class);

		if (convertedMessage != null && convertedMessage instanceof VHMessage) {
			VHMessage convertedVHMessage = (VHMessage) convertedMessage;

			// send out the message if it was successfully converted.
			vhmsg.sendMessage(convertedVHMessage.getFirstWord(), convertedVHMessage.getBody());
		}
	}

	public void disconnect() {
		vhmsg.closeConnection();
	}
}
