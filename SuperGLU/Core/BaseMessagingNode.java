package Core;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import java.util.logging.Level;
import java.util.logging.Logger;

import Util.Pair;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;

/**
 *  """ Base class for messaging """
 * @author auerbach
 *
 */
public class BaseMessagingNode{
	
	private String id;
	private MessagingGateway gateway;
	private Map<String,Pair<Message, Consumer<Message>>> requests;
	
	private static boolean CATCH_BAD_MESSAGES = false;
	
	public BaseMessagingNode(String anId, MessagingGateway gateway)
	{
		this.id = anId;
		if(gateway != null)
			this.bindToGateway(gateway);
		
		this.requests = new HashMap<>();
		
	}
	
	
	public void receiveMessage(Message msg)
	{
		this.triggerRequests(msg);
	}
	
	
	public void sendMessage(Message msg)
	{
		Logger.getGlobal().log(Level.INFO, this.id + " is sending " + msg.toString());
		if(this.gateway != null)
		{
			this.gateway.dispatchMessage(msg, this.id);
			Logger.getGlobal().log(Level.INFO, "Actually sent it");
		}
	}
	
	// """ Function to check if this node is interested in this message type """
	public boolean getMessageConditions()
	{//TODO: figure out how this function works.
		return true;
	}
	
	
	public void bindToGateway(MessagingGateway gateway)
	{
		this.unbindToGateway();
		this.gateway = gateway;
		this.gateway.register(this);
	}
	
	
	public void unbindToGateway()
	{
		if(this.gateway != null)
			this.gateway.unregister(this);
	}
	

	protected Collection<Pair<Message, Consumer<Message>>> getRequests()
	{
		return this.requests.values();
	}
	
	
	protected void addRequest(Message msg, Consumer<Message> callback)
	{
		if(callback != null)
		{
			Message clone = (Message)msg.clone(false);
			Pair<Message, Consumer<Message>> messageAndCallback = new Pair<Message, Consumer<Message>>(clone, callback);
			
			this.requests.put(msg.getId(), messageAndCallback);
		}
	}
	
	
	protected void makeRequest(Message msg, Consumer<Message> callback)
	{
		this.addRequest(msg, callback);
		this.sendMessage(msg);
	}
	
	
	protected void triggerRequests(Message msg)
	{
		String convoId = (String)msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, null);
		if(convoId != null && this.requests.containsKey(convoId))
		{
			String key = convoId;
			Pair<Message, Consumer<Message>> value = this.requests.get(key);
			Message oldMsg = value.getFirst();
			Consumer<Message> callback = value.getSecond();
			callback.accept(msg);
			if(!oldMsg.getSpeechAct().equals(SpeechActEnum.REQUEST_WHENEVER_ACT))
				this.requests.remove(key);
		}
	}
	
	
	protected Message createRequestReply(Message msg)
	{
		String oldId = msg.getId();
		Message copy = (Message)msg.clone(true);
		copy.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId);
		return copy;
	}
	
	// # Pack/Unpack Messages
	public String messageToString(Message msg)
	{
		return msg.toString();
	}
	
	
	public Message stringToMessage(String msgAsString)
	{
		Message result = null;
		if(CATCH_BAD_MESSAGES)
		{
			
			try
			{
				result = (Message)SerializationConvenience.nativeizeObject(msgAsString, SerializationFormatEnum.JSON_FORMAT);
			}
			catch(Exception e)
			{
				Logger.getGlobal().log(Level.SEVERE, "ERROR: could not process message data received.  Received: " + msgAsString);
				Logger.getGlobal().log(Level.SEVERE, "Exception Caught:" + e.toString());
			}
		}
		else
		{
			result = (Message)SerializationConvenience.nativeizeObject(msgAsString, SerializationFormatEnum.JSON_FORMAT);
		}
		
		return result;
	}
	
	
	public List<String> messagesToStringList(List<Message> msgs)
	{
		List<String> result = new ArrayList<>();
		
		for(Message msg : msgs)
		{
			result.add(msg.toString());
		}
		
		return result;
	}
	
	
	public List<Message> stringListToMessages(List<String> strMsgs)
	{
		List<Message> result = new ArrayList<>();
		
		for(String strMsg : strMsgs)
		{
			Message msg = this.stringToMessage(strMsg);
			result.add(msg);
		}
		
		return result;
	}
	
	
	
}
