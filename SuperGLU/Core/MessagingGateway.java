package Core;

import java.util.List;
import java.util.Map;

/**
 * Messaging Node specifically designed to act as a entry/exit point between systems.
 * @author auerbach
 *
 */

public class MessagingGateway extends BaseMessagingNode {

	List<Base>
	
	
	
	public MessagingGateway(String anId, MessagingGateway gateway, Map<String, Object> scope) {
		super(anId, gateway);
		// TODO Auto-generated constructor stub
	}

	public void register(BaseMessagingNode node)
	{
		
	}
	
	
	public void unregister(BaseMessagingNode node)
	{
		
	}
	
	
	public void dispatchMessage(Message msg, String gatewayId)
	{
		
	}
}
