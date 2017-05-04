package Core.Tests;

import java.io.Console;
import java.util.function.Predicate;

import org.slf4j.LoggerFactory;

import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOServer;

import Core.BaseMessage;
import Core.BaseMessagingNode;
import Core.HTTPMessagingGateway;
import Core.MessagingGateway;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 * This is a test class for the HTTP Messaging Gateway
 * @author auerbach
 *
 */

public class MinimalHttpsServer extends BaseMessagingNode
{ 
    public MinimalHttpsServer(String anId, MessagingGateway gateway, Predicate<BaseMessage> conditions)
    {
	super(anId, conditions, null);
	
	
	
    }
    
    
    

    @Override
    public void receiveMessage(BaseMessage msg)
    {
	super.receiveMessage(msg);
	
	String msgAsString = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
	
	//For now we'll just log the messages as they come in.
	log.info(msgAsString);
	
	sendMessage(msg);
    }




    public static void main(String[] args)
    {
	
	Configuration config = new Configuration();
	
	config.setPort(5333);
	
	SocketIOServer socketIO = new SocketIOServer(config);
	
	MessagingGateway gateway = new HTTPMessagingGateway("httpGatweay", null, null, null, socketIO);
	
	MinimalHttpsServer server = new MinimalHttpsServer("server", gateway, null);
	
	gateway.addNode(server);

    }

}
