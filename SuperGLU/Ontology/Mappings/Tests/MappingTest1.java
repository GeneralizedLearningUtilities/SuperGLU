package Ontology.Mappings.Tests;
import java.util.*;
import static org.junit.Assert.*;

/**
 * MessageMapTest1  Junit Testcase
 * The testfile containing the data of storing all the mappings and further performing some tests for validity checks 
 * and also for the conversions
 * @author tirthmehta
 */

import org.junit.Test;

import Core.BaseMessage;
import Core.Message;
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
		String first="requestCoachingActions";
		String body="Being Heard (Interview 1)";
		float version=0.0f;
		HashMap<String,Object> hmap=new HashMap<String, Object>();
		VHMessage v1=new VHMessage("100", hmap, first, version, body);
		
		
//---------------------------------------FIRST MAPPING ScenarioNameToSuperGLU----------------------------------------------//
		
		
		//THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
		MessageOneWayMap VHT_SuperGLU_CurrentScenario=new MessageOneWayMap();
		
		
		//CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2 MESSAGE TEMPLATES
		ArrayList<FieldData> supergluArrGeneric=new ArrayList<FieldData>();
		ArrayList<FieldData> vhMsgArrGeneric=new ArrayList<FieldData>();
		
		
		//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
		FieldData SuperGLUDefaultSpeechAct=new FieldData("INFORM_ACT");
		FieldData SuperGLUDefaultContextField =new FieldData("");
		FieldData SuperGLUDefaultVerbField=new FieldData("");
		FieldData SuperGLUDefaultObjectField=new FieldData("");
		FieldData SuperGLUDefaultResultField=new FieldData("");
		
		supergluArrGeneric.add(SuperGLUDefaultSpeechAct);
		supergluArrGeneric.add(SuperGLUDefaultContextField);
		supergluArrGeneric.add(SuperGLUDefaultVerbField);
		supergluArrGeneric.add(SuperGLUDefaultObjectField);
		supergluArrGeneric.add(SuperGLUDefaultResultField);
		
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
		String indexvh1[]=new String[1];
		String indexvh2[]=new String[1];
		indexvh1[0]=VHMessage.FIRST_WORD_KEY;
		indexvh2[0]=VHMessage.BODY_KEY;
		NestedAtomic VHT_LabelField=new NestedAtomic(indexvh1);	
		NestedAtomic VHT_BodyField=new NestedAtomic(indexvh2);
		
		//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
		String indexsg1[]=new String[1];
		String indexsg2[]=new String[1];
		indexsg1[0]=Message.OBJECT_KEY;
		indexsg2[0]=Message.VERB_KEY;
		NestedAtomic SuperGLU_ObjectField=new NestedAtomic(indexsg1);	
		NestedAtomic SuperGLU_VerbField=new NestedAtomic(indexsg2);
		
		
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
		supergluArr.add(SuperGLUDefaultResultField);
		
		MessageTemplate supergluMsgTemp=new MessageTemplate(supergluArr);
		
		
				
		
		//CREATING THE MESSAGETYPEBASED VHMESSAGE
		MessageType VHTMsgV1_8=new MessageType("ScenarioName", 0.0f, 1.1f,vhMsgTempGeneric,"VHMessage");
		
		MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_1",0.0f,1.1f,supergluMsgTempGeneric,"Message");
		
		
		//CREATING THE INNER FIELDS OF THE MAPPING 
		VHT_SuperGLU_CurrentScenario.setFieldMappings(fieldmappings);
		VHT_SuperGLU_CurrentScenario.setInDefaultMsgType(vhMsgTemp);
		VHT_SuperGLU_CurrentScenario.setOutDefaultMsgType(supergluMsgTemp);
		VHT_SuperGLU_CurrentScenario.setInMsgType(VHTMsgV1_8);
		VHT_SuperGLU_CurrentScenario.setOutMsgType(SuperGLUMsgV1);
		
//----------------------------------- FIRST MAPPING CREATION ENDS HERE------------------------------------------------//				

		
		
