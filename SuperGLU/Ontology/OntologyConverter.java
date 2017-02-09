package Ontology;

/**
 * OntologyConverter  Class 
 * This the class that provides the validity check of whether a message is valid or not and then further converts it if its 
 * mapped to one of the valid mappings
 * 
 * NOTE: This class will basically be redundant once the Ontology Broker is built.  
 * The core functionality should be relocated to MessageMapping.java  --Auerbach
 * 
 * @author tirthmehta
 */

import Core.BaseMessage;
import Core.Message;
import Ontology.Mappings.FieldData;
import Ontology.Mappings.FieldMap;
import Ontology.Mappings.MessageMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Ontology.Mappings.splitting;
import Util.SerializationConvenience;
import Util.StorageToken;
import java.util.*;

public class OntologyConverter
{
    static MessageMap correctMap = null;

    private List<MessageMap> messageMaps;

    public OntologyConverter()
    {
	messageMaps = null;
    }

    /**
     * Test code makes a mapping for scenarioName; Mapping is variable testMap;
     * x = [testMap,]
     * 
     * @param x
     */
    public OntologyConverter(List<MessageMap> x)
    {
	messageMaps = x;
    }

    /**
     * THE FUNCTION NECESSARY FOR CHECKING WHETHER THE MESSAGE INOUT TOKEN
     * COMING IN HAS A VALID MATCH WITH THE AVAIALABLE SET OF MAPPINGS
     */
    public boolean isValidSourceMsg(BaseMessage b, StorageToken input, String firstwordkey)
    {
	boolean first = false,second = false;
	
	for (MessageMap list : messageMaps)
	{    
	    MessageType in = list.getInMsgType();
					    
	    StorageToken ST_inMsgType = in.saveToToken();

	    if (input.getClassId().equals(ST_inMsgType.getItem(MessageType.MESSAGE_TYPE_CLASS_ID_KEY)))
	    {
		first=true;		
	    }
	    MessageTemplate mTemp = in.getMessageTemplate();
	    if(mTemp==null)
		System.out.println("haha mtemp is null");
	    ArrayList<NestedAtomic> arr = mTemp.getDefaultFieldData();
	   
	   
	    for (NestedAtomic nest : arr)
	    {
		
		if (nest.getFieldData().equals(firstwordkey))
		{
		    second=true; 
				
		    correctMap = list; // This is a terrible idea, and completely
				    // unnecessary to boot. What would happen if
				    // we had more than one converter running in
				    // a single process? --Auerbach
		    break;
		}
	    }
	    System.out.println("hi first"+first+" second "+second);
	    if (first && second)
		return true;

	}
	return false;
    }

    /**
     * 
     * THE CONVERT METHOD IS ACTUALLY USED TO PERFORM THE CONVERSION TO THE
     * TARGET MESSAGE OBJECT, ONCE THE VALID MAPPING HAS BEEN IDENTIFIED
     * 
     * @param b
     * @param input
     * @return
     */
    
    public BaseMessage convert(StorageToken input)
    {
	if (correctMap == null)
	    return null;
	MessageType out = correctMap.getOutMsgType();
	MessageTemplate mtemp = out.getMessageTemplate();
	StorageToken target = mtemp.createTargetStorageToken(out.getClassId());

	ArrayList<FieldMap> mappingList = correctMap.getFieldMappings();
	for (FieldMap maps : mappingList)
	{

	    NestedAtomic inFields = maps.getInFields();
	    List<String> inFieldsIndex = inFields.getIndex();
							

	    NestedAtomic outFields = maps.getOutFields();
	    List<String> outFieldsIndex = outFields.getIndex();

	    String valueToBeInserted = "";
	    HashMap<String, String> hmap = new HashMap<>();
	    for (String value : inFieldsIndex)
	    {
		if (input.contains(value))
		{

		    valueToBeInserted = (String) input.getItem(value);
		    if(maps.getSplitter()==null)
			hmap.put(value, valueToBeInserted);
		    else
		    {
			
			splitting current=maps.getSplitter();
			List<String> obtained=current.action(valueToBeInserted);
			int index=maps.getIndex();
			valueToBeInserted=obtained.get(index);
			hmap.put(value, valueToBeInserted);
			
		    }
		}

	    }

	    for (String value : outFieldsIndex)
	    {
		for (String key : hmap.keySet())
		{
		    target.setItem(value, hmap.get(key));
		    // Upgrade to a log file instead of console output --Auerbach
		}

	    }

	}
	
	
	//SETTING THE DEFAULT FIELD DATA
	
	/*
	
	MessageTemplate mtempOut = correctMap.getOutDefaulttMsgTemp();
	ArrayList<NestedAtomic> outarr=mtempOut.getDefaultFieldData();
	HashMap<String, String> hmap = new HashMap<>();
	for(NestedAtomic in:outarr)
	{
	    List<String> inside=in.getIndex();
	    String tobeset=in.getFieldData(); 
	    for(String key:inside)
	    {
		if(target.contains(key))
		{
		    hmap.put(key, in.getFieldData());
		}
	    }
	}
	System.out.println(hmap);
	
	for(String key:hmap.keySet())
	{
	    target.setItem(key, hmap.get(key));
	}
	
	*/
	
	
	
	
	

	BaseMessage targetObj = (BaseMessage) SerializationConvenience.untokenizeObject(target);
	
	if (targetObj != null)
	    return targetObj;
	else
	    return null;

    }

}
