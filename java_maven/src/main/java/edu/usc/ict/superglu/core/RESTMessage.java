package edu.usc.ict.superglu.core;

import org.apache.http.HttpRequest;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;

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

	private HTTPRequestVerbEnum verb;

	private String destination;

	private StorageToken payload;

	public RESTMessage() {
		super();
		this.verb = HTTPRequestVerbEnum.GET;
		this.destination = null;
		this.payload = null;
	}

	public RESTMessage(HTTPRequestVerbEnum verb, String destination, StorageToken payload) {
		super();
		this.verb = verb;
		this.destination = destination;
		this.payload = payload;
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
		
		return result;
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();

		result.setItem(VERB_KEY, SerializationConvenience.tokenizeObject(this.verb.toString()));
		result.setItem(DESTINATION_KEY, SerializationConvenience.tokenizeObject(this.destination));
		result.setItem(PAYLOAD_KEY, SerializationConvenience.tokenizeObject(payload));

		return result;
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);

		this.verb = HTTPRequestVerbEnum.getEnum((String) SerializationConvenience.untokenizeObject(token.getItem(VERB_KEY, true, "GET")));
		this.destination = (String) SerializationConvenience.untokenizeObject(token.getItem(DESTINATION_KEY, true, ""));
		this.payload = (StorageToken) SerializationConvenience.untokenizeObject(token.getItem(PAYLOAD_KEY, true, new StorageToken()));
	}
	
	
	public HttpRequest createRequest()
	{
		HttpRequest result = null;
		
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
		
		return result;
	}

}
