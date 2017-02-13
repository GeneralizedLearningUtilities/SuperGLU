package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Core.Message;
import Core.VHMessage;

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
    
    public static List<MessageMap> buildMessageMaps()
    {
	List<MessageMap> result = new ArrayList<>();
	result.add(buildVHTSuperGLUCurrentScenarioMapping());
	result.add(buildVHTSuperGLUCommAPIMapping());
	result.add(buildVHTSuperGLUBeginAARMapping());
	result.add(buildVHTSuperGLUGetNextAgendaItemMapping());
	result.add(buildVHTSuperGLURequestCoachingActionsMapping());
	result.add(buildVHTSuperGLUVRExpressMapping());
	result.add(buildVHTSuperGLURegisterUserInfoMapping());
	
	
	
	return result;
    }

    public static MessageMap buildVHTSuperGLUCurrentScenarioMapping()
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1 = new ArrayList<String>();
	List<String> indexsd2 = new ArrayList<String>();
	List<String> indexsd3 = new ArrayList<String>();
	List<String> indexsd4 = new ArrayList<String>();
	indexsd1.add(Message.SPEECH_ACT_KEY);
	indexsd2.add(Message.CONTEXT_KEY);
	indexsd3.add(Message.RESULT_KEY);
	indexsd4.add(Message.ACTOR_KEY);

	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(indexsd1);
	SuperGLUDefaultSpeechAct.setFieldData("INFORM_ACT");
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(indexsd2);
	SuperGLUDefaultContextField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultResultField = new NestedAtomic(indexsd3);
	SuperGLUDefaultResultField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(indexsd4);
	SuperGLUDefaultActorField.setFieldData(" ");
	
	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultContextField);
	supergluArr.add(SuperGLUDefaultResultField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE

	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1 = new ArrayList<String>();
	List<String> indexvh2 = new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	indexvh2.add(VHMessage.BODY_KEY);
	NestedAtomic VHT_LabelField = new NestedAtomic(indexvh1);
	VHT_LabelField.setFieldData("ScenarioName");
	NestedAtomic VHT_BodyField = new NestedAtomic(indexvh2);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1 = new ArrayList<String>();
	List<String> indexsg2 = new ArrayList<String>();
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(indexsg1);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(indexsg2);

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

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
	supergluArrGeneric.add(SuperGLUDefaultResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("ScenarioName", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);
	
	return result;

    }
    
    
    public static MessageMap buildVHTSuperGLUBeginAARMapping()
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1 = new ArrayList<String>();
	List<String> indexsd2 = new ArrayList<String>();
	List<String> indexsd3 = new ArrayList<String>();
	List<String> indexsd4 = new ArrayList<String>();
	indexsd1.add(Message.SPEECH_ACT_KEY);
	indexsd2.add(Message.CONTEXT_KEY);
	indexsd3.add(Message.RESULT_KEY);
	indexsd4.add(Message.ACTOR_KEY);

	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(indexsd1);
	SuperGLUDefaultSpeechAct.setFieldData("INFORM_ACT");
	NestedAtomic SuperGLUDefaultContextField = new NestedAtomic(indexsd2);
	SuperGLUDefaultContextField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultResultField = new NestedAtomic(indexsd3);
	SuperGLUDefaultResultField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(indexsd4);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");
	
	
	

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE

	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1 = new ArrayList<String>();
	List<String> indexvh2 = new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	indexvh2.add(VHMessage.BODY_KEY);
	NestedAtomic VHT_LabelField = new NestedAtomic(indexvh1);
	VHT_LabelField.setFieldData("beginAAR");
	NestedAtomic VHT_BodyField = new NestedAtomic(indexvh2);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1 = new ArrayList<String>();
	List<String> indexsg2 = new ArrayList<String>();
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	NestedAtomic SuperGLU_ObjectField = new NestedAtomic(indexsg1);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(indexsg2);

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

	ArrayList<NestedAtomic> supergluArrGeneric = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric = new ArrayList<NestedAtomic>();

	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);

	MessageTemplate vhMsgTempGeneric = new MessageTemplate(vhMsgArrGeneric);

	supergluArrGeneric.add(SuperGLUDefaultContextField);
	supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
	supergluArrGeneric.add(SuperGLUDefaultResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);

	MessageTemplate supergluMsgTempGeneric = new MessageTemplate(supergluArrGeneric);

	// CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8 = new MessageType("beginAAR", 0.0f, 1.1f, vhMsgTempGeneric, "VHMessage");

	MessageType SuperGLUMsgV1 = new MessageType("SUPERGLUMSG_1", 0.0f, 1.1f, supergluMsgTempGeneric, "Message");

	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);
	
	return result;

    }
    
    
    public static MessageMap buildVHTSuperGLUGetNextAgendaItemMapping()
    {
	// CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2
	// MESSAGE TEMPLATES
	ArrayList<NestedAtomic> supergluArr = new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr = new ArrayList<NestedAtomic>();

	// CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1 = new ArrayList<String>();
	List<String> indexsd2 = new ArrayList<String>();
	List<String> indexsd3 = new ArrayList<String>();
	
	indexsd1.add(Message.SPEECH_ACT_KEY);
	indexsd2.add(Message.OBJECT_KEY);
	indexsd3.add(Message.ACTOR_KEY);

	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(indexsd1);
	SuperGLUDefaultSpeechAct.setFieldData("INFORM_ACT");
	NestedAtomic SuperGLUDefaultObjectField = new NestedAtomic(indexsd2);
	SuperGLUDefaultObjectField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(indexsd3);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");
	
	
	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultObjectField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	NestedAtomic VHTDefaultBodyField = new NestedAtomic(indexsd1);
	VHTDefaultBodyField.setFieldData(" ");
	vhMsgArr.add(VHTDefaultBodyField);
	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1 = new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	
	NestedAtomic VHT_LabelField = new NestedAtomic(indexvh1);
	VHT_LabelField.setFieldData("getNextAgendaItem");


	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1 = new ArrayList<String>();
	
	indexsg1.add(Message.VERB_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(indexsg1);

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
	List<String> indexsd1 = new ArrayList<String>();
	List<String> indexsd2 = new ArrayList<String>();
	List<String> indexsd3 = new ArrayList<String>();
	
	indexsd1.add(Message.SPEECH_ACT_KEY);
	indexsd2.add(Message.OBJECT_KEY);
	indexsd3.add(Message.ACTOR_KEY);

	NestedAtomic SuperGLUDefaultSpeechAct = new NestedAtomic(indexsd1);
	SuperGLUDefaultSpeechAct.setFieldData("REQUEST_ACT");
	NestedAtomic SuperGLUDefaultObjectField = new NestedAtomic(indexsd2);
	SuperGLUDefaultObjectField.setFieldData(" ");
	NestedAtomic SuperGLUDefaultActorField = new NestedAtomic(indexsd3);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");
	
	
	supergluArr.add(SuperGLUDefaultSpeechAct);
	supergluArr.add(SuperGLUDefaultObjectField);
	supergluArr.add(SuperGLUDefaultActorField);

	// STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp = new MessageTemplate(supergluArr);

	// CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	NestedAtomic VHTDefaultBodyField = new NestedAtomic(indexsd1);
	VHTDefaultBodyField.setFieldData(" ");
	vhMsgArr.add(VHTDefaultBodyField);
	// STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp = new MessageTemplate(vhMsgArr);

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1 = new ArrayList<String>();
	
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	NestedAtomic VHT_LabelField = new NestedAtomic(indexvh1);
	VHT_LabelField.setFieldData("requestCoachingActions");

	// CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1 = new ArrayList<String>();
	
	indexsg1.add(Message.VERB_KEY);
	NestedAtomic SuperGLU_VerbField = new NestedAtomic(indexsg1);

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
	ArrayList<NestedAtomic> supergluArr=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr=new ArrayList<NestedAtomic>();
	
	
	//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1=new ArrayList<String>();
	

	indexsd1.add(Message.CONTEXT_KEY);
		
	NestedAtomic SuperGLUDefaultContextField =new NestedAtomic(indexsd1);
	SuperGLUDefaultContextField.setFieldData("");

	supergluArr.add(SuperGLUDefaultContextField);	
	
	//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp=new MessageTemplate(supergluArr);
	
	//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	
	
	//STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp=new MessageTemplate(vhMsgArr);
	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1=new ArrayList<String>();
	List<String> indexvh2=new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	indexvh2.add(VHMessage.BODY_KEY);
	NestedAtomic VHT_LabelField=new NestedAtomic(indexvh1);	
	VHT_LabelField.setFieldData("vrExpress");
	NestedAtomic VHT_BodyField=new NestedAtomic(indexvh2);

	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1=new ArrayList<String>();
	List<String> indexsg2=new ArrayList<String>();
	List<String> indexsg3=new ArrayList<String>();
	List<String> indexsg4=new ArrayList<String>();
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	indexsg3.add(Message.RESULT_KEY);
	indexsg4.add(Message.ACTOR_KEY);
	NestedAtomic SuperGLU_ObjectField=new NestedAtomic(indexsg1);	
	NestedAtomic SuperGLU_VerbField=new NestedAtomic(indexsg2);
	NestedAtomic SuperGLU_ResultField=new NestedAtomic(indexsg3);
	NestedAtomic SuperGLU_ActorField=new NestedAtomic(indexsg4);
	
	
	//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
	FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);
	
	FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setIndex(2);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField); 
	
	FieldMap VHT_SuperGLU_TopicResult_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicResult_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicResult_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicResult_FM.setSplitter(VHT_SuperGLU_TopicResult_FMsplitter);
	VHT_SuperGLU_TopicResult_FM.setIndex(3);
	VHT_SuperGLU_TopicResult_FM.setOutField(SuperGLU_ResultField); 
	
	FieldMap VHT_SuperGLU_TopicActor_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicActor_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicActor_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicActor_FM.setSplitter(VHT_SuperGLU_TopicActor_FMsplitter);
	VHT_SuperGLU_TopicActor_FM.setIndex(0);
	VHT_SuperGLU_TopicActor_FM.setOutField(SuperGLU_ActorField); 
	
	
	ArrayList<FieldMap> fieldmappings=new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
	fieldmappings.add(VHT_SuperGLU_TopicResult_FM);
	fieldmappings.add(VHT_SuperGLU_TopicActor_FM);
	
	
	//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
	
	
	ArrayList<NestedAtomic> supergluArrGeneric=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric=new ArrayList<NestedAtomic>();
	
	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);
	
	MessageTemplate vhMsgTempGeneric5=new MessageTemplate(vhMsgArrGeneric);
	
	supergluArrGeneric.add(SuperGLUDefaultContextField);		
	supergluArrGeneric.add(SuperGLU_ResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLU_ActorField);
	
	MessageTemplate supergluMsgTempGeneric=new MessageTemplate(supergluArrGeneric);
	
	
	
	
			
	
	//CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8=new MessageType("vrExpress", 0.0f, 1.1f,vhMsgTempGeneric5,"VHMessage");
	
	MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_5",0.0f,1.1f,supergluMsgTempGeneric,"Message");
	
	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);
	
	return result;
    }
    
    
    
    public static MessageMap buildVHTSuperGLUCommAPIMapping()
    {
	ArrayList<NestedAtomic> supergluArr=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr=new ArrayList<NestedAtomic>();
	
	
	//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1=new ArrayList<String>();
	List<String> indexsd2=new ArrayList<String>();
	

	indexsd1.add(Message.CONTEXT_KEY);
	
	indexsd2.add(Message.ACTOR_KEY);
	
	
	
	NestedAtomic SuperGLUDefaultContextField =new NestedAtomic(indexsd1);
	SuperGLUDefaultContextField.setFieldData("");
	
	NestedAtomic SuperGLUDefaultActorField=new NestedAtomic(indexsd2);
	SuperGLUDefaultActorField.setFieldData("Tutor");
	

	supergluArr.add(SuperGLUDefaultContextField);	
	supergluArr.add(SuperGLUDefaultActorField);
	
	//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp=new MessageTemplate(supergluArr);
	
	//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	
	
	//STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp=new MessageTemplate(vhMsgArr);
	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1=new ArrayList<String>();
	List<String> indexvh2=new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	indexvh2.add(VHMessage.BODY_KEY);
	NestedAtomic VHT_LabelField=new NestedAtomic(indexvh1);	
	VHT_LabelField.setFieldData("commAPI");
	NestedAtomic VHT_BodyField=new NestedAtomic(indexvh2);

	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1=new ArrayList<String>();
	List<String> indexsg2=new ArrayList<String>();
	List<String> indexsg3=new ArrayList<String>();
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	indexsg3.add(Message.RESULT_KEY);
	NestedAtomic SuperGLU_ObjectField=new NestedAtomic(indexsg1);	
	NestedAtomic SuperGLU_VerbField=new NestedAtomic(indexsg2);
	NestedAtomic SuperGLU_ResultField=new NestedAtomic(indexsg3);
	
	
	//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
	FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);
	
	FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setIndex(0);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField); 
	
	FieldMap VHT_SuperGLU_TopicResult_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicResult_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicResult_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicResult_FM.setSplitter(VHT_SuperGLU_TopicResult_FMsplitter);
	VHT_SuperGLU_TopicResult_FM.setIndex(1);
	VHT_SuperGLU_TopicResult_FM.setOutField(SuperGLU_ResultField); 
	
	
	ArrayList<FieldMap> fieldmappings=new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
	fieldmappings.add(VHT_SuperGLU_TopicResult_FM);
	
	
	//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
	
	
	ArrayList<NestedAtomic> supergluArrGeneric=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric=new ArrayList<NestedAtomic>();
	
	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);
	
	MessageTemplate vhMsgTempGeneric5=new MessageTemplate(vhMsgArrGeneric);
	
	supergluArrGeneric.add(SuperGLUDefaultContextField);		
	supergluArrGeneric.add(SuperGLU_ResultField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	supergluArrGeneric.add(SuperGLUDefaultActorField);
	
	MessageTemplate supergluMsgTempGeneric=new MessageTemplate(supergluArrGeneric);
	
	
	
	
			
	
	//CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8=new MessageType("commAPI", 0.0f, 1.1f,vhMsgTempGeneric5,"VHMessage");
	
	MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_5",0.0f,1.1f,supergluMsgTempGeneric,"Message");
	
	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);
	
	return result;
    }
    
    
    public static MessageMap buildVHTSuperGLURegisterUserInfoMapping()
    {
	ArrayList<NestedAtomic> supergluArr=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArr=new ArrayList<NestedAtomic>();
	
	
	//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
	List<String> indexsd1=new ArrayList<String>();
	List<String> indexsd2=new ArrayList<String>();
	List<String> indexsd3=new ArrayList<String>();
	

	indexsd1.add(Message.CONTEXT_KEY);	
	indexsd2.add(Message.ACTOR_KEY);
	indexsd3.add(Message.SPEECH_ACT_KEY);
	
	
	
	NestedAtomic SuperGLUDefaultContextField =new NestedAtomic(indexsd1);
	SuperGLUDefaultContextField.setFieldData("");
	
	NestedAtomic SuperGLUDefaultActorField=new NestedAtomic(indexsd2);
	SuperGLUDefaultActorField.setFieldData("DIALOG_MANAGER");
	
	NestedAtomic SuperGLUDefaultSpeechActField=new NestedAtomic(indexsd3);
	SuperGLUDefaultSpeechActField.setFieldData("INFORM_ACT");
	

	supergluArr.add(SuperGLUDefaultContextField);	
	supergluArr.add(SuperGLUDefaultActorField);
	supergluArr.add(SuperGLUDefaultSpeechActField);
	
	//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
	MessageTemplate supergluMsgTemp=new MessageTemplate(supergluArr);
	
	//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
	
	
	//STORED THE DATA IN THE VH MESSAGE TEMPLATE
	MessageTemplate vhMsgTemp=new MessageTemplate(vhMsgArr);
	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexvh1=new ArrayList<String>();
	List<String> indexvh2=new ArrayList<String>();
	indexvh1.add(VHMessage.FIRST_WORD_KEY);
	indexvh2.add(VHMessage.BODY_KEY);
	NestedAtomic VHT_LabelField=new NestedAtomic(indexvh1);	
	VHT_LabelField.setFieldData("registerUserInfo");
	NestedAtomic VHT_BodyField=new NestedAtomic(indexvh2);

	
	//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
	List<String> indexsg1=new ArrayList<String>();
	List<String> indexsg2=new ArrayList<String>();
	
	indexsg1.add(Message.OBJECT_KEY);
	indexsg2.add(Message.VERB_KEY);
	
	NestedAtomic SuperGLU_ObjectField=new NestedAtomic(indexsg1);	
	NestedAtomic SuperGLU_VerbField=new NestedAtomic(indexsg2);
	
	
	//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
	FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
	VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
	VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);
	
	FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
	Splitting VHT_SuperGLU_TopicObject_FMsplitter=new Splitting(" ");
	VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
	VHT_SuperGLU_TopicObject_FM.setSplitter(VHT_SuperGLU_TopicObject_FMsplitter);
	VHT_SuperGLU_TopicObject_FM.setIndex(2);
	VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField); 
	
	
	
	ArrayList<FieldMap> fieldmappings=new ArrayList<FieldMap>();
	fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
	fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
	
	
	
	//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
	
	
	ArrayList<NestedAtomic> supergluArrGeneric=new ArrayList<NestedAtomic>();
	ArrayList<NestedAtomic> vhMsgArrGeneric=new ArrayList<NestedAtomic>();
	
	vhMsgArrGeneric.add(VHT_BodyField);
	vhMsgArrGeneric.add(VHT_LabelField);
	
	MessageTemplate vhMsgTempGeneric=new MessageTemplate(vhMsgArrGeneric);
	
	supergluArrGeneric.add(SuperGLUDefaultContextField);	
	supergluArrGeneric.add(SuperGLUDefaultActorField);
	supergluArrGeneric.add(SuperGLUDefaultSpeechActField);
	supergluArrGeneric.add(SuperGLU_ObjectField);
	supergluArrGeneric.add(SuperGLU_VerbField);
	
	
	MessageTemplate supergluMsgTempGeneric=new MessageTemplate(supergluArrGeneric);
	
	
	
	
			
	
	//CREATING THE MESSAGETYPEBASED VHMESSAGE
	MessageType VHTMsgV1_8=new MessageType("registerUserInfo", 0.0f, 1.1f,vhMsgTempGeneric,"VHMessage");
	
	MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_5",0.0f,1.1f,supergluMsgTempGeneric,"Message");
	
	MessageMap result = new MessageMap(VHTMsgV1_8, SuperGLUMsgV1, vhMsgTemp, supergluMsgTemp, fieldmappings);
	
	return result;
    }

   
    
}
