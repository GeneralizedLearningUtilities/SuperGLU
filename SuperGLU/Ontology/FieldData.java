package Ontology;

public class FieldData {
	
	private String field_data;
	
	public FieldData(String data)
	{
		this.field_data=data;
	}
	
	public FieldData()
	{
		this.field_data="";
	}
	
	
	public String getFieldData()
	{
		return field_data;
	}
	
	public void setFieldData(String data)
	{
		field_data=data;
	}

}
