package edu.usc.ict.superglu;

import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOServer;
import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.HTTPMessagingGateway;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;

import java.util.function.Predicate;

/**
 * This is a test class for the HTTP Messaging Gateway
 *
 * @author auerbach
 */

public class MinimalHttpsServer extends BaseMessagingNode {
    public MinimalHttpsServer(String anId, MessagingGateway gateway, Predicate<BaseMessage> conditions) {
        super(anId, conditions, null, null, null, null);
    }


    @Override
    public boolean receiveMessage(BaseMessage msg) {
        super.receiveMessage(msg);

        String msgAsString = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);

        //For now we'll just log the messages as they come in.
        log.info(msgAsString);

        sendMessage(msg);
        
        return true;
    }


    public static void main(String[] args) {

        Configuration config = new Configuration();

        config.setPort(5333);

        SocketIOServer socketIO = new SocketIOServer(config);

        MessagingGateway gateway = new HTTPMessagingGateway("httpGatweay", null, null, null, null, socketIO, null, null);

        MinimalHttpsServer server = new MinimalHttpsServer("server", gateway, null);

        gateway.addNode(server);

    }

}
