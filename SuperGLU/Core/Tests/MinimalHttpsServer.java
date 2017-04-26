package Core.Tests;

import java.util.function.Predicate;
import java.util.logging.Level;
import java.util.logging.Logger;

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

    private Logger log = Logger.getLogger(this.getClass().getName());
    
    
    public MinimalHttpsServer(String anId, MessagingGateway gateway, Predicate<BaseMessage> conditions)
    {
	super(anId, gateway, conditions);
	// TODO Auto-generated constructor stub
    }
    
    
    

    @Override
    public void receiveMessage(BaseMessage msg)
    {
	super.receiveMessage(msg);
	
	String msgAsString = SerializationConvenience.serializeObject(msg, SerializationFormatEnum.JSON_FORMAT);
	
	//For now we'll just log the messages as they come in.
	log.log(Level.INFO, msgAsString);
    }




    public static void main(String[] args)
    {
	Configuration config = new Configuration();
	
	config.setPort(5333);
	
	SocketIOServer socketIO = new SocketIOServer(config);
	
	MessagingGateway gateway = new HTTPMessagingGateway("httpGatweay", null, null, null, null, socketIO);
	
	MinimalHttpsServer server = new MinimalHttpsServer("server", gateway, null);

    }

}
