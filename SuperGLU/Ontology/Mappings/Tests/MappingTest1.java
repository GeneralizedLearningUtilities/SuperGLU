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
import Ontology.Mappings.MessageMapFactory;
import Ontology.Mappings.MessageOneWayMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageTwoWayMap;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Ontology.Mappings.Splitting;
import Util.StorageToken;
import junit.framework.Assert;

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
		
		

	MessageOneWayMap VHT_SuperGLU_CurrentScenario=(MessageOneWayMap) MessageMapFactory.buildVHTSuperGLUCurrentScenarioMapping();
	
		
		
		

		
		
		
		
		
		
		
		
		
		
		
		
	
		
		
		
		
		
		
		
		
		
		//THIS IS THE POINT WHERE DATA SHOULD BE CHECKED----------
		
		/*
		//STEP 1: CREATING A TOKEN OF A VHMESSAGE THAT WAS SENT ABOVE
		
		StorageToken ST_FromInputMsg=v1.saveToToken();
		
		System.out.println(ST_FromInputMsg.getClassId());
		//System.out.println(ST_FromInputMsg.getItem(v1.FIRST_WORD_KEY));
		
		
		//STEP 2: CREATING THE ONTOLOGY CONVERTER OBJECT SO THAT WE CAN PASS IN THE MESSAGEMAPS LIST
		
		List<MessageMap> createdList=MessageMapFactory.buildMessageMaps();

		//createdList.add(VHT_SuperGLU_beginAAR);
		//createdList.add(VHT_SuperGLU_getNextAgendaItem);
		//createdList.add(VHT_SuperGLU_requestCoachingActions);
		//createdList.add(VHT_SuperGLU_commAPI);
		
		
		//MessageMap test1=new MessageMap(createdList);
		
		 
		//STEP 3: CALLING THE ISVALIDSOURCEMESSAGE CLASS
		
		String firstword=(String) ST_FromInputMsg.getItem(VHMessage.FIRST_WORD_KEY);  
		System.out.println("check "+firstword);
		
		
		boolean result=test1.isValidSourceMsg(ST_FromInputMsg,firstword);
		if(result==true)
			System.out.println("Yes there is a match and a valid source message");
		else
			System.out.println("No there is no match and its not a valid source message");
		
		
		//STEP 4: CALLING THE CONVERT FUNCTION FOR THE ACTUAL CONVERSIONS
		StorageToken convertedMessage=test1.convert(ST_FromInputMsg);
		//Assert.assertEquals(expected, actual);
		if(convertedMessage!=null)
			System.out.println("Conversion Successful!");
		else
			System.out.println("Conversion Failed");  
		
		
		
	*/
		
		
		
		
	}

}
