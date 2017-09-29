package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.core.VHMessage;
import org.junit.Test;

import java.util.HashMap;

public class CurrentScenarioTest {

	@Test
	public void test() {
		//fail("Not yet implemented");
		String given="ScenarioName Being Heard (Interview 1)";
		String first="ScenarioName";
		String body="Being Heard (Interview 1)";
		float version=0.0f;
		HashMap<String,Object> hmap=new HashMap<String, Object>();
		VHMessage v1=new VHMessage("100", hmap, first, version, body);
		
		System.out.println(v1.getFirstWord());
		System.out.println(v1.getBody());
		/*
		
		MessageType VHTMsgV1_8=new MessageType(v1.getFirstWord(), 0.0f, 1.1f);
		
		MessageType SuperGLUMsgV1=new MessageType("SUPERGLUMSG_1",0.0f,1.1f);
		
		MessageTemplate  VHTGenericTemplate =new MessageTemplate();
		
		
		FieldData SuperGLUDefaultSpeechAct=new FieldData("INFORM_ACT");
		FieldData SuperGLUDefaultContextField =new FieldData(" ");
		
		ArrayList<FieldData> superglu=new ArrayList<FieldData>();
		superglu.add(SuperGLUDefaultContextField);
		superglu.add(SuperGLUDefaultSpeechAct);
		
		NestedAtomic VHT_LabelField=new NestedAtomic();
		VHT_LabelField.setIndices("0");
		NestedAtomic VHT_BodyField=new NestedAtomic();
		VHT_BodyField.setIndices("1");
		
		NestedAtomic SuperGLU_ObjectField=new NestedAtomic();
		SuperGLU_ObjectField.setIndices("object");
		NestedAtomic SuperGLU_VerbField=new NestedAtomic();
		SuperGLU_VerbField.setIndices("verb");
		
		
		FieldMap VHT_SuperGLU_TopicVerb_FM=new FieldMap();
		VHT_SuperGLU_TopicVerb_FM.setInField(VHT_LabelField);
		VHT_SuperGLU_TopicVerb_FM.setOutField(SuperGLU_VerbField);
		
		FieldMap VHT_SuperGLU_TopicObject_FM=new FieldMap();
		VHT_SuperGLU_TopicObject_FM.setInField(VHT_BodyField);
		VHT_SuperGLU_TopicObject_FM.setOutField(SuperGLU_ObjectField);
		
		ArrayList<FieldMap> fieldmappings=new ArrayList<FieldMap>();
		fieldmappings.add(VHT_SuperGLU_TopicVerb_FM);
		fieldmappings.add(VHT_SuperGLU_TopicObject_FM);
		
		
		
		MessageTemplate SuperGLUGenericTemplate= new MessageTemplate();
		
		SuperGLUGenericTemplate.setData(superglu);
		
		MessageTwoWayMap VHT_SuperGLU_CurrentScenario=new MessageTwoWayMap();
		VHT_SuperGLU_CurrentScenario.setInMsgType(SuperGLUMsgV1);
		VHT_SuperGLU_CurrentScenario.setOutMsgType(VHTMsgV1_8);
		VHT_SuperGLU_CurrentScenario.setInDefaultMsgType(SuperGLUGenericTemplate);
		VHT_SuperGLU_CurrentScenario.setOutDefaultMsgType(VHTGenericTemplate);
		VHT_SuperGLU_CurrentScenario.setFieldMappings(fieldmappings);
		
		
		*/
		
	}

}
