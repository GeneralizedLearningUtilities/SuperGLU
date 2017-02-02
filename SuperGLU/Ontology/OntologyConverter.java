package Ontology;

/*

/**
 * OntologyConverter  Class 
 * This the class that provides the validity check of whether a message is valid or not and then further converts it if its 
 * mapped to one of the valid mappings
 * @author tirthmehta
 */

import Core.BaseMessage;
import Ontology.Mappings.FieldData;
import Ontology.Mappings.FieldMap;
import Ontology.Mappings.MessageMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Util.SerializationConvenience;
import Util.StorageToken;
import java.util.*;

public class OntologyConverter {
	static MessageMap correctMap=null;
	
	private List<MessageMap> messageMaps;
	
	public OntologyConverter()
	{
		messageMaps=null;
	}
	// Test code makes a mapping for scenarioName; Mapping is variable testMap; x = [testMap,]
	public OntologyConverter(List<MessageMap> x)
	{
		messageMaps=x;
	}
	
	
	
//THE FUNCTION NECESSARY FOR CHECKING WHETHER THE MESSAGE INOUT TOKEN COMING IN HAS A VALID MATCH WITH THE AVAIALABLE SET 
//	OF MAPPINGS
	
	public boolean isValidSourceMsg(BaseMessage b,StorageToken input,String firstwordkey)
	{
		//CURRENTLY SINCE THERE IS ONLY 1 MESSAGEMAP IN THE LIST OF MESSAGEMAPS
				for(MessageMap x:messageMaps)
				{
					int count=0;
					MessageType in=x.getInMsgType();
					
					StorageToken ST_inMsgType=in.saveToToken();
					
				
					
					if(input.getClassId().equals(ST_inMsgType.getItem(in.MESSAGE_TYPE_CLASS_ID_KEY)))
					{
						count=1;
					}
					MessageTemplate mTemp= in.getMessageTemplate();
					ArrayList<FieldData> arr=mTemp.getDefaultFieldData();
					for(FieldData y:arr)
					{
						if(y.getFieldData().equals(firstwordkey))
							{
								count+=1;
								correctMap=x;
								break;
							}			
					}
					if(count==2)
						return true;
					
				}
				return false;
	}
	
	
	//THE CONVERT METHOD IS ACTUALLY USED TO PERFORM THE CONVERSION TO THE TARGET MESSAGE OBJECT, ONCE THE VALID MAPPING
	// HAS BEEN IDENTIFIED

	public BaseMessage convert(BaseMessage b,StorageToken input)
	{
		if(correctMap==null)
			return null;
		MessageType out=correctMap.getOutMsgType();
		MessageTemplate mtemp=out.getMessageTemplate();
		StorageToken target=mtemp.createTargetStorageToken(out.getClassId());
		
				
		ArrayList<FieldMap> mappingList=correctMap.getFieldMappings();
		for(FieldMap maps: mappingList)
		{
			
			NestedAtomic inFields=maps.getInFields();
			String[] inFieldsIndex=inFields.getIndex();
			
			NestedAtomic outFields=maps.getOutFields();
			String[] outFieldsIndex=outFields.getIndex();
			
			String valueToBeInserted="";
			HashMap<String, String> hmap=new HashMap<>();
			for(String value:inFieldsIndex)
			{
				if(input.contains(value))
				{
					
					valueToBeInserted=(String) input.getItem(value); 
					
					hmap.put(value, valueToBeInserted);
				}
							
			}
			
			
			for(String value:outFieldsIndex)
			{
				for(String key: hmap.keySet())
				{		   
					target.setItem(value,hmap.get(key));
					System.out.println("check value "+target.getItem(value));
				}
			    		    
			}
								
		}
		
		BaseMessage targetObj=(BaseMessage) SerializationConvenience.untokenizeObject(target);
		
		if(targetObj!=null)
			return targetObj;
		else
			return null;
	
	}

}
