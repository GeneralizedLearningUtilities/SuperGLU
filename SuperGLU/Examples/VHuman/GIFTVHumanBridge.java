package Examples.VHuman;

import java.util.ArrayList;
import java.util.List;

import Core.ActiveMQTopicConfiguration;
import Core.ActiveMQTopicMessagingGateway;
import Core.BaseMessage;
import Core.ExternalMessagingHandler;
import Core.HTTPMessagingGateway;
import Core.MessagingGateway;
import Core.VHMessage;
import edu.usc.ict.vhmsg.VHMsg;

/**
 * This class is the internal service that will route received virtual human
 * messages to vhmsg
 * 
 * @author auerbach
 *
 */

public class GIFTVHumanBridge extends MessagingGateway {
	protected VHMsg vhmsg;

	public GIFTVHumanBridge(String brokerURL) {
		super("GIFT_VHUMAN_BRIDGE", null, null, null, null);

		String[] split = brokerURL.split(":");

		String brokerHost = brokerURL.split(":")[1].split("//")[1];
		String brokerPort = brokerURL.split(":")[2];

		this.vhmsg = new VHMsg(brokerHost, brokerPort, "DEFAULT_SCOPE");
		this.vhmsg.openConnection();

		ActiveMQTopicConfiguration config = new ActiveMQTopicConfiguration("config", null, brokerURL);
		ActiveMQTopicMessagingGateway receiver = new ActiveMQTopicMessagingGateway("receiver", null, null, null, null,
				config);

		this.onBindToNode(receiver);

		ExternalMessagingHandler handler = new ExternalMessagingHandler() {

			@Override
			public void handleMessage(BaseMessage msg) {
				receiveMessage(msg);

			}
		};

		List<ExternalMessagingHandler> handlers = new ArrayList<>();
		handlers.add(handler);

		// HTTPMessagingGateway socketGateway = new
		// HTTPMessagingGateway("socketIOGateway", null, null, null, handlers,
		// S)

		receiver.addHandler(new ExternalMessagingHandler() {

			@Override
			public void handleMessage(BaseMessage msg) {
				receiveMessage(msg);

			}
		});
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

	public static void main(String[] args) {

		// GIFTVHumanBridge bridge = new GIFTVHumanBridge();
	}

}
