package Ontology;

public class Message_Type {
	
	private String Message_Name;
	private float min_Version;
	private float max_Version;
	public Message_Template messageTypeTemplate = new Message_Template();
	
	
	
	public Message_Type(String name, float minversion, float maxversion)
	{
		this.Message_Name=name;
		this.min_Version=minversion;
		this.max_Version=maxversion;
	}
	
	public Message_Type()
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
