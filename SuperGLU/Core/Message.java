package Core;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 *
 * A message class, for passing data between components.  Messages with special
 *   meaning or messages intended to fit specific specifications should subclass
 *   this message class.  This message that expands on the Tin Can API, in terms
 *   of information available.
 * 
 * @author auerbach
 *
 */

public class Message extends BaseMessage {

	public static String ID_KEY = "id";
	public static String ACTOR_KEY = "actor";
	public static String VERB_KEY = "verb";
	public static String OBJECT_KEY = "object";
	public static String RESULT_KEY = "result";
	public static String SPEECH_ACT_KEY = "speechAct";
	public static String TIMESTAMP_KEY = "timestamp";
	
   

	
	//Context keys
	public static String SESSION_ID_CONTEXT_KEY = "sessionId";
	public static String CONTEXT_CONVERSATION_ID_KEY = "conversation-id";
	public static String CONTEXT_IN_REPLY_TO_KEY = "in-reply-to";
	public static String CONTEXT_REPLY_WITH_KEY = "reply-with";
	public static String CONTEXT_REPLY_BY_KEY = "reply-by";
	
	
	private static DateFormat timestampFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	
    /**
     * The actor performing the verb
     */
	private String actor;
    
    /**
     *  A verb, which is an action that is occurring or has occurred
     */
	private String verb;
	
	/**
	 *  A target of the verb action, being acted upon or relating the actor and object
	 */
	private String obj;
	
	/**
	 * The outcome of this interaction
	 */
	private Object result;
	
	/**
	 *  A speech act declaring the intent of this message, from SpeechActEnum
	 */
	private SpeechActEnum speechAct;
	
	/**
	 * The timestamp for when this message refers to, ISO 8601 formatted
	 */
	private Date timestamp;
	
	
	
	public Message(String actor, String verb, String obj, Object result, SpeechActEnum speechAct, Date timestamp, Map<String, Object> context, String id)
	{
		super(id, context);
		this.actor = actor;
		this.verb = verb;
		this.obj = obj;
		this.result = result;
		this.speechAct = speechAct;
		
		if(timestamp == null)
			this.timestamp = new Date();
		else
			this.timestamp = timestamp;
	}
	
	
	public Message()
	{
		super();
		this.actor = null;
		this.verb = null;
		this.obj = null;
		this.result = null;
		this.speechAct = SpeechActEnum.INFORM_ACT;
		this.timestamp = new Date();
	}


	//ACCESSORS
	public String getActor() {
		return actor;
	}


	public void setActor(String actor) {
		this.actor = actor;
	}


	public String getVerb() {
		return verb;
	}


	public void setVerb(String verb) {
		this.verb = verb;
	}


	public String getObj() {
		return obj;
	}


	public void setObj(String obj) {
		this.obj = obj;
	}


	public Object getResult() {
		return result;
	}


	public void setResult(Object result) {
		this.result = result;
	}


	public SpeechActEnum getSpeechAct() {
		return speechAct;
	}


	public void setSpeechAct(SpeechActEnum speechAct) {
		this.speechAct = speechAct;
	}


	public Date getTimestamp() {
		return timestamp;
	}


	public void setTimestamp(Date timestamp) {
		this.timestamp = timestamp;
	}
	
	
	public void updateTimestamp()
	{
		this.timestamp = new Date();
	}
	
	
	//Comparators
	@Override
	public boolean equals(Object otherObject)
	{
		if(!super.equals(otherObject))
			return false;
		if(!(otherObject instanceof Message))
			return false;
		
		Message other = (Message) otherObject;
	
		if(!this.id.equals(other.id))
			return false;
		
		if(!this.actor.equals(other.actor))
			return false;
		if(!this.verb.equals(other.verb))
			return false;
		if(!this.obj.equals(other.obj))
			return false;
		if(!this.result.equals(other.result))
			return false;
		if(!this.speechAct.equals(other.speechAct))
			return false;
		if(!this.context.equals(other.context))
			return false;
		if(!this.timestamp.equals(other.timestamp))
			return false;
		
		return true;
	}
	
	
	@Override
	/**
	 *  
     *   Generate a hash value for the message.  This does not take the context into account,
     *   as the context does not have a static set of values.
	 */
	public int hashCode()
	{
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		
		if(this.actor != null)
			result = result * arbitraryPrimeNumber + this.actor.hashCode();
		if(this.verb != null)
			result = result *arbitraryPrimeNumber + this.verb.hashCode();
		if(this.obj != null)
			result = result * arbitraryPrimeNumber + this.obj.hashCode();
		if(this.result != null)
			result = result * arbitraryPrimeNumber + this.result.hashCode();
		result = result * arbitraryPrimeNumber + this.speechAct.hashCode();
		if(this.timestamp != null)
			result = result * arbitraryPrimeNumber + this.timestamp.hashCode();
		
		return result;
	}
	
	
//Serialization/Deserialization	
	@Override
	public StorageToken saveToToken()
	{
		StorageToken result = super.saveToToken();
		
		result.setItem(ACTOR_KEY, this.actor);
		result.setItem(VERB_KEY, this.verb);
		result.setItem(OBJECT_KEY, this.obj);
		result.setItem(RESULT_KEY, SerializationConvenience.tokenizeObject(this.result));
		result.setItem(SPEECH_ACT_KEY, this.speechAct.toString());
		result.setItem(TIMESTAMP_KEY, timestampFormat.format(this.timestamp));
		result.setItem(CONTEXT_KEY, SerializationConvenience.tokenizeObject(this.context));
		
		return result;
	}
	
	
	@Override
	public void initializeFromToken(StorageToken token)
	{
		super.initializeFromToken(token);
		
		this.actor = (String)token.getItem(ACTOR_KEY, true, null);
		this.verb = (String)token.getItem(VERB_KEY, true, null);
		this.obj = (String)token.getItem(OBJECT_KEY, true, null);
		this.result = SerializationConvenience.untokenizeObject(token.getItem(RESULT_KEY, true, null));
		this.speechAct = SpeechActEnum.getEnum((String) token.getItem(SPEECH_ACT_KEY, true, SpeechActEnum.INFORM_ACT));
		try {
			this.timestamp = timestampFormat.parse((String)token.getItem(TIMESTAMP_KEY, true, null));
		} catch (ParseException e) {
			e.printStackTrace();
			System.err.println("failed to parse timestamp of message, using current time as timestamp");
			this.timestamp = new Date();
		}
		
		this.context = (Map<String, Object>)SerializationConvenience.untokenizeObject(token.getItem(CONTEXT_KEY, true, new HashMap<>()));
	}
	
	
	
}
