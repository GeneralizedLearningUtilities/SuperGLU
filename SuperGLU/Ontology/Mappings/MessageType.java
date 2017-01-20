package Ontology.Mappings;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageType extends Serializable {
	
	public static final String MESSAGE_TYPE_NAME_KEY = "messageTypeName";
	public static final String MESSAGE_TYPE_MINVERSION_KEY = "messageTypeMinversion";
	public static final String MESSAGE_TYPE_MAXVERSION_KEY = "messageTypeMaxversion";
	public static final String MESSAGE_TYPE_MESSAGETEMPLATE_KEY = "messageTypeMessagetemplate";
	
	private String Message_Name;
	private float min_Version;
	private float max_Version;
	public MessageTemplate messageTypeTemplate = new MessageTemplate();
	
	//CONSTRUCTORS
	public MessageType(String name, float minversion, float maxversion)
	{
		this.Message_Name=name;
		this.min_Version=minversion;
		this.max_Version=maxversion;
	}
	
	public MessageType()
	{
		this.Message_Name="";
		this.max_Version=0.0f;
		this.min_Version=0.0f;
	}
	
	//GETTER AND SETTER METHODS
	public String getMessageName()
	{
		return Message_Name;
	}
	
	public void setMessageName(String name)
	{
		Message_Name=name;
	}
	
	public float getMinVersion()
	{
		return min_Version;
	}
	
	public void setMinVersion(float minversion)
	{
		min_Version=minversion;
	}
	
	public float getMaxVersion()
	{
		return max_Version;
	}
	
	public void setMaxVersion(float maxversion)
	{

		max_Version=maxversion;
	}
	
	
	
	
	
	
	
	//Equality Operations
	@Override
	public boolean equals(Object otherObject) {
		if(!super.equals(otherObject))
			return false;
		
		if(!(otherObject instanceof MessageType))
			return false;
		
		MessageType other = (MessageType)otherObject;
		
		if(!fieldIsEqual(this.Message_Name, other.Message_Name))
			return false;
		if(!fieldIsEqual(this.min_Version, other.min_Version))
			return false;
		if(!fieldIsEqual(this.max_Version, other.max_Version))
			return false;
		if(!fieldIsEqual(this.messageTypeTemplate, other.messageTypeTemplate))
			return false;
		
		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		
		if(this.Message_Name != null)
			result = result * arbitraryPrimeNumber + this.Message_Name.hashCode();
		if(this.min_Version != 0.0f)
			{
				result = result * arbitraryPrimeNumber + Float.hashCode(min_Version);
			}
		if(this.max_Version != 0.0f)
			{
				result = result * arbitraryPrimeNumber + Float.hashCode(max_Version);
			}
		if(this.messageTypeTemplate != null)
			result = result * arbitraryPrimeNumber + this.messageTypeTemplate.hashCode();
		
		
		return result;
		
	}

		
	//Serialization/Deserialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.Message_Name = (String)SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_NAME_KEY));
		this.min_Version = (float)SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MINVERSION_KEY));
		this.max_Version = (float)SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MAXVERSION_KEY));
		this.messageTypeTemplate = (MessageTemplate)SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_MESSAGETEMPLATE_KEY));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		result.setItem(MESSAGE_TYPE_NAME_KEY, SerializationConvenience.tokenizeObject(this.Message_Name));
		result.setItem(MESSAGE_TYPE_MINVERSION_KEY, SerializationConvenience.tokenizeObject(this.min_Version));
		result.setItem(MESSAGE_TYPE_MAXVERSION_KEY, SerializationConvenience.tokenizeObject(this.max_Version));
		result.setItem(MESSAGE_TYPE_MESSAGETEMPLATE_KEY, SerializationConvenience.tokenizeObject(this.messageTypeTemplate));
		return result;
	}
	
	
	
	
	    
}
