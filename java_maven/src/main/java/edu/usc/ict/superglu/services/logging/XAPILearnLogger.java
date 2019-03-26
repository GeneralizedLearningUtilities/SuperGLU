package edu.usc.ict.superglu.services.logging;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.UUID;

import com.google.gson.JsonElement;
import com.google.gson.JsonPrimitive;

import edu.usc.ict.superglu.core.BaseService;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.MessagingGateway;
import edu.usc.ict.superglu.core.MessagingVerbConstants;
import edu.usc.ict.superglu.core.SpeechActEnum;
import gov.adlnet.xapi.model.Account;
import gov.adlnet.xapi.model.Activity;
import gov.adlnet.xapi.model.ActivityDefinition;
import gov.adlnet.xapi.model.Agent;
import gov.adlnet.xapi.model.Context;
import gov.adlnet.xapi.model.Statement;
import gov.adlnet.xapi.model.Verb;

public class XAPILearnLogger extends BaseService {

	public static String BASE_URI ="https://github.com/GeneralizedLearningUtilities/SuperGLU/";
	public static String SESSION_TYPE = "http://id.tincanapi.com/activitytype/tutor-session";
	public static String LESSON_TYPE = "http://adlnet.gov/expapi/activities/lesson";
	public static String SUBLESSON_TYPE = BASE_URI + "sublesson";
	public static String TASK_TYPE = "http://activitystrea.ms/schema/1.0/task";
	public static String STEP_TYPE = "http://id.tincanapi.com/activitytype/step";

	//# VERBS
	public static String START_URI = "http://activitystrea.ms/schema/1.0/start";
	public static String COMPLETED_URI = "http://activitystrea.ms/schema/1.0/complete";
	public static String TERMINATED_URI = "http://activitystrea.ms/schema/1.0/terminate";
	public static String WATCHED_URI = "http://activitystrea.ms/schema/1.0/watch";

	//# ACTIVITY DEFINITION EXTENSION
	public static String ACTIVITY_ID_URI = BASE_URI + "activityid";

	//# CONTEXT EXTENSIONS
	public static String RECOVERED_URI = BASE_URI + "recovered";
	public static String MISSING_COMPS_URI = BASE_URI + "missingCompletions";
	public static String ACTIVITY_TREE_URI = BASE_URI + "serialized_activitytree";

	private MessagingGateway gateway;
	private String userId;
	private String userName;
	private String homePage;
	private String mboxHost;
	private String errorLogName ="xap_learn_logger_errorLog.txt";
	private float secondsAfterLastTimeStamp = 1;
	
	public static SimpleDateFormat timestampFormat = new SimpleDateFormat("yyyy-MM-ddTHH:mm:ss.SSSZ");
	
	
	public XAPILearnLogger(MessagingGateway gateway, String userId, String userName, String homePage, String mboxHost)
	{
		super();
		this.gateway = gateway;
		this.userId = userId;
		this.userName = userName;
		this.homePage = homePage;
		this.mboxHost = mboxHost;
	}
	
	
	public void setUserId(String userId)
	{
		this.userId = userId;
	}
	
	
	public void setUserName(String userName)
	{
		this.userName = userName;
	}
	
	
	public Date getTimestamp()
	{
		return new Date();
	}
	
	
	//VERBS
	
	public Verb createCompletedVerb()
	{
		HashMap<String, String> display = new HashMap<>();
		display.put("en-US", "completed");
		Verb result = new Verb(COMPLETED_URI, display);
		return result;
	}
	
	
	public Verb createStartedVerb()
	{
		HashMap<String, String> display = new HashMap<>();
		display.put("en-US", "started");
		Verb result = new Verb(START_URI, display);
		return result;
	}
	
	
	public Verb createTerminatedVerb()
	{
		HashMap<String, String> display = new HashMap<>();
		display.put("en-US", "terminated");
		Verb result = new Verb(TERMINATED_URI, display);
		return result;
	}
	
	
	public Verb createWatchedVerb()
	{
		HashMap<String, String> display = new HashMap<>();
		display.put("en-US", "watched");
		Verb result = new Verb(WATCHED_URI, display);
		return result;
	}
	
	
	// ACTIVITIES
	
	public Activity createSession(String activityId, String name, String description)
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", name);
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", description);
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		definition.setType(SESSION_TYPE);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity(activityId, definition);
		return result;
		
	}
	
	
	public Activity createLesson(String activityId, String name, String description)
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", name);
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", description);
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		definition.setType(LESSON_TYPE);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity(activityId, definition);
		return result;
	}
	
	
	public Activity createSubLesson(String activityId, String name, String description)
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", name);
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", description);
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		definition.setType(SUBLESSON_TYPE);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity(activityId, definition);
		return result;
	}
	
	
	public Activity createTask(String activityId, String name, String description)
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", name);
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", description);
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		definition.setType(TASK_TYPE);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity(activityId, definition);
		return result;
	}
	
	
	public Activity createStep(String activityId, String name, String description)
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", name);
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", description);
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		definition.setType(STEP_TYPE);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity(activityId, definition);
		return result;
	}
	
	
	public Activity createVideo()
	{
		HashMap<String, String> nameMap = new HashMap<>();
		nameMap.put("en-US", "video");
		HashMap<String, String> descriptionMap = new HashMap<>();
		descriptionMap.put("en-US", "Video content of any kind");
		ActivityDefinition definition = new ActivityDefinition(nameMap, descriptionMap);
		HashMap<String, JsonElement> extensions = new HashMap<>();
		extensions.put(ACTIVITY_ID_URI, new JsonPrimitive(UUID.randomUUID().toString()));
		definition.setExtensions(extensions);
		Activity result = new Activity("http://activitystrea.ms/schema/1.0/video", definition);
		return result;
	}
	
	
	public Agent createAgent()
	{
		Agent result;
		
		if(this.mboxHost != null)
		{
			result = new Agent(this.userName, "mailto:" + this.userName + "@" + this.mboxHost);
		}
		else if(this.homePage != null)
		{
			Account account = new Account(this.userId, this.homePage);
			result = new Agent(this.userName, account);
		}
		else
		{
			result = new Agent(this.userName, "");
		}
		
		return result;
	}
	
	
	//Starting and Stopping
	
	public void sendStartSession(String activityID, String name, String description, HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Activity activity = this.createSession(activityID, name, description);
		Agent actor = this.createAgent();
		
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);

		
	}
	
	public void addContext(HashMap<String, JsonElement> contextDict)
	{
		
	}
	
	public void sendLoggingMessage(Statement statement)
	{
		Message message = new Message();
		message.setActor("logger");
		message.setVerb(MessagingVerbConstants.XAPI_LOG_VERB);
		message.setObj(null);
		message.setResult(statement.serialize().toString());
		message.setSpeechAct(SpeechActEnum.INFORM_ACT);
		this.sendMessage(message);
	}
			
}
