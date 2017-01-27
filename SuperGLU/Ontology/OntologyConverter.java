package Ontology;
/**
 * OntologyConverter  Class
 * @author tirthmehta
 */

import Core.BaseMessage;
import Core.Message;
import Core.VHMessage;
import Ontology.Mappings.FieldData;
import Ontology.Mappings.FieldMap;
import Ontology.Mappings.MessageMap;
import Ontology.Mappings.MessageTemplate;
import Ontology.Mappings.MessageTwoWayMap;
import Ontology.Mappings.MessageType;
import Ontology.Mappings.NestedAtomic;
import Util.SerializationConvenience;
import Util.StorageToken;
import java.util.*;


public class OntologyConverter {
	
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
	

	public boolean isValidSourceMsg(BaseMessage b,StorageToken input,String firstwordkey)
	{
		//CURRENTLY SINCE THERE IS ONLY 1 MESSAGEMAP IN THE LIST OF MESSAGEMAPS
		for(MessageMap x:messageMaps)
		{
			int count=0;
			MessageType in=x.getInMsgType();
			MessageType out=x.getOutMsgType();
			StorageToken ST_inMsgType=in.saveToToken();
			StorageToken ST_outMsgType=out.saveToToken();
		
			
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
						break;
					}			
			}
			if(count==2)
				return true;
			
		}
		return false;
	}
	
	
	
	
	
	

}
