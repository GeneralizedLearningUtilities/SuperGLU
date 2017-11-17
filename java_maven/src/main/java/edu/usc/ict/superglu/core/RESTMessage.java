package edu.usc.ict.superglu.core;

import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpRequest;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpUriRequest;

import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.StorageToken;

/**
 * This is a transition form for converting superglu messages into REST requests
 * 
 * @author auerbach
 *
 */
public class RESTMessage extends BaseMessage {

	public static final String VERB_KEY = "verb";
	public static final String DESTINATION_KEY = "destination";
	public static final String PAYLOAD_KEY = "payload";
	public static final String HEADERS_KEY = "headers";

	private HTTPRequestVerbEnum verb;

	private String destination;

	private StorageToken payload;
	
	private Map<String, String> headers;

	public RESTMessage() {
		super();
		this.verb = HTTPRequestVerbEnum.GET;
		this.destination = null;
		this.payload = null;
		this.headers = new HashMap<>();
	}

	public RESTMessage(HTTPRequestVerbEnum verb, String destination, StorageToken payload, Map<String,String> headers) {
		super();
		this.verb = verb;
		this.destination = destination;
		this.payload = payload;
		this.headers = headers;
		
	}
	
	public Map<String, String> getHeaders()
	{
		return headers;
	}
	
	
	public void setHeaders(Map<String, String> headers)
	{
		this.headers = headers;
	}
	

	public HTTPRequestVerbEnum getVerb() {
		return verb;
	}

	public void setVerb(HTTPRequestVerbEnum verb) {
		this.verb = verb;
	}

	public String getDestination() {
		return destination;
	}

	public void setDestination(String destination) {
		this.destination = destination;
	}

	public StorageToken getPayload() {
		return payload;
	}

	public void setPayload(StorageToken payload) {
		this.payload = payload;
	}

	@Override
	public boolean equals(Object otherObject) {
		if (!super.equals(otherObject))
			return false;

		if (!(otherObject instanceof RESTMessage))
			return false;

		RESTMessage other = (RESTMessage) otherObject;

		if (!fieldIsEqual(this.verb, other.verb))
			return false;

		if (!fieldIsEqual(this.payload, other.payload))
			return false;

		if (!fieldIsEqual(this.destination, other.destination))
			return false;
		
		if (!fieldIsEqual(this.headers, other.headers))
			return false;

		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;

		if (this.verb != null)
			result = result * arbitraryPrimeNumber + this.verb.hashCode();
		if (this.payload != null)
			result = result * arbitraryPrimeNumber + this.payload.hashCode();
		if (this.destination != null)
			result = result * arbitraryPrimeNumber + this.destination.hashCode();
		if (this.headers != null)
			result  = result * arbitraryPrimeNumber + this.headers.hashCode();
		
		return result;
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();

		result.setItem(VERB_KEY, SerializationConvenience.tokenizeObject(this.verb.toString()));
		result.setItem(DESTINATION_KEY, SerializationConvenience.tokenizeObject(this.destination));
		result.setItem(PAYLOAD_KEY, SerializationConvenience.tokenizeObject(payload));
		result.setItem(HEADERS_KEY, SerializationConvenience.tokenizeObject(this.headers));

		return result;
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);

		this.verb = HTTPRequestVerbEnum.getEnum((String) SerializationConvenience.untokenizeObject(token.getItem(VERB_KEY, true, "GET")));
		this.destination = (String) SerializationConvenience.untokenizeObject(token.getItem(DESTINATION_KEY, true, ""));
		this.payload = (StorageToken) SerializationConvenience.untokenizeObject(token.getItem(PAYLOAD_KEY, true, new StorageToken()));
		this.headers = (Map<String, String>) SerializationConvenience.untokenizeObject(token.getItem(HEADERS_KEY, true, new HashMap<>()));
	}
	
	
	public HttpUriRequest createRequest()
	{
		HttpUriRequest result = null;
		
		if(this.verb.equals(HTTPRequestVerbEnum.GET))
		{
			result = new HttpGet(destination);
			//result.addHeader("Content-type", "application/json");
		}
		else if(this.verb.equals(HTTPRequestVerbEnum.POST))
		{
			result = new HttpPost(destination);
		}
		else if(this.verb.equals(HTTPRequestVerbEnum.PUT))
		{
			result = new HttpPut(destination);
		}
		else if (this.verb.equals(HTTPRequestVerbEnum.DELETE))
		{
			result = new HttpDelete(destination);
		}
		
		
		for(String key : this.headers.keySet())
		{
			String value = this.headers.get(key);
			
			result.addHeader(key, value);
		}
		
		return result;
	}

}
