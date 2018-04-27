package edu.usc.ict.superglu.services;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.stream.Collectors;

import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.impl.client.HttpClients;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.RESTMessage;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;

/**
 * this service is designed to take an incoming message and (if possible) turn it into a rest request.
 * It will then distribute the result of that request once it receives it.
 * @author auerbach
 *
 */

public class RESTMessenger extends BaseService implements ResponseHandler<RESTMessage> {
	
	
	private HttpClient client;
	
	private Queue<RESTMessage> messages;

	
	public RESTMessenger(String id)
	{
		super(id, null);
		
		this.client = HttpClients.createDefault();
		this.messages = new LinkedBlockingQueue<>();
	}
	
	
	public RESTMessenger(ServiceConfiguration config) {
		super(config.getId(), null, null, config.getBlackList(), config.getWhiteList());
		
		this.client = HttpClients.createDefault();
		
	}
	
	
	


	@Override
	public void handleMessage(BaseMessage msg, String senderId) {
		super.handleMessage(msg, senderId);
		
		if(msg instanceof RESTMessage)
		{
			RESTMessage restMsg = (RESTMessage)msg;
			HttpUriRequest request = restMsg.createRequest();
			try {
				this.messages.add(restMsg);
				this.client.execute(request, this);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				log.warn(e.toString());
			}
		}
		
	}


	@Override
	public RESTMessage handleResponse(HttpResponse response) throws ClientProtocolException, IOException {
		
		Header[] contentTypeHeaders = response.getHeaders("content-type");
		
		RESTMessage result = null;
		
		if(contentTypeHeaders.length > 0)
		{
			Header contentType = contentTypeHeaders[0];
			
			if(contentType.getValue().contains("json"))
			{
			
				InputStream contentStream = response.getEntity().getContent();	
				String contentAsString = new BufferedReader(new InputStreamReader(contentStream)).lines().collect(Collectors.joining("\n"));
				
				result = this.messages.remove();
				result.setPayload(SerializationConvenience.makeNative(contentAsString, SerializationFormatEnum.JSON_STANDARD_FORMAT));
				
				this.sendMessage(result);
				
			}
			else
			{
				result = this.messages.remove();
				this.sendMessage(result);
			}
		}
		else
		{
			result = this.messages.remove();
			this.sendMessage(result);
		}
		
		
		return result;
	
	}
	
	
	
	
	
	
	
	
	
	
	

}
