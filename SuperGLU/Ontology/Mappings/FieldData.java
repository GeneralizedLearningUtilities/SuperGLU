package Ontology.Mappings;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This is the FieldData class that stores the String type data for the default
 * values in the respective individuals
 * 
 * @author auerbach
 *
 */
public class FieldData extends Serializable
{

    public static final String FIELD_DATA_KEY = "fieldData";

    protected String fieldData;

    // PARAMETERIZED CONSTRUCTOR
    public FieldData(String data)
    {

	if (data == null)
	    this.fieldData = "";
	else
	    this.fieldData = data;
    }

    // DEFAULT CONSTRUCTOR
    public FieldData()
    {
	this.fieldData = "";
    }

    // RETURNS THE FIELD DATA
    public String getFieldData()
    {
	return fieldData;
    }

    // SETS THE FIELD DATA
    public void setFieldData(String data)
    {
	if (data != null)
	    fieldData = data;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof FieldData))
	    return false;

	FieldData other = (FieldData) otherObject;

	if (!fieldIsEqual(this.fieldData, other.fieldData))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.fieldData != null)
	    result = result * arbitraryPrimeNumber + this.fieldData.hashCode();

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.fieldData = (String) SerializationConvenience.untokenizeObject(token.getItem(FIELD_DATA_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(FIELD_DATA_KEY, SerializationConvenience.tokenizeObject(this.fieldData));
	return result;
    }

}
