package Core;

import java.util.HashMap;
import java.util.Map;

import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * generic wrapper for a GIFT message
 * @author auerbach
 *
 */
public class GIFTMessage extends BaseMessage {

	public static String HEADER_KEY = "header";
	public static String PAYLOAD_KEY = "payload";
	
	
	protected String header;
	
	protected String payload;
	
	
	public GIFTMessage(String id, Map<String, Object> context, String header, String payload)
	{
		super(id, context);
		
		if(header == null)
			this.header = "";
		else
			this.header = header;
		
		if(payload == null)
			this.payload = "";
		else
			this.payload = payload;
	}
	
	
	public GIFTMessage()
	{
		super();
		this.header = "";
		this.payload = "";
	}
	
	
	public String getHeader() {
		return header;
	}


	public void setHeader(String header) {
		this.header = header;
	}


	public String getPayload() {
		return payload;
	}


	public void setPayload(String payload) {
		this.payload = payload;
	}


	@Override
	public boolean equals(Object otherObject)
	{
		if(!super.equals(otherObject))
			return false;
		
		if(!(otherObject instanceof GIFTMessage ))
			return false;
		
		GIFTMessage other = (GIFTMessage)otherObject;
		
		if(!this.header.equals(other.header))
			return false;
		
		if(!this.payload.equals(other.payload))
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
			result = result * arbitraryPrimeNumber + this.header.hashCode();
		if(this.payload != null)
			result =  result * arbitraryPrimeNumber + this.payload.hashCode();
		
		return result;
	}
	

	//Serialization/Deserialization	
	@Override
	public StorageToken saveToToken()
	{
		StorageToken result = super.saveToToken();
		result.setItem(HEADER_KEY, SerializationConvenience.tokenizeObject(this.header));
		result.setItem(PAYLOAD_KEY, SerializationConvenience.tokenizeObject(this.payload));
		
		return result;
	}
	
	
	@Override
	public void initializeFromToken(StorageToken token)
	{
		super.initializeFromToken(token);
		this.header = (String)SerializationConvenience.untokenizeObject(token.getItem(HEADER_KEY, true, ""));
		this.payload = (String)SerializationConvenience.untokenizeObject(token.getItem(PAYLOAD_KEY, true, ""));
	}
}
