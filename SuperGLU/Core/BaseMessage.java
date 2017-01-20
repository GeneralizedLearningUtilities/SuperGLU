package Core;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This class is a superclass for all system messages that are sent and received
 * @author auerbach
 *
 */
public class BaseMessage extends Serializable {

	public static final String CONTEXT_KEY = "context";
	
	
	/**
	*  Additional context for the message
	*/
	protected Map<String, Object> context;
	
	
	public BaseMessage(String id, Map<String, Object> context)
	{
		super(id);
		
		if(context == null)
			this.context = new HashMap<>();
		else
			this.context = context;
	}
	
	
	public BaseMessage()
	{
		super();
		this.context = new HashMap<>();
	}


	public boolean hasContextValue(String key) {
		return this.context.containsKey(key);
	}


	public Map<String, Object> getContext() {
		return this.context;
	}


	public Set<String> getContextKeys() {
		return this.context.keySet();
	}


	public Object getContextValue(String key, Object defaultValue) {
		return this.context.getOrDefault(key, defaultValue);
	}


	public Object getContextValue(String key) {
		return this.getContextValue(key, null);
	}


	public void setContextValue(String key, Object value) {
		this.context.put(key, value);
	}


	public void delContextValue(String key) {
		this.context.remove(key);
	}
	
	
	@Override
	public boolean equals(Object otherObject)
	{
		if(!super.equals(otherObject))
			return false;
		
		if(!(otherObject instanceof BaseMessage))
			return false;
		
		Message other = (Message) otherObject;
				
		if(!fieldIsEqual(this.context, other.context))
			return false;

		
		return true;
	}
	
	
	@Override
	/**
	 *  
     *   Generate a hash value for the message.
	 */
	public int hashCode()
	{
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		
		if(this.context != null)
			result = result * arbitraryPrimeNumber + this.context.hashCode();
		
		return result;
	}
	
	
//Serialization/Deserialization	
	@Override
	public StorageToken saveToToken()
	{
		StorageToken result = super.saveToToken();
		result.setItem(CONTEXT_KEY, SerializationConvenience.tokenizeObject(this.context));
		
		return result;
	}
	
	
	@Override
	public void initializeFromToken(StorageToken token)
	{
		super.initializeFromToken(token);
		this.context = (Map<String, Object>)SerializationConvenience.untokenizeObject(token.getItem(CONTEXT_KEY, true, new HashMap<>()));
	}
}
