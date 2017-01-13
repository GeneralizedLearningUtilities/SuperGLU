package Ontology.Mappings;
import java.util.*;

public class MessageMap 
{
	MessageType inMsgType= new MessageType();
	
	MessageType outMsgType= new MessageType();
	
	MessageTemplate inDefaultMsg= new MessageTemplate();
	
	MessageTemplate outDefaultMsg= new MessageTemplate();
	
	ArrayList<FieldMap> fieldMappings;
	
	public void setInMsgType(MessageType x)
	{
		inMsgType=x;
	}
	
	public void setOutMsgType(MessageType x)
	{
		outMsgType=x;
	}
	
	public void setInDefaultMsgType(MessageTemplate x)
	{
		inDefaultMsg=x;
	}
	
	public void setOutDefaultMsgType(MessageTemplate x)
	{
		outDefaultMsg=x;
	}
	
	public void setFieldMappings(ArrayList<FieldMap> x)
	{
		for(FieldMap y:x)
			fieldMappings.add(y);
	}
	
	
	
	
}

