package Ontology.Mappings;

/**
 * MessageTemplate  Class
 * It is used to store the various field data based individuals in an ArrayList
 * @author tirthmehta
 */
import java.util.ArrayList;
import java.util.List;

import Core.Message;
import Util.Pair;
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageTemplate extends Serializable
{

    private List<Pair<FieldData, Object>> defaultFieldData;
    public static final String MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY = "messageTemplate";

    // CONSTRUCTOR
    public MessageTemplate()
    {
	defaultFieldData = new ArrayList<>();
    }

    // PARAMETERIZED CONSTRUCTOR
    public MessageTemplate(List<Pair<FieldData, Object>> arrlist)
    {
	if(arrlist==null)
	    this.defaultFieldData = new ArrayList<>();
	else
	    this.defaultFieldData = arrlist;
    }

    
    // GETTER METHOD THAT RETURNS THE ARRAYLIST OF FIELDDATA PERTAINING TO AN
    // INDIVIDUAL
    public List<Pair<FieldData,Object>> getDefaultFieldData()
    {
	return defaultFieldData;
    }

    // SETTER METHOD FOR SETTING THE FIELD-DATA ARRAYLIST
    public void setData(List<Pair<FieldData,Object>> arrFieldData)
    {
	if(arrFieldData==null)
	    this.defaultFieldData = new ArrayList<>();
	else
	    this.defaultFieldData = arrFieldData;
    }

    // CREATES A STORAGE TOKEN OF THE TARGET CLASS OBJECT ONCE A VALID MAPPING
    // HAS BEEN IDENTIFIED
    public StorageToken createTargetStorageToken(String id)
    {
	if (id.equals("Message"))
	{
	    Message targetMsg = new Message();
	    StorageToken result = targetMsg.saveToToken();
	    
	    for(Pair<FieldData, Object> currentFieldDataPair : this.defaultFieldData)
	    {
		FieldData currentFieldData = currentFieldDataPair.getFirst();
		currentFieldData.storeData(result, currentFieldDataPair.getSecond());
	    }
	    
	    return result;
	    
	}
	return null;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof SimpleFieldData))
	    return false;

	MessageTemplate other = (MessageTemplate) otherObject;

	if (!fieldIsEqual(this.defaultFieldData, other.defaultFieldData))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.defaultFieldData != null)
	    result = result * arbitraryPrimeNumber + this.defaultFieldData.hashCode();

	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.defaultFieldData = (List<Pair<FieldData,Object>>) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY, SerializationConvenience.tokenizeObject(this.defaultFieldData));
	return result;
    }

}
