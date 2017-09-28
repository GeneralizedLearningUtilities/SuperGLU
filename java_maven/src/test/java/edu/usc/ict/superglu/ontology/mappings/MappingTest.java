package edu.usc.ict.superglu.ontology.mappings;

/**
 * MessageMapTest1  Junit Testcase
 * The testfile containing the data of storing all the mappings and further performing some tests for validity checks
 * and also for the conversions
 *
 * @author tirthmehta
 */

public class MappingTest
{
/*
    @Test
    public void test()
    {
	// fail("Not yet implemented");
	// CREATED THE INITIAL VHMESSAGE
	String first = "ScenarioName";
	String body = "Being Heard (Interview 1)";
	float version = 0.0f;
	HashMap<String, Object> hmap = new HashMap<String, Object>();
	VHMessage v1 = new VHMessage("100", hmap, first, version, body);

	// THE MESSAGE MAP TO BE PASSED TO THE ONTOLOGY CONVERTER-----LATER ON
	// AN ARRAYLIST OF MESSAGE-MAPS ARE TO BE PASSED
	MessageMap VHT_SuperGLU_CurrentScenario = MessageMapFactory.buildVHTSuperGLUCurrentScenarioMapping();

	// checking starts here

	// STEP 1: CREATING A TOKEN OF A VHMESSAGE THAT WAS SENT ABOVE

	StorageToken ST_FromInputMsg = v1.saveToToken();

	System.out.println(ST_FromInputMsg.getClassId());
	// System.out.println(ST_FromInputMsg.getItem(v1.FIRST_WORD_KEY));

	// STEP 2: CREATING THE ONTOLOGY CONVERTER OBJECT SO THAT WE CAN PASS IN
	// THE MESSAGEMAPS LIST

	List<MessageMap> createdList = MessageMapFactory.buildMessageMaps();
	// createdList.add(VHT_SuperGLU_CurrentScenario);
	// createdList.add(VHT_SuperGLU_beginAAR);
	// createdList.add(VHT_SuperGLU_getNextAgendaItem);
	// createdList.add(VHT_SuperGLU_requestCoachingActions);
	// createdList.add(VHT_SuperGLU_commAPI);

	OntologyConverter ontconvert = new OntologyConverter(createdList);
	MessageMap test1 = new MessageMap();

	// STEP 3: CALLING THE ISVALIDSOURCEMESSAGE CLASS

	String firstword = (String) ST_FromInputMsg.getItem(VHMessage.FIRST_WORD_KEY);
	System.out.println("check " + firstword);

	boolean result = VHT_SuperGLU_CurrentScenario.isValidSourceMsg(ST_FromInputMsg, firstword);
	if (result == true)
	    System.out.println("Yes there is a match and a valid source message");
	else
	    System.out.println("No there is no match and its not a valid source message");

	// STEP 4: CALLING THE CONVERT FUNCTION FOR THE ACTUAL CONVERSIONS
	StorageToken convertedMessage = VHT_SuperGLU_CurrentScenario.convert(ST_FromInputMsg);
	Assert.assertNotNull(convertedMessage);
	Assert.assertEquals(convertedMessage.getItem("verb"), "ScenarioName");
	System.out.println("Conversion Successful!");

	convertedMessage.setItem("context", new HashMap<>());

	Message expected = (Message) SerializationConvenience.untokenizeObject(convertedMessage);

	Assert.assertEquals(expected.getObj(), "Being Heard (Interview 1)");

	expected.toString();
    }
*/
}
