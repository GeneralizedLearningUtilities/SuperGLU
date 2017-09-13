package Examples.VHuman;

import java.io.IOException;
import java.math.BigDecimal;

import Core.BaseMessage;
import Core.GIFTMessage;
import Core.MessagingGateway;
import Core.VHMessage;
import Core.Config.ServiceConfiguration;
import edu.usc.ict.vhmsg.VHMsg;

/**
 * This class is the internal service that will route received virtual human
 * messages to vhmsg. It will also attempt to convert non-VHuman messages into
 * VHuman messages.
 * 
 * @author auerbach
 *
 */

public class GIFTVHumanBridge extends MessagingGateway {

	public static final String BROKER_HOST_PARAM_KEY = "brokerHost";
	public static final String BROKER_PORT_PARAM_KEY = "brokerPort";

	public static final String GIFT_DOMAIN_SESSION_ID_KEY = "GIFTDomainSessionID";
	public static final String GIFT_USER_NAME_KEY ="GIFTUserName";
	public static final String GIFT_USER_ID_KEY = "GIFTUserID";
	
	public GIFTVHumanBridge(ServiceConfiguration config) {
		super(config.getId(), null, null, null, null);
		
		this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, 0);
		this.context.put(GIFT_USER_ID_KEY, 0);
	//	this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, sessionID.intValue());
	}

	public GIFTVHumanBridge(String brokerURL) {
		super("GIFT_VHUMAN_BRIDGE", null, null, null, null);
	}
	
	
	//TODO:Remove this hack ASAP.  Once the module is working properly we can destroy this.
	private void addGIFTVariablesToContext(GIFTMessage msg)
	{
		BigDecimal sessionID = (BigDecimal) msg.getPayload().getItem("dsId", true, null);
		
		if(sessionID != null)
		{
			this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, sessionID.intValue());
		}
		
		BigDecimal userID = (BigDecimal)msg.getPayload().getItem("UserId", true, null);
		
		if(userID != null)
		{
			this.context.put(GIFT_USER_ID_KEY, userID.intValue());
		}
		
		
		String userName = (String)msg.getPayload().getItem("userName", true, null);
		
		if(userName != null)
		{
			this.context.put(GIFT_USER_NAME_KEY, userName);
		}
	}

	@Override
	public void receiveMessage(BaseMessage msg) {
		super.receiveMessage(msg);
		
		
		if (msg instanceof GIFTMessage) {

			addGIFTVariablesToContext((GIFTMessage)msg);
			
			// attempt to convert the recieved message to a vhuman message.
			BaseMessage convertedMessage = super.convertMessages(msg, VHMessage.class);

			if (convertedMessage != null && convertedMessage instanceof VHMessage) {
				// send out the message if it was successfully converted.
				sendMessage(convertedMessage);
			}
		} else if (msg instanceof VHMessage) {
			BaseMessage convertedMessage = super.convertMessages(msg, GIFTMessage.class);

			if (convertedMessage != null && convertedMessage instanceof GIFTMessage) {
				sendMessage(convertedMessage);
			}

			startVHuman((VHMessage) msg);
		} else if (msg instanceof Core.Message){
			
			BaseMessage convertedMessage = super.convertMessages(msg, GIFTMessage.class);

			if (convertedMessage != null && convertedMessage instanceof GIFTMessage) {
				sendMessage(convertedMessage);
			}
			
			
		}
	}

	// Special code to handle the startup of the virtual human
	private void startVHuman(VHMessage vhMessage) {
		Runtime rt = Runtime.getRuntime();

		try {
			if (vhMessage.getFirstWord().equals("vrComponent") && vhMessage.getBody().equals("nvb parser")) {
				rt.exec("cmd /c start /D ..\\VHuman\\gift\\ 02a-launch-unity-house.bat");
			}
			if (vhMessage.getFirstWord().equals("vrSpeech") && vhMessage.getBody().equals("interp user0001 1 1.0 normal THEREMIN NOSFERATU THERMOCOUPLE PATRONUS"))
				rt.exec("cmd /c start /D ..\\VHuman\\gift\\ 03b-spawn-brad.bat");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
