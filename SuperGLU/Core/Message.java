package Core;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

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

public class Message extends Serializable {

	public static String ID_KEY = "id";
	public static String ACTOR_KEY = "actor";
	public static String VERB_KEY = "verb";
	public static String OBJECT_KEY = "object";
	public static String RESULT_KEY = "result";
	public static String SPEECH_ACT_KEY = "speechAct";
	public static String TIMESTAMP_KEY = "timestamp";
	public static String CONTEXT_KEY = "context";
   

	
	//Context keys
	public static String SESSION_ID_CONTEXT_KEY = "sessionId";
	public static String CONTEXT_CONVERSATION_ID_KEY = "conversation-id";
	public static String CONTEXT_IN_REPLY_TO_KEY = "in-reply-to";
	public static String CONTEXT_REPLY_WITH_KEY = "reply-with";
	public static String CONTEXT_REPLY_BY_KEY = "reply-by";
	
	
	private static DateFormat timestampFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
	
	private String actor;
	private String verb;
	private String obj;
	private Object result;
	private SpeechActEnum speechAct;
	private Date timestamp;
	private Map<String, Object> context;
	
	
	public Message(String actor, String verb, String obj, Object result, SpeechActEnum speechAct, Date timestamp, Map<String, Object> context, String id)
	{
		super(id);
		this.actor = actor;
		this.verb = verb;
		this.obj = obj;
		this.result = result;
		this.speechAct = speechAct;
		this.timestamp = timestamp;
		
		if(context == null)
			this.context = new HashMap<>();
		else
			this.context = context;
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
		this.context = new HashMap<>();
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
	
	
	public boolean hasContextValue(String key)
	{
		return this.context.containsKey(key);
	}
	
	
	public Map<String, Object> getContext()
	{
		return this.context;
	}
	
	
	public Set<String> getContextKeys()
	{
		return this.context.keySet();
	}
	
	
	public Object getContextValue(String key, Object defaultValue)
	{
		return this.context.getOrDefault(key, defaultValue);
	}
	
	
	public Object getContextValue(String key)
	{
		return this.getContextValue(key, null);
	}

	
	public void setContextValue(String key, Object value)
	{
		this.context.put(key, value);
	}
	
	
	public void delContextValue(String key)
	{
		this.context.remove(key);
	}
	

	//Comparators
	@Override
	public boolean equals(Object otherObject)
	{
		if(otherObject == null)
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
	public int hashCode()
	{//NOTE: the python version does not include the context when computing the hashcode so I didn't either.
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
