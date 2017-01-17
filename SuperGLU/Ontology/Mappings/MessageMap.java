package Ontology.Mappings;
import java.util.*;

import Util.Serializable;
import Util.StorageToken;

public class MessageMap extends Serializable
{
	MessageType inMsgType= new MessageType();
	
	MessageType outMsgType= new MessageType();
	
	MessageTemplate inDefaultMsg= new MessageTemplate();
	
	MessageTemplate outDefaultMsg= new MessageTemplate();
	
	ArrayList<FieldMap> fieldMappings;
	
	
	
	@Override
	public boolean equals(Object otherObject) {
		// TODO Auto-generated method stub
		return super.equals(otherObject);
	}

	@Override
	public int hashCode() {
		// TODO Auto-generated method stub
		return super.hashCode();
	}

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return super.getId();
	}

	@Override
	public void updateId(String id) {
		// TODO Auto-generated method stub
		super.updateId(id);
	}

	@Override
	public String getClassId() {
		// TODO Auto-generated method stub
		return super.getClassId();
	}

	@Override
	public void initializeFromToken(StorageToken token) {
		// TODO Auto-generated method stub
		super.initializeFromToken(token);
	}

	@Override
	public StorageToken saveToToken() {
		// TODO Auto-generated method stub
		return super.saveToToken();
	}

	@Override
	public Serializable clone(boolean newId) {
		// TODO Auto-generated method stub
		return super.clone(newId);
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		// TODO Auto-generated method stub
		return super.clone();
	}

	@Override
	protected void finalize() throws Throwable {
		// TODO Auto-generated method stub
		super.finalize();
	}

	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return super.toString();
	}
	
	
	
	
	
	//my methods
	
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