//---------------------------------------SECOND MAPPING beginAARToSuperGLU----------------------------------------------//
		
		//THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
				MessageOneWayMap VHT_SuperGLU_beginAAR=new MessageOneWayMap();
				
				
				//CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2 MESSAGE TEMPLATES
				ArrayList<FieldData> supergluArrGeneric2=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArrGeneric2=new ArrayList<FieldData>();
				
				
				//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
				FieldData SuperGLUDefaultSpeechAct2=new FieldData("INFORM_ACT");
				FieldData SuperGLUDefaultContextField2 =new FieldData("");
				FieldData SuperGLUDefaultVerbField2=new FieldData("");
				FieldData SuperGLUDefaultObjectField2=new FieldData("");
				FieldData SuperGLUDefaultResultField2=new FieldData("");
				FieldData SuperGLUDefaultActorField2=new FieldData("DIALOG_MANAGER");
				
				supergluArrGeneric2.add(SuperGLUDefaultSpeechAct2);
				supergluArrGeneric2.add(SuperGLUDefaultContextField2);
				supergluArrGeneric2.add(SuperGLUDefaultVerbField2);
				supergluArrGeneric2.add(SuperGLUDefaultObjectField2);
				supergluArrGeneric2.add(SuperGLUDefaultActorField2);
				supergluArrGeneric2.add(SuperGLUDefaultResultField2);
				
				//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
				MessageTemplate supergluMsgTempGeneric2=new MessageTemplate(supergluArrGeneric2);
				
				//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
				FieldData vhMsgDefaultLabelField2 =new FieldData("beginAAR");
				FieldData vhMsgDefaultBodyField2 =new FieldData("");
				vhMsgArrGeneric2.add(vhMsgDefaultLabelField2);
				vhMsgArrGeneric2.add(vhMsgDefaultBodyField2);
				
				//STORED THE DATA IN THE VH MESSAGE TEMPLATE
				MessageTemplate vhMsgTempGeneric2=new MessageTemplate(vhMsgArrGeneric2);
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index2vh1[]=new String[1];
				String index2vh2[]=new String[1];
				index2vh1[0]=VHMessage.FIRST_WORD_KEY;
				index2vh2[0]=VHMessage.BODY_KEY;
				NestedAtomic VHT_LabelField2=new NestedAtomic(index2vh1);	
				NestedAtomic VHT_BodyField2=new NestedAtomic(index2vh2);
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index2sg1[]=new String[1];
				String index2sg2[]=new String[1];
				index2sg1[0]=Message.OBJECT_KEY;
				index2sg2[0]=Message.VERB_KEY;
				NestedAtomic SuperGLU_ObjectField2=new NestedAtomic(index2sg1);	
				NestedAtomic SuperGLU_VerbField2=new NestedAtomic(index2sg2);
				
				
				//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
				FieldMap VHT_SuperGLU_TopicVerb_FM2=new FieldMap();
				VHT_SuperGLU_TopicVerb_FM2.setInField(VHT_LabelField2);
				VHT_SuperGLU_TopicVerb_FM2.setOutField(SuperGLU_VerbField2);
				
				FieldMap VHT_SuperGLU_TopicObject_FM2=new FieldMap();
				VHT_SuperGLU_TopicObject_FM2.setInField(VHT_BodyField2);
				VHT_SuperGLU_TopicObject_FM2.setOutField(SuperGLU_ObjectField2); 
				
				ArrayList<FieldMap> fieldmappings2=new ArrayList<FieldMap>();
				fieldmappings2.add(VHT_SuperGLU_TopicVerb_FM2);
				fieldmappings2.add(VHT_SuperGLU_TopicObject_FM2);
				
				
				//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
				
				
				ArrayList<FieldData> supergluArr2=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArr2=null;
				
				MessageTemplate vhMsgTemp2=new MessageTemplate(vhMsgArr2);
				
				supergluArr2.add(SuperGLUDefaultContextField2);
				supergluArr2.add(SuperGLUDefaultSpeechAct2);
				supergluArr2.add(SuperGLUDefaultActorField2);
				supergluArr2.add(SuperGLUDefaultResultField2);
				
				MessageTemplate supergluMsgTemp2=new MessageTemplate(supergluArr2);
				
				
						
				
				//CREATING THE MESSAGETYPEBASED VHMESSAGE
				MessageType VHTMsgV2_8=new MessageType("beginAAR", 0.0f, 1.1f,vhMsgTempGeneric2,"VHMessage");
				
				MessageType SuperGLUMsgV2=new MessageType("SUPERGLUMSG_2",0.0f,1.1f,supergluMsgTempGeneric2,"Message");
				
				
				//CREATING THE INNER FIELDS OF THE MAPPING 
				VHT_SuperGLU_beginAAR.setFieldMappings(fieldmappings2);
				VHT_SuperGLU_beginAAR.setInDefaultMsgType(vhMsgTemp2);
				VHT_SuperGLU_beginAAR.setOutDefaultMsgType(supergluMsgTemp2);
				VHT_SuperGLU_beginAAR.setInMsgType(VHTMsgV2_8);
				VHT_SuperGLU_beginAAR.setOutMsgType(SuperGLUMsgV2);
		
