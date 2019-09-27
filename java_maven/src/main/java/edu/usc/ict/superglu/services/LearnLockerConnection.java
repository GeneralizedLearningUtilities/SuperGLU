package edu.usc.ict.superglu.services;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.json.simple.DeserializationException;
import org.json.simple.JsonObject;
import org.json.simple.Jsoner;

import edu.usc.ict.superglu.core.BaseMessage;
import edu.usc.ict.superglu.core.BaseMessagingNode;
import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingVerbConstants;
import edu.usc.ict.superglu.core.config.ServiceConfiguration;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import gov.adlnet.xapi.client.StatementClient;
import gov.adlnet.xapi.model.Statement;

public class LearnLockerConnection extends BaseService implements Runnable{
	
	private static final String AUTH_FILE_PATH ="authFilePath";
	private static final String URL_PROP_NAME = "url";
	private static final String USER_NAME_PROP_NAME = "userName";
	private static final String PASSWORD_PROP_NAME = "password";
	
	private String url;
	private String userName;
	private String password;
	
	private StatementClient client;


	private List<Statement> statementQueue;
	private boolean courseEnded = false;
	private Thread httpConnectionThread;
	
	
	public LearnLockerConnection(String id, String url, String userName, String password, StatementClient client)
	{
		super(id, null);
		
		this.url = url;
		this.userName =userName;
		this.password = password;
		this.client = client;
		this.statementQueue = new ArrayList<Statement>();
		httpConnectionThread = new Thread(this);
		httpConnectionThread.start();
	}
	
	
	public LearnLockerConnection(ServiceConfiguration config) {
		super(config.getId(), null, null, config.getBlackList(), config.getWhiteList());
		
		this.statementQueue = new ArrayList<>();
		
		String authFilePath = (String) config.getParams().get(AUTH_FILE_PATH);
		
		Properties prop = new Properties();

		this.statementQueue = new ArrayList<Statement>();
		httpConnectionThread = new Thread(this);
		httpConnectionThread.start();
		
		try
		{
			FileInputStream fstream  = new FileInputStream(authFilePath);
			prop.load(fstream);
			this.url =  prop.getProperty(URL_PROP_NAME);
			this.userName = prop.getProperty(USER_NAME_PROP_NAME);
			this.password = prop.getProperty(PASSWORD_PROP_NAME);
			fstream.close();
			
			client = new StatementClient(url, userName, password);
			
		}
		catch(Exception e)
		{
			throw new RuntimeException(e);
		}
	}
	
	
	@Override
	public void handleMessage(BaseMessage msg, String senderId) {
		super.handleMessage(msg, senderId);
	
		if(msg instanceof Message)
		{
			Message message = (Message)msg;
			if(message.getVerb().equals(MessagingVerbConstants.XAPI_LOG_VERB))
			{
				this.statementQueue.add((Statement) message.getResult());
			}
		}
	}
	
	
	@Override
	public void onUnbindToNode(BaseMessagingNode node) {
		super.onUnbindToNode(node);
		this.courseEnded = true;
	}


	@Override
	public void run() {
	
		while(!this.courseEnded || !this.statementQueue.isEmpty())
		{
			if(this.statementQueue.isEmpty())
			{
				try {
					Thread.sleep(1000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				continue;
			}
			
			Statement result = this.statementQueue.remove(0);
			try {
				client.postStatement(result);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		
	}
	

}
