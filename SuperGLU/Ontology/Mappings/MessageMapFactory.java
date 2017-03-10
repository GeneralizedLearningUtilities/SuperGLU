package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Core.GIFTMessage;
import Core.Message;
import Util.Pair;
import Util.Serializable;
import Util.StorageToken;

/**
 * This class is intended as a stopgap measure to build the mappings in the Java
 * code. It will be replaced once we implement the code to generate the
 * Mappings' JSON.
 * 
 * @author auerbach
 *
 */
public class MessageMapFactory
{
    
    private static String NO_TEXT =  "no text available";
    
    protected static MessageTemplate buildGIFTDisplayFeedbackTutorRequestTemplate()
    {
	NestedAtomic header = new NestedAtomic(String.class, GIFTMessage.HEADER_KEY);
	List<Pair<FieldData, Object>> templateDataList = new ArrayList<>();
	templateDataList.add(new Pair<FieldData, Object>(header, "Display Feedback Tutor Request"));
	
	List<Pair<Class<?>, String>> payloadPath = new ArrayList<>();
	
	payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
	payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, "DisplayTextAction"));
	payloadPath.add(new Pair<Class<?>, String>(String.class, "text"));
	
	NestedAtomic payload = new NestedAtomic(payloadPath);
	
	templateDataList.add(new Pair<FieldData, Object>(payload, NO_TEXT));
	
	MessageTemplate result = new MessageTemplate(templateDataList);
	
	return result;
    }
    
    
    protected static MessageTemplate buildSuperGLUGiveFeedbackMessageTemplate()
    {
	List<Pair<FieldData, Object>> templateDataList = new ArrayList<>(); 
	
	SimpleFieldData actor = new SimpleFieldData(Message.ACTOR_KEY);
	SimpleFieldData verb = new SimpleFieldData(Message.VERB_KEY);
	SimpleFieldData object =new SimpleFieldData(Message.OBJECT_KEY);
	SimpleFieldData result =new SimpleFieldData(Message.RESULT_KEY);
	
	
	templateDataList.add(new Pair<FieldData, Object>(actor, "GIFT"));
	templateDataList.add(new Pair<FieldData, Object>(verb, "GiveFeedback"));
	templateDataList.add(new Pair<FieldData, Object>(object, "VHuman"));
	templateDataList.add(new Pair<FieldData, Object>(result, NO_TEXT));
	

	MessageTemplate returnVal = new MessageTemplate(templateDataList);
	
	return returnVal;
	
    }
    
    
    protected static List<FieldMap> buildFieldMapsForDisplayFeedbackTutorRequestToGiveFeedback()
    {
	List<FieldMap> mappings = new ArrayList<>();
	
	List<Pair<Class<?>, String>> payloadPath = new ArrayList<>();
	
	payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
	payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, "DisplayTextAction"));
	payloadPath.add(new Pair<Class<?>, String>(String.class, "text"));
	
	NestedAtomic payload = new NestedAtomic(payloadPath);
	SimpleFieldData result =new SimpleFieldData(Message.RESULT_KEY);
	
	FieldMapOneToOne map = new FieldMapOneToOne(payload, result);
	
	mappings.add(map);
	
	return mappings;
    }
    
    
    protected static MessageMap buildDisplayFeedbackTutorRequestToSuperGLU()
    {
	MessageType inMsgType = new MessageType("Display Feedback Tutor Request", 1.0f, 1.0f, buildGIFTDisplayFeedbackTutorRequestTemplate(), GIFTMessage.class.getSimpleName());
	MessageType outMsgType = new MessageType("GiveFeedback", 1.0f, 1.0f, buildSuperGLUGiveFeedbackMessageTemplate(), Message.class.getSimpleName());
	MessageMap map = new MessageMap(inMsgType, outMsgType, buildFieldMapsForDisplayFeedbackTutorRequestToGiveFeedback());
	
	return map;
    }
    
    
    
    public static List<MessageMap> buildMessageMaps()
    {
	List<MessageMap> result = new ArrayList<>();
	result.add(buildDisplayFeedbackTutorRequestToSuperGLU());

	return result;
    }
