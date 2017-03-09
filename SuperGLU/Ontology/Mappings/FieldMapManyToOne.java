package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;
/**
 * This class maps many fields from the source message into a single field in the destination message.
 * @author auerbach
 *
 */
public class FieldMapManyToOne extends Serializable implements FieldMap
{
    public static final String FIELD_MAP_INFIELDS_KEY = "inFields";
    public static final String FIELD_MAP_OUTFIELD_KEY = "outField";
    public static final String FIELD_MAP_CONVERTER_KEY = "converter";

    protected List<FieldData> inFields;
    protected FieldData outField;
    protected DataConverter converter;
    
    
    public FieldMapManyToOne()
    {
	super();
	inFields = null;
	outField = null;
	this.converter = null;
    }

    public FieldMapManyToOne(List<FieldData> in, FieldData out, DataConverter converter)
    {
	super();
	inFields = in;
	outField = out;
	this.converter = converter;
    }
    
    //Accessors

    public void setInFields(List<FieldData> inFields)
    {
	this.inFields = inFields;
    }

    public List<FieldData> getInFields()
    {
	return this.inFields;
    }

    public FieldData getOutField()
    {
	return outField;
    }

    public void setOutField(FieldData out)
    {
	outField = out;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof FieldMapOneToOne))
	    return false;

	FieldMapManyToOne other = (FieldMapManyToOne) otherObject;

	if (!fieldIsEqual(this.inFields, other.inFields))
	    return false;

	if (!fieldIsEqual(this.outField, other.outField))
	    return false;
	
	if(!fieldIsEqual(this.converter, other.converter))
	    return false;
	
	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.inFields != null)
	    result = result * arbitraryPrimeNumber + this.inFields.hashCode();
	if (this.outField != null)
	    result = result * arbitraryPrimeNumber + this.outField.hashCode();
	if(this.converter != null)
	    result = result * arbitraryPrimeNumber + this.converter.hashCode();
	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.inFields = (List<FieldData>) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_INFIELDS_KEY, true, new ArrayList<FieldData>()));
	this.outField = (FieldData) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_OUTFIELD_KEY));
	this.converter = (DataConverter) SerializationConvenience.untokenizeObject(token.getItem(FIELD_MAP_CONVERTER_KEY, true, null));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(FIELD_MAP_INFIELDS_KEY, SerializationConvenience.tokenizeObject(this.inFields));
	result.setItem(FIELD_MAP_OUTFIELD_KEY, SerializationConvenience.tokenizeObject(this.outField));
	result.setItem(FIELD_MAP_CONVERTER_KEY, SerializationConvenience.tokenizeObject(this.converter));
	return result;
    }


    @Override
    public StorageToken applyMapping(StorageToken sourceMessage, StorageToken destinationMessage)
    {
	List<Object> inDataList = new ArrayList<>();
	
	for(FieldData inField : this.inFields)
	{
	    Object inData = inField.retrieveFieldData(sourceMessage);
	    inDataList.add(inData);
	}
	
	Object outData = this.converter.join(inDataList);
	this.outField.storeData(destinationMessage, outData);
	
	return destinationMessage;
    }

    @Override
    public boolean doesMappingApply(StorageToken sourceMessage)
    {
	for(FieldData inField : this.inFields)
	{
	    Object inData = inField.retrieveFieldData(sourceMessage);
	    
	    if(inData == null)
		return false;
	}
	
	return true;
    }

}
