package Examples.VHuman;

import java.io.IOException;

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

	//TODO: Remove this when we no longer need it.
	protected VHMsg vhmsg;

	public GIFTVHumanBridge(ServiceConfiguration config) {
		super(config.getId(), null, null, null, null);

		String brokerHost = (String) config.getParams().get(BROKER_HOST_PARAM_KEY);
		int brokerPort = (int) config.getParams().get(BROKER_PORT_PARAM_KEY);

		this.vhmsg = new VHMsg(brokerHost, Integer.toString(brokerPort), "DEFAULT_SCOPE");
		this.vhmsg.openConnection();

	}

	public GIFTVHumanBridge(String brokerURL) {
		super("GIFT_VHUMAN_BRIDGE", null, null, null, null);

		String brokerHost = brokerURL.split(":")[1].split("//")[1];
		String brokerPort = brokerURL.split(":")[2];

		this.vhmsg = new VHMsg(brokerHost, brokerPort, "DEFAULT_SCOPE");
		this.vhmsg.openConnection();
	}

	@Override
	public void receiveMessage(BaseMessage msg) {
		super.receiveMessage(msg);
		
		
		if (msg instanceof GIFTMessage) {

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

	public void disconnect() {
		vhmsg.closeConnection();
	}
}
