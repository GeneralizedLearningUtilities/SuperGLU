package edu.usc.ict.superglu.core.blackwhitelist;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.GIFTMessage;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.VHMessage;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;
import edu.usc.ict.superglu.util.SuperGlu_Serializable;

/**
 * This class represents a single entry in the black or white lists.
 * 
 * The each of these fields can be filled with a value or a wildcard (*)
 * 
 * @author auerbach
 *
 */

public class BlackWhiteListEntry extends SuperGlu_Serializable {

	private static final String MESSAGE_TYPE_KEY = "messageType";
	private static final String VERSION_KEY = "version";
	private static final String MESSAGE_NAME_KEY = "messageName";
	
	private static final String WILDCARD = "*";
	
	public static final String GIFT_MESSAGE_TYPE = "GIFT";
	public static final String SUPERGLU_MESSAGE_TYPE = "SuperGLU";
	public static final String VHUMAN_MESSAGE_TYPE = "VHuman";
	
	

	private String messageType;
	private String version;
	private String messageName;

	public BlackWhiteListEntry() {
		this.messageType = null;
		this.version = null;
		this.messageName = null;
	}

	public BlackWhiteListEntry(String messageType, String version, String messageName) {
		this.messageType = messageType;
		this.messageName = messageName;
		this.version = version;
	}

	public BlackWhiteListEntry(String entryAsString) {
		String[] tokenizedString = entryAsString.split("\\.");

		if (tokenizedString.length < 3) {
			logger.error("Failed to parse black/white list entry: " + entryAsString);
			throw new RuntimeException("failed to parse black/white list entry :" + entryAsString);
		}

		this.messageType = tokenizedString[0];
		this.version = tokenizedString[1];
		this.messageName = tokenizedString[2];
	}

	@Override
	public boolean equals(Object otherObject) {
		if (!super.equals(otherObject))
			return false;

		BlackWhiteListEntry other = (BlackWhiteListEntry) otherObject;

		if (!fieldIsEqual(this.messageName, other.messageName))
			return false;

		if (!fieldIsEqual(this.messageType, other.messageType))
			return false;

		if (!fieldIsEqual(this.version, other.version))
			return false;

		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;

		if (this.messageName != null)
			result = result * arbitraryPrimeNumber + this.messageName.hashCode();

		if (this.messageType != null)
			result = result * arbitraryPrimeNumber + this.messageType.hashCode();

		if (this.version != null)
			result = result * arbitraryPrimeNumber + this.version.hashCode();

		return result;
	}
	
	

	@Override
	public String toString() {
		return this.messageType + "." + this.version + "." + this.messageName;
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);

		this.messageName = (String) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_NAME_KEY));
		this.messageType = (String) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TYPE_KEY));
		this.version = (String) SerializationConvenience.untokenizeObject(token.getItem(VERSION_KEY));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();

		result.setItem(MESSAGE_NAME_KEY, SerializationConvenience.tokenizeObject(this.messageName));
		result.setItem(MESSAGE_TYPE_KEY, SerializationConvenience.tokenizeObject(this.messageType));
		result.setItem(VERSION_KEY, SerializationConvenience.tokenizeObject(this.version));

		return result;
	}

	public String getMessageType() {
		return messageType;
	}

	public void setMessageType(String messageType) {
		this.messageType = messageType;
	}

	public String getVersion() {
		return version;
	}

	public void setVersion(String version) {
		this.version = version;
	}

	public String getMessageName() {
		return messageName;
	}

	public void setMessageName(String messageName) {
		this.messageName = messageName;
	}

	private boolean evaluateMessageType(BaseMessage msg)
	{
		if(this.messageType.equals(GIFT_MESSAGE_TYPE))
			return msg instanceof GIFTMessage;
		
		else if(this.messageType.equals(SUPERGLU_MESSAGE_TYPE))
			return msg instanceof Message;
		
		else if (this.messageType.equals(VHUMAN_MESSAGE_TYPE))
			return msg instanceof VHMessage;
		
		else if (this.messageType.equals(WILDCARD))
			return true;
		
		else 
			return false;
	}
	
	
	private boolean evaluateMessageVersion(BaseMessage msg)
	{
		//For now just accept wildcards
		if(this.version.equals(WILDCARD))
			return true;
		
		
		return false;
	}
	
	
	private boolean evaluateMessageName(BaseMessage msg)
	{
		if(this.messageName.equals(WILDCARD))
			return true;
		
		if(msg instanceof VHMessage)
			return this.messageName.equals(((VHMessage) msg).getFirstWord());
		
		if(msg instanceof Message)
			return this.messageName.equals(((Message) msg).getVerb());
		
		if(msg instanceof GIFTMessage)
			return this.messageName.equals(((GIFTMessage) msg).getHeader());
		
		return false;
	}
	
	
	public boolean evaluateMessage(BaseMessage msg) {
		
		if(!evaluateMessageType(msg))
			return false;
		
		if(!evaluateMessageVersion(msg))
			return false;
		
		if(!evaluateMessageName(msg))
			return false;
		
		return true;
	}

}
