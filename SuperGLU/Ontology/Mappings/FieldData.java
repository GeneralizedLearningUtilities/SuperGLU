package Ontology.Mappings;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * 
 * @author auerbach
 *
 */
public class FieldData extends Serializable{
	
	public static final String FIELD_DATA_KEY = "fieldData";
	
	private String fieldData;
	
	
	//my methods  (DANIEL: Does this comment say anything of value?  If it doesn't replace it with one that does, or get rid of it)
	//Constructors
	public FieldData(String data)
	{
		//DANIEL: make sure to check for null values when setting field data;
		if(data == null)
			this.fieldData="";
		else
			this.fieldData=data;
	}
	
		
	public FieldData()
	{
		this.fieldData="";
	}
	
	
	//Accessors
	public String getFieldData()
	{
		return fieldData;
	}
	
	public void setFieldData(String data)
	{
		if(data != null)
		fieldData=data;
	}
	
	//Equality Operations
	@Override
	public boolean equals(Object otherObject) {
		if(!super.equals(otherObject))
			return false;
		
		if(!(otherObject instanceof FieldData))
			return false;
		
		FieldData other = (FieldData)otherObject;
		
		if(!fieldIsEqual(this.fieldData, other.fieldData))
			return false;
		
		return true;
	}

	@Override
	public int hashCode() {
		int result = super.hashCode();
		int arbitraryPrimeNumber = 23;
		
		if(this.fieldData != null)
			result = result * arbitraryPrimeNumber + this.fieldData.hashCode();
		
		return result;
		
	}

	
	//Serialization/Deserialization
	@Override
	public void initializeFromToken(StorageToken token) {
		super.initializeFromToken(token);
		this.fieldData = (String)SerializationConvenience.untokenizeObject(token.getItem(FIELD_DATA_KEY));
	}

	@Override
	public StorageToken saveToToken() {
		StorageToken result = super.saveToToken();
		result.setItem(FIELD_DATA_KEY, SerializationConvenience.tokenizeObject(this.fieldData));
		return result;
	}

}
