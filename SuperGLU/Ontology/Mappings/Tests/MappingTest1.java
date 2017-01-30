package Ontology.Mappings.Tests;
import java.util.*;
import static org.junit.Assert.*;

/**
 * MessageMapTest1  Junit Testcase
 * @author tirthmehta
 */

import org.junit.Test;

import Core.BaseMessage;
import Core.VHMessage;
import Ontology.OntologyConverter;
import Ontology.Mappings.FieldData;
import Ontology.Mappings.FieldMap;
import Ontology.Mappings.MessageMap;
import Ontology.Mappings.MessageOneWayMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageTwoWayMap;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Util.StorageToken;

public class MappingTest1 {

	@Test
	public void test() {
		//fail("Not yet implemented");
		//CREATED THE INITIAL VHMESSAGE
		String first="ScenarioName";
		String body="Being Heard (Interview 1)";
		float version=0.0f;
		HashMap<String,Object> hmap=new HashMap<String, Object>();
		VHMessage v1=new VHMessage("100", hmap, first, version, body);
		
		
		//THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
		MessageOneWayMap VHT_SuperGLU_CurrentScenario=new MessageOneWayMap();
		
		
		//CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2 MESSAGE TEMPLATES
		ArrayList<FieldData> supergluArrGeneric=new ArrayList<FieldData>();
		ArrayList<FieldData> vhMsgArrGeneric=new ArrayList<FieldData>();
		
		
		//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
		FieldData SuperGLUDefaultSpeechAct=new FieldData("INFORM_ACT");
		FieldData SuperGLUDefaultContextField =new FieldData(" ");
		FieldData SuperGLUDefaultVerbField=new FieldData(" ");
		FieldData SuperGLUDefaultObjectField=new FieldData(" ");
		
		supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
		supergluArrGeneric.add(SuperGLUDefaultContextField);
		supergluArrGeneric.add(SuperGLUDefaultVerbField);
		supergluArrGeneric.add(SuperGLUDefaultObjectField);
		
		//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
		MessageTemplate supergluMsgTempGeneric=new MessageTemplate(supergluArrGeneric);
		
		//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
		FieldData vhMsgDefaultLabelField =new FieldData("ScenarioName");
		FieldData vhMsgDefaultBodyField =new FieldData(" ");
		vhMsgArrGeneric.add(vhMsgDefaultLabelField);
		vhMsgArrGeneric.add(vhMsgDefaultBodyField);
		
		//STORED THE DATA IN THE VH MESSAGE TEMPLATE
		MessageTemplate vhMsgTempGeneric=new MessageTemplate(vhMsgArrGeneric);
		
		//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
		String indexvh1="0";
		String indexvh2="1";
		NestedAtomic VHT_LabelField=new NestedAtomic(indexvh1);	
		NestedAtomic VHT_BodyField=new NestedAtomic(indexvh2);
		
		//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
		String indexs1="object";
		String indexs2="verb";
		NestedAtomic SuperGLU_ObjectField=new NestedAtomic(indexs1);	
		NestedAtomic SuperGLU_VerbField=new NestedAtomic(indexs2);
		
		
		//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
		FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
		VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
		VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);
		
		FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
		VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
		VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField); 
		
		ArrayList<FieldMap> fieldmappings=new ArrayList<FieldMap>();
		fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
		fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
		
		
		//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
		
		
		ArrayList<FieldData> supergluArr=new ArrayList<FieldData>();
		ArrayList<FieldData> vhMsgArr=new ArrayList<FieldData>();
		vhMsgArr=null;
		MessageTemplate vhMsgTemp=new MessageTemplate(vhMsgArr);
		
		supergluArr.add(SuperGLUDefaultContextField);
		supergluArr.add(SuperGLUDefaultSpeechAct);
		
		MessageTemplate supergluMsgTemp=new MessageTemplate(supergluArr);
		
		
				
		
		//CREATING THE MESSAGETYPEBASED VHMESSAGE
		MessageType VHTMsgV1_8=new MessageType(v1.getFirstWord(), 0.0f, 1.1f,vhMsgTempGeneric,"VHMessage");
		
		MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_1",0.0f,1.1f,supergluMsgTempGeneric,"Message");
		
		
		//CREATING THE INNER FIELDS OF THE MAPPING 
		VHT_SuperGLU_CurrentScenario.setFieldMappings(fieldmappings);
		VHT_SuperGLU_CurrentScenario.setInDefaultMsgType(vhMsgTemp);
		VHT_SuperGLU_CurrentScenario.setOutDefaultMsgType(supergluMsgTemp);
		VHT_SuperGLU_CurrentScenario.setInMsgType(VHTMsgV1_8);
		VHT_SuperGLU_CurrentScenario.setOutMsgType(SuperGLUMsgV1);
		
		
		//STEP 1: CREATING A TOKEN OF A VHMESSAGE THAT WAS SENT ABOVE
		
		StorageToken ST_FromInputMsg=v1.saveToToken();
		
		System.out.println(ST_FromInputMsg.getClassId());
		System.out.println(ST_FromInputMsg.getItem(v1.FIRST_WORD_KEY));
		
		
		//STEP 2: CREATING THE ONTOLOGY CONVERTER OBJECT SO THAT WE CAN PASS IN THE MESSAGEMAPS LIST
		
		List<MessageMap> createdList=new ArrayList<MessageMap>();
		createdList.add(VHT_SuperGLU_CurrentScenario);
		
		OntologyConverter ontconvert=new OntologyConverter(createdList);
		
		//STEP 3: CALLING THE ISVALIDSOURCEMESSAGE CLASS
		
		String firstword=(String) ST_FromInputMsg.getItem(v1.FIRST_WORD_KEY);   
		
		boolean result=ontconvert.isValidSourceMsg(v1,ST_FromInputMsg,firstword);
		if(result==true)
			System.out.println("Yes there is a match and a valid source message");
		else
			System.out.println("No there is no match and its not a valid source message");
		
		//STEP 4: CALLING THE CONVERT FUNCTION FOR THE ACTUAL CONVERSIONS
		BaseMessage convertedMessage=ontconvert.convert(v1, ST_FromInputMsg);
		if(convertedMessage!=null)
			System.out.println("Conversion Successful!");
		else
			System.out.println("Conversion Failed");
		

	}

}
