package Ontology.Mappings;

import java.util.ArrayList;

public class MessageTemplate {
	
	public ArrayList<FieldData> defaultFieldData;
	
	public void setData(ArrayList<FieldData> y)
	{
		for(FieldData x:y)
		{
			defaultFieldData.add(x);
		}
	}
	
	public ArrayList<FieldData> getData()
	{
		return defaultFieldData;
	}
	
	
	
	

}
