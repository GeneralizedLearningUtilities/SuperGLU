package Ontology.Mappings;

/**
 * MessageTemplate  Class
 * It is used to store the various field data based individuals in an ArrayList
 * @author tirthmehta
 */
import java.util.ArrayList;

import Core.Message;
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

public class MessageTemplate extends Serializable
{

    private ArrayList<NestedAtomic> defaultFieldData = new ArrayList<>();
    public static final String MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY = "messageTemplate";

    // CONSTRUCTOR
    public MessageTemplate()
    {
	defaultFieldData = null;
    }

    // PARAMETERIZED CONSTRUCTOR
    public MessageTemplate(ArrayList<NestedAtomic> arrlist)
    {
	if (arrlist == null)
	    defaultFieldData = null;
	else
	{
	    for (NestedAtomic in : arrlist)
	    {
		defaultFieldData.add(in);
	    }
	}
    }

    
    // GETTER METHOD THAT RETURNS THE ARRAYLIST OF FIELDDATA PERTAINING TO AN
    // INDIVIDUAL
    public ArrayList<NestedAtomic> getDefaultFieldData()
    {
	return defaultFieldData;
    }

    // SETTER METHOD FOR SETTING THE FIELD-DATA ARRAYLIST
    public void setData(ArrayList<NestedAtomic> arrFieldData)
    {
	if (arrFieldData == null)
	    defaultFieldData = null;
	else
	{
	    for (NestedAtomic in : arrFieldData)
	    {
		defaultFieldData.add(in);
	    }
	}
    }

    // CREATES A STORAGE TOKEN OF THE TARGET CLASS OBJECT ONCE A VALID MAPPING
    // HAS BEEN IDENTIFIED
    public StorageToken createTargetStorageToken(String id)
    {
	if (id.equals("Message"))
	{
	    Message targetMsg = new Message();
	    StorageToken target = targetMsg.saveToToken();
	    return target;
	}
	return null;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof FieldData))
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
	this.defaultFieldData = (ArrayList<NestedAtomic>) SerializationConvenience.untokenizeObject(token.getItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(MESSAGE_TEMPLATE_DEFAULTFIELDDATA_KEY, SerializationConvenience.tokenizeObject(this.defaultFieldData));
	return result;
    }

}