//----------------------------------- SECOND MAPPING CREATION ENDS HERE------------------------------------------------//				
		
//---------------------------------------THIRD MAPPING getNextAgendaItemToSuperGLU----------------------------------------------//
		
				//THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
				MessageOneWayMap VHT_SuperGLU_getNextAgendaItem=new MessageOneWayMap();
				
				
				//CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2 MESSAGE TEMPLATES
				ArrayList<FieldData> supergluArrGeneric3=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArrGeneric3=new ArrayList<FieldData>();
				
				
				//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
				FieldData SuperGLUDefaultSpeechAct3=new FieldData("INFORM_ACT");
				FieldData SuperGLUDefaultVerbField3=new FieldData("");
				FieldData SuperGLUDefaultObjectField3=new FieldData("");
				FieldData SuperGLUDefaultActorField3=new FieldData("DIALOG_MANAGER");
				
				supergluArrGeneric3.add(SuperGLUDefaultSpeechAct3);				
				supergluArrGeneric3.add(SuperGLUDefaultVerbField3);
				supergluArrGeneric3.add(SuperGLUDefaultObjectField3);
				supergluArrGeneric3.add(SuperGLUDefaultActorField3);
				
				
				//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
				MessageTemplate supergluMsgTempGeneric3=new MessageTemplate(supergluArrGeneric3);
				
				//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
				FieldData vhMsgDefaultLabelField3 =new FieldData("getNextAgendaItem");
				FieldData vhMsgDefaultBodyField3 =new FieldData("");
				vhMsgArrGeneric3.add(vhMsgDefaultLabelField3);
				vhMsgArrGeneric3.add(vhMsgDefaultBodyField3);
				
				//STORED THE DATA IN THE VH MESSAGE TEMPLATE
				MessageTemplate vhMsgTempGeneric3=new MessageTemplate(vhMsgArrGeneric3);
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index3vh1[]=new String[1];
				
				index3vh1[0]=VHMessage.FIRST_WORD_KEY;
				
				NestedAtomic VHT_LabelField3=new NestedAtomic(index3vh1);	
				
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index3sg1[]=new String[1];			
				
				index3sg1[0]=Message.VERB_KEY;				
				NestedAtomic SuperGLU_VerbField3=new NestedAtomic(index3sg1);
				
				
				//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
				FieldMap VHT_SuperGLU_TopicVerb_FM3=new FieldMap();
				VHT_SuperGLU_TopicVerb_FM3.setInField(VHT_LabelField3);
				VHT_SuperGLU_TopicVerb_FM3.setOutField(SuperGLU_VerbField3);
				
				
				
				ArrayList<FieldMap> fieldmappings3=new ArrayList<FieldMap>();
				fieldmappings3.add(VHT_SuperGLU_TopicVerb_FM3);
			
				
				
				//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
				
				
				ArrayList<FieldData> supergluArr3=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArr3=null;
				
				MessageTemplate vhMsgTemp3=new MessageTemplate(vhMsgArr3);
				
				
				supergluArr3.add(SuperGLUDefaultSpeechAct3);
				supergluArr3.add(SuperGLUDefaultActorField3);
				supergluArr3.add(SuperGLUDefaultObjectField3);
				
				
				MessageTemplate supergluMsgTemp3=new MessageTemplate(supergluArr3);
				
				
						
				
				//CREATING THE MESSAGETYPEBASED VHMESSAGE
				MessageType VHTMsgV3_8=new MessageType("getNextAgendaItem", 0.0f, 1.1f,vhMsgTempGeneric3,"VHMessage");
				
				MessageType SuperGLUMsgV3=new MessageType("SUPERGLUMSG_3",0.0f,1.1f,supergluMsgTempGeneric3,"Message");
				
				
				//CREATING THE INNER FIELDS OF THE MAPPING 
				VHT_SuperGLU_getNextAgendaItem.setFieldMappings(fieldmappings3);
				VHT_SuperGLU_getNextAgendaItem.setInDefaultMsgType(vhMsgTemp3);
				VHT_SuperGLU_getNextAgendaItem.setOutDefaultMsgType(supergluMsgTemp3);
				VHT_SuperGLU_getNextAgendaItem.setInMsgType(VHTMsgV3_8);
				VHT_SuperGLU_getNextAgendaItem.setOutMsgType(SuperGLUMsgV3);			
				
				
				
