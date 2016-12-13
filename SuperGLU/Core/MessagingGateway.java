package Core;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.logging.Level;

/**
 * Messaging Node specifically designed to act as a entry/exit point between systems.
 * @author auerbach
 *
 */

public class MessagingGateway extends BaseMessagingNode {

	private Map<String, BaseMessagingNode> nodes;
	private Map<String, Object> scope;
	
	
	
	public MessagingGateway(String anId, MessagingGateway gateway, Map<String, Object> scope, Collection<BaseMessagingNode> nodes, Predicate<Message> conditions) {
		super(anId, gateway, conditions);
		if(scope == null)
			this.scope = new HashMap<>();
		else
			this.scope = scope;
		
		this.nodes = new HashMap<>();
		if(nodes != null)
		{
			for(BaseMessagingNode node : nodes)
			{
				this.nodes.put(node.id, node);
			}
		}
	}
	
	
	/**
	 *  """ When gateway receives a message, it distributes it to child nodes """
	 */
	@Override
	public void receiveMessage(Message msg)
	{
		super.receiveMessage(msg);
		this.distributeMessage(msg, null);
	}
	
	/**
	 *  """ Send a message from a child node to parent and sibling nodes """
	 * @param msg Message to be sent
	 * @param senderId Sender ID
	 */
	public void dispatchMessage(Message msg, String senderId)
	{
		this.addContextDataToMsg(msg);
		msg.setContextValue(ORIGINATING_SERVICE_ID_KEY, senderId);
		log.log(Level.INFO, "Message DISPATCH");
		log.log(Level.INFO, this.messageToString(msg));
		this.sendMessage(msg);
		log.log(Level.INFO, "Message DISPATCH SENT: " + this.messageToString(msg));
		this.distributeMessage_impl(this.nodes, msg, senderId);
		log.log(Level.INFO, "Message DISTRIBUTED: " + this.messageToString(msg));
	}
	
	/**
	 * """ Pass a message down all interested children (except sender) """
	 * @param msg
	 * @param senderId
	 */
	public void distributeMessage(Message msg, String senderId)
	{
		this.distributeMessage_impl(this.nodes, msg, senderId);
	}
	
	/**
	 * Internal implementation of DistributeMessage
	 *  """ Implement passing a message down all interested children (except sender) """
	 * @param nodes
	 * @param msg
	 * @param senderId
	 */
	protected void distributeMessage_impl(Map<String, BaseMessagingNode> nodes, Message msg, String senderId)
	{
		for(BaseMessagingNode node : nodes.values())
		{
			if(node.id != senderId && node.getMessageConditions().test(msg))
				node.receiveMessage(msg);
		}
	}
	
	
	//Manage Child Nodes
	public void addNodes(List<BaseMessagingNode> newNodes)
	{
		for(BaseMessagingNode node : newNodes)
			node.bindToGateway(this);
	}
	
	
	public Collection<BaseMessagingNode> getNodes()
	{
		return this.nodes.values();
	}
	

	/**
	 * """ Register the signatures of messages that the node is interested in """
	 * @param node
	 */
	public void register(BaseMessagingNode node)
	{
		this.nodes.put(node.id, node);
	}
	
	/**
	 *  """ Take actions to remove the node from the list """
	 * @param node
	 */
	public void unregister(BaseMessagingNode node)
	{
		if(this.nodes.containsKey(node.id))
			this.nodes.remove(node.id);
	}
	
	/**
	 * """ Add extra context to the message, if not present """
	 * @param msg
	 */
	public void addContextDataToMsg(Message msg)
	{
		for(String key : this.scope.keySet())
		{
			if(!msg.hasContextValue(key))
				msg.setContextValue(key, this.scope.get(key));
		}
	}
	
	
	
	
}
