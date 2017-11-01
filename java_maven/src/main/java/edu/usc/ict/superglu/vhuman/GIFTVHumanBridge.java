package edu.usc.ict.superglu.vhuman;

import edu.usc.ict.superglu.core.*;
import edu.usc.ict.superglu.core.config.GatewayBlackWhiteListConfiguration;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * This class is the internal service that will route received virtual human
 * messages to vhmsg. It will also attempt to convert non-VHuman messages into
 * VHuman messages.
 *
 * @author auerbach
 */

public class GIFTVHumanBridge extends MessagingGateway {

    public static final String BROKER_HOST_PARAM_KEY = "brokerHost";
    public static final String BROKER_PORT_PARAM_KEY = "brokerPort";

    public static final String GIFT_DOMAIN_SESSION_ID_KEY = "GIFTDomainSessionID";
    public static final String GIFT_USER_NAME_KEY = "GIFTUserName";
    public static final String GIFT_USER_ID_KEY = "GIFTUserID";

    public GIFTVHumanBridge(ServiceConfiguration config) {
        super(config.getId(), null, null, null, null, config);

        this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, 0);
        this.context.put(GIFT_USER_ID_KEY, 0);
        //	this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, sessionID.intValue());
    }

    public GIFTVHumanBridge(String brokerURL) {
        super("GIFT_VHUMAN_BRIDGE", null, null, null, null, new ServiceConfiguration());
    }


    //TODO:Remove this hack ASAP.  Once the module is working properly we can destroy this.
    private void addGIFTVariablesToContext(GIFTMessage msg) {
        BigDecimal sessionID = (BigDecimal) msg.getPayload().getItem("SessionId", true, null);

        if (sessionID != null) {
            this.context.put(GIFT_DOMAIN_SESSION_ID_KEY, sessionID.intValue());
        }

        BigDecimal userID = (BigDecimal) msg.getPayload().getItem("UserId", true, null);

        if (userID != null) {
            this.context.put(GIFT_USER_ID_KEY, userID.intValue());
        }


        String userName = (String) msg.getPayload().getItem("userName", true, null);

        if (userName != null) {
            this.context.put(GIFT_USER_NAME_KEY, userName);
        }
    }

    @Override
    public boolean receiveMessage(BaseMessage msg) {
        super.receiveMessage(msg);


        if (msg instanceof GIFTMessage) {

            addGIFTVariablesToContext((GIFTMessage) msg);

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
        } else if (msg instanceof Message) {

            if (((Message) msg).getResult() instanceof Integer) {
                Integer result = (Integer) ((Message) msg).getResult();
                ((Message) msg).setResult(result.doubleValue());
            }

            BaseMessage convertedMessage = super.convertMessages(msg, GIFTMessage.class);

            if (convertedMessage != null && convertedMessage instanceof GIFTMessage) {
                sendMessage(convertedMessage);
            }


        }
        
        return true;
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