//----------------------------------- THIRD MAPPING CREATION ENDS HERE------------------------------------------------//				

//---------------------------------------FOURTH MAPPING requestCoachingActionsToSuperGLU----------------------------------------------//

				//THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
				MessageOneWayMap VHT_SuperGLU_requestCoachingActions=new MessageOneWayMap();
				
				
				//CREATED THE 2 ARRAYLISTS USED TO STORE THE DEFAULT MESSAGES FOR THE 2 MESSAGE TEMPLATES
				ArrayList<FieldData> supergluArrGeneric4=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArrGeneric4=new ArrayList<FieldData>();
				
				
				//CREATED THE DEFAULT FIELDS IN THE SUPERGLUMSG TEMPLATE
				FieldData SuperGLUDefaultSpeechAct4=new FieldData("REQUEST_ACT");
				FieldData SuperGLUDefaultVerbField4=new FieldData("");
				FieldData SuperGLUDefaultObjectField4=new FieldData("");
				FieldData SuperGLUDefaultActorField4=new FieldData("DIALOG_MANAGER");
				
				supergluArrGeneric4.add(SuperGLUDefaultSpeechAct4);				
				supergluArrGeneric4.add(SuperGLUDefaultVerbField4);
				supergluArrGeneric4.add(SuperGLUDefaultObjectField4);
				supergluArrGeneric4.add(SuperGLUDefaultActorField4);
				
				
				//STORED THE DATA IN THE SUPERGLU MESSAGE TEMPLATE
				MessageTemplate supergluMsgTempGeneric4=new MessageTemplate(supergluArrGeneric4);
				
				//CREATED THE DEFAULT FIELDS IN THE VHMSG TEMPLATE
				FieldData vhMsgDefaultLabelField4 =new FieldData("requestCoachingActions");
				FieldData vhMsgDefaultBodyField4 =new FieldData("");
				vhMsgArrGeneric4.add(vhMsgDefaultLabelField4);
				vhMsgArrGeneric4.add(vhMsgDefaultBodyField4);
				
				//STORED THE DATA IN THE VH MESSAGE TEMPLATE
				MessageTemplate vhMsgTempGeneric4=new MessageTemplate(vhMsgArrGeneric4);
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index4vh1[]=new String[1];
				index4vh1[0]=VHMessage.FIRST_WORD_KEY;
				
				NestedAtomic VHT_LabelField4=new NestedAtomic(index4vh1);	
				
				
				//CREATING THE NESTED ATOMIC FIELDS THAT HAVE MATCHES (VHT)
				String index4sg1[]=new String[1];			
				
				index4sg1[0]=Message.VERB_KEY;				
				NestedAtomic SuperGLU_VerbField4=new NestedAtomic(index4sg1);
				
				
				//CREATED THE MAPPINGS FOR THE VERB AND BODY FIELDS RESPECTIVELY BELOW 
				FieldMap VHT_SuperGLU_TopicVerb_FM4=new FieldMap();
				VHT_SuperGLU_TopicVerb_FM4.setInField(VHT_LabelField4);
				VHT_SuperGLU_TopicVerb_FM4.setOutField(SuperGLU_VerbField4);
				
				
				
				ArrayList<FieldMap> fieldmappings4=new ArrayList<FieldMap>();
				fieldmappings4.add(VHT_SuperGLU_TopicVerb_FM4);
			
				
				
				//CREATING A MESSAGE TEMPLATE THAT WILL GO INTO THE DEFAULT MESSAGETEMPLATES (WHICH DOES NOT HAVE MATCHES)
				
				
				ArrayList<FieldData> supergluArr4=new ArrayList<FieldData>();
				ArrayList<FieldData> vhMsgArr4=null;
				
				MessageTemplate vhMsgTemp4=new MessageTemplate(vhMsgArr4);
				
				
				supergluArr4.add(SuperGLUDefaultSpeechAct4);
				supergluArr4.add(SuperGLUDefaultActorField4);
				supergluArr4.add(SuperGLUDefaultObjectField4);
				
				
				MessageTemplate supergluMsgTemp4=new MessageTemplate(supergluArr4);
				
				
						
				
				//CREATING THE MESSAGETYPEBASED VHMESSAGE
				MessageType VHTMsgV4_8=new MessageType("requestCoachingActions", 0.0f, 1.1f,vhMsgTempGeneric4,"VHMessage");
				
				MessageType SuperGLUMsgV4=new MessageType("SUPERGLUMSG_4",0.0f,1.1f,supergluMsgTempGeneric4,"Message");
				
				
				//CREATING THE INNER FIELDS OF THE MAPPING 
				VHT_SuperGLU_requestCoachingActions.setFieldMappings(fieldmappings4);
				VHT_SuperGLU_requestCoachingActions.setInDefaultMsgType(vhMsgTemp4);
				VHT_SuperGLU_requestCoachingActions.setOutDefaultMsgType(supergluMsgTemp4);
				VHT_SuperGLU_requestCoachingActions.setInMsgType(VHTMsgV4_8);
				VHT_SuperGLU_requestCoachingActions.setOutMsgType(SuperGLUMsgV4);				
				
								
				
//----------------------------------- FOURTH MAPPING CREATION ENDS HERE------------------------------------------------//				

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		//STEP 1: CREATING A TOKEN OF A VHMESSAGE THAT WAS SENT ABOVE
		
		StorageToken ST_FromInputMsg=v1.saveToToken();
		
		System.out.println(ST_FromInputMsg.getClassId());
		//System.out.println(ST_FromInputMsg.getItem(v1.FIRST_WORD_KEY));
		
		
		//STEP 2: CREATING THE ONTOLOGY CONVERTER OBJECT SO THAT WE CAN PASS IN THE MESSAGEMAPS LIST
		
		List<MessageMap> createdList=new ArrayList<MessageMap>();
		createdList.add(VHT_SuperGLU_CurrentScenario);
		createdList.add(VHT_SuperGLU_beginAAR);
		createdList.add(VHT_SuperGLU_getNextAgendaItem);
		createdList.add(VHT_SuperGLU_requestCoachingActions);
		
		OntologyConverter ontconvert=new OntologyConverter(createdList);
		 
		//STEP 3: CALLING THE ISVALIDSOURCEMESSAGE CLASS
		
		String firstword=(String) ST_FromInputMsg.getItem(VHMessage.FIRST_WORD_KEY);  
		
		
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
