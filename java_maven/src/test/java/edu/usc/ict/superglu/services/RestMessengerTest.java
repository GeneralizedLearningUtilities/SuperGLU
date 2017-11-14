package edu.usc.ict.superglu.services;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import edu.usc.ict.superglu.core.HTTPRequestVerbEnum;
import edu.usc.ict.superglu.core.RESTMessage;

public class RestMessengerTest {

	
	public RESTMessenger messenger;
	
	
	@Before
	public void setup()
	{
		messenger = new RESTMessenger("messenger");
	}
	
	
	@Test
	public void testSendRESTRequest() {
		
		
		RESTMessage msg = new RESTMessage(HTTPRequestVerbEnum.GET, "http://api.weather.gov", null);
		//RESTMessage msg = new RESTMessage(HTTPRequestVerbEnum.GET, "http://www.google.com", null);
		
		messenger.handleMessage(msg, "na");
		
	}

}
