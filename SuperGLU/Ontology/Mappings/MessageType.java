package Ontology.Mappings;

import Util.Serializable;
import Util.StorageToken;

public class MessageType extends Serializable {
	
	private String Message_Name;
	private float min_Version;
	private float max_Version;
	public MessageTemplate messageTypeTemplate = new MessageTemplate();
	
	
	
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

	
	
	
	
	
	
	//my methods
	
	public MessageType(String name, float minversion, float maxversion)
	{
		this.Message_Name=name;
		this.min_Version=minversion;
		this.max_Version=maxversion;
	}
	
	public MessageType()
	{
		this.Message_Name="";
		this.max_Version=0.0f;
		this.min_Version=0.0f;
	}
	
	
	public String getMessageName()
	{
		return Message_Name;
	}
	
	public void setMessageName(String name)
	{
		Message_Name=name;
	}
	
	public float getMinVersion()
	{
		return min_Version;
	}
	
	public void setMinVersion(float minversion)
	{
		min_Version=minversion;
	}
	
	public float getMaxVersion()
	{
		return max_Version;
	}
	
	public void setMaxVersion(float maxversion)
	{
		max_Version=maxversion;
	}
	
	    
}
