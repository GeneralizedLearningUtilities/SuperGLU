package Ontology.Mappings;

public class Field_Data {
	
	private String field_data;
	
	public Field_Data(String data)
	{
		this.field_data=data;
	}
	
	public Field_Data()
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
