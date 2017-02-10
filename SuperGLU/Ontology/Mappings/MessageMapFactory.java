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

}
