package edu.usc.ict.superglu.services.logging;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
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
import gov.adlnet.xapi.model.ContextActivities;
import gov.adlnet.xapi.model.Result;
import gov.adlnet.xapi.model.Score;
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
	private ActivityTree activityTree;
	
	public static SimpleDateFormat timestampFormat = new SimpleDateFormat("yyyy-MM-ddTHH:mm:ss.SSSZ");
	
	
	public XAPILearnLogger(MessagingGateway gateway, String userId, String userName, String homePage, String mboxHost)
	{
		super();
		this.gateway = gateway;
		this.userId = userId;
		this.userName = userName;
		this.homePage = homePage;
		this.mboxHost = mboxHost;
		this.activityTree = new ActivityTree();
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
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);
		statement.setContext(context);
		
		this.sendLoggingMessage(statement);
		
	}
	
	
	public void sendStartLesson(String activityID, String name, String description, HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Activity activity = this.createLesson(activityID, name, description);
		Agent actor = this.createAgent();
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);
		statement.setContext(context);
		
		this.sendLoggingMessage(statement);		
	}
	
	
	public void sendStartSubLesson(String activityID, String name, String description, HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Activity activity = this.createSubLesson(activityID, name, description);
		Agent actor = this.createAgent();
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);
		statement.setContext(context);
		
		this.sendLoggingMessage(statement);
		
	}
	
	
	public void sendStartTask(String activityID, String name, String description, HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Activity activity = this.createTask(activityID, name, description);
		Agent actor = this.createAgent();
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);
		statement.setContext(context);
		
		this.sendLoggingMessage(statement);
		
	}
	
	
	public void sendStartStep(String activityID, String name, String description, HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Activity activity = this.createStep(activityID, name, description);
		Agent actor = this.createAgent();
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		
		if(timestamp == null)
			timestamp = this.getTimestamp();
		
		Statement statement = new Statement(actor, this.createStartedVerb(), activity);
		statement.setResult(null);
		String timestampAsString = timestampFormat.format(timestamp);
		statement.setTimestamp(timestampAsString);
		statement.setContext(context);
		
		this.sendLoggingMessage(statement);
		
	}
	
	
	public HashMap<String, JsonElement> createFakeContextDict()
	{
		HashMap<String, JsonElement> result = new HashMap<>();
		
		result.put(RECOVERED_URI, new JsonPrimitive("activity"));
		return result;
	}
	
	
	public void sendTerminatedSession(HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Agent actor = this.createAgent();
		
		Activity activity = this.activityTree.findCurrentActivity();
		
		boolean missingData = false;
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
	}
	
	
	public void sendCompletedLesson(HashMap<String, JsonElement> contextDict, Date timestamp, boolean fake)
	{
		Agent actor = this.createAgent();
		Activity activity = this.activityTree.findCurrentActivity();
		Context context = this.addContext(contextDict);
		
		this.activityTree.exitActivity();
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
		Verb verb;
		if(fake)
		{
			verb = this.createTerminatedVerb();
		}
		else
		{
			verb = this.createCompletedVerb();
		}
		
		Statement statement = new Statement(actor, verb, activity);
		statement.setResult(null);
		statement.setContext(context);
		statement.setTimestamp( timestampFormat.format(timestamp));
		
		this.sendLoggingMessage(statement);
	}
	
	
	public void sendCompletedSublesson(HashMap<String, JsonElement> contextDict, Date timestamp, boolean fake)
	{
		Agent actor = this.createAgent();
		Activity activity = this.activityTree.findCurrentActivity();
		Context context = this.addContext(contextDict);
		
		this.activityTree.exitActivity();
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
		Verb verb;
		if(fake)
		{
			verb = this.createTerminatedVerb();
		}
		else
		{
			verb = this.createCompletedVerb();
		}
		
		Statement statement = new Statement(actor, verb, activity);
		statement.setResult(null);
		statement.setContext(context);
		statement.setTimestamp( timestampFormat.format(timestamp));
		
		this.sendLoggingMessage(statement);
	}
	
	
	public void sendCompletedTask(HashMap<String, JsonElement> contextDict, Date timestamp, boolean fake)
	{
		Agent actor = this.createAgent();
		Activity activity = this.activityTree.findCurrentActivity();
		Context context = this.addContext(contextDict);
		
		this.activityTree.exitActivity();
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
		Verb verb;
		if(fake)
		{
			verb = this.createTerminatedVerb();
		}
		else
		{
			verb = this.createCompletedVerb();
		}
		
		Statement statement = new Statement(actor, verb, activity);
		statement.setResult(null);
		statement.setContext(context);
		statement.setTimestamp( timestampFormat.format(timestamp));
		
		this.sendLoggingMessage(statement);
	}
	
	
	public void sendCompletedStep(String choice, HashMap<String, JsonElement> contextDict, JsonObject resultExtDict, float rawScore, float maxScore, float minScore, Date timestamp, boolean fake)
	{
		Agent actor = this.createAgent();
		
		Score score;
		if(rawScore != -1)
		{		

			score = new Score();
			score.setRaw(rawScore);
			score.setMin(minScore);
			score.setMax(maxScore);
		}
		else
		{
			score = null;
		}
		
		Result result = new Result();
		result.setResponse(choice);
		result.setScore(score);
		result.setExtensions(resultExtDict);
		
		Activity activity = this.activityTree.findCurrentActivity();
		Context context = this.addContext(contextDict);
		
		this.activityTree.exitActivity();
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
		Verb verb;
		if(fake)
		{
			verb = this.createTerminatedVerb();
		}
		else
		{
			verb = this.createCompletedVerb();
		}
		
		Statement statement = new Statement(actor, verb, activity);
		statement.setResult(result);
		statement.setContext(context);
		statement.setTimestamp( timestampFormat.format(timestamp));
		
		this.sendLoggingMessage(statement);		
	}
	
	
	public void sendWatchedVideo(HashMap<String, JsonElement> contextDict, Date timestamp)
	{
		Agent actor = createAgent();
		
		Activity activity = createVideo();
		
		this.activityTree.enterActivity(null, activity);
		Context context = this.addContext(contextDict);
		this.activityTree.exitActivity();
		
		if(timestamp == null)
		{
			timestamp = this.getTimestamp();
		}
		
		Statement statement = new Statement(actor, this.createWatchedVerb(), activity);
		statement.setResult(null);
		statement.setContext(context);
		statement.setTimestamp(timestampFormat.format(timestamp));
		this.sendLoggingMessage(statement);
	}
	
	
	
	
	
	//Utility functions
	
	public Context addContext(HashMap<String, JsonElement> contextDict)
	{
		contextDict.put(ACTIVITY_TREE_URI, new JsonPrimitive(this.activityTree.activityTreeToSimple()));
		
		List<Activity> myGrouping = this.activityTree.convertPathToGrouping();
		Activity myParent = this.activityTree.findParentActivity();
		
		Context result;
		
		if(myGrouping.size() == 0 && myParent== null)
		{
			result = new Context();
			result.setExtensions(contextDict);
		}
		else
		{
			ContextActivities myContextActivities = new ContextActivities();
			
			myContextActivities = new ContextActivities();
			ArrayList<Activity> parentList = new ArrayList<>();
			parentList.add(myParent);
			myContextActivities.setParent(parentList);
			if(myGrouping.size() > 0)
			{
				myContextActivities.setGrouping((ArrayList<Activity>) myGrouping);
			}
			
			result = new Context();
			result.setExtensions(contextDict);
			result.setContextActivities(myContextActivities);
		}
		
		return result;
	}
	
	
	public void addContext()
	{
		HashMap<String, JsonElement> contextDict = new HashMap<>();
		this.addContext(contextDict);
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
