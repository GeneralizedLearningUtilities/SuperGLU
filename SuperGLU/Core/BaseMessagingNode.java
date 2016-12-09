package Core;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

import Util.Pair;

public class BaseMessagingNode{
	
	private String id;
	private MessagingGateway gateway;
	private Map<String,Pair<Message, Consumer<Message>>> requests;
	
	
	
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
		
	}
	
	
	
	public void bindToGateway(MessagingGateway gateway)
	{
		
	}
	
	
	public void unbindToGateway()
	{
		
	}
	

	private Collection<Pair<Message, Consumer<Message>>> getRequests()
	{
		return this.requests.values();
	}
	
	
	private void addRequest(Message msg, Consumer<Message> callback)
	{
		if(callback != null)
		{
			Message clone = (Message)msg.clone(false);
			Pair<Message, Consumer<Message>> messageAndCallback = new Pair<Message, Consumer<Message>>(clone, callback);
			
			this.requests.put(msg.getId(), messageAndCallback);
		}
	}
	
	
	private void makeRequest(Message msg, Consumer<Message> callback)
	{
		this.addRequest(msg, callback);
		this.sendMessage(msg);
	}
	
	
	private void triggerRequests(Message msg)
	{
		String convoId = (String)msg.getContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, null);
		if(convoId != null && this.requests.containsKey(convoId))
		{
			String key = convoId;
			Pair<Message, Consumer<Message>> value = this.requests.get(key);
			Message oldMsg = value.getFirst();
			Consumer<Message> callback = value.getSecond();
			if(!oldMsg.getSpeechAct().equals(SpeechActEnum.REQUEST_WHENEVER_ACT))
				this.requests.remove(key);
		}
	}
	
	
	private Message createRequestReply(Message msg)
	{
		String oldId = msg.getId();
		Message copy = (Message)msg.clone(true);
		copy.setContextValue(Message.CONTEXT_CONVERSATION_ID_KEY, oldId);
		return copy;
	}
	
	
	
}