/*
    protected static MessageTemplate buildSuperGLUTemplate(String actor)
    {
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(String.class, Message.SPEECH_ACT_KEY);
	SuperGLUDefaultSpeechAct.setFieldData(SpeechActEnum.INFORM_ACT.toString());
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(HashMap.class, Message.CONTEXT_KEY);
	SuperGLUDefaultContextField.setFieldData("{}");
	NestedAtomic SuperGLUDefaultResultField = new NestedAtomic(String.class, Message.RESULT_KEY);
	SuperGLUDefaultResultField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData(actor);

	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultContextField);
	supergluArr.add(SuperGLUDefaultResultField);
	supergluArr.add(SuperGLUDefaultActorField);

	MessageTemplate result = new MessageTemplate(supergluArr);

	return result;

    }

    protected static MessageTemplate buildSuperGLUGenericTemplate(String actor)
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(String.class, Message.SPEECH_ACT_KEY);
	SuperGLUDefaultSpeechAct.setFieldData(SpeechActEnum.INFORM_ACT.toString());
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(HashMap.class, Message.CONTEXT_KEY);
	SuperGLUDefaultContextField.setFieldData("{}");
	NestedAtomic SuperGLUDefaultResultField = new NestedAtomic(String.class, Message.RESULT_KEY);
	SuperGLUDefaultResultField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData(" ");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
	supergluArrGeneric.add(SuperGLUDefaultResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);
	return supergluMsgTempGeneric;
    }

    protected static MessageTemplate buildVHMessageTemplate(String firstWord)
    {
	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData(firstWord);
	NestedAtomic VHT_BodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);

	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate result = new MessageTemplate(vhMsgArrGeneric);
	return result;
    }

    protected static NestedAtomic findNestedAtomicInTemplateByIndex(MessageTemplate template, String index)
    {
	for (NestedAtomic currentAtomic : template.getDefaultFieldData())
	{
	    for (Pair<Class<?>, String> currentIndex : currentAtomic.getIndices())
	    {
		if (currentIndex.getSecond().equals(index))
		    return currentAtomic;
	    }
	}

	return null;
    }

    public static MessageMap buildVHTSuperGLUCurrentScenarioMapping()
    {
	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = MessageMapFactory.buildSuperGLUTemplate(" ");

	MessageTemplate vhMsgTempGeneric = MessageMapFactory.buildVHMessageTemplate("ScenarioName");

	MessageTemplate supergluMsgTempGeneric = MessageMapFactory.buildSuperGLUGenericTemplate(" ");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = MessageMapFactory.findNestedAtomicInTemplateByIndex(vhMsgTempGeneric, VHMessage.FIRST_WORD_KEY);
	NestedAtomic VHT_BodyField = MessageMapFactory.findNestedAtomicInTemplateByIndex(vhMsgTempGeneric, VHMessage.BODY_KEY);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	FieldMap VHT_SuperGLU_TopicObject_FM = new FieldMap();
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("ScenarioName", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, new MessageTemplate(), supergluMsgTemp, fieldmappings);

	return result;

    }

    public static MessageMap buildVHTSuperGLUBeginAARMapping()
    {
	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = MessageMapFactory.buildSuperGLUTemplate("DIALOG_MANAGER");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("beginAAR");
	NestedAtomic VHT_BodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	FieldMap VHT_SuperGLU_TopicObject_FM = new FieldMap();
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	MessageTemplate supergluMsgTempGeneric = MessageMapFactory.buildSuperGLUGenericTemplate("DIALOG_MANAGER");

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("beginAAR", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, new MessageTemplate(), supergluMsgTemp, fieldmappings);

	return result;

    }

    public static MessageMap buildVHTSuperGLUGetNextAgendaItemMapping()
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(String.class, Message.SPEECH_ACT_KEY);
	SuperGLUDefaultSpeechAct.setFieldData(SpeechActEnum.INFORM_ACT.toString());
	NestedAtomic SuperGLUDefaultObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	SuperGLUDefaultObjectField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");

	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultObjectField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	NestedAtomic VHTDefaultBodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);
	VHTDefaultBodyField.setFieldData(" ");
	vhMsgArr.add(VHTDefaultBodyField);
	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)

	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("getNextAgendaItem");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHTDefaultBodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
	supergluArrGeneric.add(SuperGLUDefaultObjectField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);
	supergluArrGeneric.add(SuperGLU_VerbField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("getNextAgendaItem", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);

	return result;

    }

    public static MessageMap buildVHTSuperGLURequestCoachingActionsMapping()
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE

	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(String.class, Message.SPEECH_ACT_KEY);
	SuperGLUDefaultSpeechAct.setFieldData(SpeechActEnum.REQUEST_ACT.toString());
	NestedAtomic SuperGLUDefaultObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	SuperGLUDefaultObjectField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");

	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultObjectField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	NestedAtomic VHTDefaultBodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);
	VHTDefaultBodyField.setFieldData(" ");
	vhMsgArr.add(VHTDefaultBodyField);
	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("requestCoachingActions");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHTDefaultBodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
	supergluArrGeneric.add(SuperGLUDefaultObjectField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);
	supergluArrGeneric.add(SuperGLU_VerbField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("requestCoachingActions", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);

	return result;

    }

    public static MessageMap buildVHTSuperGLUVRExpressMapping()
    {
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(HashMap.class, Message.CONTEXT_KEY);
	SuperGLUDefaultContextField.setFieldData("");

	supergluArr.add(SuperGLUDefaultContextField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE

	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("vrExpress");
	NestedAtomic VHT_BodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);
	NestedAtomic SuperGLU_ResultField = new NestedAtomic(String.class, Message.RESULT_KEY);
	NestedAtomic SuperGLU_ActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	FieldMap VHT_SuperGLU_TopicObject_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setInIndex(2);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);

	FieldMap VHT_SuperGLU_TopicResult_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicResult_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicResult_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicResult_FM.setSplitter(VHT_SuperGLU_TopicResult_FMsplitter);
	VHT_SuperGLU_TopicResult_FM.setInIndex(3);
	VHT_SuperGLU_TopicResult_FM.setOutField(SuperGLU_ResultField);

	FieldMap VHT_SuperGLU_TopicActor_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicActor_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicActor_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicActor_FM.setSplitter(VHT_SuperGLU_TopicActor_FMsplitter);
	VHT_SuperGLU_TopicActor_FM.setInIndex(0);
	VHT_SuperGLU_TopicActor_FM.setOutField(SuperGLU_ActorField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
	fieldmappings.add(VHT_SuperGLU_TopicResult_FM);
	fieldmappings.add(VHT_SuperGLU_TopicActor_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric5 = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLU_ResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLU_ActorField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("vrExpress", 0.0f, 1.1f, vhMsgTempGeneric5, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_5", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);

	return result;
    }

    public static MessageMap buildVHTSuperGLUCommAPIMapping()
    {
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(HashMap.class, Message.CONTEXT_KEY);
	SuperGLUDefaultContextField.setFieldData("");

	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData("Tutor");

	supergluArr.add(SuperGLUDefaultContextField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE

	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("commAPI");
	NestedAtomic VHT_BodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1 = new ArrayList<String>();
	List<String> indexsg2 = new ArrayList<String>();
	List<String> indexsg3 = new ArrayList<String>();
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	indexsg3.add(Message.RESULT_KEY);
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);
	NestedAtomic SuperGLU_ResultField = new NestedAtomic(String.class, Message.RESULT_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	FieldMap VHT_SuperGLU_TopicObject_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setInIndex(0);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);

	FieldMap VHT_SuperGLU_TopicResult_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicResult_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicResult_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicResult_FM.setSplitter(VHT_SuperGLU_TopicResult_FMsplitter);
	VHT_SuperGLU_TopicResult_FM.setInIndex(1);
	VHT_SuperGLU_TopicResult_FM.setOutField(SuperGLU_ResultField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
	fieldmappings.add(VHT_SuperGLU_TopicResult_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric5 = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLU_ResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("commAPI", 0.0f, 1.1f, vhMsgTempGeneric5, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_5", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);

	return result;
    }

    public static MessageMap buildVHTSuperGLURegisterUserInfoMapping()
    {
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(HashMap.class, Message.CONTEXT_KEY);
	SuperGLUDefaultContextField.setFieldData("");

	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(String.class, Message.ACTOR_KEY);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");

	// Do we need to specify the exact type here or will a general string
	// do? -- Auerbach
	NestedAtomic SuperGLUDefaultSpeechActField = new NestedAtomic(String.class, Message.SPEECH_ACT_KEY);
	SuperGLUDefaultSpeechActField.setFieldData(SpeechActEnum.INFORM_ACT.toString());

	supergluArr.add(SuperGLUDefaultContextField);
	supergluArr.add(SuperGLUDefaultActorField);
	supergluArr.add(SuperGLUDefaultSpeechActField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE

	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic VHT_LabelField = new NestedAtomic(String.class, VHMessage.FIRST_WORD_KEY);
	VHT_LabelField.setFieldData("registerUserInfo");
	NestedAtomic VHT_BodyField = new NestedAtomic(String.class, VHMessage.BODY_KEY);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(String.class, Message.OBJECT_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(String.class, Message.VERB_KEY);

	// CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW
	FieldMap VHT_SuperGLU_TopicVerb_FM = new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);

	FieldMap VHT_SuperGLU_TopicObject_FM = new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter = new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setInIndex(2);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);

	ArrayList<FieldMap> fieldmappings = new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);

	// CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT
	// MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);
	supergluArrGeneric.add(SuperGLUDefaultSpeechActField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("registerUserInfo", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_5", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);

	return result;
    }
*/
}
