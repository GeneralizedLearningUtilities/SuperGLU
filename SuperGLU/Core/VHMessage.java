package Core;

import java.util.Map;

import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * Generic wrapper for a VH message.
 * @author auerbach
 *
 */
public class VHMessage extends BaseMessage {
	
	public static final String FIRST_WORD_KEY = "firstWord";
	public static final String VERSION_KEY = "version";
	public static final String BODY_KEY = "body";
	
	protected String firstWord;
	protected float version;
	protected String body;
	
	
	public VHMessage(String id, Map<String, Object> context, String firstWord, float version, String body)
	{
		super(id, context);
		
		if(firstWord == null)
			this.firstWord = "";
		else
			this.firstWord = firstWord;
		
		this.version = version;
		
		if(body == null)
			this.body = "";
		else
			this.body = body;
	}
	
	
	public VHMessage()
	{
		super();
		this.firstWord = "";
		this.body = "";
		this.version = -1.0f;
	}


	public String getFirstWord() {
		return firstWord;
	}


	public void setFirstWord(String firstWord) {
		this.firstWord = firstWord;
	}


	public float getVersion() {
		return version;
	}


	public void setVersion(float version) {
		this.version = version;
	}


	public String getBody() {
		return body;
	}


	public void setBody(String body) {
		this.body = body;
	}


	//Equality operators
	@Override
	public boolean equals(Object otherObject) {
		if(!super.equals(otherObject))
			return false;
		
		if(!(otherObject instanceof VHMessage))
			return false;
		
		VHMessage other = (VHMessage) otherObject;
		
		if(!fieldIsEqual(this.firstWord, other.firstWord))
			return false;
		
		if(this.version != other.version)
			return false;
		
		if(!fieldIsEqual(this.body, other.body))
			return false;
		
		return true;
	}


	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		
		if(this.firstWord != null)
			result = result * arbitraryPrimeNumber + firstWord.hashCode();
		
		result = result * arbitraryPrimeNumber + Float.hashCode(version);
		
		if(this.body != null)
			result = result * arbitraryPrimeNumber + body.hashCode();
		
		return result;
	}

	//Serialization
	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		result.setItem(FIRST_WORD_KEY, SerializationConvenience.tokenizeObject(this.firstWord));
		result.setItem(VERSION_KEY, SerializationConvenience.tokenizeObject(this.version));
		result.setItem(BODY_KEY, SerializationConvenience.tokenizeObject(this.body));
		return result;
	}


	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		
		this.firstWord = (String)SerializationConvenience.untokenizeObject(token.getItem(FIRST_WORD_KEY, true, ""));
		this.version = (Float)SerializationConvenience.untokenizeObject(token.getItem(VERSION_KEY, true, -1.0f));
		this.body = (String)SerializationConvenience.untokenizeObject(token.getItem(body, true, ""));
	}
	
	
	

}
